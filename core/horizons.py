"""Cliente de JPL Horizons para distancia y tiempo luz.

Detalles que importan (verificados contra la API real):

- Se pide `QUANTITIES='20'` ("Observer range & range-rate").
- La tabla llega como **texto** dentro de `result`, entre `$$SOE` y `$$EOE`.
  La cabecera es:  `Date__(UT)__HR:MN   delta   deldot`
  y una fila:      `2026-Nov-14 00:00   173.067682711039   27.1464777`
  `delta` viene en **AU**, no en km. `deldot` viene en km/s.
- No se busca la columna por posición fija: se lee el nombre en la cabecera.
  Si JPL agrega una columna, el parseo sigue funcionando.
- El tiempo luz no viene en esa tabla: se calcula con `c = 299792.458 km/s`.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from core import config

log = logging.getLogger(__name__)


def _ahora_utc() -> datetime:
    return datetime.now(timezone.utc)


def construir_parametros(
    horizons_id: str,
    inicio: datetime | None = None,
    dias: int = 1,
) -> dict[str, str]:
    """Parámetros GET para una consulta de observador geocéntrico."""
    desde = inicio or _ahora_utc()
    hasta = desde + timedelta(days=dias)
    return {
        "format": "json",
        "COMMAND": f"'{horizons_id}'",
        "EPHEM_TYPE": "'OBSERVER'",
        "CENTER": "'500@399'",  # centro: Tierra (geocéntrico)
        "START_TIME": f"'{desde:%Y-%m-%d}'",
        "STOP_TIME": f"'{hasta:%Y-%m-%d}'",
        "STEP_SIZE": f"'{dias} d'",
        "QUANTITIES": "'20'",
    }


def parsear_tabla(texto: str) -> dict[str, Any] | None:
    """Extrae la primera fila de la tabla efemérides.

    Devuelve `{"fecha_ut", "delta_au", "deldot_km_s"}` o None si no hay tabla.
    """
    if "$$SOE" not in texto or "$$EOE" not in texto:
        return None

    cabecera: list[str] | None = None
    for linea in texto.split("$$SOE", 1)[0].splitlines():
        tokens = linea.split()
        if tokens and tokens[0].startswith("Date") and "delta" in tokens:
            cabecera = tokens

    if not cabecera or "delta" not in cabecera:
        return None

    indice_delta = cabecera.index("delta")
    indice_deldot = cabecera.index("deldot") if "deldot" in cabecera else None

    bloque = texto.split("$$SOE", 1)[1].split("$$EOE", 1)[0]
    for linea in bloque.strip().splitlines():
        tokens = linea.split()
        # tokens[0] = fecha, tokens[1] = hora; luego las columnas de la cabecera
        if len(tokens) < indice_delta + 2:
            continue
        try:
            delta_au = float(tokens[indice_delta + 1])
        except ValueError:
            continue

        deldot = None
        if indice_deldot is not None and len(tokens) > indice_deldot + 1:
            try:
                deldot = float(tokens[indice_deldot + 1])
            except ValueError:
                deldot = None

        return {
            "fecha_ut": f"{tokens[0]} {tokens[1]}",
            "delta_au": delta_au,
            "deldot_km_s": deldot,
        }

    return None


def _resultado_error(mensaje: str, retrieved_at: str) -> dict[str, Any]:
    return {
        "distance_km": None,
        "light_time_s": None,
        "status": "error",
        "source": "JPL Horizons",
        "error": mensaje,
        "retrieved_at": retrieved_at,
    }


def consultar(
    horizons_id: str,
    *,
    timeout: float | None = None,
    reintentos: int | None = None,
    inicio: datetime | None = None,
) -> dict[str, Any]:
    """Consulta un objeto. Devuelve siempre un dict, nunca lanza excepción.

    Éxito:
        {"distance_km": float, "light_time_s": float, "status": "ok",
         "source": "JPL Horizons", "retrieved_at": iso, "delta_au": float,
         "deldot_km_s": float, "fecha_ut": str}

    Fallo:
        {"distance_km": None, "light_time_s": None, "status": "error",
         "source": "JPL Horizons", "retrieved_at": iso, "error": str}
    """
    limite = config.TIMEOUT_SEGUNDOS if timeout is None else timeout
    intentos = config.REINTENTOS if reintentos is None else max(1, reintentos)
    momento = _ahora_utc().isoformat(timespec="seconds")
    ultimo_error = "error desconocido"

    try:
        import requests
    except ImportError:  # pragma: no cover - requests está en requirements
        return _resultado_error("falta la dependencia 'requests'", momento)

    for intento in range(1, intentos + 1):
        try:
            respuesta = requests.get(
                config.HORIZONS_URL,
                params=construir_parametros(horizons_id, inicio=inicio),
                timeout=limite,
                headers={"User-Agent": config.USER_AGENT},
            )
            respuesta.raise_for_status()
            cuerpo = respuesta.json()
            fila = parsear_tabla(cuerpo.get("result", ""))
            if fila is None:
                raise ValueError("Horizons no devolvió una tabla con 'delta'")

            distancia_km = fila["delta_au"] * config.KM_POR_AU
            return {
                "distance_km": distancia_km,
                "light_time_s": distancia_km / config.VELOCIDAD_LUZ_KM_S,
                "status": "ok",
                "source": "JPL Horizons",
                "retrieved_at": _ahora_utc().isoformat(timespec="seconds"),
                "delta_au": fila["delta_au"],
                "deldot_km_s": fila["deldot_km_s"],
                "fecha_ut": fila["fecha_ut"],
            }
        except Exception as exc:  # red, timeout, JSON, tabla rara
            ultimo_error = f"{type(exc).__name__}: {exc}"
            log.warning(
                "Horizons falló para %s (intento %s/%s): %s",
                horizons_id,
                intento,
                intentos,
                ultimo_error,
            )

    return _resultado_error(ultimo_error, momento)


def consultar_varios(
    ids: dict[str, str],
    **opciones: Any,
) -> dict[str, dict[str, Any]]:
    """Consulta varios objetos: `{id_pieza: resultado}`."""
    return {pieza_id: consultar(hid, **opciones) for pieza_id, hid in ids.items()}
