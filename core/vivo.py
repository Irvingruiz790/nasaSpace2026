"""Datos "en vivo" con respaldo local.

Estrategia (BE-03, BE-04, BE-05):

1. Se intenta JPL Horizons para cada pieza que tenga `horizons_id`.
2. Si la API falla o tarda, se usa `data/live_snapshot.json` y se marca
   `status = "stale"` con la fecha del snapshot.
3. Si tampoco hay snapshot, se devuelve `status = "error"` sin romper la app.
4. El resultado se memoriza `CACHE_TTL_SEGUNDOS` para no golpear a JPL en cada
   interacción de Streamlit (Streamlit re-ejecuta el script en cada click).

El frontend solo consume el dict que devuelve `datos_en_vivo()`; nunca llama a
la red por su cuenta.
"""

from __future__ import annotations

import copy
import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from core import config, datos, horizons

log = logging.getLogger(__name__)

_CACHE: dict[str, tuple[float, dict[str, Any]]] = {}

CAMPOS_OBJETO = ("distance_km", "light_time_s", "status", "source")


def ahora_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def leer_snapshot(ruta: str | Path | None = None) -> dict[str, Any] | None:
    """Lee el respaldo. Devuelve None si no existe o está roto."""
    destino = Path(ruta) if ruta else config.ARCHIVO_SNAPSHOT
    if not destino.exists():
        log.warning("No existe el snapshot de respaldo: %s", destino)
        return None
    try:
        contenido = datos.leer_json(destino)
    except (OSError, json.JSONDecodeError) as exc:
        log.error("Snapshot ilegible (%s): %s", destino, exc)
        return None
    if not isinstance(contenido, dict):
        log.error("El snapshot no es un objeto JSON: %s", destino)
        return None
    return contenido


def _objeto_desde_snapshot(
    snapshot: dict[str, Any] | None, pieza_id: str
) -> dict[str, Any] | None:
    if not snapshot:
        return None
    objetos = snapshot.get("objects")
    if not isinstance(objetos, dict):
        return None
    previo = objetos.get(pieza_id)
    if not isinstance(previo, dict):
        return None
    return {campo: previo.get(campo) for campo in CAMPOS_OBJETO}


def _clave_cache(ids: dict[str, str], usar_api: bool) -> str:
    parejas = ",".join(f"{pid}={hid}" for pid, hid in sorted(ids.items()))
    return f"{parejas}|api={usar_api}"


def datos_en_vivo(
    piezas: Iterable[dict[str, Any]] | None = None,
    *,
    usar_api: bool = True,
    ttl: float | None = None,
    forzar: bool = False,
) -> dict[str, Any]:
    """Devuelve el estado para el panel "en vivo".

    Estructura (según `docs/CONTRATO_DATOS.md` sección 3):

        {
          "generated_at": "2026-11-14T18:00:00+00:00",
          "source": "JPL Horizons",
          "fallback": false,
          "objects": {
            "voyager-1": {"distance_km": 25890556821.0, "light_time_s": 86361.6,
                          "status": "ok", "source": "JPL Horizons"}
          }
        }
    """
    lista = list(piezas) if piezas is not None else datos.cargar_piezas()
    ids = datos.con_horizons(lista)
    espera = config.CACHE_TTL_SEGUNDOS if ttl is None else ttl
    clave = _clave_cache(ids, usar_api)

    if not forzar and espera > 0:
        guardado = _CACHE.get(clave)
        if guardado and (time.monotonic() - guardado[0]) < espera:
            return copy.deepcopy(guardado[1])

    snapshot = leer_snapshot()
    objetos: dict[str, Any] = {}
    hubo_respaldo = False
    hubo_vivo = False

    for pieza_id, horizons_id in ids.items():
        resultado: dict[str, Any] | None = None

        if usar_api:
            crudo = horizons.consultar(horizons_id)
            if crudo.get("status") == "ok":
                resultado = {campo: crudo.get(campo) for campo in CAMPOS_OBJETO}
                hubo_vivo = True

        if resultado is None:
            respaldo = _objeto_desde_snapshot(snapshot, pieza_id)
            if respaldo is not None:
                resultado = respaldo
                # El dato era válido cuando se capturó; ahora es antiguo.
                resultado["status"] = "stale"
                if not resultado.get("source"):
                    resultado["source"] = (snapshot or {}).get("source")
                hubo_respaldo = True
            else:
                resultado = {
                    "distance_km": None,
                    "light_time_s": None,
                    "status": "error",
                    "source": None,
                }

        objetos[pieza_id] = resultado

    if hubo_vivo:
        generated_at = ahora_iso()
        source = "JPL Horizons"
    elif hubo_respaldo and snapshot:
        generated_at = snapshot.get("generated_at") or ahora_iso()
        source = snapshot.get("source")
    else:
        generated_at = ahora_iso()
        source = None

    salida = {
        "generated_at": generated_at,
        "source": source,
        "fallback": hubo_respaldo or not hubo_vivo,
        "objects": objetos,
    }

    if espera > 0:
        _CACHE[clave] = (time.monotonic(), copy.deepcopy(salida))

    return salida


def limpiar_cache() -> None:
    """Útil en pruebas y antes de una demo."""
    _CACHE.clear()


def objeto(datos_panel: dict[str, Any], pieza_id: str) -> dict[str, Any]:
    """Acceso seguro a un objeto del panel, con valores neutros si falta."""
    objetos = datos_panel.get("objects") or {}
    actual = objetos.get(pieza_id) or {}
    return {
        "distance_km": actual.get("distance_km"),
        "light_time_s": actual.get("light_time_s"),
        "status": actual.get("status", "error"),
        "source": actual.get("source"),
    }


def aviso_panel(datos_panel: dict[str, Any]) -> str | None:
    """Frase corta para mostrar debajo del odómetro. None = sin aviso."""
    if datos_panel.get("fallback"):
        from core import formato

        return (
            "Mostrando el último dato guardado "
            f"({formato.antiguedad_texto(datos_panel.get('generated_at'))})."
        )
    return None
