"""Genera `docs/Guia_Equipo.docx`, la guía única de trabajo del equipo.

    .\\.venv\\Scripts\\python.exe scripts\\generar_guia_word.py

El Word se puede regenerar cuando cambie el plan; el contenido vive aquí.
"""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "docs" / "Guia_Equipo.docx"

AZUL = "1F3864"
AZUL_MEDIO = "2E5C8A"
VERDE = "0F7B6C"
NARANJA = "C55A11"
GRIS = "595959"
FONDO_CABECERA = "1F3864"
FONDO_SUAVE = "EEF3F8"
FONDO_AVISO = "FFF4E5"
FONDO_OK = "EAF5EE"
FONDO_CODIGO = "F4F4F4"

doc = Document()

# --- Estilos base ----------------------------------------------------------

seccion = doc.sections[0]
seccion.page_width = Cm(21)
seccion.page_height = Cm(29.7)
seccion.left_margin = Cm(2.2)
seccion.right_margin = Cm(2.2)
seccion.top_margin = Cm(2.0)
seccion.bottom_margin = Cm(2.0)

normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(10.5)
normal.paragraph_format.space_after = Pt(4)
normal.paragraph_format.line_spacing = 1.08

for nombre, tam, color, antes, despues in (
    ("Heading 1", 18, AZUL, 0, 5),
    ("Heading 2", 13.5, AZUL_MEDIO, 12, 4),
    ("Heading 3", 11.5, VERDE, 9, 2),
):
    estilo = doc.styles[nombre]
    estilo.font.name = "Calibri"
    estilo.font.size = Pt(tam)
    estilo.font.bold = True
    estilo.font.color.rgb = RGBColor.from_string(color)
    estilo.paragraph_format.space_before = Pt(antes)
    estilo.paragraph_format.space_after = Pt(despues)
    estilo.paragraph_format.keep_with_next = True

# --- Utilidades ------------------------------------------------------------


def sombrear(celda, color: str) -> None:
    tcPr = celda._tc.get_or_add_tcPr()
    sombra = OxmlElement("w:shd")
    sombra.set(qn("w:val"), "clear")
    sombra.set(qn("w:color"), "auto")
    sombra.set(qn("w:fill"), color)
    tcPr.append(sombra)


def repetir_encabezado(fila) -> None:
    trPr = fila._tr.get_or_add_trPr()
    cabecera = OxmlElement("w:tblHeader")
    cabecera.set(qn("w:val"), "true")
    trPr.append(cabecera)


def h1(texto: str, salto: bool = True) -> None:
    encabezado = doc.add_heading(texto, level=1)
    if salto:
        # page_break_before evita la página en blanco que deja add_page_break()
        encabezado.paragraph_format.page_break_before = True


def h2(texto: str) -> None:
    doc.add_heading(texto, level=2)


def h3(texto: str) -> None:
    doc.add_heading(texto, level=3)


def p(texto: str = "", *, negrita: bool = False, cursiva: bool = False, tam: float | None = None) -> None:
    parrafo = doc.add_paragraph()
    run = parrafo.add_run(texto)
    run.bold = negrita
    run.italic = cursiva
    if tam:
        run.font.size = Pt(tam)


def vinetas(items: list[str]) -> None:
    for item in items:
        doc.add_paragraph(item, style="List Bullet")


def paso(numero: int, titulo: str, texto: str = "", hecho: str = "") -> None:
    parrafo = doc.add_paragraph()
    parrafo.paragraph_format.space_before = Pt(7)
    parrafo.paragraph_format.space_after = Pt(1)
    run = parrafo.add_run(f"Paso {numero}. {titulo}")
    run.bold = True
    run.font.size = Pt(10.5)
    if texto:
        parrafo2 = doc.add_paragraph(texto)
        parrafo2.paragraph_format.left_indent = Cm(0.4)
        parrafo2.paragraph_format.space_after = Pt(1)
    if hecho:
        parrafo3 = doc.add_paragraph()
        parrafo3.paragraph_format.left_indent = Cm(0.4)
        r = parrafo3.add_run(f"Quedó bien cuando: {hecho}")
        r.italic = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor.from_string(VERDE)


def codigo(texto: str) -> None:
    parrafo = doc.add_paragraph()
    parrafo.paragraph_format.left_indent = Cm(0.3)
    parrafo.paragraph_format.space_before = Pt(3)
    parrafo.paragraph_format.space_after = Pt(6)
    pPr = parrafo._p.get_or_add_pPr()
    sombra = OxmlElement("w:shd")
    sombra.set(qn("w:val"), "clear")
    sombra.set(qn("w:color"), "auto")
    sombra.set(qn("w:fill"), FONDO_CODIGO)
    pPr.append(sombra)
    lineas = texto.split("\n")
    for indice, linea in enumerate(lineas):
        run = parrafo.add_run(linea)
        run.font.name = "Consolas"
        run.font.size = Pt(8.5)
        if indice < len(lineas) - 1:
            run.add_break()


def caja(titulo: str, texto: str, fondo: str = FONDO_AVISO, color: str = NARANJA) -> None:
    tabla_caja = doc.add_table(rows=1, cols=1)
    tabla_caja.alignment = WD_TABLE_ALIGNMENT.CENTER
    celda = tabla_caja.cell(0, 0)
    sombrear(celda, fondo)
    parrafo = celda.paragraphs[0]
    run = parrafo.add_run(titulo)
    run.bold = True
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor.from_string(color)
    parrafo2 = celda.add_paragraph(texto)
    parrafo2.runs[0].font.size = Pt(9.5)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def tabla(
    encabezados: list[str],
    filas: list[list[str]],
    anchos: list[float] | None = None,
    tam: float = 9,
) -> None:
    t = doc.add_table(rows=1, cols=len(encabezados))
    t.style = "Table Grid"
    t.autofit = False
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    t._tbl.tblPr.append(layout)

    cabecera = t.rows[0]
    repetir_encabezado(cabecera)
    for indice, texto in enumerate(encabezados):
        celda = cabecera.cells[indice]
        celda.text = ""
        run = celda.paragraphs[0].add_run(texto)
        run.bold = True
        run.font.size = Pt(tam)
        run.font.color.rgb = RGBColor.from_string("FFFFFF")
        sombrear(celda, FONDO_CABECERA)

    for numero_fila, fila in enumerate(filas):
        celdas = t.add_row().cells
        for indice, valor in enumerate(fila):
            celdas[indice].text = ""
            run = celdas[indice].paragraphs[0].add_run(str(valor))
            run.font.size = Pt(tam)
            if numero_fila % 2 == 1:
                sombrear(celdas[indice], FONDO_SUAVE)

    if anchos:
        total = sum(anchos)
        anchos = [ancho * 16.6 / total for ancho in anchos]
        for fila in t.rows:
            for indice, ancho in enumerate(anchos):
                fila.cells[indice].width = Cm(ancho)

    doc.add_paragraph().paragraph_format.space_after = Pt(2)


# =========================================================================
# PORTADA
# =========================================================================

for _ in range(3):
    doc.add_paragraph()

titulo = doc.add_paragraph()
titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = titulo.add_run("¿DÓNDE ESTÁ AHORA?")
run.bold = True
run.font.size = Pt(34)
run.font.color.rgb = RGBColor.from_string(AZUL)

subtitulo = doc.add_paragraph()
subtitulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitulo.add_run("Guía de trabajo del equipo")
run.font.size = Pt(20)
run.font.color.rgb = RGBColor.from_string(AZUL_MEDIO)

reto = doc.add_paragraph()
reto.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = reto.add_run("NASA Space Apps Challenge 2026")
run.font.size = Pt(13)
run.font.color.rgb = RGBColor.from_string(GRIS)

doc.add_paragraph()
frase = doc.add_paragraph()
frase.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = frase.add_run(
    "Qué hace cada equipo, con qué herramientas\ny en qué formato — paso por paso"
)
run.font.size = Pt(12)
run.italic = True

for _ in range(2):
    doc.add_paragraph()

tabla(
    ["Dato", "Detalle"],
    [
        ["Versión", "1.0 — documento único de coordinación"],
        ["Fecha", "14 de noviembre de 2026"],
        ["Equipos", "Frontend (2 personas) · Backend (1) · Investigación (1)"],
        ["Duración", "44 horas de hackatón"],
        ["Público de la app", "Niños y niñas de 8 a 12 años, en español"],
    ],
    anchos=[4.5, 11.5],
    tam=10,
)

