# Plan de trabajo y tareas por equipo

**Proyecto:** ¿Dónde está ahora?  
**Repo:** https://github.com/Irvingruiz790/nasaSpace2026  
**Equipo:** 4 personas — 2 frontend, 1 backend e integraciones, 1 contenido y datos  
**Duración:** 44 horas  
**Objetivo:** construir una experiencia interactiva que cuente la historia del hardware que NASA dejó en la Luna, Marte y el espacio profundo, para público de 8 a 12 años.

> **T+0** = hora de inicio. Si ya empezaron, ajusten los tiempos.  
> La prioridad es **terminar y poder demoear**, no agregar features.

---

## 0. Primeras 2 horas (hacer esto antes de programar)

- [ ] **BE:** crear estructura del repo, `.gitignore`, `requirements.txt` y deploy "hola mundo" en Streamlit Cloud.
- [ ] **CD:** traer el roster de 10 piezas y el borrador del esquema de datos.
- [ ] **FE1:** traer referencias visuales y wireframe de inicio + ficha.
- [ ] **FE2:** traer referencias de mapas y un prototipo de 3 marcadores sobre una imagen.
- [ ] **Todos:** acordar `docs/CONTRATO_DATOS.md` y el mapa de dueños de archivos.
- [ ] **BE:** primer commit a `main` con el esqueleto.

Si no hay consenso en 30 minutos, decide el dueño del área y se documenta en `docs/DECISIONES.md`.

---

## 1. Reglas para trabajar en conjunto (no negociables)

1. **Un dueño por archivo.** Si necesitas tocar un archivo que no es tuyo, pide en el chat o abre un issue. No lo edites por tu cuenta.
2. **`main` siempre debe funcionar.** Nada de merges con la app rota.
3. **Ramas cortas y PRs pequeños.** Una tarea = una rama = un PR. Nada de ramas de 12 horas.
4. **Integración cada 4 horas.** Se hace `pull`, se prueba la app y se mergea lo que esté listo.
5. **El contrato de datos se congela en T+2.** Después de eso, solo se agregan campos opcionales con aprobación de BE + CD.
6. **No renombrar imágenes ni IDs.** Frontend referencia rutas; no las cambia.
7. **Prefijos para evitar colisiones:** clases CSS `fe1-` / `fe2-`; llaves de `st.session_state` `fe1_` / `fe2_` / `be_` / `cd_`.
8. **Pull antes de push. Nunca `force push` a `main`.**
9. **El merge captain es BE.** Después de T+36, solo BE mergea.
10. **Si hay conflicto, resuelve el dueño del archivo.** Nunca "accept both" a ciegas.

### Definición de terminado de cualquier tarea

- Corre localmente sin errores.
- No agrega dependencias sin avisar a BE.
- No cambia el esquema de datos sin aprobación.
- Si es UI, incluye captura en el PR.
- Tiene un revisor asignado.
- El PR menciona el ID de la tarea.

---

## 2. Dueños de archivos (mapa anti-conflictos)

| Archivo / carpeta | Dueño | Regla |
|---|---|---|
| `app.py` | FE1 | Solo FE1 lo edita. FE2 crea páginas en `pages/`. |
| `pages/` | FE2 | Solo FE2. |
| `components/` | FE1 | FE2 puede importar, no editar. |
| `maps/` | FE2 | Solo FE2. |
| `core/` | BE | Solo BE. |
| `data/artifacts.json` | CD | Solo CD escribe. BE y FE leen. |
| `data/live_snapshot.json` | BE | Solo BE escribe. FE lee. |
| `data/sources.json` | CD | Solo CD. |
| `assets/img/` | CD | FE referencia, no renombra. |
| `assets/maps/` | FE2 | CD puede proveer imágenes base, pero FE2 las integra. |
| `assets/styles.css` | FE1 | FE2 avisa si necesita clases nuevas. |
| `requirements.txt` | BE | Nadie más lo edita. |
| `.streamlit/config.toml` | FE1 | BE lo revisa para deploy. |
| `README.md` | CD | BE revisa los comandos. |
| `docs/` | CD | FE/BE aportan secciones vía PR. |
| `tests/` | BE | Solo BE. |

> Si dos personas necesitan el mismo archivo, se parte en módulos antes de seguir. Es más rápido dividir que resolver un conflicto.

---

## 3. Flujo de Git

### Ramas

- `feat/fe1-layout`
- `feat/fe2-mapa-luna`
- `feat/be-horizons`
- `feat/cd-fichas-luna`
- `fix/...`
- `docs/...`

