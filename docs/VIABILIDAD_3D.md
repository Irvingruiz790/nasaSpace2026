# Modelos 3D en los mapas — evaluación con 10 horas restantes

## Recomendación

Conservar los mapas actuales para esta entrega. Un globo decorativo es viable
como prototipo; sustituir el mapa interactivo completo no es una apuesta
recomendable dentro de las 10 horas que también cubren integración y entrega.
Las esferas CSS del selector de inicio son ilustraciones, no modelos 3D.

## Qué exige el código actual

- `components/mapa.py` coloca botones Streamlit sobre imágenes con coordenadas
  x/y de 0 a 100, definidas en `assets/maps/posiciones.json`.
- Esas coordenadas representan posiciones en las imágenes actuales, no
  latitud/longitud. No se pueden trasladar directamente a una esfera.
- Los clics guardan `pieza_sel` y abren `pages/7_Ficha.py`. Un visor WebGL
  necesita comunicar su selección a Python y conservar ese recorrido.
- Espacio profundo no es un planeta: necesita otra representación.
- La Luna es un satélite; las piezas en órbita tampoco deben dibujarse como
  puntos sobre una superficie.

## Estimaciones de ingeniería (no tiempos medidos)

| Trabajo | Horas aproximadas |
|---|---:|
| Prototipo de esfera con giro, cámara y textura local | 2–4 |
| Obtener y revisar coordenadas geográficas y texturas | 2–4 |
| Marcadores, ocultación detrás del globo y selección hacia Streamlit | 3–5 |
| Teclado, táctil, rendimiento y respaldo sin WebGL | 2–4 |
| Integración, pruebas y correcciones | 2–3 |
| Total estimado | 11–20 |

Puede hacerse con JavaScript/WebGL y un componente Streamlit sin React ni
Node. Una biblioteca 3D local facilitaría el trabajo, pero sería una dependencia
nueva y requeriría autorización. WebGL puro evita esa dependencia a cambio de
más código de cámara, geometría y detección de clics. Un visor externo no cumple
la exigencia de funcionar sin recursos de internet.

## Condiciones para una fase posterior

1. Aprobar la biblioteca y empaquetar código, licencias y texturas localmente.
2. Añadir coordenadas geográficas verificadas sin sustituir las x/y actuales.
3. Prototipar primero la Luna y medir carga y fluidez en un celular real.
4. Mantener lista de fichas y mapa 2D como alternativa accesible.
5. Verificar giro táctil, foco, selección, navegación y funcionamiento sin red.

## Implementado en esta fase

- Selector de destinos en inicio, con Sol y Tierra como contexto y botones
  para Luna, Marte y espacio profundo. Indica explícitamente que no está a escala.
- Vista previa textual nativa de Streamlit al pasar por «Ver ficha», con nombre,
  descripción y ubicación. El clic sigue abriendo la ficha, también en móvil.
- Sin bibliotecas nuevas ni imágenes externas.
