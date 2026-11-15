"""Selector de destinos con CSS local y navegación nativa de Streamlit."""

import streamlit as st


def sistema_solar() -> None:
    st.subheader("Explora el sistema solar")
    st.caption(
        "Toca un destino para explorar sus máquinas. "
        "Es un dibujo: los tamaños y las distancias no están a escala."
    )
    with st.container(key="sistema_solar"):
        st.html(
            '<div class="fe2-orbitas" aria-hidden="true">'
            '<span class="fe2-sol">Sol</span>'
            '<span class="fe2-tierra">Tierra</span></div>'
        )
        destinos = (
            ("luna", "La Luna", "pages/1_Luna.py"),
            ("marte", "Marte", "pages/2_Marte.py"),
            ("profundo", "Espacio profundo", "pages/3_Espacio_profundo.py"),
        )
        for clave, nombre, pagina in destinos:
            if st.button(nombre, key=f"destino_{clave}", width="stretch"):
                st.switch_page(pagina)
    st.caption("La Luna gira alrededor de la Tierra. Más allá de los planetas, viajan las Voyager.")