### Commits

- `feat(fe1): crear componente de tarjeta`
- `fix(be): manejar timeout de Horizons`
- `data(cd): agregar ficha de Voyager 1`
- `docs: actualizar fuentes`

### PRs

- Título: `[FE1-03] Componente de tarjeta`
- Descripción: qué cambia, por qué, cómo probarlo.
- Máximo ~300 líneas.
- Un revisor: FE1 ↔ FE2; BE revisa `core/` y `data/`; CD revisa contenido.
- Si es UI, captura antes/después.
- No se mergea si la app no arranca.

### Merge captain

**BE** es el merge captain. Su trabajo es:

- Revisar que `main` esté desplegable.
- Mergear PRs pequeños y frecuentes.
- Detectar conflictos de esquema o de nombres.
- Congelar el código a T+38.

---

## 4. Tareas por equipo

### FE1 — Frontend 1: sistema visual, inicio, fichas y accesibilidad

- [ ] **FE1-01 · Identidad visual y CSS base** — P0 · 2 h
  - Entregable: `assets/styles.css`, paleta, tipografía, badges de estado.
  - Hecho cuando: la app se ve consistente y legible en desktop y móvil.
  - Depende de: nada.

- [ ] **FE1-02 · Layout base y navegación** — P0 · 2 h
  - Entregable: header, footer, contenedor, navegación entre secciones en `app.py`.
  - Hecho cuando: se puede navegar sin callejones sin salida.
  - Depende de: FE1-01.

- [ ] **FE1-03 · Componente de tarjeta** — P0 · 2 h
  - Entregable: tarjeta reutilizable con imagen, nombre, zona, estado y apodo.
  - Hecho cuando: se usa en inicio, mapa y fichas.
  - Depende de: contrato de datos.

- [ ] **FE1-04 · Vista de detalle de ficha** — P0 · 3 h
  - Entregable: imagen, badge, 5 bloques, "última señal", fuentes y crédito.
  - Hecho cuando: una ficha real se ve completa y bien en móvil.
  - Depende de: FE1-03 + datos de CD.

- [ ] **FE1-05 · Página de inicio / hero narrativo** — P1 · 2 h
  - Entregable: explicación del proyecto en 30 segundos + llamada a explorar.
  - Hecho cuando: alguien entiende de qué trata sin que se lo expliquen.
  - Depende de: FE1-02.

- [ ] **FE1-06 · Responsive y accesibilidad** — P0 · 3 h
  - Entregable: contraste, tamaños de texto, alt text, navegación con teclado.
  - Hecho cuando: se usa en teléfono sin zoom y un lector de pantalla no se pierde.
  - Depende de: FE1-02, FE1-04.

- [ ] **FE1-07 · Página de fuentes y créditos** — P1 · 1 h
  - Entregable: lista de fuentes por pieza y créditos de imágenes.
  - Hecho cuando: cualquier dato se puede rastrear.
  - Depende de: `data/sources.json`.

- [ ] **FE1-08 · Estados vacíos, de carga y error** — P1 · 1 h
  - Entregable: mensajes claros si falta una imagen o falla la API.
  - Hecho cuando: la app no se rompe ni muestra una pantalla en blanco.
  - Depende de: BE.

- [ ] **FE1-09 · Estilos del quiz** — P2 · 1 h
  - Entregable: tarjetas de pregunta, botones y puntaje.
  - Hecho cuando: el quiz se ve parte de la misma app.
  - Depende de: FE2-08.

- [ ] **FE1-10 · Pulido visual y microinteracciones** — P2 · 2 h
  - Entregable: hover, transiciones suaves, detalles.
  - Hecho cuando: no distrae ni ralentiza.
  - Depende de: todo lo anterior.

---

### FE2 — Frontend 2: mapas, navegación, panel en vivo y quiz

- [ ] **FE2-01 · Prototipo de mapa con imagen y 3 marcadores** — P0 · 2 h
  - Entregable: una imagen de fondo y marcadores clickeables.
  - Hecho cuando: al hacer click se abre una ficha.
  - Depende de: contrato de datos.
  - **No usar `st.map`**: solo funciona con coordenadas terrestres.

- [ ] **FE2-02 · Mapa de la Luna** — P0 · 3 h
  - Entregable: 4 piezas ubicadas (Apolo 11, LRV 17, Surveyor 3, etc.).
  - Hecho cuando: los marcadores caen en la zona correcta y son clickeables.
  - Depende de: FE2-01 + datos de CD.

