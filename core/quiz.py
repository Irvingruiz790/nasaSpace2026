"""Banco editorial del quiz y estado de una partida, sin llamadas de red.

Cada pregunta referencia una pieza y un campo de su historia. La explicación
y los enlaces se leen del dataset oficial, sin duplicar las fuentes.
"""

from copy import deepcopy
import random
from uuid import uuid4

# Pieza, campo de evidencia, pregunta, respuesta correcta, tres distractores.
BANCO = [
    ("apollo-11-lm", "que_es", "¿Cuántas patas tiene la parte de Eagle que quedó en la Luna?", "Cuatro", "Dos", "Seis", "Ocho"),
    ("apollo-11-lm", "por_que", "¿A qué astronautas llevó Eagle a la Luna?", "Neil Armstrong y Buzz Aldrin", "Eugene Cernan y Harrison Schmitt", "Solo a Neil Armstrong", "No llevaba astronautas"),
    ("apollo-11-lm", "dato_curioso", "¿Cómo viajaban los astronautas dentro de Eagle?", "De pie", "En asientos reclinables", "En una bicicleta", "Acostados en camas"),
    ("apollo-17-lrv", "que_es", "¿Cómo llegó el coche lunar del Apolo 17 a la Luna?", "Doblado dentro del módulo lunar", "Volando con hélices", "En un cohete propio", "Lo construyeron con rocas lunares"),
    ("apollo-17-lrv", "descubrimiento", "¿Qué color tenía el suelo que encontró Harrison Schmitt?", "Naranja", "Azul", "Verde", "Morado"),
    ("apollo-17-lrv", "dato_curioso", "¿Cómo se manejaba el coche lunar del Apolo 17?", "Con una palanca en forma de T", "Con un volante de autobús", "Con pedales de bicicleta", "Con órdenes de voz"),
    ("surveyor-3", "que_es", "¿Qué llevaba Surveyor 3 para explorar la Luna?", "Una cámara y un brazo con pala", "Un helicóptero", "Una tripulación de tres personas", "Un submarino"),
    ("surveyor-3", "por_que", "¿Qué quería comprobar Surveyor 3 sobre el suelo lunar?", "Si podía sostener una nave con astronautas", "Si podían crecer árboles", "Si había peces", "Si estaba hecho de hielo"),
    ("surveyor-3", "dato_curioso", "¿Qué hizo Surveyor 3 al aterrizar?", "Rebotó dos veces", "Dio diez vueltas a la Luna", "Se convirtió en un rover", "Regresó de inmediato a la Tierra"),
    ("sojourner", "que_es", "¿Qué fue Sojourner?", "El primer robot con ruedas que rodó por Marte", "El primer coche de la Luna", "Un telescopio terrestre", "Un satélite de Saturno"),
    ("sojourner", "por_que", "¿Con qué base viajó Sojourner?", "Pathfinder", "Eagle", "InSight", "Voyager"),
    ("sojourner", "dato_curioso", "¿A quién recuerda el nombre Sojourner?", "A Sojourner Truth, defensora de los derechos civiles", "A un astronauta del Apolo 17", "A una luna de Júpiter", "A un volcán de Marte"),
    ("spirit", "que_es", "¿De qué rover era gemelo Spirit?", "Opportunity", "Sojourner", "Perseverance", "El coche lunar del Apolo 17"),
    ("spirit", "por_que", "¿En qué cráter aterrizó Spirit?", "Gusev", "Jezero", "Gale", "Tycho"),
    ("spirit", "descubrimiento", "¿Qué pasado de Marte ayudó a confirmar Spirit?", "Que hubo agua en su superficie", "Que tuvo ciudades", "Que tuvo bosques", "Que nunca tuvo agua"),
    ("opportunity", "que_es", "¿De dónde obtenía energía Opportunity?", "De paneles solares", "De gasolina", "De un molino de viento", "De una presa de agua"),
    ("opportunity", "descubrimiento", "¿Qué distancia recorrió Opportunity?", "45.16 km", "7.7 km", "1 km", "450 km"),
    ("opportunity", "ahora", "¿Qué fenómeno ocurrió cuando llegó la última señal de Opportunity?", "Una gran tormenta de polvo", "Una inundación", "Una nevada terrestre", "Un eclipse de la Luna"),
    ("insight", "que_es", "¿Qué instrumento usó InSight para sentir temblores?", "Un sismómetro", "Un telescopio", "Una brújula", "Un paracaídas"),
    ("insight", "descubrimiento", "¿Cómo se llaman los temblores de Marte?", "Martemotos", "Mareas", "Huracanes", "Eclipses"),
    ("insight", "dato_curioso", "¿Qué era el «topo» de InSight?", "Un instrumento que intentaba cavar", "Un animal llevado desde la Tierra", "Un coche pequeño", "Una antena para escuchar música"),
    ("ingenuity", "que_es", "¿Cómo viajó Ingenuity hasta Marte?", "Pegado a la panza de Perseverance", "Dentro de Voyager 1", "Volando desde la Tierra", "En el coche lunar"),
    ("ingenuity", "por_que", "¿Cuántos vuelos de prueba tenía planeados Ingenuity al principio?", "Cinco", "Setenta y dos", "Cien", "Uno"),
    ("ingenuity", "descubrimiento", "¿Cuántos vuelos llegó a realizar Ingenuity?", "72", "5", "17", "24"),
    ("voyager-1", "por_que", "¿Qué planetas salió a visitar Voyager 1?", "Júpiter y Saturno", "Marte y Venus", "Urano y Neptuno", "Mercurio y la Tierra"),
    ("voyager-1", "descubrimiento", "¿Qué planeta aparece como «Un punto azul pálido»?", "La Tierra", "Marte", "Júpiter", "Saturno"),
    ("voyager-1", "dato_curioso", "¿Qué lleva Voyager 1 como mensaje para otros mundos?", "Un disco de oro con saludos, sonidos y música", "Una caja de rocas lunares", "Un libro de papel", "Una bolsa de semillas"),
    ("voyager-2", "que_es", "¿Qué sonda es la única que visitó Urano y Neptuno?", "Voyager 2", "Voyager 1", "InSight", "Surveyor 3"),
    ("voyager-2", "descubrimiento", "¿Dónde encontró Voyager 2 la Gran Mancha Oscura?", "En Neptuno", "En Marte", "En la Luna", "En la Tierra"),
    ("voyager-2", "ahora", "¿Qué límite cruzó Voyager 2 al entrar al espacio interestelar?", "La heliopausa, el borde de la burbuja del Sol", "La superficie de la Luna", "La atmósfera de la Tierra", "Los anillos de Saturno"),
]


