# `tests/` — pruebas automáticas

**Dueño:** Backend e integraciones (BE).
Framework: **pytest**.

---

## Qué va aquí

| Archivo | Qué prueba |
|---|---|
| `test_conversion.py` | Que el CSV de investigación se convierta bien |
| `test_datos.py` | Carga, validación y búsqueda de piezas |
| `test_formato.py` | Números, distancias y fechas para niños |
| `test_horizons.py` | Parseo de JPL Horizons |
| `test_vivo.py` | Panel en vivo, respaldo y caché |
| `conftest.py` | Utilidades compartidas por las pruebas |

## Formato y convenciones

- Archivos `test_*.py`; funciones `test_*()`.
- Cada prueba debe poder correr **sin internet**: la red se simula con
  `monkeypatch`. La única prueba real de red se salta salvo que se pida.
- Los nombres y mensajes van en español, igual que el resto del proyecto.

---

## Cómo se corren

```powershell
# Todas las pruebas (rápido, sin red)
.\.venv\Scripts\python.exe -m pytest -q

# Solo un archivo
.\.venv\Scripts\python.exe -m pytest tests\test_datos.py -q

# Prueba real contra JPL Horizons (opcional, tarda un poco)
$env:PROBAR_RED="1"; .\.venv\Scripts\python.exe -m pytest tests\test_horizons.py -k real
```

## Reglas

- `main` no se mergea con pruebas en rojo.
- Si se cambia una función de `core/`, se actualiza su prueba en el mismo PR.
- No se borra una prueba para que «pase»: se arregla el código o se explica en
  el PR por qué la prueba ya no aplica.
- Una prueba nueva por cada error que se arregle, para que no vuelva a pasar.
