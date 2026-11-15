"""Mapa sencillo de una zona.

Dueño: Frontend.

Este es el esqueleto que ya funciona. Dibuja la imagen de fondo (si existe) y
pone un botón por pieza, ordenados de izquierda a derecha según las posiciones
que recibe ya cargadas desde `assets/maps/posiciones.json`.

El mapa "de verdad" —marcadores superpuestos sobre la imagen en las coordenadas
x/y del JSON— es la tarea 7 del frontend. Aquí se deja lo mínimo para que las
tres zonas ya se puedan recorrer.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import streamlit as st

RAIZ = Path(__file__).resolve().parent.parent

FONDOS = {
    "luna": "luna.jpg",
    "marte": "marte.jpg",
    "espacio_profundo": "espacio_profundo.jpg",
}


def mapa_zona(
    zona: str,
    piezas: list[dict[str, Any]],
    posiciones: dict[str, dict[str, dict[str, float]]],
) -> None:
    """Pinta el fondo de la zona y un botón por pieza."""
    fondo = RAIZ / "assets" / "maps" / FONDOS.get(zona, "")

    if fondo.is_file():
        st.image(str(fondo), width="stretch")
    else:
        st.markdown(
            '<div class="fe1-mapa-vacio">Mapa de la zona'
            "<br><small>Fondo pendiente: assets/maps/"
            f"{FONDOS.get(zona, 'zona.jpg')}</small></div>",
            unsafe_allow_html=True,
        )

    marcadores = posiciones.get(zona) or {}

    def clave_orden(pieza: dict[str, Any]) -> float:
        return float(marcadores.get(pieza.get("id", ""), {}).get("x", 50))

    ordenadas = sorted(piezas, key=clave_orden)
    columnas = st.columns(max(1, len(ordenadas)))

    for columna, pieza in zip(columnas, ordenadas):
        with columna:
            if st.button(
                pieza.get("nombre", "Pieza"),
                key=f"marcador_{zona}_{pieza.get('id')}",
                width="stretch",
            ):
                st.session_state["pieza_sel"] = pieza.get("id")
                st.switch_page("pages/7_Ficha.py")
