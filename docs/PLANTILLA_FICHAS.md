# Plantilla de fichas

**Uso:** copiar una ficha por pieza en `data/artifacts.json` y en la vista de detalle.  
**Dueño:** Contenido y datos (CD).  
**Revisión:** otra persona del equipo antes de publicar.

Los nombres de los campos deben coincidir con [docs/CONTRATO_DATOS.md](CONTRATO_DATOS.md). No se renombran después de T+2.

---

## 1. Reglas de llenado

**Público:** niños y niñas de 8 a 12 años.

**Tono:**
- Frases cortas, una idea por frase.
- Presente y segunda persona cuando ayude: "Si miraras al cielo…".
- Comparaciones cotidianas: "del tamaño de un auto", "como un horno de pan".
- Una pregunta al lector por ficha, máximo.
- No atribuir emociones que confundan: un rover "mide", no "extraña". Se puede usar voz narrativa, pero sin inventar ciencia.

**Límites de extensión:**

| Bloque | Límite |
|---|---|
| ¿Qué es? | ≤ 35 palabras |
| ¿Por qué lo enviamos? | ≤ 40 palabras |
| ¿Qué descubrió? | ≤ 45 palabras |
| ¿Dónde está ahora? | ≤ 45 palabras |
| Dato curioso | ≤ 30 palabras |
| **Total** | **≤ 195 palabras** |

**Rigor:**
- Cada dato crítico (fecha, coordenada, distancia, estado) necesita dos fuentes oficiales.
- Fuente primaria: `.nasa.gov`, NSSDCA, JPL/Caltech.
- Registrar URL y fecha de consulta.
- Etiquetar lo aproximado: "unos", "aproximadamente", "según el modelo de JPL".
- Nada de frases virales sin verificar.
- Cada imagen lleva crédito y texto alternativo.

**Taxonomía de estado:**

| `estado` | Etiqueta para niños | Significado |
|---|---|---|
| `activo` | "Sigue despierto" | Todavía funciona y se comunica |
| `en_silencio` | "En silencio" | Dejó de comunicarse |
| `se_quedo` | "Se quedó aquí" | Está en un lugar fijo, sin moverse |
| `en_orbita` | "En órbita para siempre" | Da vueltas sin energía |
| `perdido` | "Se perdió" | No se sabe dónde está o falló |

---

## 2. Ficha en blanco

```markdown
### Ficha: [Nombre]

**ID:** [slug-estable]
**Apodo:** [frase corta y memorable]
**Tipo:** [lander / rover / orbitador / nave / instrumento]
**Misión:** [nombre de la misión]
**Agencia:** [NASA / NASA-JPL / otra]
**Zona:** [luna / marte / espacio_profundo / orbita / asteroide]
**Estado:** [activo / en_silencio / se_quedo / en_orbita / perdido]
**Etiqueta de estado:** [texto para niños]

**Ubicación:** [lugar con nombre]
**Latitud / Longitud:** [si aplica; si no, "no aplica"]
**Lanzamiento:** [fecha]
**Última señal / fin de misión:** [fecha o "sigue activo"]
**Distancia actual:** [solo si aplica; indicar fuente y fecha]

**Imagen:** [ruta o ID de NASA Images]
**Crédito:** [NASA/JPL-Caltech, etc.]
**Texto alternativo:** [descripción de la imagen para accesibilidad]

#### Historia

**¿Qué es?**
[≤ 35 palabras]

**¿Por qué lo enviamos?**
[≤ 40 palabras]

**¿Qué descubrió?**
[≤ 45 palabras]

**¿Dónde está ahora?**
[≤ 45 palabras]

**Dato curioso**
[≤ 30 palabras]

#### Fuentes
1. [Título](URL) — consultado el [fecha]
2. [Título](URL) — consultado el [fecha]
3. [Fuente de datos en vivo, si aplica]

#### Control de calidad
- [ ] Revisado por: [nombre]
- [ ] Fecha de verificación: [fecha]
- [ ] Dos fuentes oficiales por dato crítico
- [ ] Imagen con crédito y alt text
- [ ] Longitud dentro de los límites
- [ ] Lenguaje apto para 8–12 años
```

