"""Página de inicio de «¿Dónde está ahora?».

Dueño: Frontend.
Aquí no hay lógica de datos: se usa `core.datos` y se pinta.
"""

from __future__ import annotations

import streamlit as st

from components.tarjeta import tarjeta
from components.ui import aplicar_estilos
from core import datos

st.set_page_config(
    page_title="¿Dónde está ahora?",
    page_icon="🚀",
    layout="wide",
)

aplicar_estilos()

st.markdown(
    '<div class="fe1-hero">'
    "<h1>¿Dónde está ahora?</h1>"
    "<p>Un viaje por las máquinas que la NASA dejó en la Luna, en Marte y en el "
    "espacio profundo. Todavía están ahí. Algunas siguen hablando.</p>"
    "</div>",
    unsafe_allow_html=True,
)

piezas = datos.cargar_piezas()

if not piezas:
    st.warning(
        "Todavía no hay datos cargados. Backend debe generar `data/artifacts.json` "
        "con `python scripts/fichas_a_json.py`."
    )
    st.stop()

zonas = datos.contar_por_zona(piezas)
columnas = st.columns(4)
columnas[0].metric("Piezas en total", len(piezas))
columnas[1].metric("En la Luna", zonas["luna"])
columnas[2].metric("En Marte", zonas["marte"])
columnas[3].metric("En el espacio profundo", zonas["espacio_profundo"])

st.subheader("Elige una zona")

enlaces = st.columns(3)
with enlaces[0]:
    st.page_link("pages/1_Luna.py", label="La Luna", icon="🌕")
with enlaces[1]:
    st.page_link("pages/2_Marte.py", label="Marte", icon="🔴")
with enlaces[2]:
    st.page_link("pages/3_Espacio_profundo.py", label="Espacio profundo", icon="🌌")

st.subheader("Algunas de las piezas")

destacadas = [pieza for pieza in piezas if pieza.get("estado") == "activo"][:3]
if not destacadas:
    destacadas = piezas[:3]

for pieza in destacadas:
    tarjeta(pieza)

st.divider()
st.caption(
    "Proyecto del NASA Space Apps Challenge 2026. Datos de NASA, NSSDCA y JPL. "
    "No está afiliado a NASA."
)