- [ ] **FE2-03 · Mapa de Marte** — P0 · 3 h
  - Entregable: 6 piezas (Sojourner, Spirit, Opportunity, InSight, Ingenuity, etc.).
  - Hecho cuando: se distinguen los sitios y se abre la ficha.
  - Depende de: FE2-01 + datos de CD.

- [ ] **FE2-04 · Mapa de espacio profundo** — P0 · 3 h
  - Entregable: diagrama estilizado, **no a escala**, con Voyager 1, Voyager 2 y una referencia al Sol/Tierra.
  - Hecho cuando: se entiende "qué tan lejos" sin necesitar una maestría.
  - Depende de: FE2-01 + datos de BE.

- [ ] **FE2-05 · Navegación entre zonas y fichas** — P0 · 2 h
  - Entregable: pasar de Luna a Marte a espacio profundo, y volver.
  - Hecho cuando: no hay callejones sin salida.
  - Depende de: FE1-02.

- [ ] **FE2-06 · Responsive de mapas** — P0 · 2 h
  - Entregable: mapas usables en teléfono.
  - Hecho cuando: los marcadores no se enciman y se pueden tocar.
  - Depende de: FE2-02, FE2-03, FE2-04.

- [ ] **FE2-07 · Panel "en vivo" (odómetro)** — P1 · 3 h
  - Entregable: distancia, tiempo luz, timestamp y aviso de respaldo.
  - Hecho cuando: funciona con datos en vivo y con `live_snapshot.json`.
  - Depende de: BE-04, BE-05.

- [ ] **FE2-08 · Quiz "¿Quién soy?"** — P1 · 3 h
  - Entregable: 5 preguntas, puntaje y reinicio.
  - Hecho cuando: se puede jugar sin recargar la página.
  - Depende de: FE1-03 + datos de CD.

- [ ] **FE2-09 · Integración de imágenes en mapas** — P1 · 1 h
  - Entregable: miniaturas o íconos por tipo de pieza.
  - Hecho cuando: se distingue un rover de un lander.
  - Depende de: CD-06.

- [ ] **FE2-10 · Pulido de mapas y quiz** — P2 · 2 h
  - Entregable: zoom, transiciones, leyenda.
  - Hecho cuando: no distrae ni rompe el responsive.
  - Depende de: todo lo anterior.

---

### BE — Backend e integraciones

- [ ] **BE-01 · Estructura del repo y entorno** — P0 · 1 h
  - Entregable: carpetas, `.gitignore`, `requirements.txt`, README base.
  - Hecho cuando: otro compañero clona y puede instalar.
  - Depende de: nada.

- [ ] **BE-02 · Carga y validación del dataset** — P0 · 2 h
  - Entregable: lector de `data/artifacts.json` con validación de campos.
  - Hecho cuando: si falta un campo, avisa claro y no explota.
  - Depende de: contrato de datos.

- [ ] **BE-03 · Snapshot de datos en vivo** — P0 · 1 h
  - Entregable: `data/live_snapshot.json` con datos dummy, timestamp y fuente.
  - Hecho cuando: frontend puede construir el panel sin esperar la API.
  - Depende de: contrato de datos.

- [ ] **BE-04 · Cliente de JPL Horizons** — P0 · 3 h
  - Entregable: consulta de distancia para Voyager 1/2 con timeout, reintento y caché.
  - Hecho cuando: devuelve datos o falla en menos de 5 segundos.
  - Depende de: BE-02.

- [ ] **BE-05 · Respaldo si la API falla** — P0 · 1 h
  - Entregable: lectura de `live_snapshot.json` y aviso de fecha.
  - Hecho cuando: se puede apagar la red y la app sigue funcionando.
  - Depende de: BE-03, BE-04.

- [ ] **BE-06 · Deploy en Streamlit Community Cloud** — P0 · 1 h + continuo
  - Entregable: URL pública actualizada desde `main`.
  - Hecho cuando: el link funciona en otro dispositivo.
  - Depende de: BE-01.

- [ ] **BE-07 · Merge captain y release manager** — P0 · continuo
  - Entregable: `main` desplegable, PRs revisados, conflictos resueltos.
  - Hecho cuando: cada integración termina con deploy funcionando.
  - Depende de: todo el equipo.

- [ ] **BE-08 · Formateo de unidades y comparaciones** — P1 · 2 h
  - Entregable: km, AU, tiempo luz y comparaciones cotidianas.
  - Hecho cuando: un niño entiende "qué tan lejos" sin números gigantes.
  - Depende de: BE-04.

