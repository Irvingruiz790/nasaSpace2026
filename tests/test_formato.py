"""Pruebas del formateo para público de 8 a 12 años."""

from __future__ import annotations

from datetime import datetime, timezone

from core import config, formato


def test_separar_miles_usa_espacios() -> None:
    assert formato.separar_miles(25890556821) == "25 890 556 821"


def test_distancia_texto() -> None:
    assert formato.distancia_texto(25_890_556_821) == "25 891 millones de km"
    assert formato.distancia_texto(384_400) == "384 400 km"
    assert formato.distancia_texto(0) == "0 km"


def test_distancia_sin_dato() -> None:
    assert formato.distancia_texto(None) == "sin dato"
    assert formato.distancia_texto("hola") == "sin dato"
    assert formato.distancia_texto(-5) == "sin dato"


def test_tiempo_luz_texto() -> None:
    assert formato.tiempo_luz_texto(0.5) == "menos de 1 segundo"
    assert formato.tiempo_luz_texto(1) == "1 segundo"
    assert formato.tiempo_luz_texto(45) == "45 segundos"
    assert formato.tiempo_luz_texto(120) == "2 minutos"
    assert formato.tiempo_luz_texto(7_200) == "2 horas"
    assert formato.tiempo_luz_texto(86_361.6) == "23 horas 59 minutos"
    assert formato.tiempo_luz_texto(86_400) == "1 día"
    assert formato.tiempo_luz_texto(90_000) == "1 día 1 hora"


def test_tiempo_luz_desde_km() -> None:
    segundos = formato.tiempo_luz_desde_km(config.VELOCIDAD_LUZ_KM_S)
    assert segundos is not None
    assert round(segundos, 6) == 1.0
    assert formato.tiempo_luz_desde_km_texto(None) == "sin dato"


def test_au_texto() -> None:
    assert formato.au_texto(config.KM_POR_AU) == "1,0 UA"


def test_comparacion_texto() -> None:
    assert formato.comparacion_texto(1_000).startswith("es menos que")
    assert formato.comparacion_texto(config.KM_TIERRA_LUNA * 10).startswith("es como ir a la Luna")
    assert formato.comparacion_texto(config.KM_POR_AU * 173.067682) == "es como ir al Sol 173,1 veces"
    assert formato.comparacion_texto(None) == ""


def test_fecha_texto() -> None:
    assert formato.fecha_texto("2026-11-14") == "14 de noviembre de 2026"
    assert formato.fecha_texto("1969-08-27T12:00:00Z") == "27 de agosto de 1969"
    assert formato.fecha_texto(None) == "sin fecha"


def test_antiguedad_texto() -> None:
    ahora = datetime(2026, 11, 14, 12, 0, tzinfo=timezone.utc)
    assert formato.antiguedad_texto("2026-11-14T10:00:00Z", ahora) == "hace 2 horas"
    assert formato.antiguedad_texto("2026-11-14T11:30:00Z", ahora) == "hace 30 minutos"
    assert formato.antiguedad_texto("2026-11-12T12:00:00Z", ahora) == "hace 2 días"
    assert formato.antiguedad_texto("2026-11-14T11:59:30Z", ahora) == "hace un momento"
    assert formato.antiguedad_texto("no-es-fecha", ahora) == "fecha desconocida"
