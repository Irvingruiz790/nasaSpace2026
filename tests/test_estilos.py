"""Pruebas de la identidad visual y de las fuentes locales."""

from __future__ import annotations

import tomllib
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
CSS = RAIZ / "assets" / "styles.css"
CONFIG = RAIZ / ".streamlit" / "config.toml"
FUENTES = RAIZ / "static" / "fonts"

FAMILIAS = {
    "Exo 2": FUENTES / "exo2-latin.woff2",
    "Overpass": FUENTES / "overpass-latin.woff2",
}


@pytest.fixture(scope="module")
def css() -> str:
    return CSS.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def config() -> dict:
    with CONFIG.open("rb") as archivo:
        return tomllib.load(archivo)


@pytest.mark.parametrize("familia,archivo", FAMILIAS.items())
def test_la_fuente_existe_y_pesa_menos_de_60_kb(familia: str, archivo: Path) -> None:
    assert archivo.is_file(), f"Falta la fuente {familia}: {archivo}"
    assert 0 < archivo.stat().st_size < 60 * 1024


@pytest.mark.parametrize(
    "licencia",
    ["OFL-Exo2.txt", "OFL-Overpass.txt"],
)
def test_la_licencia_ofl_esta_empaquetada(licencia: str) -> None:
    archivo = FUENTES / licencia
    assert archivo.is_file()
    assert "SIL OPEN FONT LICENSE" in archivo.read_text(encoding="utf-8").upper()


def test_el_css_no_pide_nada_por_internet(css: str) -> None:
    assert "http://" not in css
    assert "https://" not in css


def test_el_css_declara_las_dos_familias_locales(css: str) -> None:
    assert '@font-face' in css
    assert "/app/static/fonts/exo2-latin.woff2" in css
    assert "/app/static/fonts/overpass-latin.woff2" in css
    assert 'font-family: "Exo 2"' in css
    assert 'font-family: "Overpass"' in css


def test_el_css_usa_la_paleta_oficial(css: str) -> None:
    for color in ("#07173f", "#0042a6", "#0960e1", "#2e96f5", "#e43700", "#eafe07"):
        assert color in css.lower()


def test_el_css_tiene_foco_visible_y_movimiento_reducido(css: str) -> None:
    assert ":focus-visible" in css
    assert "prefers-reduced-motion" in css
    assert "min-height: 2.7rem" in css


def test_el_css_trae_los_encabezados_tematicos(css: str) -> None:
    for variante in (
        "luna",
        "marte",
        "espacio-profundo",
        "vivo",
        "quiz",
        "fuentes",
        "inicio",
    ):
        assert f".fe1-hero--{variante}" in css


def test_la_barra_lateral_dice_menu(css: str) -> None:
    assert '[data-testid="stSidebarNav"]::before' in css
    assert 'content: "Menú"' in css


def test_el_tema_es_oscuro_y_oficial(config: dict) -> None:
    tema = config["theme"]
    assert tema["base"] == "dark"
    assert tema["backgroundColor"].lower() == "#07173f"
    assert tema["primaryColor"].lower() == "#eafe07"
    assert tema["textColor"].lower() == "#eaf0ff"


def test_el_tema_carga_las_dos_familias_locales(config: dict) -> None:
    tema = config["theme"]
    assert "Exo 2" in tema["headingFont"]
    assert "Overpass" in tema["font"]

    familias = {fuente["family"]: fuente for fuente in tema["fontFaces"]}
    assert set(familias) == {"Exo 2", "Overpass"}
    for fuente in familias.values():
        assert fuente["url"].startswith("app/static/fonts/")
        assert fuente["url"].endswith(".woff2")


def test_el_servidor_sirve_los_archivos_estaticos(config: dict) -> None:
    assert config["server"]["enableStaticServing"] is True


def _luminancia(color: str) -> float:
    """Luminancia relativa WCAG de un color hexadecimal."""
    valor = color.lstrip("#")
    canales = [int(valor[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    lineales = [
        canal / 12.92 if canal <= 0.04045 else ((canal + 0.055) / 1.055) ** 2.4
        for canal in canales
    ]
    return 0.2126 * lineales[0] + 0.7152 * lineales[1] + 0.0722 * lineales[2]


def _contraste(texto: str, fondo: str) -> float:
    alto, bajo = sorted((_luminancia(texto), _luminancia(fondo)), reverse=True)
    return (alto + 0.05) / (bajo + 0.05)


@pytest.mark.parametrize(
    "texto,fondo",
    [
        ("#EAF0FF", "#07173F"),  # texto principal sobre Deep Blue
        ("#B9C8E8", "#0A2258"),  # texto suave sobre superficie
        ("#93A7CE", "#07173F"),  # texto tenue sobre fondo
        ("#EAFE07", "#07173F"),  # acento sobre Deep Blue
        ("#07173F", "#EAFE07"),  # botón primario
        ("#FFFFFF", "#0042A6"),  # blanco sobre Electric Blue
        ("#07173F", "#2E96F5"),  # texto oscuro sobre Blue Yonder
    ],
)
def test_el_contraste_cumple_aa(texto: str, fondo: str) -> None:
    assert _contraste(texto, fondo) >= 4.5