caja(
    "Antes de empezar",
    "Este documento reemplaza, para el trabajo diario, a los archivos largos de la "
    "carpeta docs/. Si algo de esos documentos dice una cosa y esta guía dice otra, "
    "manda esta guía. Cada equipo lee la sección 1 a la 6, después la suya, y usa el "
    "resto solo como consulta.",
    fondo=FONDO_SUAVE,
    color=AZUL_MEDIO,
)

# =========================================================================
# 1. CÓMO USAR ESTA GUÍA
# =========================================================================

h1("1. Cómo usar esta guía (5 minutos)")

p(
    "No hay que leer las 20 páginas de corrido. Cada persona lee una parte distinta "
    "y vuelve a la suya cuando se pierde."
)

tabla(
    ["Si eres…", "Lee con atención", "Consulta cuando lo necesites"],
    [
        ["Todos", "Secciones 1, 2, 3, 4, 5, 6 y 10", "Resto del documento"],
        ["Investigación", "Sección 7 completa", "Sección 11 (fechas) y anexo A"],
        ["Backend", "Sección 8 completa", "Sección 12 (problemas) y anexo A"],
        ["Frontend", "Sección 9 completa", "Sección 12 (problemas) y anexo A"],
    ],
    anchos=[3.5, 7.0, 6.5],
)

h2("La regla de oro")

caja(
    "Si no sabes qué hacer, no preguntes \"¿y ahora qué?\"",
    "Ve a la sección de tu equipo, busca el primer paso que NO esté terminado y haz "
    "solo ese. Cuando lo termines, tacha y pasa al siguiente. Así se avanza sin "
    "depender de que alguien te lo recuerde.",
    fondo=FONDO_OK,
    color=VERDE,
)

# =========================================================================
# 2. EL PROYECTO EN UNA PÁGINA
# =========================================================================

h1("2. El proyecto en una página")

p(
    "«¿Dónde está ahora?» es una aplicación web donde un niño o una niña de 8 a 12 "
    "años explora tres zonas —la Luna, Marte y el espacio profundo—, hace clic en una "
    "máquina que la NASA dejó ahí y lee su historia: qué es, por qué se envió, qué "
    "descubrió y dónde está hoy."
)

h2("Qué se entrega al final")

tabla(
    ["Entregable", "Quién lo cierra", "Cómo se ve"],
    [
        ["App pública funcionando", "Backend (deploy) + Frontend (pantallas)", "Una URL que abre en cualquier teléfono"],
        ["Repo ordenado en GitHub", "Backend (merge captain)", "Código, datos y documentos"],
        ["Video de 2 minutos", "Investigación + Frontend", "Grabación de la app con narración"],
        ["Pitch hablado", "Investigación", "2 minutos frente al jurado"],
    ],
    anchos=[5.0, 6.0, 6.0],
)

h2("Las tres zonas")

tabla(
    ["Zona", "Qué se cuenta", "Ejemplos"],
    [
        ["La Luna", "Máquinas que se quedaron quietas hace décadas", "Apolo 11, LRV del Apolo 17, Surveyor 3"],
        ["Marte", "Robots que dejaron de responder", "Sojourner, Spirit, Opportunity, InSight, Ingenuity"],
        ["Espacio profundo", "Naves que todavía hablan y están lejísimos", "Voyager 1, Voyager 2"],
    ],
    anchos=[3.5, 7.0, 6.5],
)

h2("Lo que el jurado va a mirar")

vinetas(
    [
        "Que la app funcione en vivo, sin excusas técnicas.",
        "Que un niño entienda la historia sin ayuda de un adulto.",
        "Que cada dato se pueda rastrear a una fuente oficial de NASA.",
        "Que el equipo sepa explicar qué hizo cada quien.",
    ]
)

p(
    "El jurado no evalúa cuántas líneas de código escribieron. Evalúa si la historia "
    "se entiende, si los datos son ciertos y si la app funciona.",
    cursiva=True,
)

# =========================================================================
# 3. CÓMO ENCAJAN LOS TRES EQUIPOS
# =========================================================================

h1("3. Cómo encajan los tres equipos")

p(
    "Piénsenlo como un restaurante. Investigación consigue los ingredientes y la "
    "receta. Backend cocina y deja los platos listos en un formato estándar. Frontend "
    "es el mesero que sirve el plato para que se vea rico y se entienda."
)

t = doc.add_table(rows=1, cols=5)
t.style = "Table Grid"
contenido = [
    ("INVESTIGACIÓN", "Llena el CSV y consigue las imágenes"),
    ("→", "entrega"),
    ("BACKEND", "Convierte el CSV en JSON y lo sirve"),
    ("→", "entrega"),
    ("FRONTEND", "Dibuja las pantallas y los mapas"),
]
for indice, (titulo_celda, texto_celda) in enumerate(contenido):
    celda = t.cell(0, indice)
    if indice in (1, 3):
        celda.text = ""
        run = celda.paragraphs[0].add_run("→")
        run.bold = True
        run.font.size = Pt(20)
        run.font.color.rgb = RGBColor.from_string(NARANJA)
        celda.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    else:
        celda.text = ""
        run = celda.paragraphs[0].add_run(titulo_celda)
        run.bold = True
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor.from_string("FFFFFF")
        sombrear(celda, FONDO_CABECERA)
        parrafo = celda.add_paragraph(texto_celda)
        parrafo.runs[0].font.size = Pt(9)

for indice, ancho in enumerate([4.4, 1.2, 4.4, 1.2, 5.4]):
    t.cell(0, indice).width = Cm(ancho)

doc.add_paragraph()

h2("El \"enchufe\" entre equipos")

p(
    "Los tres equipos no se hablan por WhatsApp: se hablan por un archivo con una "
    "forma fija. Ese archivo es el dataset. Si investigación escribe un campo con "
    "otro nombre, el backend no lo encuentra y la pantalla sale vacía."
)

p(
    "Por eso existe el «contrato de datos»: una lista de nombres de campos que nadie "
    "cambia a mitad del proyecto. Es como la forma del enchufe. Si alguien cambia la "
    "forma, el aparato ya no entra."
)

caja(
    "Regla práctica",
    "Si necesitas un campo nuevo, se pide en el chat y se agrega AL FINAL. Nunca se "
    "renombra un campo que ya existe. Un campo renombrado sin avisar rompe las tres "
    "pantallas al mismo tiempo.",
    fondo=FONDO_AVISO,
    color=NARANJA,
)

h2("Quién produce qué")

tabla(
    ["Produce", "Quién", "Formato", "Quién lo consume"],
    [
        ["Las fichas de las 10 piezas", "Investigación", "CSV (Excel)", "Backend"],
        ["Las imágenes y sus créditos", "Investigación", "JPG o WebP", "Frontend"],
        ["El dataset de la app", "Backend (lo genera)", "JSON", "Frontend"],
        ["El respaldo de datos en vivo", "Backend", "JSON", "Frontend"],
        ["Las funciones de datos", "Backend", "Python (.py)", "Frontend"],
        ["Las pantallas y el estilo", "Frontend", "Python (.py) y CSS", "El usuario final"],
    ],
    anchos=[6.0, 3.5, 3.5, 4.0],
)

# =========================================================================
# 4. FORMATOS DE TRABAJO
# =========================================================================

h1("4. Formatos de trabajo")

p(
    "Cada equipo trabaja en un formato distinto a propósito. El formato se elige "
    "para que esa persona no tenga que pelear con cosas que no le tocan."
)

tabla(
    ["Formato", "Para qué sirve", "Quién lo usa", "Dónde vive"],
    [
        ["CSV", "Tabla de una fila por pieza. Se abre en Excel o Google Sheets, como cualquier hoja de cálculo.", "Investigación", "contenido/fichas.csv"],
        ["JSON", "Datos con estructura, los lee la app. Nadie lo escribe a mano.", "Backend lo genera", "data/artifacts.json y data/live_snapshot.json"],
        ["Python (.py)", "Código de la app y de las funciones de datos.", "Backend y Frontend", "core/, app.py, pages/"],
        ["CSS", "Colores, tamaños, tipografía y estilos.", "Frontend", "assets/styles.css"],
        ["JPG o WebP", "Fotos e imágenes de fondo.", "Investigación y Frontend", "assets/img/ y assets/maps/"],
        ["Markdown (.md)", "Documentos y notas del equipo.", "Todos", "docs/"],
    ],
    anchos=[2.6, 6.4, 3.4, 4.6],
)

