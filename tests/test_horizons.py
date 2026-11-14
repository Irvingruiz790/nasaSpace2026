"""Pruebas del cliente y del parseo de JPL Horizons.

La tabla de abajo es un recorte real de la respuesta de Horizons para
Voyager 1 (`COMMAND='-31'`, `QUANTITIES='20'`) del 14 de noviembre de 2026.
No se toca la red en estas pruebas: se simula `requests.get`.
"""

from __future__ import annotations

import requests

from core import config, horizons

TABLA_REAL = """
*******************************************************************************
 Date__(UT)__HR:MN                delta      deldot
***************************************************
$$SOE
 2026-Nov-14 00:00     173.067682711039  27.1464777
 2026-Nov-15 00:00     173.083248374167  26.7585866
$$EOE
*******************************************************************************
"""


class RespuestaFalsa:
    def __init__(self, payload: dict | None = None, status: int = 200) -> None:
        self.payload = payload or {}
        self.status = status

    def raise_for_status(self) -> None:
        if self.status >= 400:
            raise requests.HTTPError(f"HTTP {self.status}")

    def json(self) -> dict:
        return self.payload


def test_parsea_la_tabla_real() -> None:
    fila = horizons.parsear_tabla(TABLA_REAL)
    assert fila is not None
    assert fila["fecha_ut"] == "2026-Nov-14 00:00"
    assert fila["delta_au"] == 173.067682711039
    assert fila["deldot_km_s"] == 27.1464777


def test_sin_tabla_devuelve_none() -> None:
    assert horizons.parsear_tabla("No hubo efemérides.") is None
    assert horizons.parsear_tabla("$$SOE\n$$EOE\n") is None


def test_parametros_de_consulta() -> None:
    params = horizons.construir_parametros("-31")
    assert params["COMMAND"] == "'-31'"
    assert params["EPHEM_TYPE"] == "'OBSERVER'"
    assert params["CENTER"] == "'500@399'"
    assert params["QUANTITIES"] == "'20'"
    assert params["format"] == "json"


def test_consulta_exitosa(monkeypatch) -> None:
    monkeypatch.setattr(
        requests, "get", lambda *a, **k: RespuestaFalsa({"result": TABLA_REAL})
    )
    resultado = horizons.consultar("-31")
    assert resultado["status"] == "ok"
    assert resultado["source"] == "JPL Horizons"
    esperado = 173.067682711039 * config.KM_POR_AU
    assert abs(resultado["distance_km"] - esperado) < 1
    assert abs(resultado["light_time_s"] - esperado / config.VELOCIDAD_LUZ_KM_S) < 0.001
    # ~24 horas de viaje de la luz
    assert 23.9 < resultado["light_time_s"] / 3600 < 24.1


def test_reintenta_y_luego_falla(monkeypatch) -> None:
    llamadas = {"n": 0}

    def get_con_fallo(*args, **kwargs):
        llamadas["n"] += 1
        raise requests.Timeout("sin respuesta")

    monkeypatch.setattr(requests, "get", get_con_fallo)
    resultado = horizons.consultar("-31", reintentos=2)
    assert llamadas["n"] == 2
    assert resultado["status"] == "error"
    assert resultado["distance_km"] is None
    assert "Timeout" in resultado["error"]


def test_tabla_inesperada_no_explota(monkeypatch) -> None:
    monkeypatch.setattr(
        requests, "get", lambda *a, **k: RespuestaFalsa({"result": "sin efemérides"})
    )
    resultado = horizons.consultar("-31", reintentos=1)
    assert resultado["status"] == "error"
    assert resultado["distance_km"] is None


def test_consulta_varios(monkeypatch) -> None:
    monkeypatch.setattr(
        requests, "get", lambda *a, **k: RespuestaFalsa({"result": TABLA_REAL})
    )
    resultados = horizons.consultar_varios({"voyager-1": "-31", "voyager-2": "-32"})
    assert set(resultados) == {"voyager-1", "voyager-2"}
    assert all(r["status"] == "ok" for r in resultados.values())


def test_contra_la_api_real(monkeypatch) -> None:
    """Prueba de humo opcional. Se salta salvo que se pida explícitamente.

    Uso:  PROBAR_RED=1 pytest tests/test_horizons.py -k real
    """
    import os

    if os.environ.get("PROBAR_RED") != "1":
        import pytest

        pytest.skip("define PROBAR_RED=1 para consultar JPL de verdad")

    resultado = horizons.consultar("-31")
    assert resultado["status"] == "ok", resultado.get("error")
    assert resultado["distance_km"] > 20_000_000_000
