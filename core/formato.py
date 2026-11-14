"""Formato de números, distancias y fechas para público de 8 a 12 años.

Reglas:

- Nada de notación científica ni números de 12 cifras.
- Espacio como separador de miles (norma en español): "25 900".
- Coma decimal: "173,1".
- Un dato desconocido se dice "sin dato", nunca "None" ni "0".
"""

from __future__ import annotations

from datetime import date, datetime, timezone

from core import config

MESES = (
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
)


def separar_miles(numero: int | float) -> str:
    """1234567 -> '1 234 567'."""
    return f"{int(round(numero)):,}".replace(",", " ")


def formatear_decimal(valor: float, decimales: int = 1) -> str:
    """173.0676 -> '173,1'."""
    texto = f"{float(valor):,.{decimales}f}"
    return texto.replace(",", " ").replace(".", ",")


def _plural(cantidad: int, singular: str, plural: str) -> str:
    return f"{cantidad} {singular if cantidad == 1 else plural}"


def _numero(valor) -> float | None:
    """Convierte a float si se puede. None si no, o si es NaN/negativo."""
    if valor is None or isinstance(valor, bool):
        return None
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        return None
    if numero != numero or numero < 0:  # NaN o negativo
        return None
    return numero


def distancia_texto(km) -> str:
    """25_890_556_821 -> '25 891 millones de km'."""
    numero = _numero(km)
    if numero is None:
        return "sin dato"
    if numero < 1_000_000:
        return f"{separar_miles(numero)} km"
    return f"{separar_miles(numero / 1_000_000)} millones de km"


def tiempo_luz_texto(segundos) -> str:
    """86_361 -> '23 horas 59 minutos'."""
    numero = _numero(segundos)
    if numero is None:
        return "sin dato"
    if numero < 1:
        return "menos de 1 segundo"
    if numero < 60:
        return _plural(round(numero), "segundo", "segundos")
    if numero < 3_600:
        return _plural(round(numero / 60), "minuto", "minutos")
    if numero < 86_400:
        horas = int(numero // 3_600)
        minutos = round((numero % 3_600) / 60)
        if minutos == 60:
            horas, minutos = horas + 1, 0
        if minutos == 0:
            return _plural(horas, "hora", "horas")
        return f"{_plural(horas, 'hora', 'horas')} {_plural(minutos, 'minuto', 'minutos')}"
    dias = int(numero // 86_400)
    horas = round((numero % 86_400) / 3_600)
    if horas == 24:
        dias, horas = dias + 1, 0
    if horas == 0:
        return _plural(dias, "día", "días")
    return f"{_plural(dias, 'día', 'días')} {_plural(horas, 'hora', 'horas')}"


def tiempo_luz_desde_km(km) -> float | None:
    """Distancia en km -> segundos de viaje de la luz."""
    numero = _numero(km)
    if numero is None:
        return None
    return numero / config.VELOCIDAD_LUZ_KM_S


def tiempo_luz_desde_km_texto(km) -> str:
    return tiempo_luz_texto(tiempo_luz_desde_km(km))


def au_texto(km) -> str:
    """Distancia en km -> '173,1 UA'."""
    numero = _numero(km)
    if numero is None:
        return "sin dato"
    return f"{formatear_decimal(numero / config.KM_POR_AU)} UA"


def comparacion_texto(km) -> str:
    """Traduce una distancia a algo cotidiano (Luna o Sol)."""
    numero = _numero(km)
    if numero is None:
        return ""
    if numero < config.KM_TIERRA_LUNA * 1.5:
        return "es menos que la distancia de la Tierra a la Luna"
    if numero < config.KM_POR_AU * 0.5:
        veces = round(numero / config.KM_TIERRA_LUNA)
        return f"es como ir a la Luna {separar_miles(veces)} veces"
    veces = numero / config.KM_POR_AU
    return f"es como ir al Sol {formatear_decimal(veces)} veces"


def fecha_texto(valor) -> str:
    """'2026-11-14' -> '14 de noviembre de 2026'."""
    if not valor:
        return "sin fecha"
    try:
        fecha = date.fromisoformat(str(valor)[:10])
    except ValueError:
        return str(valor)
    return f"{fecha.day} de {MESES[fecha.month - 1]} de {fecha.year}"


def _instante(valor) -> datetime | None:
    if not valor:
        return None
    texto = str(valor).replace("Z", "+00:00")
    try:
        momento = datetime.fromisoformat(texto)
    except ValueError:
        return None
    if momento.tzinfo is None:
        momento = momento.replace(tzinfo=timezone.utc)
    return momento


def antiguedad_texto(valor, ahora: datetime | None = None) -> str:
    """'2026-11-14T12:00:00Z' -> 'hace 2 horas'."""
    momento = _instante(valor)
    if momento is None:
        return "fecha desconocida"

    referencia = ahora or datetime.now(timezone.utc)
    if referencia.tzinfo is None:
        referencia = referencia.replace(tzinfo=timezone.utc)

    segundos = max(0.0, (referencia - momento).total_seconds())
    if segundos < 90:
        return "hace un momento"
    if segundos < 3_600:
        return f"hace {_plural(round(segundos / 60), 'minuto', 'minutos')}"
    if segundos < 86_400:
        return f"hace {_plural(round(segundos / 3_600), 'hora', 'horas')}"
    return f"hace {_plural(round(segundos / 86_400), 'día', 'días')}"