h2("¿Por qué investigación no escribe JSON?")

p(
    "Porque el JSON tiene llaves, comas y corchetes. Un solo punto y coma mal puesto "
    "rompe todo el archivo y nadie sabe por qué la app no carga. En Excel eso no pasa."
)

p(
    "Investigación llena una fila por pieza en el CSV. El backend corre un comando que "
    "convierte ese CSV en JSON y avisa si falta algo. Cada quien trabaja en lo suyo."
)

caja(
    "Traducción automática",
    "El comando es:  python scripts/fichas_a_json.py\n"
    "Lee contenido/fichas.csv, revisa que todo esté completo y escribe "
    "data/artifacts.json. Si hay errores, los lista con el nombre de la pieza y el "
    "campo exacto. No hace falta abrir el JSON nunca.",
    fondo=FONDO_SUAVE,
    color=AZUL_MEDIO,
)

h2("Nombres de archivo: no se inventan")

tabla(
    ["Tipo", "Patrón", "Ejemplo correcto", "Ejemplo incorrecto"],
    [
        ["ID de pieza", "minúsculas y guiones", "voyager-1", "Voyager 1"],
        ["Imagen principal", "{id}_main.jpg", "voyager-1_main.jpg", "foto final.JPG"],
        ["Imagen pequeña", "{id}_thumb.jpg", "voyager-1_thumb.jpg", "voyager mini.jpg"],
        ["Página de la app", "número + nombre", "pages/1_Luna.py", "pages/luna nueva.py"],
    ],
    anchos=[3.6, 4.4, 4.6, 4.4],
)

# =========================================================================
# 5. GLOSARIO
# =========================================================================

h1("5. Glosario (los 12 términos que van a escuchar)")

tabla(
    ["Término", "Qué es, en simple"],
    [
        ["Repositorio (repo)", "La carpeta del proyecto en GitHub. Ahí vive la versión oficial de todo."],
        ["Clonar", "Bajar el repo a tu computadora por primera vez."],
        ["Commit", "Guardar una foto de tus cambios, con un mensaje que explica qué hiciste."],
        ["Rama (branch)", "Una copia paralela del proyecto para trabajar sin romper lo demás."],
        ["Push", "Subir tus commits de tu computadora a GitHub."],
        ["Pull", "Bajar los cambios que hicieron los demás."],
        ["PR (pull request)", "Pedir permiso para unir tu rama con main. Ahí te revisan."],
        ["Merge", "Unir una rama con main. Lo hace el backend."],
        ["JSON", "Archivo de datos con estructura. Lo lee la app; no se edita a mano."],
        ["CSV", "Tabla separada por comas. Se abre en Excel."],
        ["API", "Servicio de otra persona en internet al que le pides datos. Aquí: JPL Horizons."],
        ["Deploy", "Publicar la app en internet para que cualquiera entre con un link."],
    ],
    anchos=[4.2, 12.4],
)

# =========================================================================
# 6. REGLAS
# =========================================================================

h1("6. Las cuatro reglas que evitan el 90% de los problemas")

h2("Regla 1. Un dueño por archivo")

p("Nadie edita un archivo que no es suyo. Si lo necesitas, lo pides en el chat.")

tabla(
    ["Archivo o carpeta", "Dueño", "Qué hace ahí"],
    [
        ["contenido/fichas.csv", "Investigación", "Escribe las fichas"],
        ["assets/img/", "Investigación", "Guarda las imágenes con su crédito"],
        ["data/artifacts.json", "Backend (lo genera)", "Nadie lo edita a mano"],
        ["data/live_snapshot.json", "Backend (lo genera)", "Respaldo de datos en vivo"],
        ["core/", "Backend", "Funciones de datos, API y respaldo"],
        ["scripts/", "Backend", "Conversor CSV→JSON y actualizador del respaldo"],
        ["requirements.txt", "Backend", "Dependencias. Nadie más lo toca"],
        ["app.py", "Frontend", "Pantalla de inicio"],
        ["pages/", "Frontend", "Una pantalla por archivo"],
        ["components/", "Frontend", "Tarjetas y piezas reutilizables"],
        ["assets/styles.css", "Frontend", "Todo el estilo visual"],
        ["assets/maps/", "Frontend", "Imágenes de fondo y posiciones de marcadores"],
        ["docs/", "Todos, con aviso", "Documentación"],
    ],
    anchos=[5.4, 4.6, 6.6],
)

h2("Regla 2. main siempre debe funcionar")

p(
    "Nadie sube algo roto a main. Si tu rama no abre la app, no la mergeas. Es mejor "
    "perder una función que perder la demo."
)

h2("Regla 3. Integración cada 4 horas")

p(
    "Cada 4 horas el equipo se detiene 30 minutos, junta lo que esté listo, prueba la "
    "app completa y avisa qué falta. El paso a paso está en la sección 10."
)

h2("Regla 4. El contrato no se cambia en silencio")

p(
    "Si necesitas cambiar el nombre de un campo o agregar uno nuevo, se avisa, se "
    "aprueba entre backend e investigación y se cambia en el mismo momento en todos "
    "lados. Nunca \"después lo arreglo\"."
)

h2("Los seis comandos de Git que van a usar")

tabla(
    ["Comando", "Cuándo", "Qué hace"],
    [
        ["git clone URL", "Una sola vez", "Baja el repo a tu computadora"],
        ["git switch -c feat/mi-tarea", "Al empezar una tarea", "Crea tu rama de trabajo"],
        ["git add .", "Antes de guardar", "Prepara tus cambios"],
        ["git commit -m \"feat: ...\"", "Al terminar un avance", "Guarda la foto de tus cambios"],
        ["git pull --rebase origin main", "Antes de subir", "Trae lo nuevo de los demás"],
        ["git push -u origin feat/mi-tarea", "Al terminar la tarea", "Sube tu rama a GitHub"],
    ],
    anchos=[6.2, 4.0, 6.4],
)

caja(
    "Nunca",
    "Nunca uses  git push --force  sobre main. Borra el trabajo de tus compañeros y "
    "no se recupera fácil.",
    fondo="FDEAEA",
    color="B00020",
)

# =========================================================================
# 7. INVESTIGACIÓN
# =========================================================================

h1("7. Equipo de investigación y contenido")

p(
    "Eres el proveedor de la materia prima. Sin tus fichas, la app es un cascarón "
    "vacío. Tu trabajo no es programar: es investigar, escribir claro y llenar una "
    "tabla."
)

h2("7.1 Lo que entregas (cuatro cosas)")

tabla(
    ["Entregable", "Dónde", "Cuándo"],
    [
        ["10 filas llenas en el CSV", "contenido/fichas.csv", "Bloques 1 y 2"],
        ["10 imágenes con nombre correcto", "assets/img/", "Bloques 2 y 3"],
        ["Crédito y texto alternativo de cada imagen", "Dentro del CSV", "Con cada imagen"],
        ["Nombre del revisor en cada ficha", "Columna revisor", "Antes del bloque 4"],
    ],
    anchos=[6.6, 5.4, 4.6],
)

h2("7.2 Herramientas")

tabla(
    ["Herramienta", "Para qué", "Costo"],
    [
        ["Excel o Google Sheets", "Llenar contenido/fichas.csv (una fila por pieza)", "Gratis"],
        ["NSSDCA (nssdc.gsfc.nasa.gov/nmc/)", "Datos técnicos y estado final de cada nave", "Gratis"],
        ["NASA Science (science.nasa.gov)", "Historia, descubrimientos y estado actual", "Gratis"],
        ["NASA Images (images.nasa.gov)", "Fotos reales con crédito", "Gratis"],
        ["NASA Space Place (spaceplace.nasa.gov/sp/)", "Cómo explicar cosas difíciles con palabras simples", "Gratis"],
        ["Squoosh (squoosh.app)", "Reducir el peso de las imágenes", "Gratis, en el navegador"],
        ["Google Docs", "Escribir el guion del pitch y tomar notas", "Gratis"],
    ],
    anchos=[6.6, 8.6, 2.4],
)

h2("7.3 Paso a paso")

paso(
    1,
    "Abre el CSV",
    "Entra a contenido/fichas.csv con Excel o súbelo a Google Sheets. Ya tiene tres "
    "filas de ejemplo llenas: Voyager 1, Voyager 2 y Apolo 11. Esas tres te sirven de "
    "modelo. Complétalas y agrega las que faltan hasta tener 10.",
    "ves 34 columnas en la primera fila y 3 piezas de ejemplo.",
)

