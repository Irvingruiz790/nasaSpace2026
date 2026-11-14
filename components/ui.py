"""Utilidades visuales compartidas por todas las páginas.

Dueño: Frontend.
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

RAIZ = Path(__file__).resolve().parent.parent
ARCHIVO_CSS = RAIZ / "assets" / "styles.css"


def aplicar_estilos() -> None:
    """Inyecta `assets/styles.css` en la página actual.

    Streamlit vuelve a ejecutar cada página por separado, así que hay que
    llamarla al principio de cada archivo de `pages/`.
    """
    if not ARCHIVO_CSS.exists():
        return
    st.markdown(
        f"<style>{ARCHIVO_CSS.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )


def encabezado(titulo: str, descripcion: str) -> None:
    """Título de zona con una frase de contexto."""
    st.markdown(
        f'<div class="fe1-hero fe1-hero--pequeno"><h1>{titulo}</h1>'
        f"<p>{descripcion}</p></div>",
        unsafe_allow_html=True,
    )
