"""Utilidades visuales compartidas por todas las páginas.

Dueño: Frontend.
"""

from __future__ import annotations

from html import escape
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


def encabezado(
    titulo: str,
    descripcion: str,
    *,
    variante: str = "",
    grande: bool = False,
) -> None:
    """Título de sección con una frase de contexto.

    `variante` elige el cielo del encabezado (luna, marte, espacio-profundo,
    vivo, quiz, fuentes o inicio). `grande` deja el formato de portada; sin él
    se usa el formato compacto de las páginas internas.
    """
    clases = ["fe1-hero", "fe1-hero--inicio" if grande else "fe1-hero--pequeno"]
    if variante:
        clases.append(f"fe1-hero--{variante}")

    st.markdown(
        f'<div class="{" ".join(clases)}"><h1>{escape(titulo)}</h1>'
        f"<p>{escape(descripcion)}</p></div>",
        unsafe_allow_html=True,
    )