paso(
    2,
    "Elige las 10 piezas",
    "Ya están decididas en el plan: 3 de la Luna, 5 de Marte y 2 del espacio profundo. "
    "No cambies la lista sin avisar, porque el mapa del frontend se dibuja con esas 10.",
    "las 10 piezas están en la tabla 7.5.",
)

paso(
    3,
    "Investiga cada pieza en dos fuentes",
    "Abre NSSDCA y NASA Science. Busca la pieza por su nombre. Copia los datos duros "
    "(fecha de lanzamiento, coordenadas, estado, última señal) y anota la URL de cada "
    "fuente. Necesitas dos fuentes oficiales por cada dato importante.",
    "puedes mostrar dos URLs distintas que dicen lo mismo.",
)

paso(
    4,
    "Escribe los cinco bloques de la historia",
    "Cada pieza lleva: ¿Qué es?, ¿Por qué la enviamos?, ¿Qué descubrió?, ¿Dónde está "
    "ahora? y un Dato curioso. Frases cortas, una idea por frase. Respeta los límites "
    "de palabras de la tabla 7.6.",
    "el total queda por debajo de 195 palabras.",
)

paso(
    5,
    "Busca la imagen y guárdala",
    "En NASA Images busca la pieza. Descarga la mejor foto horizontal. Cámbiale el "
    "nombre a {id}_main.jpg (por ejemplo voyager-1_main.jpg) y guárdala en "
    "assets/img/. Si pesa más de 300 KB, pásala por Squoosh.",
    "la imagen abre, se ve nítida y pesa menos de 300 KB.",
)

paso(
    6,
    "Escribe el crédito y el texto alternativo",
    "El crédito va en la columna credito_imagen (por ejemplo NASA/JPL-Caltech). El "
    "texto alternativo describe lo que se ve en una frase, para quien no puede ver la "
    "imagen.",
    "una persona que no ve la pantalla entiende qué muestra la foto.",
)

paso(
    7,
    "Completa fuentes, revisor y fecha",
    "En las columnas fuente1_titulo, fuente1_url, fuente2_titulo y fuente2_url pega "
    "las dos fuentes. Escribe tu nombre en revisor y la fecha en fecha_verificacion "
    "(formato 2026-11-14).",
    "ninguna de esas celdas queda vacía.",
)

paso(
    8,
    "Revisión cruzada",
    "Otra persona del equipo lee la ficha y compara con las fuentes. Busca: datos "
    "inventados, palabras difíciles, párrafos largos e imágenes sin crédito. Quien "
    "revisa escribe su nombre en revisor.",
    "alguien más además de ti leyó la ficha y la aprobó.",
)

paso(
    9,
    "Avisa a backend",
    "Escribe en el chat: «Fichas listas: voyager-1, apollo-11-lm, …». Backend corre el "
    "conversor y te devuelve la lista de errores si hay alguno.",
    "backend confirmó que el reporte dice Errores: 0.",
)

paso(
    10,
    "Mira la app y compara",
    "Cuando la app esté desplegada, abre tu ficha y compara lo que se ve contra tu "
    "fuente. Si un número no coincide, avísale a backend. Tú eres la última defensa "
    "de la precisión.",
    "lo que se ve en pantalla dice exactamente lo que dice tu fuente.",
)

h2("7.4 Las 34 columnas del CSV")

p(
    "No hay que memorizarlas. Están agrupadas por tema y cada una tiene un ejemplo. "
    "Si una celda no aplica, se deja vacía (no se escribe «no hay» ni «N/A»)."
)

h3("Grupo A — Identificación")

tabla(
    ["Columna", "Qué escribir", "Ejemplo"],
    [
        ["id", "Nombre corto en minúsculas y guiones. No se cambia nunca.", "voyager-1"],
        ["nombre", "Nombre completo y formal.", "Voyager 1"],
        ["apodo", "Frase corta y memorable para un niño.", "La mensajera más lejana"],
        ["tipo", "Uno de: lander, rover, orbitador, nave, instrumento.", "nave"],
        ["mision", "Misión a la que pertenece.", "Voyager"],
        ["agencia", "Quién la construyó o la opera.", "NASA/JPL-Caltech"],
        ["zona", "Uno de: luna, marte, espacio_profundo, orbita, asteroide.", "espacio_profundo"],
        ["estado", "Uno de: activo, en_silencio, se_quedo, en_orbita, perdido.", "activo"],
        ["etiqueta_estado", "El estado dicho para un niño.", "Sigue despierta"],
    ],
    anchos=[4.0, 9.4, 4.2],
)

h3("Grupo B — Ubicación y fechas")

tabla(
    ["Columna", "Qué escribir", "Ejemplo"],
    [
        ["ubicacion_texto", "Lugar con nombre, en palabras.", "Mar de la Tranquilidad"],
        ["lat", "Latitud en grados decimales. Solo Luna o Marte. Si no aplica, vacío.", "0.67416"],
        ["lon", "Longitud en grados decimales. Solo Luna o Marte. Si no aplica, vacío.", "23.47314"],
        ["lanzamiento", "Fecha en formato AAAA-MM-DD.", "1977-09-05"],
        ["ultima_senal", "Fecha de la última señal o «sigue activa».", "sigue activa"],
        ["distancia_actual", "Distancia en palabras, solo si aplica.", "unos 25 900 millones de km"],
        ["horizons_id", "Solo espacio profundo. Lo confirma backend.", "-31"],
    ],
    anchos=[3.6, 9.6, 4.4],
)

h3("Grupo C — Imagen y accesibilidad")

tabla(
    ["Columna", "Qué escribir", "Ejemplo"],
    [
        ["imagen", "Solo el nombre del archivo. La carpeta la pone el script.", "voyager-1_main.jpg"],
        ["credito_imagen", "Quién tomó o hizo la imagen.", "NASA/JPL-Caltech"],
        ["alt_text", "Descripción de la imagen en una frase.", "Ilustración de la nave Voyager con su gran antena parabólica…"],
    ],
    anchos=[3.6, 8.4, 5.6],
)

h3("Grupo D — Historia (los cinco bloques)")

tabla(
    ["Columna", "Qué escribir", "Límite"],
    [
        ["que_es", "Qué es, con una comparación cotidiana.", "35 palabras"],
        ["por_que", "La pregunta o misión que fue a resolver.", "40 palabras"],
        ["descubrimiento", "Un descubrimiento concreto.", "45 palabras"],
        ["ahora", "Dónde está y qué hace hoy.", "45 palabras"],
        ["dato_curioso", "Un dato que se recuerde.", "30 palabras"],
    ],
    anchos=[4.0, 10.6, 3.0],
)

h3("Grupo E — Fuentes y control de calidad")

tabla(
    ["Columna", "Qué escribir", "Ejemplo"],
    [
        ["fuente1_titulo", "Nombre de la primera fuente oficial.", "NASA Science — Voyager"],
        ["fuente1_url", "Su enlace completo.", "https://science.nasa.gov/mission/voyager/"],
        ["fuente2_titulo", "Nombre de la segunda fuente.", "JPL Horizons API"],
        ["fuente2_url", "Su enlace completo.", "https://ssd.jpl.nasa.gov/api/horizons.api"],
        ["fuente3_titulo", "Tercera fuente, si la hay. Opcional.", ""],
        ["fuente3_url", "Su enlace. Opcional.", ""],
        ["consultado", "Fecha en que consultaste. AAAA-MM-DD.", "2026-11-14"],
        ["revisor", "Quién verificó la ficha.", "Ana"],
        ["fecha_verificacion", "Fecha de esa revisión. AAAA-MM-DD.", "2026-11-14"],
        ["notas_verificacion", "Aclaraciones o dudas. Opcional.", "El destino de la etapa de ascenso es incierto."],
    ],
    anchos=[4.0, 7.0, 5.6],
)

h2("7.5 Las 10 piezas del proyecto")

