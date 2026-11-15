# Registro de decisiones

**Regla:** toda decisión que afecte a más de una persona se anota aquí. Si no está aquí, no existe.

| Fecha | Decisión | Dueño | Alternativas consideradas | Razón |
|---|---|---|---|---|
| 2026-11-14 | Público objetivo: 8–12 años | CD | 6–8, 12–15, público general | Es la edad con más curiosidad y capacidad de lectura autónoma |
| 2026-11-14 | Stack: Streamlit | BE | Flask, HTML/CSS/JS, Java | Prioridad: terminar y desplegar rápido con lo que ya saben |
| 2026-11-14 | 10 piezas en el MVP | CD | 6, 14, 20 | Permite profundidad narrativa sin sacrificar cobertura |
| 2026-11-14 | Tres zonas: Luna, Marte, espacio profundo | CD | Solo Luna, solo Marte | Cubre el brief completo y da un recorrido narrativo |
| 2026-11-14 | Datos estáticos + live con respaldo | BE | Solo estático, solo live | El live es el gancho; el estático garantiza la demo |
| 2026-11-14 | Taxonomía de 5 estados | CD | 3 estados, 8 estados | Simple para niños, suficiente para contar historias |
| 2026-11-14 | Un dueño por archivo | Todos | Todos editan todo | Evita conflictos de merge |
| 2026-11-14 | BE es merge captain | Todos | Rotativo | Una sola persona controla la integración |
| 2026-11-14 | Code freeze en T+38 | Todos | T+42 | Deja 6 horas para ensayo y entrega |
| 2026-11-14 | Cierre del pitch: hito de un día luz de Voyager 1 | CD | Cierre genérico | Es un evento real y cercano (18 nov 2026) |
| 2026-11-14 | Investigación llena `contenido/fichas.csv` y backend genera `data/artifacts.json` | BE + CD | Investigación escribe el JSON a mano | Evita errores de sintaxis en un equipo sin experiencia técnica |
| 2026-11-14 | Una guía única en Word (`docs/Guia_Equipo.docx`) como documento de trabajo diario | Todos | Los ocho documentos de `docs/` por separado | El equipo se perdía entre documentos; la guía tiene un paso a paso por rol |
| 2026-11-14 | Paleta oficial de NASA Space Apps en tema oscuro: Deep Blue `#07173F` de fondo, Electric `#0042A6` y Neon Blue `#0960E1` en bloques, Neon Yellow `#EAFE07` solo como acento | FE | Paleta clara actual; azules inventados | Es la identidad documentada en la Brand Guide (jun 2026) y el amarillo como acento respeta la regla 60-30-10 |
| 2026-11-14 | Tipografía Exo 2 (títulos) + Overpass (texto), empaquetadas en `static/fonts/` | FE | Fira Sans oficial; Orbitron; Alvaro Wide | Exo 2 da el aire espacial que pidió el equipo, Overpass mantiene legibilidad y las dos son OFL; «Alvaro Wide» no existe y «Alvaro» es solo uso personal |
| 2026-11-14 | Las fuentes se sirven desde `static/` con `server.enableStaticServing`, no desde un CDN | FE + BE | Google Fonts por URL | Streamlit solo publica `./static`; sin red la app debe verse igual |
| 2026-11-14 | Encabezado «Menú» y encabezados temáticos por sección con CSS propio | FE | Fotos de fondo por sección | La guía de marca pide no poner texto encima de fotografías; el patrón de estrellas es CSS y pesa 0 KB |
| 2026-11-14 | Sin 3D real (WebGL/Three.js) por ahora | FE | Three.js o componente propio | Pesaría más de 600 KB, rompe «sin librerías nuevas» y castiga el celular; se prefieren esferas y fondos con CSS |

---

## Cómo agregar una decisión

1. Escribe la fecha.
2. Describe la decisión en una frase.
3. Indica quién es el dueño.
4. Anota al menos una alternativa que se descartó.
5. Explica la razón en una frase.

Si la decisión cambia el contrato de datos, actualiza también [CONTRATO_DATOS.md](CONTRATO_DATOS.md).
