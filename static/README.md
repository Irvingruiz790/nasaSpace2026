# `static/` — archivos que Streamlit sirve al navegador

**Dueño:** Frontend (fuentes y estilos) y Backend (configuración del servidor).

Streamlit solo expone al navegador el contenido de `./static`. Por eso las
fuentes tipográficas viven aquí y no en `assets/`: desde `assets/` darían 404.

---

## Qué va aquí

| Ruta | Contenido | Licencia |
|---|---|---|
| `fonts/exo2-latin.woff2` | Exo 2, títulos y encabezados | SIL Open Font License 1.1 |
| `fonts/overpass-latin.woff2` | Overpass, texto corrido | SIL Open Font License 1.1 |
| `fonts/OFL-Exo2.txt` | Licencia de Exo 2 | — |
| `fonts/OFL-Overpass.txt` | Licencia de Overpass | — |

Las dos familias son libres, se pueden empaquetar y se sirven desde el propio
dominio de la app. Así se ve igual sin internet y no hay peticiones a Google
Fonts ni a ningún CDN.

## Cómo se sirven

En `.streamlit/config.toml`:

```toml
[server]
enableStaticServing = true

[[theme.fontFaces]]
family = "Exo 2"
url = "app/static/fonts/exo2-latin.woff2"
weight_range = "100 900"
```

El navegador las pide en `/app/static/fonts/...`. `assets/styles.css` declara
los mismos `@font-face` para que también las usen los encabezados escritos con
HTML propio.

## Reglas

- Archivos `.woff2` únicamente, subset **latin**, menos de 60 KB cada uno.
- No se agregan fuentes con licencia solo para uso personal.
- Si se cambia o actualiza una fuente, se sube también su licencia OFL.
- No se sirven aquí datos, CSV ni nada que deba pasar por `core.datos`.
