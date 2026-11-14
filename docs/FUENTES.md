# Registro de fuentes y verificación

**Dueño:** Contenido y datos (CD).  
**Regla:** cada dato crítico necesita dos fuentes oficiales.  
**Fecha de consulta base:** 14 de noviembre de 2026.

---

## 1. Fuentes primarias

| Fuente | Qué aporta | Enlace |
|---|---|---|
| NSSDCA Master Catalog | Catálogo de naves, coordenadas, masa, estado final | https://nssdc.gsfc.nasa.gov/nmc/ |
| NSSDCA — búsqueda de naves | Localizar una pieza por nombre o ID | https://nssdc.gsfc.nasa.gov/nmc/SpacecraftQuery.jsp |
| NASA Science — misiones | Fichas narrativas, descubrimientos y estado | https://science.nasa.gov/science-missions/ |
| NASA Science — Voyager | Distancias, tiempo luz y estado de instrumentos | https://science.nasa.gov/mission/voyager/where-are-voyager-1-and-voyager-2-now/ |
| JPL Horizons | Posiciones y distancias de naves | https://ssd.jpl.nasa.gov/horizons/ |
| Horizons API | Consulta programática | https://ssd-api.jpl.nasa.gov/doc/horizons.html |
| DSN Now | Comunicación en vivo (best-effort) | https://eyes.nasa.gov/apps/dsn-now/dsn.html |
| NASA Images API | Imágenes y metadatos | https://images-api.nasa.gov/ |
| NASA Photojournal | Imágenes con pies de foto técnicos | https://photojournal.jpl.nasa.gov/ |
| NASA Space Place | Lenguaje para niños | https://spaceplace.nasa.gov/sp/ |
| NASA en Español | Noticias y contexto en español | https://www.nasa.gov/es/ |

---

## 2. Protocolo de verificación

Para cada ficha:

1. **Identificar la pieza** en NSSDCA o en la página de misión de NASA.
2. **Copiar los datos críticos:** nombre, tipo, misión, lanzamiento, coordenadas o ubicación, estado, última señal.
3. **Buscar una segunda fuente oficial** para los datos críticos.
4. **Registrar URL y fecha de consulta** en la tabla de abajo.
5. **Marcar ambigüedades** en `notas_verificacion` (por ejemplo, "el destino de la etapa de ascenso es incierto").
6. **Revisión cruzada:** otra persona del equipo lee la ficha y compara con las fuentes.
7. **Imagen:** descargar de NASA Images o Photojournal, registrar crédito y escribir alt text.

### Reglas de oro

- Si un dato no tiene dos fuentes, se escribe como "aproximadamente" o se elimina.
- No se usan citas virales sin verificar.
- No se inventan diálogos ni emociones que contradigan la ciencia.
- Las distancias se muestran como aproximaciones y con fecha.
- Las imágenes deben tener crédito visible.

---

## 3. Bitácora por pieza

| ID | Pieza | Fuente 1 | Fuente 2 | Imagen / crédito | Revisor | Fecha | Notas |
|---|---|---|---|---|---|---|---|
| `apollo-11-lm` | Módulo Lunar Eagle | NSSDCA 1969-059C | NSSDCA Apollo 11 | NASA | | | Destino de la etapa de ascenso incierto |
| `apollo-17-lrv` | LRV del Apolo 17 | NSSDCA | NASA Science | NASA | | | |
| `surveyor-3` | Surveyor 3 | NASA Science | NSSDCA | NASA | | | |
| `sojourner` | Sojourner | NASA Pathfinder | NSSDCA | NASA/JPL | | | |
| `spirit` | Spirit | NASA Science | NSSDCA | NASA/JPL-Caltech | | | |
| `opportunity` | Opportunity | NASA Science | NSSDCA | NASA/JPL-Caltech | | | |
| `insight` | InSight | NASA Science | NSSDCA | NASA/JPL-Caltech | | | |
| `ingenuity` | Ingenuity | NASA Science | NSSDCA | NASA/JPL-Caltech | | | |
| `voyager-1` | Voyager 1 | NASA Voyager | JPL Horizons | NASA/JPL-Caltech | | | `horizons_id = -31` |
| `voyager-2` | Voyager 2 | NASA Voyager | JPL Horizons | NASA/JPL-Caltech | | | Verificar ID en Horizons |

---

## 4. Créditos de imágenes

| Archivo | Pieza | Crédito | URL de origen |
|---|---|---|---|
| `apollo-11-lm_main.jpg` | Apolo 11 | NASA | pendiente |
| `apollo-17-lrv_main.jpg` | LRV Apolo 17 | NASA | pendiente |
| `surveyor-3_main.jpg` | Surveyor 3 | NASA | pendiente |
| `sojourner_main.jpg` | Sojourner | NASA/JPL | pendiente |
| `spirit_main.jpg` | Spirit | NASA/JPL-Caltech | pendiente |
| `opportunity_main.jpg` | Opportunity | NASA/JPL-Caltech | pendiente |
| `insight_main.jpg` | InSight | NASA/JPL-Caltech | pendiente |
| `ingenuity_main.jpg` | Ingenuity | NASA/JPL-Caltech | pendiente |
| `voyager-1_main.jpg` | Voyager 1 | NASA/JPL-Caltech | pendiente |
| `voyager-2_main.jpg` | Voyager 2 | NASA/JPL-Caltech | pendiente |

---

## 5. Cambios

| Fecha | Cambio | Autor |
|---|---|---|
| 2026-11-14 | Creación del registro | Equipo |