def construir_preguntas(piezas):
    por_id = {p["id"]: p for p in piezas}
    preguntas = []
    for numero, (pieza_id, campo, texto, correcta, *otras) in enumerate(BANCO):
        pieza = por_id.get(pieza_id)
        if not pieza or not pieza.get("historia", {}).get(campo) or not pieza.get("fuentes"):
            continue
        preguntas.append({
            "id": f"q{numero + 1:02}",
            "pieza_id": pieza_id,
            "pregunta": texto,
            "correcta": correcta,
            "opciones": [correcta, *otras],
            "explicacion": pieza["historia"][campo],
            "fuentes": deepcopy(pieza["fuentes"]),
        })
    return preguntas


def nueva_partida(preguntas, rng=None):
    rng = rng or random.SystemRandom()
    orden = deepcopy(preguntas)
    rng.shuffle(orden)
    for pregunta in orden:
        rng.shuffle(pregunta["opciones"])
    return {"id": uuid4().hex, "preguntas": orden, "respuestas": [], "aciertos": 0}


def responder(partida, partida_id, indice, respuesta):
    """Ignora eventos atrasados o dobles clics de una pregunta ya contestada."""
    if partida_id != partida["id"] or indice != len(partida["respuestas"]):
        return False
    if indice >= len(partida["preguntas"]):
        return False
    pregunta = partida["preguntas"][indice]
    if respuesta not in pregunta["opciones"]:
        return False
    partida["respuestas"].append(respuesta)
    partida["aciertos"] += int(respuesta == pregunta["correcta"])
    return True