tabla(
    ["#", "Pieza", "Zona", "Estado", "Dato vivo"],
    [
        ["1", "Apolo 11, etapa de descenso", "Luna", "se_quedo", "No"],
        ["2", "LRV del Apolo 17", "Luna", "se_quedo", "No"],
        ["3", "Surveyor 3", "Luna", "se_quedo", "No"],
        ["4", "Sojourner", "Marte", "en_silencio", "No"],
        ["5", "Spirit", "Marte", "en_silencio", "No"],
        ["6", "Opportunity", "Marte", "en_silencio", "No"],
        ["7", "InSight", "Marte", "en_silencio", "No"],
        ["8", "Ingenuity", "Marte", "se_quedo", "No"],
        ["9", "Voyager 1", "Espacio profundo", "activo", "Sí (-31)"],
        ["10", "Voyager 2", "Espacio profundo", "activo", "Sí (-32)"],
    ],
    anchos=[1.2, 7.0, 3.8, 3.0, 2.6],
)

h2("7.6 Cómo se escribe para 8 a 12 años")

tabla(
    ["Sí", "No"],
    [
        ["Frases cortas, una idea por frase.", "Párrafos de seis líneas."],
        ["Comparaciones cotidianas: «del tamaño de un auto».", "«Vehículo de exploración de superficie»."],
        ["Explicar el término técnico entre paréntesis.", "Suponer que el niño sabe qué es un espectrómetro."],
        ["Decir «aproximadamente» cuando el dato es aproximado.", "Inventar precisión que no existe."],
        ["Una pregunta al lector por ficha como máximo.", "Tres signos de exclamación por párrafo."],
    ],
    anchos=[8.3, 8.3],
)

caja(
    "Ejemplo real de traducción",
    "Mal: «El vehículo realizó análisis espectrométricos de la composición regolítica».\n"
    "Bien: «Es un robot del tamaño de un carrito de supermercado. Olfatea las rocas "
    "para saber de qué están hechas».",
    fondo=FONDO_OK,
    color=VERDE,
)

h2("7.7 Cómo verificar un dato")

vinetas(
    [
        "Busca la pieza en NSSDCA o en la página de misión de NASA Science.",
        "Copia el dato tal cual, sin redondear a tu gusto.",
        "Busca una segunda fuente oficial que diga lo mismo.",
        "Si las dos no coinciden, escribe el dato como aproximado o quítalo.",
        "Anota las dos URLs y la fecha en que las consultaste.",
        "Si hay una ambigüedad real, escríbela en notas_verificacion.",
    ]
)

p(
    "Wikipedia, blogs, canales de YouTube y notas de prensa NO son fuentes válidas "
    "para datos críticos. Se pueden leer para entender, pero el dato se verifica en "
    "NASA.",
    cursiva=True,
)

h2("7.8 Reglas de las imágenes")

tabla(
    ["Regla", "Detalle"],
    [
        ["Nombre", "{id}_main.jpg, todo en minúsculas, con guiones."],
        ["Formato", "JPG o WebP. No PNG gigante, no BMP."],
        ["Peso", "Menos de 300 KB. Usa Squoosh si se pasa."],
        ["Tamaño", "Unos 1200 píxeles de ancho. Que se vea bien en celular."],
        ["Crédito", "Va en la columna credito_imagen. Sin crédito no se publica."],
        ["Alt text", "Describe lo que se ve, no repitas el nombre de la pieza."],
    ],
    anchos=[4.0, 12.6],
)

h2("7.9 Checklist de una ficha terminada")

vinetas(
    [
        "La fila está completa y sin celdas obligatorias vacías.",
        "El id es único y está en minúsculas con guiones.",
        "Los cinco bloques respetan sus límites de palabras.",
        "Hay dos fuentes oficiales pegadas con URL.",
        "La imagen existe en assets/img/ con el nombre correcto.",
        "Tiene crédito y texto alternativo.",
        "Otra persona la revisó y puso su nombre en revisor.",
        "Backend confirmó «Errores: 0».",
    ]
)

h2("7.10 Errores comunes")

tabla(
    ["Error", "Por qué pasa", "Cómo se arregla"],
    [
        ["Escribir «Sí» o «No» en estado", "No es uno de los valores permitidos", "Usa activo, en_silencio, se_quedo, en_orbita o perdido"],
        ["Dejar la celda vacía", "Falta el dato y la app muestra huecos", "Investígalo; si no existe, escribe «aproximadamente» o quítalo"],
        ["Poner la ruta completa en imagen", "El script ya agrega la carpeta", "Escribe solo voyager-1_main.jpg"],
        ["Cambiar el id después de avisar", "Se rompen los enlaces y los mapas", "El id se decide una vez y no se toca"],
        ["Guardar el CSV como «CSV (delimitado por punto y coma)»", "Excel en español a veces usa ;", "El script detecta ambos, pero usa coma si puedes"],
        ["Copiar texto de una web con negritas", "Aparecen asteriscos y símbolos", "Pega como texto sin formato"],
        ["Usar una foto de Google Imágenes", "No tiene licencia clara", "Solo NASA Images o Photojournal"],
    ],
    anchos=[4.6, 5.4, 6.6],
)

# =========================================================================
# 8. BACKEND
# =========================================================================

h1("8. Equipo de backend e integraciones")

p(
    "Eres el dueño de los datos y del deploy. Tu trabajo es que la información llegue "
    "limpia al frontend, que la app nunca se caiga por una API y que main siempre "
    "funcione. También eres el merge captain: la única persona que mergea a main."
)

h2("8.1 Lo que entregas")

tabla(
    ["Entregable", "Archivo", "Cuándo"],
    [
        ["Dataset de la app", "data/artifacts.json (generado)", "Cada vez que llegan fichas"],
        ["Respaldo de datos en vivo", "data/live_snapshot.json (generado)", "Antes de cada demo"],
        ["Funciones de datos", "core/", "Bloque 1, luego se mantiene"],
        ["Pruebas que pasan", "tests/", "Siempre"],
        ["App desplegada", "URL pública", "Bloque 1 y se mantiene"],
        ["Dependencias estables", "requirements.txt", "Bloque 1 y se mantiene"],
        ["Main mergeado y funcionando", "GitHub", "Cada 4 horas"],
    ],
    anchos=[5.6, 7.0, 4.0],
)

h2("8.2 Herramientas")

tabla(
    ["Herramienta", "Para qué", "¿Obligatoria?"],
    [
        ["Python 3.12 o superior", "Correr todo", "Sí"],
        ["VS Code", "Escribir y depurar", "Sí"],
        ["Terminal de PowerShell", "Ejecutar comandos", "Sí"],
        ["Git + GitHub", "Ramas, PRs, deploy", "Sí"],
        ["Streamlit", "Framework de la app", "Sí (viene en requirements)"],
        ["requests", "Hablar con JPL Horizons", "Sí (viene en requirements)"],
        ["pytest", "Correr las pruebas", "Sí para desarrollo"],
        ["Streamlit Community Cloud", "Publicar la app", "Sí"],
        ["Navegador con DevTools", "Revisar por qué algo se ve vacío", "Sí"],
        ["Postman o el navegador", "Probar la API de Horizons a mano", "Opcional"],
        ["GitHub Desktop", "Git sin terminal", "Opcional"],
    ],
    anchos=[5.4, 7.4, 3.8],
)

h2("8.3 Los formatos que manejas")

tabla(
    ["Entra", "Sale", "Cómo"],
    [
        ["CSV de investigación", "data/artifacts.json", "scripts/fichas_a_json.py"],
        ["Respuesta de texto de Horizons", "JSON en memoria", "core/horizons.py (parseo)"],
        ["JSON en memoria", "data/live_snapshot.json", "scripts/actualizar_snapshot.py"],
        ["Piezas ya cargadas", "Diccionario para el frontend", "core/vivo.py"],
    ],
    anchos=[5.6, 5.6, 5.4],
)

caja(
    "Lo que NO usas",
    "Nada de bases de datos, Docker, FastAPI, Flask, Redis ni variables de entorno. "
    "Son 10 registros en un JSON: una base de datos solo agrega formas de fallar. "
    "Tampoco hay API keys: Horizons es abierta.",
    fondo=FONDO_AVISO,
    color=NARANJA,
)

h2("8.4 Paso a paso")

paso(
    1,
    "Prepara tu máquina",
    "Instala Python 3.12 o superior y verifica en la terminal. Instala VS Code con la "
    "extensión de Python.",
    "python --version responde 3.12 o más.",
)

codigo("python --version")

paso(
    2,
    "Clona el repositorio",
    "Baja el proyecto y entra a la carpeta.",
    "ves las carpetas core, data, docs, scripts y tests.",
)

codigo(
    'git clone https://github.com/Irvingruiz790/nasaSpace2026.git\n'
    "cd nasaSpace2026"
)

