"""Quiz de tres preguntas. Dueño: Frontend.

Las preguntas se arman con las piezas reales del dataset: si investigación
agrega una pieza, el quiz la puede usar sin tocar el código.
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from components.ui import aplicar_estilos, encabezado
from core import datos

NOMBRES_ZONA = {
    "luna": "La Luna",
    "marte": "Marte",
    "espacio_profundo": "El espacio profundo",
    "orbita": "La órbita de la Tierra",
    "asteroide": "Un asteroide",
}

st.set_page_config(
    page_title="Quiz — ¿Dónde está ahora?",
    page_icon="🧠",
    layout="wide",
)
aplicar_estilos()
encabezado(
    "Quiz",
    "Tres preguntas rápidas para ver si estuviste poniendo atención. "
    "Puedes intentarlo todas las veces que quieras.",
    variante="quiz",
)


def construir_preguntas(piezas: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Una pregunta de zona por cada una de las tres primeras piezas."""
    preguntas: list[dict[str, Any]] = []
    opciones = list(dict.fromkeys(NOMBRES_ZONA.values()))

    for pieza in piezas[:3]:
        preguntas.append(
            {
                "pregunta": f"¿Dónde está {pieza.get('nombre', 'esta pieza')}?",
                "opciones": opciones,
                "correcta": NOMBRES_ZONA.get(pieza.get("zona", ""), ""),
            }
        )
    return preguntas


piezas = datos.cargar_piezas()
preguntas = construir_preguntas(piezas)

if not preguntas:
    st.info(
        "Todavía no hay piezas para armar el quiz. Backend debe generar "
        "`data/artifacts.json`."
    )
    st.stop()

respuestas: list[str | None] = []

for numero, pregunta in enumerate(preguntas, start=1):
    st.markdown(f"**{numero}. {pregunta['pregunta']}**")
    respuestas.append(
        st.radio(
            "Elige una opción",
            pregunta["opciones"],
            index=None,
            key=f"quiz_{numero}",
            label_visibility="collapsed",
        )
    )

if st.button("Revisar respuestas", type="primary"):
    aciertos = 0
    for numero, (pregunta, respuesta) in enumerate(zip(preguntas, respuestas), start=1):
        if respuesta is None:
            st.warning(f"Pregunta {numero}: te faltó responder.")
        elif respuesta == pregunta["correcta"]:
            aciertos += 1
            st.success(f"Pregunta {numero}: ¡correcto! Es {pregunta['correcta']}.")
        else:
            st.error(
                f"Pregunta {numero}: era {pregunta['correcta']}, no «{respuesta}»."
            )

    st.metric("Aciertos", f"{aciertos} de {len(preguntas)}")
    if aciertos == len(preguntas):
        st.balloons()

st.divider()
st.page_link("app.py", label="Volver al inicio", icon="🏠")
