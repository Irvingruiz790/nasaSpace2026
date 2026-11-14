"""Refresca `data/live_snapshot.json` con datos reales de JPL Horizons.

Lo corre backend antes de una demo o cuando quiere actualizar el respaldo:

    .\\.venv\\Scripts\\python.exe scripts\\actualizar_snapshot.py

Si la API falla, el script avisa y **no** sobrescribe el respaldo anterior.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from core import config, datos, vivo  # noqa: E402


def main() -> int:
    piezas = datos.cargar_piezas()
    panel = vivo.datos_en_vivo(piezas, usar_api=True, forzar=True)

    hay_datos = any(
        objeto.get("status") == "ok" for objeto in panel["objects"].values()
    )
    if not hay_datos:
        print("No se pudo consultar Horizons. Se conserva el respaldo anterior.")
        return 1

    # Se conservan los objetos que ya estaban en el respaldo para no borrar
    # datos buenos si el dataset todavía no incluye todas las piezas.
    anterior = vivo.leer_snapshot() or {}
    objetos = dict(anterior.get("objects") or {})
    objetos.update(panel["objects"])

    contenido = {
        "generated_at": panel["generated_at"],
        "source": panel["source"] or "JPL Horizons",
        "fallback": True,
        "objects": objetos,
    }
    config.ARCHIVO_SNAPSHOT.write_text(
        json.dumps(contenido, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Respaldo actualizado: {config.ARCHIVO_SNAPSHOT.relative_to(RAIZ)}")
    for pieza_id, objeto in panel["objects"].items():
        print(
            f"  {pieza_id}: {objeto['status']} | "
            f"{objeto['distance_km']} km | {objeto['light_time_s']} s de luz"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
