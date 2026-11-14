"""Pruebas del cargador y del validador del dataset."""

from __future__ import annotations

import copy

from core import datos


def piezas() -> list[dict]:
    return datos.cargar_piezas()


def test_carga_el_archivo_de_ejemplo() -> None:
    lista = piezas()
    assert len(lista) >= 2
    assert {p["id"] for p in lista} >= {"voyager-1", "apollo-11-lm"}


def test_el_ejemplo_no_tiene_errores_de_contrato() -> None:
    problemas = datos.validar_piezas(piezas())
    assert datos.errores(problemas) == [], [str(p) for p in datos.errores(problemas)]


def test_las_imagenes_faltantes_son_aviso_y_no_error() -> None:
    problemas = datos.validar_piezas(piezas())
    de_imagen = [p for p in problemas if p.campo == "imagen"]
    assert de_imagen, "el ejemplo todavía no tiene imágenes reales"
    assert all(p.severidad == "aviso" for p in de_imagen)


def test_detecta_id_repetido() -> None:
    lista = piezas()
    lista.append(copy.deepcopy(lista[0]))
    problemas = datos.errores(datos.validar_piezas(lista))
    assert any("repetido" in p.mensaje for p in problemas)


def test_detecta_zona_invalida() -> None:
    pieza = copy.deepcopy(piezas()[0])
    pieza["zona"] = "jupiter"
    problemas = datos.errores(datos.validar_pieza(pieza))
    assert any(p.campo == "zona" for p in problemas)


def test_detecta_id_que_no_es_kebab() -> None:
    pieza = copy.deepcopy(piezas()[0])
    pieza["id"] = "Voyager_Uno"
    problemas = datos.errores(datos.validar_pieza(pieza))
    assert any(p.campo == "id" for p in problemas)


def test_detecta_historia_incompleta() -> None:
    pieza = copy.deepcopy(piezas()[0])
    del pieza["historia"]["dato_curioso"]
    problemas = datos.errores(datos.validar_pieza(pieza))
    assert any(p.campo == "historia.dato_curioso" for p in problemas)


def test_bloque_demasiado_largo_es_aviso() -> None:
    pieza = copy.deepcopy(piezas()[0])
    pieza["historia"]["que_es"] = "palabra " * 60
    problemas = datos.validar_pieza(pieza)
    largos = [p for p in problemas if p.campo == "historia.que_es"]
    assert largos and largos[0].severidad == "aviso"


def test_buscar_y_filtrar_por_zona() -> None:
    lista = piezas()
    assert datos.buscar(lista, "voyager-1")["nombre"] == "Voyager 1"
    assert datos.buscar(lista, "no-existe") is None
    assert all(p["zona"] == "luna" for p in datos.por_zona(lista, "luna"))


def test_mapa_de_horizons() -> None:
    assert datos.con_horizons(piezas()) == {"voyager-1": "-31", "voyager-2": "-32"}


def test_resumen() -> None:
    resumen = datos.resumen(piezas())
    assert resumen["total"] == len(piezas())
    assert resumen["errores"] == 0
    assert set(resumen["por_zona"]) == {
        "luna",
        "marte",
        "espacio_profundo",
        "orbita",
        "asteroide",
    }


def test_archivo_inexistente_no_explota() -> None:
    assert datos.cargar_piezas("no-existe.json") == []
