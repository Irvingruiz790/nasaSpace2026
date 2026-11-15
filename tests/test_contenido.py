"""Pruebas de las reglas que debe cumplir `contenido/fichas.csv`."""

from __future__ import annotations

import csv
from datetime import date

from core import config
from core.contrato import LIMITES_HISTORIA
from scripts.fichas_a_json import COLUMNAS, leer_filas

RUTA_CSV = config.RAIZ / "contenido" / "fichas.csv"


def filas() -> list[dict[str, str]]:
    return leer_filas(RUTA_CSV)


def test_columnas_congeladas() -> None:
    with RUTA_CSV.open(encoding="utf-8-sig", newline="") as archivo:
        assert next(csv.reader(archivo)) == COLUMNAS


def test_hay_diez_fichas_con_ids_unicos() -> None:
    datos = filas()
    assert len(datos) == 10
    ids = [fila["id"] for fila in datos]
    assert len(ids) == len(set(ids))


def test_revisor_y_fecha_asignados() -> None:
    for fila in filas():
        assert fila["revisor"].strip().lower() not in {"", "por asignar"}, fila["id"]
        date.fromisoformat(fila["fecha_verificacion"])


def test_alt_text_no_queda_pendiente() -> None:
    for fila in filas():
        assert fila["alt_text"].strip(), fila["id"]
        assert "por confirmar" not in fila["alt_text"].lower(), fila["id"]


def test_al_menos_dos_fuentes_https() -> None:
    for fila in filas():
        urls = [
            fila[f"fuente{n}_url"].strip()
            for n in (1, 2, 3)
            if fila[f"fuente{n}_url"].strip()
        ]
        assert len(urls) >= 2, fila["id"]
        assert all(url.startswith("https://") for url in urls), fila["id"]


def test_imagen_sigue_el_patron() -> None:
    for fila in filas():
        assert fila["imagen"] == f"{fila['id']}_main.jpg", fila["id"]


def test_los_bloques_respetan_el_limite_de_palabras() -> None:
    for fila in filas():
        for campo, limite in LIMITES_HISTORIA.items():
            palabras = len(fila[campo].split())
            assert palabras <= limite, (fila["id"], campo, palabras)
