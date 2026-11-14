# Contrato de datos — versión 1.0

**Estado:** congelado en T+2.  
**Dueños:** CD (contenido) y BE (backend).  
**Regla:** después de esta versión, solo se agregan campos opcionales con aprobación de ambos. No se renombran campos existentes.

Este documento es la fuente de verdad para que frontend, backend y contenido trabajen en paralelo sin romperse.

---

## 1. Enumeraciones cerradas

### Zona (`zona`)

| Valor | Etiqueta para niños |
|---|---|
| `luna` | La Luna |
| `marte` | Marte |
| `espacio_profundo` | Espacio profundo |
| `orbita` | En órbita |
| `asteroide` | En un asteroide |

### Estado (`estado`)

| Valor | Etiqueta para niños | Significado |
|---|---|---|
| `activo` | "Sigue despierto" | Todavía funciona y se comunica |
| `en_silencio` | "En silencio" | Dejó de comunicarse |
| `se_quedo` | "Se quedó aquí" | Está en un lugar fijo, sin moverse |
| `en_orbita` | "En órbita para siempre" | Da vueltas sin energía |
| `perdido` | "Se perdió" | No se sabe dónde está o falló |

### Tipo (`tipo`)

`lander`, `rover`, `orbitador`, `nave`, `instrumento`.

---

## 2. Campos de cada pieza

| Campo | Tipo | Obligatorio | Ejemplo | Dueño | Notas |
|---|---|---|---|---|---|
| `id` | string | Sí | `apollo-11-lm` | CD | kebab-case, único, estable |
| `nombre` | string | Sí | Módulo Lunar Eagle | CD | Nombre completo |
| `apodo` | string | Sí | "El águila que se quedó" | CD | Frase corta y memorable |
| `tipo` | enum | Sí | `lander` | CD | Ver enumeración |
| `mision` | string | Sí | Apolo 11 | CD | |
| `agencia` | string | Sí | NASA | CD | |
| `zona` | enum | Sí | `luna` | CD | Ver enumeración |
| `estado` | enum | Sí | `se_quedo` | CD | Ver enumeración |
| `etiqueta_estado` | string | Sí | "Se quedó en la Luna" | CD | Texto para niños |
| `ubicacion_texto` | string | Sí | Mar de la Tranquilidad | CD | |
| `lat` | float \| null | Condicional | `0.67416` | CD | Obligatorio si hay coordenadas |
| `lon` | float \| null | Condicional | `23.47314` | CD | Obligatorio si hay coordenadas |
| `lanzamiento` | string (ISO) | Sí | `1969-07-16` | CD | |
| `ultima_senal` | string \| null | No | `1969-08-27` | CD | Fecha o "sigue activo" |
| `distancia_actual` | string \| null | No | "unos 25 900 millones de km" | CD/BE | Texto legible; el dato vivo va aparte |
| `horizons_id` | string \| null | No | `-31` | BE | Solo para espacio profundo |
| `imagen` | string | Sí | `assets/img/apollo-11-lm_main.jpg` | CD | La ruta debe existir |
| `credito_imagen` | string | Sí | NASA/JPL-Caltech | CD | |
| `alt_text` | string | Sí | El módulo lunar Eagle posado en la Luna… | CD | Accesibilidad |
| `historia` | objeto | Sí | ver abajo | CD | 5 bloques con límite de palabras |
| `fuentes` | array | Sí | ver abajo | CD | Mínimo 2 para datos críticos |
| `revisor` | string | Sí | nombre | CD | Quién verificó |
| `fecha_verificacion` | string (ISO) | Sí | `2026-11-14` | CD | |
| `notas_verificacion` | string \| null | No | "El destino de la etapa de ascenso es incierto" | CD | Honestidad sobre ambigüedades |

### Objeto `historia`

| Campo | Límite | Contenido |
|---|---|---|
| `que_es` | ≤ 35 palabras | Qué es, con comparación cotidiana |
| `por_que` | ≤ 40 palabras | La pregunta o misión que fue a resolver |
| `descubrimiento` | ≤ 45 palabras | Un descubrimiento concreto |
| `ahora` | ≤ 45 palabras | Dónde está y qué hace hoy |
| `dato_curioso` | ≤ 30 palabras | Un dato memorable |

