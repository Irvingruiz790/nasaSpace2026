# `assets/` — archivos estáticos

**Dueño:** Frontend (estilos y mapas) e Investigación (imágenes).
Aquí no hay código Python: solo archivos que la app muestra tal cual.

---

## Qué va aquí

| Ruta | Contenido | Formato |
|---|---|---|
| `styles.css` | Colores, tipografía, tarjetas y estados | CSS |
| `img/` | Fotos de las piezas | JPG o WebP |
| `maps/` | Fondos de los mapas y coordenadas de marcadores | JPG/WebP + JSON |

## Reglas

- Los nombres de archivo van en **minúsculas y con guiones**. Sin espacios,
  sin acentos, sin «foto final (2).jpg».
- Las imágenes pesan **menos de 300 KB** y miden unos 1200 px de ancho.
- Toda imagen necesita crédito en `contenido/fichas.csv`.
- No se usan fuentes, iconos ni CSS desde internet: si se cae la red, la app
  debe verse igual.
- No se suben archivos de diseño (`.psd`, `.ai`, `.fig`): solo el resultado
  exportado.
