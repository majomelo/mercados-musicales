# Documento de funcionalidades — Mercados Musicales

## 1. Para quién y para qué

**Frase de método (S9):** La app **optimiza una decisión de promoción**: compara cada región cultural con el promedio de su género (índice de afinidad) y simula 5.000 escenarios bootstrap para estimar la probabilidad de que cada región sea la mejor. Usa los datos de Spotify 2024 (500 registros, 4 regiones culturales, 10 géneros) y está pensada para quien debe decidir dónde promover un género musical, por ejemplo **Valentina**, coordinadora de marketing de un sello independiente en Bogotá con presupuesto para una sola campaña regional.

**Pregunta que responde:** «¿En qué región lanzo el sencillo de Indie, y qué tan segura es esa elección?»

## 2. Lo que ya existe

- **Stack:** Streamlit, publicada en Community Cloud desde GitHub.
- **Funciones de `pipeline.py`** (nombre, recibe, devuelve). Ya están programadas y probadas en el notebook; **confirmar los nombres exactos antes de entregar**:
  - `recomendar_region(genero)` → región recomendada, afinidad, probabilidad de ser la mejor, nivel de evidencia y segunda opción. *[nombre por confirmar]*
  - `nivel_evidencia(probabilidad)` → «Alta» (≥ 70 %), «Media» (40–70 %) o «Baja» (< 40 %). *[nombre por confirmar]*
  - `ranking_por_region(region)` → géneros con promedio de streams y número de registros. *[nombre por confirmar]*
  - `normalizar_entrada(texto)` → género o región válida, sugerencia («¿Quisiste decir Jazz?») o lista de géneros disponibles. *[nombre por confirmar]*
- **Datos:**
  - Tabla `resultados_app`: 40 filas (10 géneros × 4 regiones) con afinidad, probabilidad de ser la mejor, nivel de evidencia y número de registros.
  - Base original: 500 registros sintéticos de Spotify 2024 (Kaggle, licencia Apache 2.0), agrupados en 4 regiones: anglosajón, Latinoamérica, Asia y Europa continental.
  - **¿Se pueden publicar?** Sí. La licencia Apache 2.0 lo permite y el repositorio es público. La app declara que los datos son sintéticos y los resultados exploratorios.

## 3. Pantallas

**Mapa de navegación:** cuatro pantallas, todas con salida. El regreso está siempre arriba a la izquierda.

```
P0 Inicio → P1 Recomendación → P2 Evidencia
P0 Inicio → P3 Ranking por región → P1 Recomendación (al tocar un género)
```

**Estructura común a todas las pantallas:** barra superior, filtros a la izquierda, resultados a la derecha y la misma paleta. Verde = región recomendada, gris = todo lo demás.

### Pantalla: P0 · Inicio

- **Lo primero que ve el usuario («la única cosa»):** la pregunta «¿Qué quieres decidir hoy?».
- **Entradas (qué ingresa o elige el usuario):**
  - Botón principal (relleno): «Tengo un género».
  - Botón secundario: «Tengo un mercado».
- **Salidas (qué le muestra la app):**
  - Los dos caminos de entrada.
  - La fuente de los datos al pie.
  - Enlace «Acerca de los datos» arriba a la derecha (deseable).
- **Función del pipeline que produce esa salida:** ninguna. Es navegación.
- **Qué pasa si el usuario ingresa algo inválido:** no aplica, porque solo hay botones.
- **Cambios de usabilidad acordados hoy (Bloque 3):** *[completar con los acuerdos de la sesión]*

### Pantalla: P1 · Recomendación (pantalla principal)

- **Lo primero que ve el usuario («la única cosa»):** la región recomendada, en un titular de 30 pt y en verde: **«Prioriza Latinoamérica»** (caso Indie).
- **Entradas (qué ingresa o elige el usuario):**
  - Filtro de género a la izquierda, con selección o texto libre.
  - Botón «Ver evidencia», solo con borde.
  - Enlace de regreso arriba a la izquierda.
- **Salidas (qué le muestra la app):**
  - Una tarjeta con el titular, la afinidad traducida a porcentaje («+34 % frente al promedio del género») y el nivel de evidencia («alta»).
  - La segunda opción, a la izquierda (Indie: mercado anglosajón).
  - Un gráfico de barras de las 4 regiones contra la línea de 100. Solo la región recomendada va en verde, con etiquetas directas y sin cuadrícula, ejes ni leyenda.
