"""Enumeraciones y límites del contrato de datos.

Este archivo es la versión ejecutable de `docs/CONTRATO_DATOS.md`.
Si el contrato cambia, se cambia aquí y en el documento, en el mismo PR.
"""

from __future__ import annotations

ZONAS: dict[str, str] = {
    "luna": "La Luna",
    "marte": "Marte",
    "espacio_profundo": "Espacio profundo",
    "orbita": "En órbita",
    "asteroide": "En un asteroide",
}

ESTADOS: dict[str, str] = {
    "activo": "Sigue despierto",
    "en_silencio": "En silencio",
    "se_quedo": "Se quedó aquí",
    "en_orbita": "En órbita para siempre",
    "perdido": "Se perdió",
}

TIPOS: frozenset[str] = frozenset(
    {"lander", "rover", "orbitador", "nave", "instrumento"}
)

# Límite de palabras por bloque de la ficha (público de 8 a 12 años).
LIMITES_HISTORIA: dict[str, int] = {
    "que_es": 35,
    "por_que": 40,
    "descubrimiento": 45,
    "ahora": 45,
    "dato_curioso": 30,
}

# Campos de texto que no pueden faltar ni estar vacíos.
CAMPOS_TEXTO_OBLIGATORIOS: tuple[str, ...] = (
    "id",
    "nombre",
    "apodo",
    "tipo",
    "mision",
    "agencia",
    "zona",
    "estado",
    "etiqueta_estado",
    "ubicacion_texto",
    "lanzamiento",
    "imagen",
    "credito_imagen",
    "alt_text",
    "revisor",
    "fecha_verificacion",
)
