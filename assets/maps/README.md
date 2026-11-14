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
    "apollo-11-lm": { "x": 34, "y": 44 }
  },
  "marte": {},
  "espacio_profundo": {
    "voyager-1": { "x": 66, "y": 32 }
  }
}
```

- La llave de cada pieza es su `id` del CSV.
- Si una pieza no aparece en el JSON, se dibuja al centro (`x = 50`).
- Si una zona no tiene piezas todavía, se deja `{}`.

## Reglas

- No se usan `st.map` ni Leaflet: esos mapas usan latitud y longitud
  terrestres. La Luna y Marte se dibujan con una imagen y marcadores encima.
- Las imágenes de fondo no llevan texto ni logos incrustados.
- Comprimir con Squoosh antes de subir.
- Los marcadores se ubican a ojo sobre la imagen: se ajustan hasta que coincidan.
