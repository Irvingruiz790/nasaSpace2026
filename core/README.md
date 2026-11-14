# `core/` — guía para el frontend

**Dueño:** Backend e integraciones (BE).
**Regla:** el frontend **importa** estas funciones. No llama a JPL ni lee JSON a mano.
Si falta algo, se pide a BE; no se copia la lógica en `app.py` ni en `pages/`.

Los módulos **no importan Streamlit**. Se pueden probar con pytest sin levantar la app.

---

## Qué hay aquí

| Módulo | Para qué |
|---|---|
| `core.datos` | Cargar `data/artifacts.json` y validarlo |
| `core.vivo` | Panel "en vivo" con respaldo automático |
| `core.formato` | Números, distancias, tiempo luz y fechas para niños |
| `core.horizons` | Cliente de JPL Horizons (uso interno de BE) |
| `core.contrato` | Enums y límites del contrato de datos |
| `core.config` | Rutas, constantes y timeouts |

---

## Receta 1 — cargar las piezas

```python
from core import datos

piezas = datos.cargar_piezas()          # lista de dicts
pieza = datos.buscar(piezas, "voyager-1")
luna = datos.por_zona(piezas, "luna")
conteo = datos.contar_por_zona(piezas)
```

`cargar_piezas()` lee `data/artifacts.json`, que se genera desde
`contenido/fichas.csv` con `scripts/fichas_a_json.py`. Si el archivo no existe,
devuelve `[]` y deja en el log el comando exacto para generarlo.
**Nunca lanza excepción:** si el archivo está roto devuelve `[]`.

En Streamlit conviene envolverla una vez:

```python
@st.cache_data
def piezas():
    return datos.cargar_piezas()
```

## Receta 2 — saber si los datos están bien

```python
problemas = datos.validar_piezas(piezas)
errores = datos.errores(problemas)     # rompen el contrato
avisos = datos.avisos(problemas)       # calidad o archivo pendiente
```

Cada `Problema` trae `pieza_id`, `campo`, `mensaje` y `severidad`.
Sugerencia de UI: si `datos.hay_errores(problemas)`, mostrar un `st.warning`
discreto en la página de fuentes, no un `st.stop()`.

## Receta 3 — panel en vivo

```python
from core import vivo, formato

panel = vivo.datos_en_vivo(piezas)                 # usa API + respaldo + caché
v1 = vivo.objeto(panel, "voyager-1")

v1["distance_km"]   # float | None
v1["light_time_s"]  # float | None
v1["status"]        # "ok" | "stale" | "error"

formato.distancia_texto(v1["distance_km"])   # "25 891 millones de km"
formato.tiempo_luz_texto(v1["light_time_s"]) # "23 horas 59 minutos"
formato.comparacion_texto(v1["distance_km"]) # "es como ir al Sol 173,1 veces"
vivo.aviso_panel(panel)                      # str | None
```

Comportamiento:

- **`status = "ok"`** → dato fresco de JPL Horizons.
- **`status = "stale"`** → vino del snapshot; mostrar "último dato guardado".
- **`status = "error"`** → no hay ni API ni snapshot; mostrar "sin dato" sin romper.

El resultado se memoriza 10 minutos (`config.CACHE_TTL_SEGUNDOS`), así que puedes
llamar `datos_en_vivo()` en cada rerun sin miedo. Para forzar: `forzar=True`.

**Nunca** uses `st.cache_data` encima de `datos_en_vivo`: ya tiene su propia caché
con TTL, y si la envuelves el respaldo deja de refrescarse.

## Receta 4 — tarjeta de pieza

```python
formato.fecha_texto(pieza["lanzamiento"])        # "16 de julio de 1969"
pieza["etiqueta_estado"]                          # "Se quedó en la Luna"
pieza["historia"]["ahora"]                        # bloque ¿Dónde está ahora?
```

Los cinco bloques de `historia` ya vienen validados en longitud.

## Receta 5 — aviso de antigüedad

```python
formato.antiguedad_texto(panel["generated_at"])   # "hace 2 horas"
```

---

## Reglas de formato (no reinventarlas)

| Función | Entrada | Salida |
|---|---|---|
| `separar_miles` | `25890556821` | `"25 890 556 821"` |
| `distancia_texto` | `25890556821.0` | `"25 891 millones de km"` |
| `tiempo_luz_texto` | `86361.6` | `"23 horas 59 minutos"` |
| `au_texto` | `149597870.7` | `"1,0 UA"` |
| `comparacion_texto` | `25890556821.0` | `"es como ir al Sol 173,1 veces"` |
| `fecha_texto` | `"1969-07-16"` | `"16 de julio de 1969"` |
| `antiguedad_texto` | ISO con hora | `"hace 2 horas"` |

Sin dato se devuelve `"sin dato"`, nunca `None` ni `0`. Eso evita "None millones de km"
en pantalla.

---

## Pruebas

```bash
.venv\Scripts\python.exe -m pytest -q
```

Prueba contra la API real (opcional, tarda un segundo):

```bash
PROBAR_RED=1 .venv\Scripts\python.exe -m pytest tests/test_horizons.py -k real
```

En PowerShell:

```powershell
$env:PROBAR_RED="1"; .\.venv\Scripts\python.exe -m pytest tests/test_horizons.py -k real
```

---

## Lo que no se hace

- No editar `core/` desde FE. Es de BE.
- No importar `requests` en `app.py` ni en `pages/`.
- No leer `data/*.json` directo: se pierde la validación y el respaldo.
- No cambiar nombres de campos sin pasar por `docs/CONTRATO_DATOS.md`.
