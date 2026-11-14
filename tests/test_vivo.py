"""Pruebas del panel en vivo y del respaldo."""

from __future__ import annotations

import pytest

from core import config, datos, horizons, vivo


@pytest.fixture(autouse=True)
def cache_limpia() -> None:
    vivo.limpiar_cache()


@pytest.fixture()
def piezas() -> list[dict]:
    return datos.cargar_piezas()


def test_sin_api_usa_el_snapshot(piezas) -> None:
    panel = vivo.datos_en_vivo(piezas, usar_api=False)
    assert panel["fallback"] is True
    assert panel["source"] == "JPL Horizons"

    v1 = panel["objects"]["voyager-1"]
    assert v1["status"] == "stale"
    assert v1["distance_km"] == pytest.approx(25_890_556_821.0, rel=1e-9)
    assert v1["light_time_s"] == pytest.approx(86_361.6, rel=1e-6)


def test_con_api_responde_ok(piezas, monkeypatch) -> None:
    monkeypatch.setattr(
        horizons,
        "consultar",
        lambda hid: {"distance_km": 1.0, "light_time_s": 2.0, "status": "ok", "source": "JPL Horizons"},
    )
    panel = vivo.datos_en_vivo(piezas, usar_api=True)
    assert panel["fallback"] is False
    assert panel["objects"]["voyager-1"]["status"] == "ok"
    assert panel["objects"]["voyager-1"]["distance_km"] == 1.0


def test_api_caida_y_sin_snapshot_da_error(piezas, monkeypatch) -> None:
    monkeypatch.setattr(
        horizons, "consultar", lambda hid: {"status": "error", "distance_km": None}
    )
    panel = vivo.datos_en_vivo(
        [{"id": "pioneer-10", "horizons_id": "-23"}], usar_api=True
    )
    assert panel["objects"]["pioneer-10"]["status"] == "error"
    assert panel["objects"]["pioneer-10"]["distance_km"] is None
    assert panel["fallback"] is True


def test_la_cache_evita_repetir_llamadas(piezas, monkeypatch) -> None:
    llamadas = {"n": 0}

    def falso(hid):
        llamadas["n"] += 1
        return {"distance_km": 10.0, "light_time_s": 0.1, "status": "ok", "source": "JPL Horizons"}

    monkeypatch.setattr(horizons, "consultar", falso)
    esperadas = len(datos.con_horizons(piezas))
    vivo.datos_en_vivo(piezas, usar_api=True)
    vivo.datos_en_vivo(piezas, usar_api=True)
    assert llamadas["n"] == esperadas

    vivo.datos_en_vivo(piezas, usar_api=True, forzar=True)
    assert llamadas["n"] == esperadas * 2


def test_aviso_de_respaldo(piezas) -> None:
    panel = vivo.datos_en_vivo(piezas, usar_api=False)
    aviso = vivo.aviso_panel(panel)
    assert aviso is not None
    assert "último dato guardado" in aviso
    assert vivo.aviso_panel({"fallback": False}) is None


def test_acceso_seguro_a_un_objeto(piezas) -> None:
    panel = vivo.datos_en_vivo(piezas, usar_api=False)
    assert vivo.objeto(panel, "voyager-1")["status"] == "stale"
    assert vivo.objeto(panel, "no-existe")["status"] == "error"


def test_snapshot_corrupto_no_explota(tmp_path) -> None:
    roto = tmp_path / "roto.json"
    roto.write_text("{ esto no es json", encoding="utf-8")
    assert vivo.leer_snapshot(roto) is None
    assert vivo.leer_snapshot(tmp_path / "no-existe.json") is None


def test_constantes_coherentes() -> None:
    assert config.KM_POR_AU == pytest.approx(149_597_870.7)
    assert config.VELOCIDAD_LUZ_KM_S == pytest.approx(299_792.458)
