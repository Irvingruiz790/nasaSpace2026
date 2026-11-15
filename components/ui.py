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
    "quiz": "NASA/JPL · Montaje del sistema solar",
}


# Streamlit pinta un enlace junto a cada título, pero al tocarlo el navegador
# salta a la sección en vez de copiar la dirección. Este script lo intercepta,
# copia el enlace completo y muestra un aviso breve. Es JavaScript propio, sin
# librerías ni peticiones de red.
COPIAR_ANCLAS = """
<script>
(() => {
  if (window.__fe1Anclas) return;
  window.__fe1Anclas = true;

  const AVISO_ID = "fe1-aviso-ancla";

  function avisar(texto) {
    let aviso = document.getElementById(AVISO_ID);
    if (!aviso) {
      aviso = document.createElement("div");
      aviso.id = AVISO_ID;
      aviso.className = "fe1-aviso-ancla";
      aviso.setAttribute("role", "status");
      aviso.setAttribute("aria-live", "polite");
      document.body.appendChild(aviso);
    }
    aviso.textContent = texto;
    aviso.classList.add("fe1-aviso-ancla--visible");
    window.clearTimeout(window.__fe1Aviso);
    window.__fe1Aviso = window.setTimeout(
      () => aviso.classList.remove("fe1-aviso-ancla--visible"),
      1900
    );
  }

  function copiaDeRespaldo(texto) {
    return new Promise((resolver, rechazar) => {
      const area = document.createElement("textarea");
      area.value = texto;
      area.setAttribute("readonly", "");
      area.style.position = "fixed";
      area.style.top = "-1000px";
      area.style.opacity = "0";
      document.body.appendChild(area);
      area.select();
      const listo = document.execCommand("copy");
      area.remove();
      listo ? resolver() : rechazar(new Error("copy"));
    });
  }

  function copiar(texto) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard
        .writeText(texto)
        .catch(() => copiaDeRespaldo(texto));
    }
    return copiaDeRespaldo(texto);
  }

  document.addEventListener("click", (evento) => {
    const enlace = evento.target.closest(
      '[data-testid="stHeaderActionElements"] a[href^="#"]'
    );
    if (!enlace) return;

    // Sin esto el navegador cambia el hash y la página salta de sección.
    evento.preventDefault();
    evento.stopPropagation();

    const hash = enlace.getAttribute("href") || "";
    const base = location.origin + location.pathname + location.search;
    copiar(base + hash).then(
      () => avisar("Enlace copiado"),
      () => avisar("No se pudo copiar el enlace")
    );
  });

  // El rótulo que trae Streamlit está en inglés; lo pasamos a español.
  const traducir = () => {
    document
      .querySelectorAll('a[aria-label="Link to heading"]')
      .forEach((enlace) => {
        enlace.setAttribute("aria-label", "Copiar enlace a esta sección");
        enlace.setAttribute("title", "Copiar enlace a esta sección");
      });
  };
  traducir();
  new MutationObserver(traducir).observe(document.body, {
    childList: true,
    subtree: true,
  });
})();
</script>
"""


def aplicar_estilos() -> None:
    """Inyecta `assets/styles.css` y el copiador de anclas en la página actual.

    Streamlit vuelve a ejecutar cada página por separado, así que hay que
    llamarla al principio de cada archivo de `pages/`.
    """
    if not ARCHIVO_CSS.exists():
        return
    st.markdown(
        f"<style>{ARCHIVO_CSS.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )
    st.html(COPIAR_ANCLAS, unsafe_allow_javascript=True)


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
