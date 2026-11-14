# `pages/` — una pantalla por archivo

**Dueño:** Frontend.
Streamlit arma el menú lateral solo, con el nombre de cada archivo.

---

## Qué va aquí

| Archivo | Pantalla |
|---|---|
| `1_Luna.py` | Mapa y fichas de la Luna |
| `2_Marte.py` | Mapa y fichas de Marte |
| `3_Espacio_profundo.py` | Mapa y fichas del espacio profundo |
| `4_En_vivo.py` | Panel con distancia y tiempo de luz |
| `5_Quiz.py` | Quiz de tres preguntas |
| `6_Fuentes.py` | Fuentes de cada pieza y enlaces oficiales |
| `7_Ficha.py` | Ficha completa de la pieza elegida |

## Formato y convenciones

- **Python** (`.py`), una pantalla por archivo.
- El nombre empieza con número y guion bajo: `8_Mi_pagina.py`. Así se controla
  el orden del menú.
- Cada archivo llama a `aplicar_estilos()` al inicio.
- Los datos se piden a `core` (`datos`, `vivo`, `formato`). **Nunca** se abre un
  JSON a mano ni se importa `requests`.
- La pieza elegida viaja en `st.session_state["pieza_sel"]`; para cambiar de
  pantalla se usa `st.switch_page("pages/7_Ficha.py")`.

## Reglas

- No dejar una pantalla en blanco: siempre un mensaje amable si faltan datos.
- No duplicar lógica entre páginas: si se repite, va a `components/`.
- No cambiar nombres de campos del dataset desde aquí.
- Toda página nueva se agrega a la guía Word (`scripts/generar_guia_word.py`).
- Probar en celular (ancho de 390 px) antes de abrir el PR.