- [ ] **BE-09 · Pruebas de humo y checklist de demo** — P1 · 1 h
  - Entregable: lista de verificación de 10 puntos.
  - Hecho cuando: se corre antes de cada demo.
  - Depende de: app integrada.

- [ ] **BE-10 · Video y capturas de respaldo** — P1 · 1 h
  - Entregable: video de la app funcionando y capturas.
  - Hecho cuando: si falla el internet, hay plan B.
  - Depende de: app integrada.

- [ ] **BE-11 · DSN Now como extra** — P2 · 2 h
  - Entregable: "qué nave está hablando ahora" con respaldo.
  - Hecho cuando: no bloquea el resto de la app si falla.
  - Depende de: BE-04.

- [ ] **BE-12 · Dependencias y secretos** — P1 · 1 h
  - Entregable: `requirements.txt` estable y `.streamlit/secrets.toml` fuera de Git.
  - Hecho cuando: el deploy no falla por dependencias.
  - Depende de: BE-01.

---

### CD — Contenido y datos

- [ ] **CD-01 · Roster de 10 piezas y estados** — P0 · 1 h
  - Entregable: tabla con pieza, zona, estado, fuente principal y responsable.
  - Hecho cuando: BE y FE saben exactamente qué datos van a recibir.
  - Depende de: nada.

- [ ] **CD-02 · Congelar el contrato de datos con BE** — P0 · 1 h
  - Entregable: `docs/CONTRATO_DATOS.md` aprobado.
  - Hecho cuando: no hay campos ambiguos ni nombres que cambien después.
  - Depende de: CD-01 + BE.

- [ ] **CD-03 · Escribir 4 fichas de Luna y Marte** — P0 · 6 h
  - Entregable: Apolo 11, LRV 17, Surveyor 3, Sojourner (o el roster acordado).
  - Hecho cuando: cumplen la plantilla y tienen 2 fuentes.
  - Depende de: CD-02.

- [ ] **CD-04 · Escribir 2 fichas de espacio profundo** — P0 · 3 h
  - Entregable: Voyager 1 y Voyager 2.
  - Hecho cuando: incluyen distancia, tiempo luz y estado.
  - Depende de: CD-02 + BE-04.

- [ ] **CD-05 · Verificar coordenadas, fechas y distancias** — P0 · 3 h
  - Entregable: registro en `docs/FUENTES.md`.
  - Hecho cuando: cada dato crítico tiene 2 fuentes oficiales.
  - Depende de: CD-03, CD-04.

- [ ] **CD-06 · Imágenes, créditos y alt text** — P0 · 3 h
  - Entregable: `assets/img/{id}_main.jpg` y `{id}_thumb.jpg`, con crédito.
  - Hecho cuando: todas las fichas tienen imagen y texto alternativo.
  - Depende de: CD-01.

- [ ] **CD-07 · Registro de fuentes** — P0 · 1 h
  - Entregable: `data/sources.json` y `docs/FUENTES.md`.
  - Hecho cuando: la página de fuentes puede generarse desde ahí.
  - Depende de: CD-05.

- [ ] **CD-08 · Revisión de tono para 8–12 años** — P0 · 2 h
  - Entregable: fichas revisadas por otra persona.
  - Hecho cuando: no hay párrafos largos ni tecnicismos sin explicar.
  - Depende de: CD-03, CD-04.

- [ ] **CD-09 · Apoyo en pitch y video** — P1 · 2 h
  - Entregable: guion de 2 minutos y datos clave.
  - Hecho cuando: el pitch se entiende sin la app.
  - Depende de: CD-03, CD-04.

- [ ] **CD-10 · QA de datos dentro de la app** — P1 · 2 h
  - Entregable: comparación ficha vs JSON vs fuente.
  - Hecho cuando: no hay discrepancias ni imágenes rotas.
  - Depende de: app integrada.

- [ ] **CD-11 · Fichas extra (stretch)** — P2 · 4 h
  - Entregable: Viking 1, InSight, Ingenuity o Pioneer 10.
  - Hecho cuando: el MVP ya está cerrado y probado.
  - Depende de: todo lo anterior.

---

## 5. Tareas compartidas

- [ ] **S-01 · Kickoff y contrato** — T+0 · 30 min · todos.
- [ ] **S-02 · Integración #1** — T+6 · 30 min · todos.
- [ ] **S-03 · Integración #2** — T+12 · 30 min · todos.
- [ ] **S-04 · Integración #3** — T+18 · 30 min · todos.
- [ ] **S-05 · Demo interna #1** — T+24 · 15 min · todos.
- [ ] **S-06 · Demo interna #2** — T+36 · 15 min · todos.
- [ ] **S-07 · Code freeze** — T+38 · solo BE mergea.
- [ ] **S-08 · Pitch y video** — T+30–40 · CD + FE2.
- [ ] **S-09 · Retrospectiva** — T+43 · 15 min · todos.