- **Función del pipeline que produce esa salida:** `recomendar_region(genero)` y `nivel_evidencia(probabilidad)`. *[confirmar nombres]*
- **Qué pasa si el usuario ingresa algo inválido:**

  | Caso | Entrada | Respuesta de la app |
  |---|---|---|
  | Error de escritura | «Jaz» | «¿Quisiste decir Jazz?» |
  | Escribe un país | «México» | Lo traduce a la región Latinoamérica |
  | Género inexistente | «Salsa» | Lista de géneros disponibles |
  | Llega sin elegir | (vacío) | «Elige un género para ver la recomendación» |
  | Evidencia baja | Rock (37 %) | Titular «Sin región dominante»; pierde el verde y resalta las dos primeras regiones (Latinoamérica y anglosajón) |
  | Pocos datos | Género con menos de 5 registros | Alerta para interpretar con cautela |

- **Cambios de usabilidad acordados hoy (Bloque 3):** *[completar con los acuerdos de la sesión]*

### Pantalla: P2 · Evidencia

- **Lo primero que ve el usuario («la única cosa»):** qué tan segura es la recomendación. Cada región aparece como un punto (afinidad) con una línea (rango del 90 % de los escenarios simulados) frente a la referencia de 100.
- **Entradas (qué ingresa o elige el usuario):** ninguna. Llega desde P1 con el género ya elegido. Tiene enlace de regreso arriba a la izquierda.
- **Salidas (qué le muestra la app):**
  - Gráfico de puntos con intervalos del 90 % por región.
  - Probabilidad de ser la mejor de cada región.
  - Número de registros que respaldan cada resultado (Indie en Latinoamérica: 7).
  - Guía de lectura: si la línea cruza 100, la región no se distingue del promedio.
- **Función del pipeline que produce esa salida:** `recomendar_region(genero)`, que devuelve afinidad, intervalo del 90 % y probabilidad por región, y `nivel_evidencia(probabilidad)`. *[confirmar nombres]*
- **Qué pasa si el usuario ingresa algo inválido:** no hay entradas libres. Si llega sin género seleccionado, vuelve a P1 con el mensaje «Elige un género para ver la recomendación».
- **Cambios de usabilidad acordados hoy (Bloque 3):** *[completar con los acuerdos de la sesión]*

### Pantalla: P3 · Ranking por región

- **Lo primero que ve el usuario («la única cosa»):** el género líder de la región elegida (Latinoamérica → Indie).
- **Entradas (qué ingresa o elige el usuario):**
  - Selector de región (Latinoamérica, anglosajón, Asia, Europa continental).
  - Toque en un género para ir a su recomendación.
  - Enlace de regreso arriba a la izquierda.
- **Salidas (qué le muestra la app):**
  - Ranking de géneros de la región con promedio de streams y número de registros.
  - Alerta si un género tiene menos de 5 registros (ej. R&B con 4).
- **Función del pipeline que produce esa salida:** `ranking_por_region(region)`. *[confirmar nombre]*
- **Qué pasa si el usuario ingresa algo inválido:**
  - Si escribe un país, lo traduce a su región.
  - Si escribe una región que no existe, muestra las 4 disponibles.
  - Si llega sin elegir, muestra «Elige una región para ver el ranking».
- **Cambios de usabilidad acordados hoy (Bloque 3):** *[completar con los acuerdos de la sesión]*

## 4. Fuera de alcance

Lo que la app **NO** va a hacer, incluidas las limitaciones del método (Semana 10):

- **Vista por país.** El 53,5 % de las combinaciones país-género tiene 2 registros o menos. La app trabaja solo con 4 regiones culturales.
- **Mapa coroplético.** Sugeriría una precisión por país que no existe.
- **Datos reales del mercado.** La base es sintética (Kaggle). Los resultados son exploratorios y no describen el mercado real. Por ejemplo, la caída de Reggaeton en Latinoamérica es un patrón de esta base.
- **Recomendación firme con evidencia baja.** Para géneros como Rock (37 %), la app no declara una región ganadora.
- **Predicción o tendencias.** No pronostica resultados de campañas ni ventas.
- **Mapa de calor completo en la pantalla principal.** Obliga a buscar el género entre 40 celdas.
- **Flujo que empiece por la región como camino principal.** El usuario plantea la decisión desde su género. El camino por mercado es solo secundario.
- **Deseables, solo si alcanza el tiempo:** «Acerca de los datos», tendencia de los últimos 30 días, comparar dos géneros y descargar en PDF.

## 5. Restricciones

- Equipo de 2 personas (María José Melo González y Nicolás Gaitán Casas). Construcción en las semanas 12, 13 y 14 (8, 22 y 29 de oct.) más trabajo autónomo:
  - **Semana 12:** P0 y P1, con validación de entradas.
  - **Semana 13:** P2 y P3, con navegación y regresos.
  - **Semana 14:** prueba con usuarios externos, ajustes y publicación.
- ~1 GB de RAM (Streamlit Community Cloud). La app lee solo la tabla `resultados_app` precalculada (40 filas), sin recalcular el bootstrap en vivo.
- Repositorio público en GitHub.
- **MVP:** P0 a P3, validación de entradas y prueba con usuarios.
