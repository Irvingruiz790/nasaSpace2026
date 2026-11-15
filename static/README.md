# `static/` — archivos que Streamlit sirve al navegador

**Dueño:** Frontend (fuentes y estilos) y Backend (configuración del servidor).

Streamlit solo expone al navegador el contenido de `./static`. Por eso las
fuentes tipográficas viven aquí y no en `assets/`: desde `assets/` darían 404.

---

## Qué va aquí

| Ruta | Contenido | Licencia |
|---|---|---|
| `fonts/orbitron-latin.woff2` | Orbitron, títulos y encabezados | SIL Open Font License 1.1 |
| `fonts/overpass-latin.woff2` | Overpass, texto corrido | SIL Open Font License 1.1 |
| `fonts/OFL-Orbitron.txt` | Licencia de Orbitron | — |
| `fonts/OFL-Overpass.txt` | Licencia de Overpass | — |
| `img/encabezados/` | Fondos fotográficos de los encabezados (1200 × 675) | Dominio público NASA y una imagen aportada por el equipo |

Los cinco fondos se recortaron a 1200 × 675 px para que pesen menos de
300 KB. La portada es una ilustración de Marte, la Luna y la Tierra aportada
por el equipo; las otras cuatro salen del archivo de imágenes del NSSDCA:

| Archivo | Foto | Crédito |
|---|---|---|
| `img/encabezados/inicio_tres_mundos.jpg` | Marte, la Luna y la Tierra en una sola escena | Aportada por el equipo; crédito pendiente de confirmar |
| `img/encabezados/luna_apollo17.jpg` | Harrison Schmitt junto a la roca Boulder, Apollo 17 | NASA, 1972 |
| `img/encabezados/marte_viking1.jpg` | Panorama del Viking 1 Lander en Marte | NASA/JPL, 1976 |
| `img/encabezados/espacio_voyager.jpg` | Sonda Voyager | NASA/JPL |
| `img/encabezados/vivo_apollo8.jpg` | Earthrise, Apollo 8 | NASA, 1968 |

Las dos familias son libres, se pueden empaquetar y se sirven desde el propio
dominio de la app. Así se ve igual sin internet y no hay peticiones a Google
Fonts ni a ningún CDN.

## Cómo se sirven

En `.streamlit/config.toml`:

```toml
[server]
enableStaticServing = true

[[theme.fontFaces]]
family = "Orbitron"
url = "app/static/fonts/orbitron-latin.woff2"
weight_range = "400 900"
```

El navegador las pide en `/app/static/fonts/...`. `assets/styles.css` declara
los mismos `@font-face` para que también las usen los encabezados escritos con
HTML propio.

## Reglas

- Archivos `.woff2` únicamente, subset **latin**, menos de 60 KB cada uno.
- No se agregan fuentes con licencia solo para uso personal.
- Si se cambia o actualiza una fuente, se sube también su licencia OFL.
- No se sirven aquí datos, CSV ni nada que deba pasar por `core.datos`.
