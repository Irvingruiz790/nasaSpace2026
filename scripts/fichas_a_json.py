"""Convierte `contenido/fichas.csv` en `data/artifacts.json`.

Lo usa el equipo de backend cada vez que investigación entrega fichas nuevas.

    .\\.venv\\Scripts\\python.exe scripts\\fichas_a_json.py

Ventaja del CSV: investigación trabaja en Excel o Google Sheets (una fila por
pieza) y nunca tiene que escribir llaves, comas ni corchetes de JSON.
El script hace la traducción y avisa si falta algo.
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from core import datos  # noqa: E402
from core.contrato import LIMITES_HISTORIA  # noqa: E402

ENTRADA = RAIZ / "contenido" / "fichas.csv"
SALIDA = RAIZ / "data" / "artifacts.json"

COLUMNAS = [
    # identificación
    "id",
    "nombre",
    "apodo",
    "tipo",
    "mision",
    "agencia",
    "zona",
    "estado",
    "etiqueta_estado",
    # ubicación
    "ubicacion_texto",
    "lat",
    "lon",
    "lanzamiento",
    "ultima_senal",
    "distancia_actual",
    "horizons_id",
    # imagen
    "imagen",
    "credito_imagen",
    "alt_text",
    # historia
    "que_es",
    "por_que",
    "descubrimiento",
    "ahora",
    "dato_curioso",
    # fuentes
    "fuente1_titulo",
    "fuente1_url",
    "fuente2_titulo",
    "fuente2_url",
    "fuente3_titulo",
    "fuente3_url",
    "consultado",
    # control de calidad
    "revisor",
    "fecha_verificacion",
    "notas_verificacion",
]

VACIOS = {"", "n/a", "na", "null", "none", "-", "—"}


def _celda(fila: dict[str, str], campo: str) -> str:
    return str(fila.get(campo) or "").strip()


def _texto_o_nulo(texto: str) -> str | None:
    limpio = texto.strip()
    return None if limpio.lower() in VACIOS else limpio


def _numero(texto: str) -> float | str | None:
    limpio = _texto_o_nulo(texto)
    if limpio is None:
        return None
    try:
        return float(limpio.replace(",", "."))
    except ValueError:
        # Se devuelve el texto para que la validación explique el error
        return limpio


def _imagen(texto: str) -> str:
    limpio = _texto_o_nulo(texto)
    if limpio is None:
        return ""
    if limpio.startswith("assets/"):
        return limpio
    return f"assets/img/{limpio}"


def _fuentes(fila: dict[str, str], consultado: str) -> list[dict[str, str]]:
    fuentes: list[dict[str, str]] = []
    for indice in (1, 2, 3):
        titulo = _texto_o_nulo(_celda(fila, f"fuente{indice}_titulo"))
        url = _texto_o_nulo(_celda(fila, f"fuente{indice}_url"))
        if titulo or url:
            fuentes.append(
                {"titulo": titulo or "", "url": url or "", "consultado": consultado}
            )
    return fuentes


def a_pieza(fila: dict[str, str]) -> dict[str, Any]:
    """Traduce una fila del CSV a un registro del contrato de datos."""
    consultado = _texto_o_nulo(_celda(fila, "consultado")) or date.today().isoformat()

    return {
        "id": _celda(fila, "id"),
        "nombre": _celda(fila, "nombre"),
        "apodo": _celda(fila, "apodo"),
        "tipo": _celda(fila, "tipo"),
        "mision": _celda(fila, "mision"),
        "agencia": _celda(fila, "agencia"),
        "zona": _celda(fila, "zona"),
        "estado": _celda(fila, "estado"),
        "etiqueta_estado": _celda(fila, "etiqueta_estado"),
        "ubicacion_texto": _celda(fila, "ubicacion_texto"),
        "lat": _numero(_celda(fila, "lat")),
        "lon": _numero(_celda(fila, "lon")),
        "lanzamiento": _celda(fila, "lanzamiento"),
        "ultima_senal": _texto_o_nulo(_celda(fila, "ultima_senal")),
        "distancia_actual": _texto_o_nulo(_celda(fila, "distancia_actual")),
        "horizons_id": _texto_o_nulo(_celda(fila, "horizons_id")),
        "imagen": _imagen(_celda(fila, "imagen")),
        "credito_imagen": _celda(fila, "credito_imagen"),
        "alt_text": _celda(fila, "alt_text"),
        "historia": {campo: _celda(fila, campo) for campo in LIMITES_HISTORIA},
        "fuentes": _fuentes(fila, consultado),
        "revisor": _texto_o_nulo(_celda(fila, "revisor")) or "pendiente",
        "fecha_verificacion": _texto_o_nulo(_celda(fila, "fecha_verificacion"))
        or consultado,
        "notas_verificacion": _texto_o_nulo(_celda(fila, "notas_verificacion")),
    }


def leer_filas(ruta: Path) -> list[dict[str, str]]:
    """Lee el CSV aceptando BOM de Excel y filas vacías al final."""
    with ruta.open(encoding="utf-8-sig", newline="") as archivo:
        muestra = archivo.read(4096)
        archivo.seek(0)
        # Excel en español a veces guarda con punto y coma.
        separador = ";" if muestra.count(";") > muestra.count(",") else ","
        lector = csv.DictReader(archivo, delimiter=separador)
        if not lector.fieldnames:
            return []
        lector.fieldnames = [nombre.strip() for nombre in lector.fieldnames]
        filas = []
        for fila in lector:
            limpia = {clave: (valor or "").strip() for clave, valor in fila.items() if clave}
            if any(valor for valor in limpia.values()):
                filas.append(limpia)
        return filas


def convertir(
    entrada: Path | None = None,
    salida: Path | None = None,
    *,
    escribir: bool = True,
) -> tuple[list[dict[str, Any]], list[datos.Problema]]:
    """Lee el CSV, valida y (opcionalmente) escribe el JSON."""
    origen = Path(entrada) if entrada else ENTRADA
    destino = Path(salida) if salida else SALIDA

    if not origen.exists():
        raise FileNotFoundError(
            f"No existe {origen}. Investigación debe entregar ese archivo."
        )

    filas = leer_filas(origen)
    piezas = [a_pieza(fila) for fila in filas]
    problemas = datos.validar_piezas(piezas)

    if escribir:
        destino.parent.mkdir(parents=True, exist_ok=True)
        contenido = {"piezas": piezas}
        destino.write_text(
            json.dumps(contenido, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    return piezas, problemas


def main() -> int:
    print(f"Leyendo {ENTRADA.relative_to(RAIZ)} ...")
    try:
        piezas, problemas = convertir()
    except FileNotFoundError as exc:
        print(f"\nERROR: {exc}")
        print("Pide el archivo a investigación o revisa contenido/fichas.csv.")
        return 1

    errores = datos.errores(problemas)
    avisos = datos.avisos(problemas)

    print(f"{len(piezas)} pieza(s) convertidas -> {SALIDA.relative_to(RAIZ)}")
    print(f"Errores: {len(errores)} | Avisos: {len(avisos)}")

    for problema in problemas:
        print(f"  {problema}")

    if errores:
        print("\nHay errores de contrato. Corrige el CSV y vuelve a ejecutar.")
        print("No hagas commit de data/artifacts.json hasta que Errores sea 0.")
        return 1

    print("\nListo. El frontend ya puede usar estas piezas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