paso(
    3,
    "Crea el entorno e instala dependencias",
    "El entorno virtual evita que las librerías de otros proyectos te rompan este. Se "
    "crea una sola vez.",
    "no hay errores en rojo al final.",
)

codigo(
    "python -m venv .venv\n"
    ".\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt\n"
    ".\\.venv\\Scripts\\python.exe -m pip install -r requirements-dev.txt"
)

paso(
    4,
    "Corre las pruebas",
    "Antes de tocar nada, confirma que todo está sano. Deben pasar todas, menos una "
    "que se salta a propósito (la de red).",
    "dice algo como 40 passed, 1 skipped.",
)

codigo(".\\.venv\\Scripts\\python.exe -m pytest -q")

paso(
    5,
    "Convierte las fichas de investigación",
    "Cuando investigación avise que el CSV está listo, corre el conversor. Lee el CSV, "
    "valida contra el contrato y escribe data/artifacts.json.",
    "el reporte dice Errores: 0.",
)

codigo(".\\.venv\\Scripts\\python.exe scripts\\fichas_a_json.py")

paso(
    6,
    "Lee el reporte y devuélvelo",
    "Si hay errores, no los arregles tú: cópialos y mándalos a investigación. Cada "
    "línea dice la pieza y el campo exacto. Los avisos (por ejemplo imagen faltante) "
    "no bloquean, pero hay que resolverlos antes de la demo.",
    "investigación recibió la lista y sabe qué corregir.",
)

paso(
    7,
    "Refresca el respaldo de datos en vivo",
    "Este comando consulta JPL Horizons y guarda las distancias reales en "
    "data/live_snapshot.json. Es lo que salva la demo si el internet falla.",
    "ves la distancia en km y el tiempo de luz de Voyager 1 y 2.",
)

codigo(".\\.venv\\Scripts\\python.exe scripts\\actualizar_snapshot.py")

paso(
    8,
    "Prueba el panel con y sin internet",
    "Primero con red: debe decir status ok. Después desconecta el wifi y vuelve a "
    "abrir la app: debe mostrar el último dato guardado con su fecha, no una pantalla "
    "en blanco.",
    "la app funciona en los dos casos.",
)

paso(
    9,
    "Despliega en Streamlit Community Cloud",
    "Entra a share.streamlit.io con tu cuenta de GitHub, elige el repo, la rama main y "
    "el archivo app.py. En configuración avanzada elige Python 3.12. Copia la URL y "
    "compártela en el chat.",
    "el link abre en tu teléfono con datos móviles, no solo en tu wifi.",
)

paso(
    10,
    "Sé el merge captain",
    "Cada 4 horas: revisa los PRs abiertos, mira que la app arranque, mergea uno por "
    "uno y avisa en el chat. Si un PR rompe main, se revierte sin discusión.",
    "main está desplegada y funcionando después de cada integración.",
)

paso(
    11,
    "Cuida las dependencias",
    "Si necesitas una librería nueva, agrégala a requirements.txt con versión fija y "
    "avisa al equipo. Cada dependencia extra es una forma nueva de que el deploy "
    "falle.",
    "requirements.txt tiene versiones fijas y el deploy sigue funcionando.",
)

paso(
    12,
    "Prepara el plan B de la demo",
    "Graba un video de 2 minutos de la app funcionando y guarda capturas. El día de "
    "la demo, abre la URL 10 minutos antes: Streamlit Cloud duerme las apps sin uso y "
    "tarda en despertar.",
    "hay video de respaldo y la URL ya está despierta.",
)

h2("8.5 Tu mapa de archivos")

codigo(
    "core/\n"
    "├─ config.py      rutas, URLs, timeouts, constantes\n"
    "├─ contrato.py    enums y límites del contrato de datos\n"
    "├─ datos.py       carga y valida data/artifacts.json\n"
    "├─ formato.py     números y fechas para niños\n"
    "├─ horizons.py    cliente y parseo de JPL Horizons\n"
    "└─ vivo.py        panel en vivo con respaldo y caché\n"
    "\n"
    "scripts/\n"
    "├─ fichas_a_json.py        CSV -> data/artifacts.json\n"
    "├─ actualizar_snapshot.py  Horizons -> live_snapshot.json\n"
    "└─ generar_guia_word.py    este documento\n"
    "\n"
    "data/\n"
    "├─ artifacts.json      (generado, no editar a mano)\n"
    "└─ live_snapshot.json  (generado, no editar a mano)\n"
    "\n"
    "tests/            pytest\n"
    "requirements.txt  dependencias"
)

h2("8.6 Cómo funciona el panel en vivo (en simple)")

p(
    "El frontend pide las distancias a una función tuya. Esa función intenta tres "
    "cosas en orden:"
)

tabla(
    ["Orden", "Qué intenta", "Qué devuelve", "Qué ve el niño"],
    [
        ["1", "Preguntar a JPL Horizons", "status = ok", "El dato real, recién calculado"],
        ["2", "Leer data/live_snapshot.json", "status = stale", "El último dato guardado y hace cuánto"],
        ["3", "Nada disponible", "status = error", "«Sin dato», sin que la app se caiga"],
    ],
    anchos=[1.4, 5.5, 4.0, 5.7],
)

p(
    "La respuesta se guarda 10 minutos en memoria. Así, aunque el niño haga clic 30 "
    "veces, a JPL solo le llega una consulta."
)

h2("8.7 Errores comunes")

tabla(
    ["Error", "Causa", "Solución"],
    [
        ["«streamlit no se reconoce»", "El comando no está en el PATH", "Usa python -m streamlit run app.py"],
        ["ModuleNotFoundError: core", "Estás corriendo desde otra carpeta", "Ejecuta siempre desde la raíz del repo"],
        ["El deploy falla y en local funciona", "Ruta con mayúsculas o archivo no subido", "Linux distingue mayúsculas: revisa el nombre exacto"],
        ["Horizons tarda y la app se queda pensando", "Falta timeout", "Ya está en config.TIMEOUT_SEGUNDOS; no lo quites"],
        ["El panel dice error", "La API cambió o no hay snapshot", "Corre actualizar_snapshot.py y revisa el log"],
        ["El JSON sale con acentos raros", "Se guardó sin UTF-8", "El script ya escribe UTF-8; no lo edites en Notepad"],
        ["El CSV se lee vacío", "Excel guardó con punto y coma", "El script detecta ambos; si falla, guarda como CSV UTF-8"],
    ],
    anchos=[5.0, 5.4, 6.2],
)

h2("8.8 Checklist de cada integración")

vinetas(
    [
        "git pull y la app arranca localmente.",
        "pytest dice todo en verde.",
        "El conversor dice Errores: 0.",
        "El panel en vivo funciona con red y sin red.",
        "El deploy está actualizado con lo último de main.",
        "requirements.txt no cambió sin avisar.",
        "Los PRs revisados están mergeados o comentados.",
        "Avisé en el chat qué quedó y qué falta.",
    ]
)

# =========================================================================
# 9. FRONTEND
# =========================================================================

h1("9. Equipo de frontend")

p(
    "Ustedes son la cara del proyecto: si una pantalla no se entiende, el trabajo de "
    "los otros dos equipos no se ve. Programan en Python con Streamlit, no en React."
)

h2("9.1 Lo que entregan")

tabla(
    ["Entregable", "Archivo", "Cuándo"],
    [
        ["Pantalla de inicio", "app.py", "Bloque 1"],
        ["Mapas de las tres zonas", "pages/ y assets/maps/", "Bloques 1 y 2"],
        ["Ficha de cada pieza", "pages/ y components/", "Bloque 2"],
        ["Panel en vivo", "pages/", "Bloque 3"],
        ["Quiz", "pages/", "Bloque 4"],
        ["Estilos y accesibilidad", "assets/styles.css", "Continuo"],
        ["Página de fuentes", "pages/", "Bloque 4"],
    ],
    anchos=[5.6, 6.0, 5.0],
)

h2("9.2 Herramientas")

tabla(
    ["Herramienta", "Para qué"],
    [
        ["Python + Streamlit", "Escribir la app (Streamlit ya viene en requirements)"],
        ["VS Code", "Editor de código"],
        ["Figma o Excalidraw", "Dibujar el wireframe antes de programar"],
        ["Chrome o Edge con DevTools", "Ver la app como en un celular (modo dispositivo)"],
        ["Inkscape o Photopea", "Preparar las imágenes de fondo de los mapas"],
        ["Google Fonts", "Tipografía legible para niños (Nunito, Fredoka)"],
        ["Squoosh", "Comprimir imágenes de fondo"],
        ["WebAIM Contrast Checker", "Verificar que el texto se lea bien"],
    ],
    anchos=[5.6, 11.0],
)