---

## 3. Ejemplo completo 1 — Voyager 1

### Ficha: Voyager 1

**ID:** `voyager-1`  
**Apodo:** "La mensajera más lejana"  
**Tipo:** nave espacial de sobrevuelo  
**Misión:** Voyager  
**Agencia:** NASA/JPL-Caltech  
**Zona:** `espacio_profundo`  
**Estado:** `activo`  
**Etiqueta de estado:** "Sigue despierta"

**Ubicación:** espacio interestelar, más allá de la heliopausa  
**Latitud / Longitud:** no aplica  
**Lanzamiento:** 5 de septiembre de 1977  
**Última señal / fin de misión:** sigue comunicándose; su señal tarda unas 24 horas en llegar a la Tierra  
**Distancia actual:** unos 25 900 millones de km (18 de noviembre de 2026), según NASA/JPL

**Imagen:** `assets/img/voyager-1_main.jpg`  
**Crédito:** NASA/JPL-Caltech  
**Texto alternativo:** Ilustración de la nave Voyager con su gran antena parabólica apuntando hacia la Tierra.

#### Historia

**¿Qué es?**
Una nave del tamaño de un auto pequeño con una antena de casi 4 metros. Fue construida para visitar los planetas gigantes y nunca volver.

**¿Por qué la enviamos?**
Para aprovechar una alineación poco común de los planetas gigantes y estudiar sus lunas, anillos y atmósferas.

**¿Qué descubrió?**
Volcanes activos en Ío, la atmósfera de Titán, la estructura de los anillos de Saturno y el borde del viento solar.

**¿Dónde está ahora?**
En el espacio interestelar, a unos 25 900 millones de km. Su señal tarda unas 24 horas en llegar a la Tierra.

**Dato curioso**
Lleva un disco de oro con saludos en 55 idiomas, sonidos de la Tierra y música. Si alguien lo encuentra, sabrá que existimos.

