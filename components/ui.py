"""Utilidades visuales compartidas por todas las páginas.

Dueño: Frontend.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

import streamlit as st

RAIZ = Path(__file__).resolve().parent.parent
ARCHIVO_CSS = RAIZ / "assets" / "styles.css"

# Crédito que se pinta bajo el texto de los encabezados con foto real.
CREDITOS = {
    "luna": "NASA · Apollo 17, 1972",
    "marte": "NASA/JPL · Viking 1, 1976",
    "espacio-profundo": "NASA/JPL · Voyager",
    "vivo": "NASA · Apollo 8, 1968",
}


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
    vivo, quiz, fuentes o inicio). Las variantes con foto real muestran su
    crédito debajo del texto. `grande` deja el formato de portada; sin él se
    usa el formato compacto de las páginas internas.
    """
    clases = ["fe1-hero", "fe1-hero--inicio" if grande else "fe1-hero--pequeno"]
    if variante:
        clases.append(f"fe1-hero--{variante}")

    credito = CREDITOS.get(variante)
    pie = f'<small class="fe1-hero__credito">{escape(credito)}</small>' if credito else ""

    st.markdown(
        f'<div class="{" ".join(clases)}"><h1>{escape(titulo)}</h1>'
        f"<p>{escape(descripcion)}</p>{pie}</div>",
        unsafe_allow_html=True,
    )
