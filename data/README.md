# `data/` — datos que consume la app

**Dueño:** Backend e integraciones (BE).
**Regla de oro:** los dos archivos se **generan**. Nadie los edita a mano.

---

## Qué va aquí

| Archivo | Lo genera | Contenido |
|---|---|---|
| `artifacts.json` | `scripts/fichas_a_json.py` | Las piezas del juego (historia, fuentes, imagen) |
| `live_snapshot.json` | `scripts/actualizar_snapshot.py` | Última distancia y tiempo de luz de JPL Horizons |

## Formato

Ambos son **JSON UTF-8**. La estructura exacta está en
`docs/CONTRATO_DATOS.md`.

`artifacts.json`:

```json
{
  "piezas": [
    { "id": "voyager-1", "nombre": "Voyager 1", "zona": "espacio_profundo", "...": "..." }
  ]
}
```

`live_snapshot.json`:

```json
{
  "generated_at": "2026-11-14T18:00:00+00:00",
  "source": "JPL Horizons",
  "objects": {
    "voyager-1": { "distance_km": 25890556821.0, "light_time_s": 86361.6, "status": "ok" }
  }
}
```

---

## Cómo se regeneran

```powershell
# Desde la raíz del repo, con el entorno virtual activo
.\.venv\Scripts\python.exe scripts\fichas_a_json.py
.\.venv\Scripts\python.exe scripts\actualizar_snapshot.py
```

- `fichas_a_json.py` lee `contenido/fichas.csv` y **sobrescribe**
  `artifacts.json`. Si hay errores de contrato, avisa y no debe subirse.
- `actualizar_snapshot.py` consulta Horizons. Si la API falla, **conserva** el
  respaldo anterior en vez de dejarlo vacío.

## Reglas

- No editar ninguno de los dos archivos en VS Code ni en Notepad.
- El JSON siempre va en UTF-8 y con acentos correctos.
- `artifacts.json` debe existir para que la app arranque: si falta, la app
  muestra un aviso que dice cómo generarlo.
- Los archivos se suben al repo; son parte del entregable.
