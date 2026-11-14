# `components/` — piezas visuales reutilizables

**Dueño:** Frontend.
Aquí vive lo que se repite en varias pantallas. No hay lógica de datos.

---

## Qué va aquí

| Archivo | Qué aporta |
|---|---|
| `ui.py` | `aplicar_estilos()` y `encabezado()` |
| `tarjeta.py` | Tarjeta de una pieza con imagen, estado y botón |
| `mapa.py` | Fondo de zona y botones de marcadores |
| `zonas.py` | Página común de las tres zonas |
| `__init__.py` | Marca la carpeta como paquete de Python |

## Formato y convenciones

- **Python** (`.py`), funciones pequeñas que reciben datos y pintan.
- Una función pública por responsabilidad; nombres en español.
- Los componentes **no leen archivos ni llaman a la API**: reciben `pieza` o
  `piezas` ya cargadas.
- El estilo va en `assets/styles.css`, no en líneas `style="..."` sueltas.
- Usar las clases `fe1-*` que ya existen (`.fe1-hero`, `.fe1-badge`, etc.).

## Reglas

- Si un componente se usa una sola vez, se queda en su página.
- Si una página crece más de ~150 líneas, se parte en un componente.
- No agregar librerías nuevas sin avisar a backend.
- Todo texto visible se escribe para un niño de 8 a 12 años.