---

## 6. Calendario de 44 horas

| Horas | FE1 | FE2 | BE | CD | Hito |
|---|---|---|---|---|---|
| 0–2 | Identidad visual | Referencias + prototipo | Repo + deploy | Roster + esquema | Contrato congelado |
| 2–6 | Layout + tarjeta | Mapa Luna | Loader + snapshot | 3 fichas | App con 2 fichas |
| 6–10 | Detalle de ficha | Mapa Marte | Horizons | 3 fichas | **Gate 1** |
| 10–14 | Inicio / hero | Espacio profundo | Respaldo | Imágenes | 6 fichas |
| 14–18 | Responsive | Navegación + live | Formateo | Verificación | **Gate 2** |
| 18–24 | Fuentes + accesibilidad | Quiz | Pruebas | QA de datos | **Demo #1** |
| 24–30 | Pulido | Estilos de quiz | Optimización | Fichas extra | Feature complete |
| 30–36 | Fixes de UI | Fixes de mapas | Deploy final | Pitch / video | **Demo #2** |
| 36–38 | QA final | QA final | Code freeze | Fuentes / créditos | **Code freeze** |
| 38–44 | Buffer | Buffer | Buffer | Ensayo | Entrega |

**Ruta crítica:** contenido → tarjetas → mapas. Si CD se atrasa, BE ayuda a verificar datos y FE1 ayuda con el tono. El mapa es el mayor riesgo técnico: FE2 debe tener el prototipo antes de T+6.

**Descanso:** entre T+18 y T+26, dos personas duermen 4–5 horas mientras las otras dos cubren integración y contenido. Luego rotan. Nadie aguanta 44 horas despierto y programa bien.

---

## 7. Checklist de integración (cada 4 horas)

- [ ] `git pull origin main` en la rama de cada uno.
- [ ] La app arranca sin errores.
- [ ] Las 10 fichas cargan.
- [ ] Los 3 mapas son clickeables.
- [ ] El panel en vivo funciona con respaldo.
- [ ] Se ve bien en móvil.
- [ ] No hay imágenes rotas.
- [ ] El deploy está actualizado.
- [ ] La página de fuentes está completa.
- [ ] No hay errores en la consola.

---

## 8. Checklist de PR

- [ ] Rama actualizada con `main`.
- [ ] Cambio pequeño y con un solo propósito.
- [ ] Probado localmente.
- [ ] No cambia el esquema ni renombra archivos.
- [ ] No agrega dependencias sin avisar a BE.
- [ ] Captura si es UI.
- [ ] Un revisor asignado.
- [ ] El título incluye el ID de la tarea.

---

## 9. Riesgos y dueños

| Riesgo | Probabilidad | Impacto | Mitigación | Dueño |
|---|---|---|---|---|
| La API falla en la demo | Media | Alto | Snapshot + caché + aviso de fecha | BE |
| El mapa consume demasiado tiempo | Alta | Alto | Prototipo simple antes de T+6 | FE2 |
| El contenido llega tarde | Alta | Alto | Plantilla + mínimo 8 fichas + apoyo de BE | CD |
| Conflictos de merge | Media | Medio | Dueños de archivo + integración cada 4 h | BE |
| Deploy falla al final | Media | Alto | Deploy desde T+1 + video de respaldo | BE |
| Scope creep | Alta | Medio | Parking lot + guardián del alcance | CD |
| Datos incorrectos | Media | Alto | Doble fuente + revisión cruzada | CD |
| Cansancio | Alta | Medio | Turnos de sueño | Todos |

---

## 10. Parking lot (ideas fuera del MVP)

- Narración en audio.
- Versión en inglés.
- Más piezas (Viking, InSight, Pioneer).
- Modelos 3D.
- Realidad aumentada.
- Modo docente con actividades.
- Mapa a escala real.
- Integración con DSN Now en vivo.

No se toca nada de esta lista hasta que el MVP esté desplegado y probado.

---

## 11. Tablero sugerido

**Columnas:** Backlog → Este bloque → En progreso → Revisión → Hecho → Bloqueado.

**Etiquetas:** `fe1`, `fe2`, `be`, `cd`, `datos`, `contenido`, `bug`, `pitch`.

**Regla:** una tarjeta no pasa a "Hecho" sin revisión de otra persona.
