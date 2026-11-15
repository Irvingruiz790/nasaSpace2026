# `assets/maps/` — fondos de mapas y posiciones

**Dueño:** Frontend.
Aquí viven las imágenes de fondo de las tres zonas y las coordenadas de sus
marcadores.

---

## Qué va aquí

| Archivo | Contenido | Formato |
|---|---|---|
| `luna.jpg` | Fondo del mapa de la Luna | JPG/WebP, ~1600 px de ancho |
| `marte.jpg` | Fondo del mapa de Marte | JPG/WebP, ~1600 px de ancho |
| `espacio_profundo.jpg` | Fondo del espacio profundo | JPG/WebP, ~1600 px de ancho |
| `posiciones.json` | Coordenadas de cada marcador | JSON |

## Formato de `posiciones.json`

Las coordenadas son **porcentajes** del ancho y alto de la imagen: `x` y `y`
van de 0 a 100, con el origen arriba a la izquierda.

```json
{
  "luna": {
    "apollo-11-lm": { "x": 63.4, "y": 49.5 }
  },
  "marte": {
    "sojourner": { "x": 15.7, "y": 38.2 }
  },
  "espacio_profundo": {
    "voyager-1": { "x": 66, "y": 32 }
  }
}
```

- La llave de cada pieza es su `id` del CSV.
- Si una pieza no aparece en el JSON, se dibuja al centro (`x = 50`).
- Si una zona no tiene piezas todavía, se deja `{}`.
- El archivo ya trae las 10 piezas del CSV repartidas en sus tres zonas.

## Fuente de los fondos

Los tres fondos salen del **NSSDCA de la NASA** (`nssdc.gsfc.nasa.gov`):

| Archivo | Imagen original | Tratamiento |
|---|---|---|
| `luna.jpg` | `image/planetary/moon/clem_full_moon_strtrk.jpg` (Clementine) | Recorte al disco y lienzo 4:3 |
| `marte.jpg` | `image/hi-res/planetary/mars/mars_dim.tiff` (Mars Digital Image Model) | Reproyectado de sinusoidal a rectangular, centrado en 90° E |
| `espacio_profundo.jpg` | `image/hi-res/astro/hst_deep_field.tiff` (Hubble Deep Field) | Recorte a 4:3 |

Las coordenadas de cada pieza son su latitud y longitud reales según las
fichas del NSSDCA, proyectadas sobre cada fondo:

- **Luna:** proyección ortográfica sobre el disco (0° de longitud en el centro).
- **Marte:** proyección equirectangular con el meridiano 90° E en el centro.
- **Espacio profundo:** posición decorativa; la imagen no es un mapa celeste.

## Reglas

- No se usan `st.map` ni Leaflet: esos mapas usan latitud y longitud
  terrestres. La Luna y Marte se dibujan con una imagen y marcadores encima.
- Las imágenes de fondo no llevan texto ni logos incrustados.
- Comprimir con Squoosh antes de subir.
- Las posiciones se calculan con la latitud y longitud reales de cada pieza y se
  guardan como porcentajes. Si se cambia el fondo, se recalculan y se verifica
  el encuadre dibujando los marcadores.