### Objeto `fuentes`

| Campo | Tipo | Ejemplo |
|---|---|---|
| `titulo` | string | NSSDCA — Apollo 11 Lunar Module |
| `url` | string | https://nssdc.gsfc.nasa.gov/... |
| `consultado` | string (ISO) | `2026-11-14` |

---

## 3. Snapshot de datos en vivo

**Archivo:** `data/live_snapshot.json`  
**Dueño:** BE.  
**Uso:** respaldo cuando Horizons o DSN Now fallan.

| Campo | Tipo | Ejemplo | Notas |
|---|---|---|---|
| `generated_at` | string (ISO) | `2026-11-14T18:00:00Z` | Fecha de la última actualización |
| `source` | string | `JPL Horizons` | Fuente del dato |
| `fallback` | boolean | `true` | Si es un respaldo |
| `objects` | objeto | ver abajo | Mapa por `id` de pieza |

Cada objeto dentro de `objects`:

| Campo | Tipo | Ejemplo |
|---|---|---|
| `distance_km` | number \| null | `25900000000` |
| `light_time_s` | number \| null | `86400` |
| `status` | string | `ok` / `stale` / `error` |
| `source` | string | `JPL Horizons` |

---

## 4. Convenciones de nombres

- **IDs:** minúsculas, guiones, sin acentos. Ejemplo: `apollo-11-lm`, `voyager-1`.
- **Imágenes:** `{id}_main.jpg` y `{id}_thumb.jpg`. Ejemplo: `voyager-1_main.jpg`.
- **Páginas:** nombres cortos y sin espacios. Ejemplo: `1_Mapa.py`.
- **Clases CSS:** prefijo `fe1-` o `fe2-`.
- **Llaves de `st.session_state`:** prefijo `fe1_`, `fe2_`, `be_`, `cd_`.
- **Variables de datos:** `snake_case`.

---

## 5. Reglas de validación

Antes de considerar un registro "listo":

- [ ] `id` único y en kebab-case.
- [ ] `zona` y `estado` están en la enumeración.
- [ ] `imagen` existe en `assets/img/`.
- [ ] `alt_text` no está vacío.
- [ ] `historia` tiene los 5 campos y respeta los límites.
- [ ] `fuentes` tiene al menos 2 entradas.
- [ ] `fecha_verificacion` está completa.
- [ ] Si `zona` es `luna` o `marte`, hay `lat`/`lon` o una `ubicacion_texto` clara.
- [ ] Si hay `horizons_id`, BE verificó que responde.

---

## 6. Ejemplo de registro (descrito, no código)

**Voyager 1**

- `id`: `voyager-1`
- `nombre`: Voyager 1
- `apodo`: "La mensajera más lejana"
- `tipo`: `nave`
- `mision`: Voyager
- `agencia`: NASA/JPL-Caltech
- `zona`: `espacio_profundo`
- `estado`: `activo`
- `etiqueta_estado`: "Sigue despierta"
- `ubicacion_texto`: espacio interestelar
- `lat` / `lon`: null
- `lanzamiento`: 1977-09-05
- `ultima_senal`: "sigue activa"
- `distancia_actual`: "unos 25 900 millones de km"
- `horizons_id`: `-31`
- `imagen`: `assets/img/voyager-1_main.jpg`
- `credito_imagen`: NASA/JPL-Caltech
- `historia`: los 5 bloques de la ficha
- `fuentes`: NASA Voyager, NASA Where are they now, JPL Horizons
- `revisor`: por asignar
- `fecha_verificacion`: 2026-11-14

---

## 7. Cambios al contrato

1. Propone el cambio quien lo necesita (FE, BE o CD).
2. Lo aprueban BE y CD.
3. Se actualiza este documento con versión nueva.
4. Se avisa en el chat y se actualiza el código en la misma integración.

**No se cambia el contrato en silencio.** Un campo renombrado sin aviso es la forma más rápida de romper el proyecto.
