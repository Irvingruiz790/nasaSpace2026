"""Configuración compartida del backend.

Un solo lugar para rutas, constantes físicas y límites de red.
Si algo cambia (timeout, URL, ruta), se cambia aquí y no en tres archivos.
"""

from __future__ import annotations

from pathlib import Path

# --- Rutas -----------------------------------------------------------------

RAIZ = Path(__file__).resolve().parent.parent
DIR_DATOS = RAIZ / "data"
DIR_IMAGENES = RAIZ / "assets" / "img"

ARCHIVO_PIEZAS = DIR_DATOS / "artifacts.json"
ARCHIVO_SNAPSHOT = DIR_DATOS / "live_snapshot.json"

# --- Fuentes externas ------------------------------------------------------

HORIZONS_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"
DSN_URL = "https://eyes.nasa.gov/dsn/data/dsn.json"

USER_AGENT = "nasaSpace2026/1.0 (proyecto educativo; NASA Space Apps Challenge)"

# --- Red -------------------------------------------------------------------

TIMEOUT_SEGUNDOS = 6.0
REINTENTOS = 2
CACHE_TTL_SEGUNDOS = 600  # 10 minutos: suficiente para la demo, sin castigar a JPL

# --- Constantes físicas (JPL Horizons: 1 au = 149597870.700 km) ------------

KM_POR_AU = 149_597_870.7
VELOCIDAD_LUZ_KM_S = 299_792.458
KM_TIERRA_LUNA = 384_400.0
