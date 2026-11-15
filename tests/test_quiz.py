"""Banco con evidencia y transiciones de partidas completas."""

import random

from streamlit.testing.v1 import AppTest

from core import datos, quiz


def test_banco_tiene_30_preguntas_con_fuentes_y_una_respuesta():
    piezas = datos.cargar_piezas()
    preguntas = quiz.construir_preguntas(piezas)
    assert len(preguntas) == len({p["id"] for p in preguntas}) == 30
    assert len({p["pregunta"] for p in preguntas}) == 30
    assert len({p["pieza_id"] for p in preguntas}) == 10
    por_id = {p["id"]: p for p in piezas}
    for p in preguntas:
        assert len(set(p["opciones"])) == 4
        assert p["opciones"].count(p["correcta"]) == 1
        assert p["explicacion"] in por_id[p["pieza_id"]]["historia"].values()
        assert p["fuentes"] == por_id[p["pieza_id"]]["fuentes"]


def test_aleatorizar_no_pierde_preguntas_ni_modifica_banco():
    preguntas = quiz.construir_preguntas(datos.cargar_piezas())
    a = quiz.nueva_partida(preguntas, random.Random(1))
    b = quiz.nueva_partida(preguntas, random.Random(2))
    assert [p["id"] for p in a["preguntas"]] != [p["id"] for p in b["preguntas"]]
    assert {p["id"] for p in a["preguntas"]} == {p["id"] for p in preguntas}
    assert all(p["opciones"][0] == p["correcta"] for p in preguntas)
    assert any(p["opciones"][0] != p["correcta"] for p in a["preguntas"])


def test_respuestas_duplicadas_y_eventos_de_otra_partida_se_ignoran():
    partida = quiz.nueva_partida(quiz.construir_preguntas(datos.cargar_piezas()))
    p = partida["preguntas"][0]
    assert not quiz.responder(partida, "vieja", 0, p["correcta"])
    assert not quiz.responder(partida, partida["id"], 0, "inventada")
    assert quiz.responder(partida, partida["id"], 0, p["correcta"])
    assert not quiz.responder(partida, partida["id"], 0, p["correcta"])
    assert partida["aciertos"] == 1
    for i, p in enumerate(partida["preguntas"][1:], 1):
        incorrecta = next(o for o in p["opciones"] if o != p["correcta"])
        assert quiz.responder(partida, partida["id"], i, incorrecta)
    assert len(partida["respuestas"]) == 30
    assert partida["aciertos"] == 1
    assert not quiz.responder(partida, partida["id"], 30, "extra")


def test_menu_partida_completa_y_record_al_reiniciar():
    app = AppTest.from_file("../app.py").run()
    app.switch_page("pages/5_Quiz.py").run()
    assert not app.exception
    assert app.button(key="quiz_iniciar")
    app.button(key="quiz_iniciar").click().run()
    for i in range(30):
        partida = app.session_state["quiz_partida"]
        assert len(partida["respuestas"]) == i
        pregunta = partida["preguntas"][i]
        opciones = [b for b in app.button if b.key.startswith("quiz_opcion_")]
        assert len(opciones) == 4
        next(b for b in opciones if b.label[3:] == pregunta["correcta"]).click().run()
        assert not app.exception
    assert app.session_state["quiz_mejor"] == 30
    app.button(key="quiz_menu").click().run()
    app.button(key="quiz_iniciar").click().run()
    assert app.session_state["quiz_mejor"] == 30
    assert app.session_state["quiz_partida"]["respuestas"] == []
