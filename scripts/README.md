# `scripts/` — automatizaciones del backend

**Dueño:** Backend e integraciones (BE).
Todos se ejecutan **desde la raíz del repo**.

---

## Qué va aquí

| Script | Qué hace | Entrada → Salida |
|---|---|---|
| `fichas_a_json.py` | Convierte las fichas y las valida | `contenido/fichas.csv` → `data/artifacts.json` |
| `actualizar_snapshot.py` | Refresca el respaldo de Horizons | API JPL → `data/live_snapshot.json` |
| `generar_guia_word.py` | Regenera la guía del equipo | Este script → `docs/Guia_Equipo.docx` |

## Formato

Todos son **Python 3.12+** (`.py`), sin Streamlit: se pueden correr en la
terminal y probar con pytest.

---

## Cómo se ejecutan

```powershell
.\.venv\Scripts\python.exe scripts\fichas_a_json.py
.\.venv\Scripts\python.exe scripts\actualizar_snapshot.py
.\.venv\Scripts\python.exe scripts\generar_guia_word.py
```

## Reglas

- Se corre con el Python del `.venv`, no con el del sistema.
- Cada script imprime un reporte en español y devuelve **código 1** si algo
  falló. Eso permite usarlos en un checklist.
- Un script nuevo debe empezar con un docstring que explique qué hace, cuándo
  se usa y un ejemplo del comando.
- No se agregan librerías sin actualizar `requirements.txt` (o
  `requirements-dev.txt` si es solo para desarrollo).
- Los scripts no escriben en archivos que no les corresponden.
