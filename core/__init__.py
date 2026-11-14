"""Backend de "¿Dónde está ahora?".

Módulos, todos sin dependencia de Streamlit para poder probarlos con pytest:

- `config`    : rutas, constantes físicas y límites de red.
- `contrato`  : enums y límites de `docs/CONTRATO_DATOS.md`.
- `datos`     : carga y validación de `data/artifacts.json`.
- `horizons`  : cliente y parseo de JPL Horizons.
- `vivo`      : datos en vivo con respaldo (`live_snapshot.json`).
- `formato`   : números, distancias y fechas para niños de 8 a 12 años.

Uso desde el frontend (Streamlit):

    from core import datos, formato, vivo

    piezas = datos.cargar_piezas()
    panel = vivo.datos_en_vivo(piezas)
    texto = formato.distancia_texto(panel["objects"]["voyager-1"]["distance_km"])
"""

from __future__ import annotations

__all__ = ["config", "contrato", "datos", "formato", "horizons", "vivo"]
