"""Carga y validación del dataset curado (`data/artifacts.json`).

Reglas de diseño:

- El backend **no importa Streamlit**. Estos módulos se prueban con pytest puro,
  sin levantar la app.
- `data/artifacts.json` **se genera** desde `contenido/fichas.csv` con
  `scripts/fichas_a_json.py`. Nadie lo edita a mano.
- La validación **nunca lanza excepción**: devuelve una lista de `Problema`.
  La app decide si muestra un aviso o una pantalla de error.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable

from core import config
from core.contrato import (
    CAMPOS_TEXTO_OBLIGATORIOS,
    ESTADOS,
    LIMITES_HISTORIA,
    TIPOS,
    ZONAS,
)

log = logging.getLogger(__name__)

RE_KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(frozen=True)
class Problema:
    """Un problema detectado en el dataset.

    `severidad` vale:
      - "error": rompe el contrato, hay que corregirlo antes del release.
      - "aviso": calidad de contenido o archivo todavía no entregado.
    """

    pieza_id: str
    campo: str
    mensaje: str
    severidad: str = "error"

    def __str__(self) -> str:
        return f"[{self.severidad}] {self.pieza_id} · {self.campo}: {self.mensaje}"


# --- Lectura ---------------------------------------------------------------


def leer_json(ruta: str | Path) -> Any:
    """Lee un JSON en UTF-8. Lanza `FileNotFoundError` si no existe."""
    ruta = Path(ruta)
    with ruta.open(encoding="utf-8") as archivo:
        return json.load(archivo)


def ruta_piezas() -> Path:
    """Ruta del dataset que consume la app."""
    return config.ARCHIVO_PIEZAS


def cargar_piezas(ruta: str | Path | None = None) -> list[dict[str, Any]]:
    """Devuelve la lista de piezas. Si algo falla, devuelve lista vacía."""
    destino = Path(ruta) if ruta else ruta_piezas()

    if not destino.exists():
        log.error(
            "No existe %s. Genera el dataset con: python scripts/fichas_a_json.py",
            destino,
        )
        return []

    try:
        datos = leer_json(destino)
    except (OSError, json.JSONDecodeError) as exc:
        log.error("No se pudo leer %s: %s", destino, exc)
        return []

    # Se aceptan las dos formas: lista directa o {"piezas": [...]}
    if isinstance(datos, dict) and "piezas" in datos:
        datos = datos["piezas"]

    if not isinstance(datos, list):
        log.error("El archivo %s no contiene una lista de piezas.", destino)
        return []

    return [pieza for pieza in datos if isinstance(pieza, dict)]


# --- Consultas -------------------------------------------------------------


def buscar(piezas: Iterable[dict[str, Any]], pieza_id: str) -> dict[str, Any] | None:
    """Busca una pieza por id. Devuelve None si no existe."""
    for pieza in piezas:
        if pieza.get("id") == pieza_id:
            return pieza
    return None


def por_zona(piezas: Iterable[dict[str, Any]], zona: str) -> list[dict[str, Any]]:
    """Piezas de una zona, en el orden del dataset."""
    return [pieza for pieza in piezas if pieza.get("zona") == zona]


def contar_por_zona(piezas: Iterable[dict[str, Any]]) -> dict[str, int]:
    """Conteo por zona, con las cinco zonas siempre presentes."""
    conteo = {zona: 0 for zona in ZONAS}
    for pieza in piezas:
        zona = pieza.get("zona")
        if zona in conteo:
            conteo[zona] += 1
    return conteo


def con_horizons(piezas: Iterable[dict[str, Any]]) -> dict[str, str]:
    """Mapa `id de pieza -> id de Horizons` para las piezas que tienen dato vivo."""
    return {
        str(pieza["id"]): str(pieza["horizons_id"])
        for pieza in piezas
        if pieza.get("id") and pieza.get("horizons_id")
    }


# --- Validación ------------------------------------------------------------


def validar_piezas(piezas: Iterable[dict[str, Any]]) -> list[Problema]:
    """Valida todo el dataset y detecta ids repetidos."""
    problemas: list[Problema] = []
    vistos: set[str] = set()

    for pieza in piezas:
        if not isinstance(pieza, dict):
            problemas.append(
                Problema("(desconocido)", "*", "La pieza no es un objeto JSON", "error")
            )
            continue
        problemas.extend(validar_pieza(pieza))
        pieza_id = pieza.get("id")
        if isinstance(pieza_id, str) and pieza_id:
            if pieza_id in vistos:
                problemas.append(
                    Problema(pieza_id, "id", "ID repetido: cada pieza debe ser única", "error")
                )
            vistos.add(pieza_id)

    return problemas


def validar_pieza(pieza: dict[str, Any]) -> list[Problema]:
    """Valida una pieza contra el contrato. No lanza excepción."""
    problemas: list[Problema] = []

    if not isinstance(pieza, dict):
        return [Problema("(desconocido)", "*", "La pieza no es un objeto JSON", "error")]

    pieza_id = pieza.get("id")
    etiqueta = pieza_id if isinstance(pieza_id, str) and pieza_id else "(sin id)"

    def error(campo: str, mensaje: str) -> None:
        problemas.append(Problema(etiqueta, campo, mensaje, "error"))

    def aviso(campo: str, mensaje: str) -> None:
        problemas.append(Problema(etiqueta, campo, mensaje, "aviso"))

    # id
    if not isinstance(pieza_id, str) or not pieza_id.strip():
        error("id", "Falta el id")
    elif not RE_KEBAB.match(pieza_id):
        error("id", f"El id '{pieza_id}' debe ser kebab-case (minúsculas y guiones)")

    # Campos de texto obligatorios
    for campo in CAMPOS_TEXTO_OBLIGATORIOS:
        if campo == "id":
            continue
        valor = pieza.get(campo)
        if not isinstance(valor, str) or not valor.strip():
            error(campo, f"Falta el campo obligatorio '{campo}'")

    # Enumeraciones
    if pieza.get("zona") not in ZONAS:
        error("zona", f"'{pieza.get('zona')}' no está en {sorted(ZONAS)}")
    if pieza.get("estado") not in ESTADOS:
        error("estado", f"'{pieza.get('estado')}' no está en {sorted(ESTADOS)}")
    if pieza.get("tipo") not in TIPOS:
        error("tipo", f"'{pieza.get('tipo')}' no está en {sorted(TIPOS)}")

    # Fechas ISO
    for campo in ("lanzamiento", "fecha_verificacion"):
        valor = pieza.get(campo)
        if isinstance(valor, str) and valor.strip():
            try:
                date.fromisoformat(valor)
            except ValueError:
                error(campo, f"'{valor}' no es una fecha ISO válida (AAAA-MM-DD)")

    _validar_ubicacion(pieza, error, aviso)
    _validar_historia(pieza, error, aviso)
    _validar_fuentes(pieza, error, aviso)
    _validar_imagen(pieza, error, aviso)

    return problemas


def _validar_ubicacion(pieza, error, aviso) -> None:
    lat = pieza.get("lat")
    lon = pieza.get("lon")
    tiene_coords = isinstance(lat, (int, float)) and isinstance(lon, (int, float))

    if lat is not None and not isinstance(lat, (int, float)):
        error("lat", "lat debe ser número o null")
    if lon is not None and not isinstance(lon, (int, float)):
        error("lon", "lon debe ser número o null")

    if tiene_coords:
        if not -90 <= float(lat) <= 90:
            error("lat", f"{lat} está fuera del rango -90..90")
        if not -180 <= float(lon) <= 180:
            error("lon", f"{lon} está fuera del rango -180..180")

    if pieza.get("zona") in {"luna", "marte"}:
        texto = pieza.get("ubicacion_texto")
        if not tiene_coords and not (isinstance(texto, str) and texto.strip()):
            error(
                "ubicacion_texto",
                "En Luna o Marte hace falta lat/lon o una ubicacion_texto clara",
            )


def _validar_historia(pieza, error, aviso) -> None:
    historia = pieza.get("historia")
    if not isinstance(historia, dict):
        error("historia", "Falta el objeto 'historia' con los 5 bloques")
        return

    for campo, limite in LIMITES_HISTORIA.items():
        texto = historia.get(campo)
        if not isinstance(texto, str) or not texto.strip():
            error(f"historia.{campo}", "Bloque vacío")
            continue
        palabras = len(texto.split())
        if palabras > limite:
            aviso(
                f"historia.{campo}",
                f"{palabras} palabras; el límite para 8-12 años es {limite}",
            )


def _validar_fuentes(pieza, error, aviso) -> None:
    fuentes = pieza.get("fuentes")
    if not isinstance(fuentes, list) or not fuentes:
        error("fuentes", "Falta la lista de fuentes (mínimo 2 para datos críticos)")
        return

    if len(fuentes) < 2:
        aviso("fuentes", f"Hay {len(fuentes)} fuente(s); se piden 2 oficiales")

    for indice, fuente in enumerate(fuentes, start=1):
        if not isinstance(fuente, dict) or not fuente.get("titulo") or not fuente.get("url"):
            error(f"fuentes[{indice}]", "Cada fuente necesita 'titulo' y 'url'")


def _validar_imagen(pieza, error, aviso) -> None:
    ruta = pieza.get("imagen")
    if not isinstance(ruta, str) or not ruta.strip():
        error("imagen", "Falta la ruta de la imagen")
        return

    if not (config.RAIZ / ruta).exists():
        aviso(
            "imagen",
            f"No se encontró '{ruta}'. CD debe entregarla antes del release.",
        )


# --- Utilidades de reporte -------------------------------------------------


def errores(problemas: Iterable[Problema]) -> list[Problema]:
    return [p for p in problemas if p.severidad == "error"]


def avisos(problemas: Iterable[Problema]) -> list[Problema]:
    return [p for p in problemas if p.severidad == "aviso"]


def hay_errores(problemas: Iterable[Problema]) -> bool:
    return any(p.severidad == "error" for p in problemas)


def resumen(piezas: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Resumen listo para mostrar en un panel de estado."""
    piezas = list(piezas)
    problemas = validar_piezas(piezas)
    return {
        "total": len(piezas),
        "por_zona": contar_por_zona(piezas),
        "errores": len(errores(problemas)),
        "avisos": len(avisos(problemas)),
        "archivo": ruta_piezas().name,
    }