h2("9.3 Formatos")

tabla(
    ["Formato", "Para qué", "Dónde"],
    [
        ["Python (.py)", "Cada pantalla y cada componente", "app.py, pages/, components/"],
        ["CSS", "Colores, tipografía, tarjetas, badges", "assets/styles.css"],
        ["JSON", "Posiciones x/y de los marcadores en cada mapa", "assets/maps/posiciones.json"],
        ["JPG o WebP", "Fondos de mapas e imágenes", "assets/maps/ y assets/img/"],
    ],
    anchos=[3.4, 7.2, 6.0],
)

h2("9.4 Paso a paso")

paso(
    1,
    "Dibuja antes de programar",
    "En papel, Figma o Excalidraw dibuja tres pantallas: inicio, mapa y ficha. Diez "
    "minutos de dibujo ahorran dos horas de código.",
    "puedes mostrar el dibujo y alguien entiende el recorrido.",
)

paso(
    2,
    "Prepara el entorno",
    "Es el mismo del backend. Si ya lo hicieron, sigan con el paso 3.",
    "streamlit --version responde.",
)

codigo(
    "python -m venv .venv\n"
    ".\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt\n"
    ".\\.venv\\Scripts\\python.exe -m streamlit run app.py"
)

paso(
    3,
    "Crea app.py",
    "Es la portada. Tres líneas de configuración, un título y un botón para entrar. "
    "No pongas lógica de datos aquí.",
    "la app abre en localhost:8501 y se ve el título.",
)

codigo(
    "import streamlit as st\n"
    "\n"
    'st.set_page_config(page_title="¿Dónde está ahora?", page_icon="🚀", layout="wide")\n'
    'st.title("¿Dónde está ahora?")\n'
    'st.write("Un viaje por las máquinas que la NASA dejó en el espacio.")'
)

paso(
    4,
    "Crea las páginas",
    "Una pantalla por archivo dentro de pages/: 1_Luna.py, 2_Marte.py, "
    "3_Espacio_profundo.py, 4_En_vivo.py, 5_Quiz.py, 6_Fuentes.py y 7_Ficha.py. "
    "Streamlit arma el menú solo.",
    "puedes navegar entre todas sin callejones sin salida.",
)

paso(
    5,
    "Carga los datos con core",
    "Nunca abras el JSON a mano. Usa las funciones del backend. Si un campo falta, la "
    "función te lo dice en vez de romperse.",
    "las tres piezas de ejemplo aparecen en pantalla.",
)

codigo(
    "import streamlit as st\n"
    "from core import datos\n"
    "\n"
    "@st.cache_data\n"
    "def piezas():\n"
    "    return datos.cargar_piezas()\n"
    "\n"
    'st.write(f"Tenemos {len(piezas())} piezas")'
)

paso(
    6,
    "Haz el componente de tarjeta",
    "Una tarjeta muestra imagen, nombre, apodo, zona y estado con color. Se reutiliza "
    "en el inicio, en los mapas y en las fichas.",
    "cambias un dato en el CSV y la tarjeta se actualiza sola.",
)

paso(
    7,
    "Dibuja los mapas",
    "Una imagen de fondo dentro de un contenedor, y encima botones posicionados con "
    "porcentajes. Las posiciones van en assets/maps/posiciones.json, no en el código.",
    "al hacer clic en un marcador se abre la ficha correcta.",
)

caja(
    "No uses st.map ni Leaflet",
    "Esos mapas son para la Tierra: usan latitud y longitud terrestres. La Luna y "
    "Marte se dibujan con una imagen de fondo y marcadores encima, ubicados a ojo con "
    "porcentajes.",
    fondo=FONDO_AVISO,
    color=NARANJA,
)

paso(
    8,
    "Arma el panel en vivo",
    "Pide los datos a core.vivo y muéstralos con core.formato. Si el estado es stale, "
    "muestra el aviso de fecha. Si es error, muestra «sin dato».",
    "funciona con internet y sin internet.",
)

codigo(
    "from core import vivo, formato\n"
    "\n"
    "panel = vivo.datos_en_vivo(piezas())\n"
    'v1 = vivo.objeto(panel, "voyager-1")\n'
    "\n"
    'st.metric("Distancia", formato.distancia_texto(v1["distance_km"]))\n'
    'st.metric("Tiempo de la señal", formato.tiempo_luz_texto(v1["light_time_s"]))\n'
    "\n"
    "aviso = vivo.aviso_panel(panel)\n"
    "if aviso:\n"
    "    st.info(aviso)"
)

paso(
    9,
    "Estilos y accesibilidad",
    "Un solo archivo de CSS con variables de color. Texto mínimo de 16 px, contraste "
    "alto, foco visible y alt text en todas las imágenes.",
    "se lee en un celular sin hacer zoom.",
)

paso(
    10,
    "Prueba como un niño",
    "Pídele a alguien de 10 años que use la app sin explicarle nada. Anota dónde se "
    "pierde. Eso vale más que cualquier opinión del equipo.",
    "el niño llega solo hasta una ficha y entiende qué está viendo.",
)

h2("9.5 Reglas del frontend")

vinetas(
    [
        "No leas data/*.json a mano: usa core.datos y core.vivo.",
        "No importes requests: la red es del backend.",
        "No cambies nombres de campos ni de imágenes.",
        "No agregues librerías sin avisar a backend.",
        "No uses CSS por CDN: si se cae el internet, la app se ve rota.",
        "No dejes una pantalla en blanco: siempre un mensaje claro.",
    ]
)

h2("9.6 Checklist de cada pantalla")

vinetas(
    [
        "Se entiende sin explicación de un adulto.",
        "Funciona en celular (390 px de ancho).",
        "No hay imágenes rotas ni textos «None».",
        "Todos los botones llevan a algún lado o hacen algo.",
        "El estado vacío tiene un mensaje amable.",
        "Se puede navegar con Tab y el foco se ve.",
    ]
)

# =========================================================================
# 10. INTEGRACIÓN
# =========================================================================

h1("10. El ritual de integración (cada 4 horas)")

p(
    "Cada 4 horas, el equipo se detiene 30 minutos. No se programa nada nuevo en ese "
    "rato: solo se junta, se prueba y se avisa. Esto es lo que evita descubrir un "
    "problema a la hora 43."
)

tabla(
    ["#", "Quién", "Qué hace"],
    [
        ["1", "Todos", "Suben su rama y abren el PR con el nombre de la tarea."],
        ["2", "Backend", "Revisa los PRs, uno por uno, y mergea solo lo que funciona."],
        ["3", "Todos", "Hacen git pull y prueban la app completa en su máquina."],
        ["4", "Backend", "Verifica el deploy y que la URL esté actualizada."],
        ["5", "Investigación", "Revisa que sus fichas se vean bien en pantalla."],
        ["6", "Todos", "Dicen en el chat: qué quedó, qué falta y qué está bloqueado."],
    ],
    anchos=[1.2, 3.4, 12.0],
)

h2("Formato del mensaje de integración")

caja(
    "Copia y pega esto en el chat",
    "Integración #3 — hora 12\n"
    "Quedó: mapa de la Luna con 3 marcadores\n"
    "Falta: ficha de Opportunity, imagen de Spirit\n"
    "Bloqueado: necesito el id definitivo de InSight\n"
    "La app: funciona / no funciona",
    fondo=FONDO_SUAVE,
    color=AZUL_MEDIO,
)

# =========================================================================
# 11. CRONOGRAMA
# =========================================================================

h1("11. Cronograma de 44 horas")

tabla(
    ["Horas", "Investigación", "Backend", "Frontend", "Hito"],
    [
        ["0–4", "Roster y 2 fichas", "Repo, deploy, conversor", "Wireframe y app.py", "App vacía desplegada"],
        ["4–8", "4 fichas + imágenes", "Dataset y pruebas", "Inicio y tarjetas", "Se ven 3 piezas"],
        ["8–12", "3 fichas más", "Panel en vivo y respaldo", "Mapa de la Luna", "Gate 1"],
        ["12–16", "Últimas fichas", "Formato y snapshot", "Mapa de Marte", "6 fichas"],
        ["16–20", "Verificación de fuentes", "Pruebas y fixes", "Espacio profundo", "Gate 2"],
        ["20–26", "Revisión cruzada", "Deploy estable", "Quiz y responsive", "Demo interna 1"],
        ["26–32", "Ajustes de tono", "Optimización", "Accesibilidad y fuentes", "Feature complete"],
        ["32–38", "Pitch y video", "Code freeze y QA", "QA visual", "Code freeze"],
        ["38–44", "Ensayo", "Soporte", "Ensayo", "Entrega"],
    ],
    anchos=[1.8, 3.8, 3.8, 3.8, 3.4],
)

