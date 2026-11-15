"""Pruebas de los marcadores del mapa."""

from __future__ import annotations

import pytest

from components.mapa import clase_key, coordenada, etiqueta_marcador, repartir


def pieza(**extra: object) -> dict:
    base = {
        "id": "apollo-11-lm",
        "nombre": "Apolo 11, etapa de descenso del módulo lunar Eagle",
        "apodo": "Eagle",
    }
    base.update(extra)
    return base


def test_el_apodo_corto_es_la_etiqueta() -> None:
    assert etiqueta_marcador(pieza()) == "Eagle"


def test_un_apodo_frase_no_se_usa_como_etiqueta() -> None:
    larga = pieza(apodo="El robot que probó el suelo de la Luna")
    assert etiqueta_marcador(larga) == "Apolo 11"


def test_la_etiqueta_quita_el_parentesis() -> None:
    assert etiqueta_marcador(pieza(apodo="", nombre="Vehículo (LRV-3)")) == "Vehículo"


def test_la_etiqueta_no_pasa_del_limite() -> None:
    etiqueta = etiqueta_marcador(pieza(apodo="", nombre="Una pieza con un nombre larguísimo"))
    assert len(etiqueta) <= 23
    assert etiqueta.endswith("…")


@pytest.mark.parametrize("valor", [0, 100, 63.4, 0.0])
def test_coordenada_valida(valor: float) -> None:
    assert coordenada(valor) == float(valor)


@pytest.mark.parametrize("valor", [-1, 101, "50", None, True, False])
def test_coordenada_invalida(valor: object) -> None:
    assert coordenada(valor) is None


def test_repartir_separa_las_piezas_sin_posicion() -> None:
    piezas = [
        pieza(id="con-x", apodo="Eagle"),
        pieza(id="sin-x", apodo="Rover"),
    ]
    marcadores = {"con-x": {"x": 63.4, "y": 49.5}, "sin-x": {"x": 150, "y": 10}}

    colocadas, sueltas = repartir(piezas, marcadores)

    assert [p["id"] for p, _, _ in colocadas] == ["con-x"]
    assert [p["id"] for p in sueltas] == ["sin-x"]


def test_repartir_aguanta_un_json_raro() -> None:
    colocadas, sueltas = repartir([pieza()], None)
    assert colocadas == []
    assert len(sueltas) == 1


def test_la_clase_key_es_segura_para_css() -> None:
    assert clase_key("marcador_luna_apollo-11-lm") == "st-key-marcador_luna_apollo-11-lm"
    assert clase_key("a b.c") == "st-key-a-b-c"
