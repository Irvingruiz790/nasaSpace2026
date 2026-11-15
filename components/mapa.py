"""Mapa de una zona con marcadores sobre la imagen de fondo.

Dueño: Frontend.

El fondo se dibuja a todo el ancho y encima van botones en las coordenadas
x/y (porcentajes de 0 a 100) que entrega `core.datos` desde
`assets/maps/posiciones.json`. Al tocar un marcador se abre su ficha.

Las piezas sin coordenada no desaparecen: caen a una fila debajo del mapa.
El estilo base vive en `assets/styles.css`; aquí solo se generan las
posiciones, porque vienen de los datos y cambian con cada zona.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import streamlit as st

RAIZ = Path(__file__).resolve().parent.parent

FONDOS = {
    "luna": "luna.jpg",
    "marte": "marte.jpg",
    "espacio_profundo": "espacio_profundo.jpg",
}

# Las piezas que caen al otro lado del globo no se ven en el disco: en vez de
# decir que «no tienen posición», se explica dónde están.
LETREROS_SUELTAS = {
    "marte": "Al otro lado de Marte",
}
LETRERO_SUELTAS = "Piezas sin posición en el mapa"


def letrero_sueltas(zona: str) -> str:
    """Frase que encabeza la fila de piezas que no caben en el mapa."""
    return LETREROS_SUELTAS.get(zona, LETRERO_SUELTAS)

# Un apodo más largo que esto ya es una frase, no una etiqueta de mapa.
LARGO_APODO = 18
LARGO_NOMBRE = 22


def etiqueta_marcador(pieza: dict[str, Any]) -> str:
    """Texto corto del marcador: «Eagle», «Surveyor 3», «Voyager 1»."""
    apodo = str(pieza.get("apodo") or "").strip()
    if 0 < len(apodo) <= LARGO_APODO:
        return apodo

    nombre = str(pieza.get("nombre") or pieza.get("id") or "Pieza")
    corto = re.sub(r"\s*\([^)]*\)", " ", nombre).split(",")[0]
    corto = re.sub(r"\s{2,}", " ", corto).strip()
    if len(corto) > LARGO_NOMBRE:
        corto = corto[:LARGO_NOMBRE].rsplit(" ", 1)[0].rstrip(" ,.;:") + "…"
    return corto or "Pieza"


def clase_key(key: str) -> str:
    """Clase CSS que Streamlit agrega al elemento que tiene `key`."""
    return "st-key-" + re.sub(r"[^a-zA-Z0-9_-]", "-", key)


def coordenada(valor: Any) -> float | None:
    """Devuelve el número si es una coordenada válida (0 a 100); si no, None."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        return None
    numero = float(valor)
    return numero if 0 <= numero <= 100 else None


def repartir(
    piezas: list[dict[str, Any]],
    marcadores: Any,
) -> tuple[
    list[tuple[dict[str, Any], float, float]],
    list[dict[str, Any]],
]:
    """Separa las piezas con posición de las que no la tienen.

    Conserva el orden recibido en las dos listas para que el mapa sea estable
    entre recargas.
    """
    por_id = marcadores if isinstance(marcadores, dict) else {}

    con_posicion: list[tuple[dict[str, Any], float, float]] = []
    sin_posicion: list[dict[str, Any]] = []

    for pieza in piezas:
        xy = por_id.get(str(pieza.get("id", "")))
        x = coordenada(xy.get("x")) if isinstance(xy, dict) else None
        y = coordenada(xy.get("y")) if isinstance(xy, dict) else None
        if x is None or y is None:
            sin_posicion.append(pieza)
        else:
            con_posicion.append((pieza, x, y))

    return con_posicion, sin_posicion


def _estilos(zona: str, colocadas: list[tuple[dict[str, Any], float, float]]) -> str:
    """Bloque `<style>` con la posición de cada marcador."""
    reglas: list[str] = []
    for pieza, x, y in colocadas:
        key = f"marcador_{zona}_{pieza.get('id')}"
        reglas.append(f".{clase_key(key)}{{left:{x:.2f}%;top:{y:.2f}%;}}")

    return f"<style>{''.join(reglas)}</style>" if reglas else ""


def _abrir_ficha(pieza_id: Any) -> None:
    st.session_state["pieza_sel"] = pieza_id
    st.switch_page("pages/7_Ficha.py")


def _boton(
    pieza: dict[str, Any],
    key: str,
    etiqueta: str,
    *,
    ancho: str = "content",
) -> None:
    if st.button(
        etiqueta,
        key=key,
        help=str(pieza.get("nombre") or pieza.get("id") or ""),
        width=ancho,
    ):
        _abrir_ficha(pieza.get("id"))


def mapa_zona(
    zona: str,
    piezas: list[dict[str, Any]],
    posiciones: dict[str, dict[str, dict[str, float]]],
) -> None:
    """Pinta el fondo de la zona y un marcador por pieza encima."""
    fondo = RAIZ / "assets" / "maps" / FONDOS.get(zona, "")

    marcadores = posiciones.get(zona) if isinstance(posiciones, dict) else None
    colocadas, sueltas = repartir(piezas, marcadores)

    st.markdown(_estilos(zona, colocadas), unsafe_allow_html=True)

    with st.container(key=f"mapa_{zona}"):
        if fondo.is_file():
            st.image(str(fondo), width="stretch")
        else:
            st.markdown(
                '<div class="fe1-mapa-vacio">Mapa de la zona'
                "<br><small>Fondo pendiente: assets/maps/"
                f"{FONDOS.get(zona, 'zona.jpg')}</small></div>",
                unsafe_allow_html=True,
            )

        with st.container(key=f"capa_{zona}"):
            for pieza, _, _ in colocadas:
                _boton(
                    pieza,
                    key=f"marcador_{zona}_{pieza.get('id')}",
                    etiqueta=etiqueta_marcador(pieza),
                )

    if sueltas:
        st.caption(letrero_sueltas(zona))
        columnas = st.columns(len(sueltas))
        for columna, pieza in zip(columnas, sueltas):
            with columna:
                _boton(
                    pieza,
                    key=f"suelto_{zona}_{pieza.get('id')}",
                    etiqueta=etiqueta_marcador(pieza),
                    ancho="stretch",
                )
