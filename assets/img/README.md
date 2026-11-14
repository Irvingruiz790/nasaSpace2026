# `assets/img/` — fotos de las piezas

**Dueño:** Investigación y contenido (CD).
**Formato:** JPG o WebP. **Peso:** menos de 300 KB.

---

## Cómo se nombra

| Archivo | Cuándo se usa |
|---|---|
| `{id}_main.jpg` | Imagen principal de la ficha |
| `{id}_thumb.jpg` | Miniatura para tarjetas (opcional) |

`{id}` es el mismo `id` del CSV, en minúsculas y con guiones.

| Correcto | Incorrecto |
|---|---|
| `voyager-1_main.jpg` | `Voyager 1.jpg` |
| `apollo-11-lm_main.jpg` | `apolo final (2).JPG` |
| `opportunity_thumb.webp` | `opp mini.png` |

---

## Cómo se prepara una imagen

1. Búscala en **NASA Images** (`images.nasa.gov`) o **NASA Photojournal**.
2. Descarga la versión horizontal más grande.
3. Recórtala a unos **1200 px de ancho**.
4. Pásala por **Squoosh** (`squoosh.app`) hasta que pese menos de 300 KB.
5. Guárdala aquí con el nombre exacto del patrón.
6. Escribe el crédito y el texto alternativo en el CSV.

## Reglas

- Sin crédito no se publica.
- No se usan imágenes de Google Imágenes: no tienen licencia clara.
- No se suben PNG gigantes, BMP ni archivos sin extensión.
- Si una imagen falta, el conversor lo reporta como **aviso** (no como error),
  pero debe resolverse antes de la demo.
- El texto alternativo describe lo que se ve, no repite el nombre de la pieza.
