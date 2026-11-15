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
| `apollo-11-lm` | Módulo Lunar Eagle | NSSDCA 1969-059C | NSSDCA Apollo 11 | NASA | Eduardo | 2026-11-14 | Destino de la etapa de ascenso incierto |
| `apollo-17-lrv` | LRV del Apolo 17 | NSSDCA | NASA Science | NASA | Eduardo | 2026-11-14 | |
| `surveyor-3` | Surveyor 3 | NASA Science | NSSDCA | NASA | Eduardo | 2026-11-14 | |
| `sojourner` | Sojourner | NASA Pathfinder | NSSDCA | NASA/JPL-Caltech | Eduardo | 2026-11-14 | |
| `spirit` | Spirit | NASA Science | NSSDCA | NASA/JPL-Caltech | Eduardo | 2026-11-14 | |
| `opportunity` | Opportunity | NASA Science | NSSDCA 2003-032A | NASA/JPL-Caltech/Cornell/Arizona State | Eduardo | 2026-11-14 | Imagen PIA18079 |
| `insight` | InSight | NASA Science | NSSDCA | NASA/JPL-Caltech | Eduardo | 2026-11-14 | |
| `ingenuity` | Ingenuity | NASA Science | NSSDCA 2020-052A | NASA/JPL-Caltech | Eduardo | 2026-11-14 | Imagen PIA23720 |
| `voyager-1` | Voyager 1 | NASA Voyager | JPL Horizons | NASA/JPL-Caltech | Eduardo | 2026-11-14 | `horizons_id = -31` |
| `voyager-2` | Voyager 2 | NASA Voyager | JPL Horizons | NASA/JPL-Caltech | Eduardo | 2026-11-14 | `horizons_id = -32` |

---

## 4. Créditos de imágenes

| Archivo | Pieza | Crédito | URL de origen |
|---|---|---|---|
| `apollo-11-lm_main.jpg` | Apolo 11 | NASA | https://nssdc.gsfc.nasa.gov/planetary/image/ap11_lm_as11_40_5927.jpg |
| `apollo-17-lrv_main.jpg` | LRV Apolo 17 | NASA | https://nssdc.gsfc.nasa.gov/planetary/image/as17_147_22526.jpg |
| `surveyor-3_main.jpg` | Surveyor 3 | NASA | https://nssdc.gsfc.nasa.gov/imgcat/higher_res/apollo/as12_48_7133.jpg |
| `sojourner_main.jpg` | Sojourner | NASA/JPL-Caltech | https://nssdc.gsfc.nasa.gov/image/hi-res/spacecraft/mpath_sojourner_pia01122.tiff |
| `spirit_main.jpg` | Spirit | NASA/JPL-Caltech | https://nssdc.gsfc.nasa.gov/planetary/image/mer_2003.jpg |
| `opportunity_main.jpg` | Opportunity | NASA/JPL-Caltech/Cornell Univ./Arizona State Univ. | https://images-assets.nasa.gov/image/PIA18079/PIA18079~orig.jpg |
| `insight_main.jpg` | InSight | NASA/JPL-Caltech | https://nssdc.gsfc.nasa.gov/planetary/image/insight.jpg |
| `ingenuity_main.jpg` | Ingenuity | NASA/JPL-Caltech | https://images-assets.nasa.gov/image/PIA23720/PIA23720~orig.jpg |
| `voyager-1_main.jpg` | Voyager 1 | NASA/JPL-Caltech | https://nssdc.gsfc.nasa.gov/image/spacecraft/voyager.jpg |
| `voyager-2_main.jpg` | Voyager 2 | NASA/JPL-Caltech | https://nssdc.gsfc.nasa.gov/image/spacecraft/voyager2.jpg |

Los fondos de los mapas también salen de NSSDCA. Su origen y tratamiento
están documentados en `assets/maps/README.md`.

---

## 5. Cambios

| Fecha | Cambio | Autor |
|---|---|---|
| 2026-11-14 | Creación del registro | Equipo |
| 2026-11-14 | Revisión cruzada de las 10 fichas, segundas fuentes de Opportunity e Ingenuity y URLs de créditos | Eduardo |
