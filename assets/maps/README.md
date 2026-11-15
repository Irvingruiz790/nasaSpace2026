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
    "sojourner": { "x": 28.9, "y": 35.7 }
  },
  "espacio_profundo": {
    "voyager-1": { "x": 66, "y": 32 }
  },
  "al_otro_lado": ["spirit", "insight"]
}
```

- La llave de cada pieza es su `id` del CSV.
- Si una pieza no aparece en el JSON, su botón se dibuja debajo del mapa, en
  una fila aparte, para que nunca desaparezca.
- `al_otro_lado` no es una zona: es la lista de piezas que caen detrás del
  globo y por eso no tienen marcador visible. Hoy son Spirit e InSight, en la
  cara oculta de Marte desde el meridiano 10° E. La prueba
  `test_las_posiciones_cubren_todas_las_piezas` exige que toda pieza esté en
  el mapa o en esta lista.
- Si una zona no tiene piezas todavía, se deja `{}`.
- El archivo ya trae las 10 piezas del CSV repartidas en sus tres zonas.

## Fuente de los fondos

Los tres fondos salen del **NSSDCA de la NASA** (`nssdc.gsfc.nasa.gov`):

| Archivo | Imagen original | Tratamiento |
|---|---|---|
| `luna.jpg` | `image/planetary/moon/clem_full_moon_strtrk.jpg` (Clementine) | Recorte al disco y lienzo 4:3 |
| `marte.jpg` | `image/hi-res/planetary/mars/mars_dim.tiff` (Mars Digital Image Model), vía el mapa ecuatóreo que ya estaba en el repositorio; color tomado de PIA00407 (NASA/JPL/USGS) | Reproyectado a disco ortográfico sobre lienzo negro 4:3 |
| `espacio_profundo.jpg` | `image/hi-res/astro/hst_deep_field.tiff` (Hubble Deep Field) | Recorte a 4:3 |

Las coordenadas de cada pieza son su latitud y longitud reales según las
fichas del NSSDCA, proyectadas sobre cada fondo:

- **Luna:** proyección ortográfica sobre el disco (0° de longitud en el centro).
- **Marte:** proyección ortográfica sobre el disco, con el meridiano 10° E y el
  ecuador en el centro. Solo caben 180° de longitud, y los cinco sitios de
  Marte abarcan 209°: Spirit e InSight quedan al otro lado y se listan en
  `al_otro_lado`.
- **Espacio profundo:** posición decorativa; la imagen no es un mapa celeste.

### Cómo se genera el disco de Marte

El lienzo es de 1600 × 1200 px, con el disco centrado en (800, 600) y un radio
de 520 px, igual que `luna.jpg`. Cada píxel dentro del disco se convierte a
latitud y longitud y se muestrea el mapa ecuatóreo con interpolación bilineal.
Para pasar de latitud/longitud al porcentaje del marcador se usa:

```
x = 800 + 520 · cos(lat) · sen(lon − 10°)
y = 600 − 520 · sen(lat)
x% = x / 1600 · 100        y% = y / 1200 · 100
```

Si se cambia el meridiano central hay que recalcular las tres posiciones de
Marte y volver a comprobar qué piezas quedan visibles.

## Reglas

- No se usan `st.map` ni Leaflet: esos mapas usan latitud y longitud
  terrestres. La Luna y Marte se dibujan con una imagen y marcadores encima.
- Las imágenes de fondo no llevan texto ni logos incrustados.
- Comprimir con Squoosh antes de subir.
- Las posiciones se calculan con la latitud y longitud reales de cada pieza y se
  guardan como porcentajes. Si se cambia el fondo, se recalculan y se verifica
  el encuadre dibujando los marcadores.