#### Fuentes
1. [NASA Science — Voyager](https://science.nasa.gov/mission/voyager/) — consultado el 14 nov 2026
2. [NASA Science — Where are Voyager 1 and 2 now?](https://science.nasa.gov/mission/voyager/where-are-voyager-1-and-voyager-2-now/) — consultado el 14 nov 2026
3. [JPL Horizons API](https://ssd.jpl.nasa.gov/api/horizons.api) — `COMMAND='-31'` — consultado el 14 nov 2026
4. [NASA Science — The Golden Record](https://science.nasa.gov/mission/voyager/voyager-golden-record-overview/) — consultado el 14 nov 2026

#### Control de calidad
- [ ] Revisado por: [nombre]
- [ ] Fecha de verificación: 14 nov 2026
- [x] Dos fuentes oficiales por dato crítico
- [x] Imagen con crédito y alt text
- [x] Longitud dentro de los límites
- [x] Lenguaje apto para 8–12 años

---

## 4. Ejemplo completo 2 — Apolo 11, módulo lunar Eagle

### Ficha: Módulo Lunar Eagle (etapa de descenso)

**ID:** `apollo-11-lm`  
**Apodo:** "El águila que se quedó"  
**Tipo:** lander  
**Misión:** Apolo 11  
**Agencia:** NASA  
**Zona:** `luna`  
**Estado:** `se_quedo`  
**Etiqueta de estado:** "Se quedó en la Luna"

**Ubicación:** Mar de la Tranquilidad  
**Latitud / Longitud:** 0.67416, 23.47314  
**Lanzamiento:** 16 de julio de 1969  
**Última señal / fin de misión:** la etapa de descenso quedó en la superficie el 20 de julio de 1969; el paquete EASEP transmitió hasta el 27 de agosto de 1969  
**Distancia actual:** unos 384 400 km de la Tierra, en promedio

**Imagen:** `assets/img/apollo-11-lm_main.jpg`  
**Crédito:** NASA  
**Texto alternativo:** El módulo lunar Eagle posado en la Luna, con un astronauta junto a una de sus piernas.

#### Historia

**¿Qué es?**
La parte baja del módulo lunar que llevó a Neil Armstrong y Buzz Aldrin a la Luna. Servía como plataforma de aterrizaje y como base para despegar.

**¿Por qué la enviamos?**
Para cumplir el objetivo de Kennedy: llevar humanos a la Luna y traerlos de vuelta antes de que terminara la década de 1960.

**¿Qué descubrió?**
Trajo 21.55 kg de rocas y polvo lunar; dejó un sismómetro y un espejo especial para medir la distancia a la Luna.

**¿Dónde está ahora?**
Sigue en el Mar de la Tranquilidad, en 0.674°N, 23.473°E. La etapa de ascenso se separó y se cree que se estrelló.

**Dato curioso**
El espejo (retrorreflector) no usa electricidad. Desde la Tierra le disparan láseres y sigue respondiendo más de 50 años después.

#### Fuentes
1. [NSSDCA — Apollo 11 Lunar Module / EASEP](https://nssdc.gsfc.nasa.gov/nmc/spacecraft/display.action?id=1969-059C) — consultado el 14 nov 2026
2. [NSSDCA — Apollo 11 Mission](https://nssdc.gsfc.nasa.gov/planetary/lunar/apollo11.html) — consultado el 14 nov 2026
3. [NASA Science — Apollo](https://science.nasa.gov/mission/apollo-11/) — consultado el 14 nov 2026

#### Control de calidad
- [ ] Revisado por: [nombre]
- [ ] Fecha de verificación: 14 nov 2026
- [x] Dos fuentes oficiales por dato crítico
- [x] Imagen con crédito y alt text
- [x] Longitud dentro de los límites
- [x] Lenguaje apto para 8–12 años

> **Nota de verificación:** NSSDCA indica que el destino de la etapa de ascenso "no se conoce, pero se asume que se estrelló". Por eso la ficha dice "se cree que se estrelló", no "se estrelló".

---

## 5. Hoja de trabajo de las 10 piezas

| # | Pieza | Zona | Estado | Fuente principal | Responsable | Revisor | Listo |
|---|---|---|---|---|---|---|---|
| 1 | Apolo 11, etapa de descenso | Luna | `se_quedo` | NSSDCA 1969-059C | | | ☐ |
| 2 | LRV del Apolo 17 | Luna | `se_quedo` | NSSDCA | | | ☐ |
| 3 | Surveyor 3 | Luna | `se_quedo` | NASA Science | | | ☐ |
| 4 | Sojourner | Marte | `en_silencio` | NASA Pathfinder | | | ☐ |
| 5 | Spirit | Marte | `en_silencio` | NASA Science | | | ☐ |
| 6 | Opportunity | Marte | `en_silencio` | NASA Science | | | ☐ |
| 7 | InSight | Marte | `en_silencio` | NASA Science | | | ☐ |
| 8 | Ingenuity | Marte | `se_quedo` | NASA Science | | | ☐ |
| 9 | Voyager 1 | Espacio profundo | `activo` | NASA/JPL + Horizons | | | ☐ |
| 10 | Voyager 2 | Espacio profundo | `activo` | NASA/JPL + Horizons | | | ☐ |

**Reparto sugerido:** CD escribe las 4 de Luna y Marte; BE verifica los datos de Horizons; FE1 revisa el tono y la longitud; FE2 revisa que la imagen y el alt text funcionen en la interfaz.

---

## 6. Checklist final por ficha

- [ ] ID único y estable.
- [ ] Nombre y apodo.
- [ ] Zona y estado correctos según la taxonomía.
- [ ] Ubicación con coordenadas o descripción clara.
- [ ] Fecha de lanzamiento y última señal.
- [ ] Los 5 bloques dentro de los límites.
- [ ] Dos fuentes oficiales por dato crítico.
- [ ] Imagen con crédito y alt text.
- [ ] Revisión cruzada por otra persona.
- [ ] Sin frases virales ni citas inventadas.
- [ ] Lenguaje comprensible para 8–12 años.
