# ¿Dónde está ahora?
### Postales desde los objetos que dejamos en el espacio

Una experiencia interactiva para que niños y niñas de 8 a 12 años descubran qué pasó con el hardware que la NASA dejó en la Luna, en Marte y en el espacio profundo.

**Estado:** en desarrollo — NASA Space Apps Challenge 2026  
**Demo:** [pendiente de deploy]  
**Video:** [pendiente]  
**Reto:** [Abandoned but not Forgotten — NASA Space Apps Challenge 2026](https://www.spaceappschallenge.org/2026/challenges/nasas-discarded-equipment-storytelling/)

**Documentación del equipo:**
- [Plan de tareas por equipo](docs/TAREAS.md)
- [Contrato de datos](docs/CONTRATO_DATOS.md)
- [Plantilla de fichas](docs/PLANTILLA_FICHAS.md)
- [Registro de fuentes](docs/FUENTES.md)

---

## El reto

Durante más de 50 años, la humanidad ha dejado máquinas en la Luna, en Marte y en el espacio profundo. Muchas terminaron su misión y siguen ahí, en silencio. Otras todavía nos hablan.

Este proyecto responde al desafío de contar esa historia a un público escolar: qué es cada pieza, por qué se envió, qué descubrió y dónde está ahora.

---

## ¿Qué hace la app?

- **Mapa en tres zonas:** Luna, Marte y espacio profundo, con marcadores clickeables.
- **10 fichas narrativas:** cada pieza tiene su historia en cinco bloques, imagen, estado y fuentes.
- **Odómetro en vivo:** distancia y tiempo de señal de las naves de espacio profundo, con respaldo si la API falla.
- **Quiz:** un juego rápido para adivinar "¿quién soy?".
- **Página de fuentes:** transparencia total sobre de dónde salió cada dato.

---

## Capturas

| Inicio | Mapa | Ficha |
|---|---|---|
| [captura pendiente] | [captura pendiente] | [captura pendiente] |

---

## Cómo funciona

```
[Fuentes oficiales] ──► [Dataset curado] ──┐
[APIs en vivo] ───────► [Servicios + caché + respaldo] ──► [App Streamlit] ──► [Navegador]
[Imágenes] ───────────► [Assets locales + créditos] ──────┘
```

- **Datos estáticos:** `data/artifacts.json` con las 10 piezas, verificado contra fuentes oficiales.
- **Datos en vivo:** JPL Horizons para distancias; DSN Now como extra.
- **Respaldo:** si una API falla, la app usa `data/live_snapshot.json` y muestra la fecha de actualización.
- **Frontend:** Streamlit con mapas de fondo y marcadores superpuestos; diseño legible y responsive.

El detalle de los campos está en [docs/CONTRATO_DATOS.md](docs/CONTRATO_DATOS.md).

---

## Datos y fuentes

| Fuente | Uso | Enlace |
|---|---|---|
| NSSDCA Master Catalog | Catálogo, coordenadas y estado final | https://nssdc.gsfc.nasa.gov/nmc/ |
| NASA Science | Fichas de misión y descubrimientos | https://science.nasa.gov/science-missions/ |
| JPL Horizons | Posiciones y distancias | https://ssd.jpl.nasa.gov/horizons/ |
| Horizons API | Datos en vivo | https://ssd-api.jpl.nasa.gov/doc/horizons.html |
| DSN Now | Comunicación en vivo (best-effort) | https://eyes.nasa.gov/apps/dsn-now/dsn.html |
| NASA Images | Imágenes y metadatos | https://images.nasa.gov/ |
| NASA Photojournal | Imágenes con pies de foto técnicos | https://photojournal.jpl.nasa.gov/ |
| NASA Space Place | Lenguaje para niños | https://spaceplace.nasa.gov/sp/ |

**Fecha de consulta de las fuentes:** 14 de noviembre de 2026.

---

## Rigor y verificación

- Cada dato crítico tiene al menos dos fuentes oficiales.
- Las coordenadas de la Luna y Marte provienen de NSSDCA y de las páginas de misión de NASA.
- Las distancias de espacio profundo se calculan con JPL Horizons y se muestran como aproximaciones.
- Las imágenes son de NASA y llevan crédito.
- No se usan citas virales sin verificar.
- Las fichas se revisan por una segunda persona antes de publicarse.

El protocolo completo está en [docs/FUENTES.md](docs/FUENTES.md).

---

## Estructura del repositorio

```
nasaSpace2026/
├─ app.py                  # entrada de Streamlit (FE1)
├─ pages/                  # pantallas (FE2)
├─ components/             # tarjetas, badges (FE1)
├─ maps/                   # mapas y marcadores (FE2)
├─ core/                   # datos, APIs, caché, respaldo (BE)
├─ data/
│  ├─ artifacts.json       # dataset curado (CD)
│  ├─ live_snapshot.json   # respaldo de datos en vivo (BE)
│  └─ sources.json         # registro de fuentes (CD)
├─ assets/
│  ├─ img/                 # imágenes con créditos (CD)
│  ├─ maps/                # imágenes base de mapas (FE2)
│  └─ styles.css           # sistema visual (FE1)
├─ docs/
│  ├─ TAREAS.md
│  ├─ CONTRATO_DATOS.md
│  ├─ PLANTILLA_FICHAS.md
│  ├─ FUENTES.md
│  ├─ DECISIONES.md
│  └─ PITCH.md
├─ tests/
└─ requirements.txt        # dependencias (BE)
```

---

## Cómo ejecutarlo localmente

Requisitos: Python 3.10 o superior.

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

La app se abre en `http://localhost:8501`.

> `requirements.txt` y `app.py` los crea BE/FE1 en el primer bloque de trabajo. Si todavía no existen, el repo está en la fase de esqueleto.

---

## Equipo

| Rol | Responsabilidad |
|---|---|
| Frontend 1 | Sistema visual, inicio, fichas, accesibilidad |
| Frontend 2 | Mapas, navegación, panel en vivo, quiz |
| Backend e integraciones | Datos, APIs, caché, respaldo, deploy |
| Contenido y datos | Fichas, fuentes, imágenes, verificación |

Los detalles de tareas y dueños de archivos están en [docs/TAREAS.md](docs/TAREAS.md).

---

## Plan de trabajo

El proyecto se desarrolla en bloques de 44 horas con integraciones cada 4 horas. La regla principal es que `main` siempre esté desplegable y que cada archivo tenga un solo dueño.

Ver [docs/TAREAS.md](docs/TAREAS.md).

---

## Limitaciones y trabajo futuro

- No es una herramienta de navegación ni una fuente de datos en tiempo real certificada.
- Las distancias de naves muy lejanas son aproximaciones basadas en modelos de JPL.
- Algunas piezas no tienen posición "en vivo" porque están fijas en la Luna o en Marte.
- Próximos pasos: sumar más piezas, narración en audio, versión en inglés y un modo docente.

---

## Créditos de imágenes

Las imágenes pertenecen a NASA, JPL-Caltech u otras instituciones, según se indica en cada ficha. Se usan con fines educativos y se respeta la política de uso de imágenes de NASA.

---

## Licencia

- Código: MIT.
- Contenido original: CC BY 4.0.
- Imágenes: según la política de uso de NASA y los créditos indicados.

---

## Agradecimientos

- NASA Space Apps Challenge.
- JPL Solar System Dynamics por Horizons.
- NASA Space Place por el lenguaje accesible.
- A los niños y niñas que probaron la app y nos dijeron qué no se entendía.

> Este es un proyecto de hackatón. No está afiliado a NASA.