caja(
    "Ruta crítica",
    "El contenido es lo primero que se atrasa y lo último que se recupera. Si "
    "investigación se atrasa, backend y frontend deben seguir con las piezas de "
    "ejemplo: nunca esperar con las manos cruzadas.",
    fondo=FONDO_AVISO,
    color=NARANJA,
)

# =========================================================================
# 12. PROBLEMAS
# =========================================================================

h1("12. Qué hacer si…")

tabla(
    ["Situación", "Qué se hace"],
    [
        ["La API de Horizons no responde", "La app usa live_snapshot.json automáticamente. No se toca nada. Backend avisa que está en respaldo."],
        ["El deploy está roto", "Backend revisa el log en Streamlit Cloud, compara requisitos y hace rollback al último commit bueno."],
        ["Hay conflicto de merge", "Se resuelve el dueño del archivo, no quien llegó último. Nunca «accept both» a ciegas."],
        ["El contenido llega tarde", "Frontend usa las 3 piezas de ejemplo. Backend ayuda a verificar datos."],
        ["Alguien tocó un archivo ajeno", "Se avisa en el chat y se revierte ese cambio. No se discute en el PR."],
        ["Se acabó el tiempo y falta una función", "Se quita del menú y se deja el resto estable. Una app que funciona vale más que una llena de botones rotos."],
        ["No entiendo un error", "Pega el mensaje completo en el chat con: qué hacías, qué archivo y qué ya probaste."],
        ["Dos personas editaron lo mismo", "Se queda la versión del dueño del archivo y se reintegra lo del otro a mano."],
    ],
    anchos=[5.4, 11.2],
)

h2("Cómo pedir ayuda (para que te respondan rápido)")

codigo(
    "Estoy en la tarea: [nombre]\n"
    "Archivo: [ruta]\n"
    "Quería: [qué intentaba hacer]\n"
    "Pasó: [mensaje de error completo]\n"
    "Ya probé: [qué intentaste]"
)

# =========================================================================
# 13. CHECKLIST FINAL
# =========================================================================

h1("13. Checklist final antes de la demo")

vinetas(
    [
        "La URL abre en un teléfono con datos móviles, no solo en el wifi del lugar.",
        "La URL se abrió 10 minutos antes (Streamlit Cloud duerme las apps).",
        "Las 10 fichas cargan y ninguna tiene imagen rota.",
        "Los tres mapas son clickeables y llevan a la ficha correcta.",
        "El panel en vivo muestra datos o el respaldo con fecha.",
        "El quiz se puede jugar de principio a fin.",
        "La página de fuentes lista todas las fuentes.",
        "Ningún texto dice «None», «NaN» ni «sin datos» donde debería haber información.",
        "Se ve bien en un celular de 390 px.",
        "Hay video de respaldo descargado en el equipo, no solo en la nube.",
        "El pitch dura menos de 2 minutos y ya se ensayó dos veces.",
        "Todos saben responder: «¿de dónde salió ese dato?».",
    ]
)

# =========================================================================
# ANEXOS
# =========================================================================

h1("Anexo A. Comandos que van a usar, explicados")

h2("Git (los tres equipos)")

tabla(
    ["Comando", "Qué hace", "Cuándo lo usas"],
    [
        ["git status", "Muestra qué archivos cambiaste", "Antes de guardar, siempre"],
        ["git add .", "Prepara todos tus cambios", "Antes del commit"],
        ["git commit -m \"...\"", "Guarda la foto con un mensaje", "Al terminar un avance"],
        ["git pull --rebase origin main", "Trae lo nuevo sin crear un merge raro", "Antes de subir"],
        ["git push -u origin mi-rama", "Sube tu rama a GitHub", "Al terminar la tarea"],
        ["git log --oneline -5", "Ver los últimos commits", "Cuando algo se rompió y no sabes cuándo"],
    ],
    anchos=[6.2, 6.2, 4.2],
)

h2("Backend: los seis comandos del día a día")

codigo(
    "# 1. Actualizar el repo\n"
    "git pull --rebase origin main\n"
    "\n"
    "# 2. Correr pruebas\n"
    ".\\.venv\\Scripts\\python.exe -m pytest -q\n"
    "\n"
    "# 3. Convertir fichas\n"
    ".\\.venv\\Scripts\\python.exe scripts\\fichas_a_json.py\n"
    "\n"
    "# 4. Refrescar respaldo\n"
    ".\\.venv\\Scripts\\python.exe scripts\\actualizar_snapshot.py\n"
    "\n"
    "# 5. Correr la app\n"
    ".\\.venv\\Scripts\\python.exe -m streamlit run app.py\n"
    "\n"
    "# 6. Regenerar esta guía si cambia el plan\n"
    ".\\.venv\\Scripts\\python.exe scripts\\generar_guia_word.py"
)

h2("Investigación: no necesitas comandos")

p(
    "Todo tu trabajo pasa por Excel o Google Sheets y por la carpeta assets/img/. Si "
    "necesitas subir algo a GitHub y no sabes cómo, pídele a backend que lo suba por "
    "ti. No es vergüenza: es división de trabajo."
)

h1("Anexo B. Dónde está cada cosa")

tabla(
    ["Necesito…", "Está en…"],
    [
        ["Llenar una ficha", "contenido/fichas.csv"],
        ["Guardar una imagen", "assets/img/{id}_main.jpg"],
        ["Ver el contrato de datos completo", "docs/CONTRATO_DATOS.md"],
        ["Ver un ejemplo de ficha escrita", "contenido/fichas.csv (las 3 primeras filas)"],
        ["Entender las funciones de datos", "core/README.md"],
        ["Saber qué va en cada carpeta", "README.md de esa carpeta"],
        ["Ver los datos que usa la app", "data/artifacts.json (generado, no editar)"],
        ["Registrar una decisión del equipo", "docs/DECISIONES.md"],
        ["Preparar el pitch", "docs/PITCH.md"],
        ["Ver las fuentes oficiales", "docs/FUENTES.md"],
    ],
    anchos=[7.6, 9.0],
)

h1("Anexo C. Enlaces oficiales")

tabla(
    ["Recurso", "Enlace"],
    [
        ["Reto de Space Apps", "spaceappschallenge.org/2026/challenges/nasas-discarded-equipment-storytelling/"],
        ["NSSDCA (catálogo de naves)", "nssdc.gsfc.nasa.gov/nmc/"],
        ["NASA Science (misiones)", "science.nasa.gov/science-missions/"],
        ["NASA Images", "images.nasa.gov"],
        ["JPL Horizons", "ssd.jpl.nasa.gov/horizons/"],
        ["NASA Space Place (en español)", "spaceplace.nasa.gov/sp/"],
        ["Streamlit (documentación)", "docs.streamlit.io"],
        ["Streamlit Community Cloud", "share.streamlit.io"],
        ["GitHub del equipo", "github.com/Irvingruiz790/nasaSpace2026"],
    ],
    anchos=[5.6, 11.0],
)

cierre = doc.add_paragraph()
cierre.paragraph_format.space_before = Pt(24)
run = cierre.add_run(
    "Si algo de esta guía no se entiende, avísale a backend para corregirla. "
    "Una guía que nadie entiende no sirve."
)
run.italic = True
run.font.color.rgb = RGBColor.from_string(GRIS)

# --- Propiedades y guardado -------------------------------------------------

doc.core_properties.title = "¿Dónde está ahora? — Guía de trabajo del equipo"
doc.core_properties.subject = "NASA Space Apps Challenge 2026"
doc.core_properties.author = "Equipo ¿Dónde está ahora?"
doc.core_properties.language = "es-MX"

SALIDA.parent.mkdir(parents=True, exist_ok=True)
doc.save(SALIDA)
print(f"Documento generado: {SALIDA}")
print(f"Párrafos: {len(doc.paragraphs)} | Tablas: {len(doc.tables)}")
