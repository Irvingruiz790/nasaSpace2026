# `contenido/` — lo que escribe el equipo de investigación

**Dueño:** Investigación y contenido (CD).
**Archivo principal:** `fichas.csv`.

---

## Qué va aquí

| Archivo | Qué es | Formato |
|---|---|---|
| `fichas.csv` | Una fila por pieza: historia, datos, fuentes e imagen | CSV UTF-8, 34 columnas |

No va aquí: imágenes (van en `assets/img/`), JSON (lo genera backend) ni
documentos (van en `docs/`).

---

## Cómo se trabaja

1. Abre `fichas.csv` con **Excel** o súbelo a **Google Sheets**.
2. Llena **una fila por pieza**. Las tres primeras filas son ejemplos reales
   (Voyager 1, Voyager 2 y Apolo 11): úsalas como modelo.
3. Guarda como **CSV UTF-8**. Si Excel ofrece «CSV (delimitado por comas)» o
   «CSV UTF-8», elige CSV UTF-8.
4. Avisa en el chat: «Fichas listas: …». Backend ejecuta
   `python scripts/fichas_a_json.py` y devuelve el reporte.

**Nunca escribas el JSON a mano.** El CSV es la única fuente de verdad del
contenido.

---

## Reglas del CSV

- **No renombres ni borres columnas.** El orden y los nombres están congelados.
- **No cambies un `id`** después de avisarlo: rompe enlaces y mapas.
- Fechas en formato `AAAA-MM-DD` (ejemplo: `1969-07-16`).
- Decimales con punto o coma: el conversor acepta las dos (`0.67416` o `0,67416`).
- En `imagen` escribe **solo el nombre del archivo** (`voyager-1_main.jpg`);
  la carpeta `assets/img/` la agrega el script.
- Si una celda no aplica, déjala **vacía**. No escribas «N/A» ni «no hay».
- `estado` solo acepta: `activo`, `en_silencio`, `se_quedo`, `en_orbita`, `perdido`.
- `zona` solo acepta: `luna`, `marte`, `espacio_profundo`, `orbita`, `asteroide`.

El significado de cada columna está en `docs/CONTRATO_DATOS.md` y en la guía
`docs/Guia_Equipo.docx` (sección 7.4).
