"""Pruebas del conversor CSV -> JSON (investigación -> backend)."""

from __future__ import annotations

import json

from core import config, datos
from scripts.fichas_a_json import COLUMNAS, convertir


def test_convierte_el_csv_real(tmp_path) -> None:
    salida = tmp_path / "artifacts.json"
    piezas, problemas = convertir(
        config.RAIZ / "contenido" / "fichas.csv", salida, escribir=True
    )

    assert len(piezas) == 3
    assert datos.errores(problemas) == [], [str(p) for p in datos.errores(problemas)]

    guardado = json.loads(salida.read_text(encoding="utf-8"))
    assert len(guardado["piezas"]) == 3

    voyager = datos.buscar(guardado["piezas"], "voyager-1")
    assert voyager is not None
    assert voyager["historia"]["que_es"].startswith("Una nave")
    assert len(voyager["fuentes"]) == 3
    assert voyager["lat"] is None
    assert voyager["horizons_id"] == "-31"


def test_la_imagen_se_convierte_en_ruta_completa(tmp_path) -> None:
    piezas, _ = convertir(
        config.RAIZ / "contenido" / "fichas.csv", tmp_path / "x.json", escribir=False
    )
    assert all(p["imagen"].startswith("assets/img/") for p in piezas)


def test_acepta_coma_decimal(tmp_path) -> None:
    csv_texto = ",".join(COLUMNAS) + "\n"
    fila = {columna: "" for columna in COLUMNAS}
    fila.update(
        {
            "id": "prueba-1",
            "nombre": "Prueba",
            "apodo": "La de prueba",
            "tipo": "lander",
            "mision": "Prueba",
            "agencia": "NASA",
            "zona": "luna",
            "estado": "se_quedo",
            "etiqueta_estado": "Se quedó",
            "ubicacion_texto": "un cráter",
            "lat": "0,67416",
            "lon": "-23,47314",
            "lanzamiento": "1969-07-16",
            "imagen": "prueba-1_main.jpg",
            "credito_imagen": "NASA",
            "alt_text": "Una prueba",
            "que_es": "a",
            "por_que": "b",
            "descubrimiento": "c",
            "ahora": "d",
            "dato_curioso": "e",
            "fuente1_titulo": "F1",
            "fuente1_url": "https://nasa.gov",
            "fuente2_titulo": "F2",
            "fuente2_url": "https://nasa.gov",
        }
    )
    import csv as modulo_csv

    archivo = tmp_path / "fichas.csv"
    with archivo.open("w", encoding="utf-8-sig", newline="") as f:
        escritor = modulo_csv.DictWriter(f, fieldnames=COLUMNAS)
        escritor.writeheader()
        escritor.writerow(fila)

    piezas, problemas = convertir(archivo, tmp_path / "x.json", escribir=False)
    assert len(piezas) == 1
    assert piezas[0]["lat"] == 0.67416
    assert piezas[0]["lon"] == -23.47314
    assert datos.errores(problemas) == []


def test_avisa_si_falta_un_campo(tmp_path) -> None:
    archivo = tmp_path / "incompleto.csv"
    archivo.write_text("id,nombre\nsolo-id,Una pieza\n", encoding="utf-8")
    _, problemas = convertir(archivo, tmp_path / "x.json", escribir=False)
    assert datos.hay_errores(problemas)
