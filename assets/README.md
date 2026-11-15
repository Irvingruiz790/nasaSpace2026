# `assets/` — archivos estáticos

**Dueño:** Frontend (estilos y mapas) e Investigación (imágenes).
Aquí no hay código Python: solo archivos que la app muestra tal cual.

---

## Qué va aquí

| Ruta | Contenido | Formato |
|---|---|---|
| `styles.css` | Colores, tipografía, tarjetas, encabezados y estados | CSS |
| `img/` | Fotos de las piezas | JPG o WebP |
| `maps/` | Fondos de los mapas y coordenadas de marcadores | JPG/WebP + JSON |

## Tipografía

`styles.css` declara `@font-face` para **Orbitron** (títulos) y **Overpass**
(texto). Los archivos no viven aquí: Streamlit solo sirve la carpeta `static/`
del proyecto, así que las fuentes y sus licencias OFL están en
[`static/fonts/`](../static/README.md). La app no pide ninguna fuente a
internet.

Los fondos fotográficos de los encabezados también viven en `static/img/`
porque la CSS los pide al navegador; sus créditos están en
[`static/README.md`](../static/README.md).

## Reglas

- Los nombres de archivo van en **minúsculas y con guiones**. Sin espacios,
  sin acentos, sin «foto final (2).jpg».
- Las fotos de `img/` pesan **menos de 300 KB**, son **horizontales** y miden
  unos **1200 px de ancho**.
- Los fondos de `static/img/encabezados/` miden **1200 × 675 px** y pesan
  **menos de 300 KB**.
- Los fondos de `maps/` pesan **menos de 300 KB** y miden unos **1600 px de
  ancho**.
- Toda imagen necesita crédito y `alt_text` en `contenido/fichas.csv`.
- No se usan fuentes, iconos ni CSS desde internet: si se cae la red, la app
  debe verse igual.
- No se suben archivos de diseño (`.psd`, `.ai`, `.fig`): solo el resultado
  exportado.
