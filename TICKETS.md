# TICKETS — Mercados Musicales

Plan de construcción de la app (Streamlit + Community Cloud desde GitHub). Es un borrador: el plan es del equipo.

**Reglas que cumple cada ticket**
- Es un cambio pequeño y autocontenido, de 1 a 2 horas como máximo.
- Hace una sola cosa, idealmente en un solo archivo o una sola pantalla.
- Después de cada ticket la app sigue funcionando, aunque esté incompleta.
- Todo corresponde a algo del documento de funcionalidades. No hay funcionalidades nuevas.
- El «hola mundo» se publica en Community Cloud entre los primeros tickets (T-02).

**Archivos del repositorio**
- `app.py`: interfaz Streamlit, navegación y pantallas.
- `pipeline.py`: funciones que ya existen (se reutilizan, no se reescriben).
- `data/resultados_app.csv`: tabla de 40 filas (10 géneros × 4 regiones).
- `requirements.txt` y `README.md`.

> Los nombres de funciones de `pipeline.py` (`recomendar_region`, `nivel_evidencia`, `ranking_por_region`, `normalizar_entrada`) son los tentativos del documento de funcionalidades. Ajústenlos a los reales.

**Orden sugerido**

| Fase | Tickets | Semana |
|---|---|---|
| Despliegue temprano | T-01 a T-03 | 12 |
| Base de la app | T-04 a T-06 | 12 |
| P0 y P1 | T-07 a T-13 | 12 |
| P2 y P3 | T-14 a T-18 | 13 |
| Cierre | T-19 a T-22 | 13 y 14 |

---

## Despliegue temprano

### T-01 — Crear el repositorio público con la estructura mínima
- Pantalla / archivo: repositorio de GitHub, `README.md`, `requirements.txt`
- Qué hay que hacer: crear el repositorio público. Agregar un `README.md` con el nombre del proyecto y una línea sobre qué hace la app. Agregar `requirements.txt` con `streamlit`, `pandas` y `numpy`.
- Depende de: nada
- Criterio de aceptación (cómo compruebo a mano que está listo): abro la URL del repositorio sin iniciar sesión y veo el README. El `requirements.txt` lista las librerías.
- Fuera de este ticket: código de la app, datos, pantallas.
- Responsable: (en blanco)
- Estado: hecho

### T-02 — Publicar un «hola mundo» en Community Cloud
- Pantalla / archivo: `app.py`
- Qué hay que hacer: crear `app.py` con un título «Mercados Musicales» y una línea de texto. Conectar el repositorio a Streamlit Community Cloud y desplegar.
- Depende de: T-01
- Criterio de aceptación (cómo compruebo a mano que está listo): abro la URL pública desde otro navegador y veo el título. Un cambio de texto en GitHub se refleja en la URL.
- Fuera de este ticket: datos, pantallas reales, estilos.
- Responsable: (en blanco)
- Estado: hecho

### T-03 — Subir `pipeline.py` y la tabla `resultados_app`
- Pantalla / archivo: `pipeline.py`, `data/resultados_app.csv`
- Qué hay que hacer: copiar al repositorio, sin modificarlas, las funciones ya probadas en el notebook (`pipeline.py`). Subir `resultados_app.csv` con sus 40 filas. Documentar en el README las columnas de la tabla y que los datos son sintéticos (Kaggle, Apache 2.0).
- Depende de: T-01
- Criterio de aceptación (cómo compruebo a mano que está listo): `python -c "import pipeline"` corre sin error. `pandas.read_csv("data/resultados_app.csv")` devuelve 40 filas. El README lista las columnas.
- Fuera de este ticket: usar los datos en la app, reescribir funciones.
- Responsable: (en blanco)
- Estado: hecho

## Base de la app

### T-04 — Cargar la tabla en la app con caché
- Pantalla / archivo: `app.py`
- Qué hay que hacer: leer `resultados_app.csv` con `@st.cache_data` y mostrar temporalmente el número de filas.
- Depende de: T-02, T-03
- Criterio de aceptación (cómo compruebo a mano que está listo): la URL pública muestra «40 filas». Recargar la página no vuelve a leer el archivo, o lo hace sin demora notable.
- Fuera de este ticket: mostrar la tabla completa al usuario, pantallas.
- Responsable: (en blanco)
- Estado: hecho

### T-05 — Esqueleto de navegación entre P0, P1, P2 y P3
- Pantalla / archivo: `app.py`
- Qué hay que hacer: guardar la pantalla actual en `st.session_state` y crear cuatro funciones vacías (`pantalla_inicio`, `pantalla_recomendacion`, `pantalla_evidencia`, `pantalla_ranking`) con un título cada una. Agregar botones provisionales para pasar de una a otra.
- Depende de: T-04
- Criterio de aceptación (cómo compruebo a mano que está listo): puedo pasar por las cuatro pantallas con los botones provisionales sin errores. Al recargar la página vuelvo a P0.
- Fuera de este ticket: contenido real de las pantallas, diseño visual.
- Responsable: (en blanco)
- Estado: hecho

### T-06 — Paleta, barra superior y enlace de regreso comunes
- Pantalla / archivo: `app.py` (o `estilos.py`)
- Qué hay que hacer: definir las constantes de color (un verde para la región recomendada y grises para lo demás). Crear una barra superior con el nombre de la app y un enlace «← Volver» arriba a la izquierda. El enlace aparece en todas las pantallas menos P0 y lleva a la pantalla anterior.
- Depende de: T-05
- Criterio de aceptación (cómo compruebo a mano que está listo): en P1, P2 y P3 veo el enlace «← Volver» en la misma esquina. Al tocarlo regreso a la pantalla anterior. En P0 no aparece.
- Fuera de este ticket: contenido de las pantallas, gráficos, «Acerca de los datos».
- Responsable: (en blanco)
- Estado: hecho

## P0 y P1 (semana 12)

### T-07 — P0 Inicio: pregunta y dos caminos
- Pantalla / archivo: P0 · Inicio (`app.py`)
- Qué hay que hacer: mostrar la pregunta «¿Qué quieres decidir hoy?», un botón principal relleno «Tengo un género» (lleva a P1) y un botón secundario «Tengo un mercado» (lleva a P3). Agregar al pie la fuente de los datos.
- Depende de: T-05, T-06
- Criterio de aceptación (cómo compruebo a mano que está listo): veo la pregunta y los dos botones, con el de género más destacado. «Tengo un género» abre P1. «Tengo un mercado» abre P3. Se lee la fuente al pie.
- Fuera de este ticket: contenido de P1 y P3, enlace «Acerca de los datos».
- Responsable: (en blanco)
- Estado: hecho

### T-08 — P1 Recomendación: filtro de género y titular
- Pantalla / archivo: P1 · Recomendación (`app.py`, `pipeline.py`)
- Qué hay que hacer: agregar a la izquierda un selector con los 10 géneros. Al elegir uno, llamar a la función existente del pipeline y mostrar en 30 pt y en verde el titular «Prioriza [región]».
- Depende de: T-04, T-06, T-07
- Criterio de aceptación (cómo compruebo a mano que está listo): al elegir Indie veo «Prioriza Latinoamérica». Al elegir Hip Hop veo «Prioriza Anglosajón». Los resultados coinciden con la tabla del Anexo B.
- Fuera de este ticket: tarjeta de datos, gráfico, mensajes de error, evidencia baja.
- Responsable: (en blanco)
- Estado: hecho

### T-09 — P1: tarjeta con afinidad, evidencia y segunda opción
- Pantalla / archivo: P1 · Recomendación (`app.py`)
- Qué hay que hacer: debajo del titular, y dentro de una misma tarjeta, mostrar la afinidad como porcentaje («+34 % frente al promedio del género») y el nivel de evidencia («Alta», «Media» o «Baja»). A la izquierda, mostrar la segunda opción. Agregar el botón «Ver evidencia», solo con borde, que lleva a P2.
- Depende de: T-08
- Criterio de aceptación (cómo compruebo a mano que está listo): con Indie veo «+34 %», evidencia «Alta» y segunda opción «Anglosajón». Con Jazz veo «+27 %» y evidencia «Media». El botón «Ver evidencia» abre P2.
- Fuera de este ticket: gráfico de barras, contenido de P2.
- Responsable: (en blanco)
- Estado: hecho

### T-10 — P1: gráfico de barras de las 4 regiones contra 100
- Pantalla / archivo: P1 · Recomendación (`app.py`)
- Qué hay que hacer: debajo de la tarjeta, graficar la afinidad de las 4 regiones con una línea de referencia en 100. Solo la barra de la región recomendada va en verde y las demás en gris. Poner etiquetas directas sobre las barras. Sin cuadrícula, ejes, leyenda ni bordes.
- Depende de: T-09
- Criterio de aceptación (cómo compruebo a mano que está listo): con Indie veo 4 barras y solo la de Latinoamérica en verde, con 134 sobre la barra y la línea de 100 visible. No hay cuadrícula ni leyenda. Al cambiar de género, el verde se mueve a la región correspondiente.
- Fuera de este ticket: caso de evidencia baja, intervalos de confianza.
- Responsable: (en blanco)
- Estado: hecho

### T-11 — P1: validar lo que escribe el usuario
- Pantalla / archivo: P1 · Recomendación (`app.py`, `pipeline.py`)
- Qué hay que hacer: permitir escribir el género en un campo de texto. Reutilizar la función de normalización del pipeline para manejar estos casos:
  - «Jaz» → «¿Quisiste decir Jazz?».
  - «México» → traducir a la región Latinoamérica.
  - «Salsa» → mostrar la lista de géneros disponibles.
  - Campo vacío → «Elige un género para ver la recomendación».
- Depende de: T-08
- Criterio de aceptación (cómo compruebo a mano que está listo): escribo cada una de las cuatro entradas y veo el mensaje indicado. Ninguna produce un error ni una pantalla en blanco.
- Fuera de este ticket: caso de evidencia baja, alerta de pocos datos.
- Responsable: (en blanco)
- Estado: hecho

### T-12 — P1: caso de evidencia baja («Sin región dominante»)
- Pantalla / archivo: P1 · Recomendación (`app.py`)
- Qué hay que hacer: cuando el nivel de evidencia es «Baja», cambiar el titular a «Sin región dominante, compara [región 1] y [región 2]». Quitar el verde del titular y de la barra. Resaltar en el gráfico las dos primeras regiones.
- Depende de: T-10
- Criterio de aceptación (cómo compruebo a mano que está listo): con Rock veo «Sin región dominante», sin verde, y resaltadas Latinoamérica y Anglosajón. Con Indie el titular sigue verde y normal.
- Fuera de este ticket: alerta de pocos datos, pantalla de evidencia.
- Responsable: (en blanco)
- Estado: hecho

### T-13 — P1: alerta cuando hay menos de 5 registros
- Pantalla / archivo: P1 · Recomendación (`app.py`)
- Qué hay que hacer: si la región recomendada tiene menos de 5 registros, mostrar una alerta discreta: «Pocos datos: interpreta este resultado con cautela».
- Depende de: T-09
- Criterio de aceptación (cómo compruebo a mano que está listo): elijo un género cuya región recomendada tenga menos de 5 registros en la tabla y veo la alerta. Con Indie (7 registros) no aparece.
- Fuera de este ticket: alerta en el ranking (T-17).
- Responsable: (en blanco)
- Estado: hecho

## P2 y P3 (semana 13)

### T-14 — P2 Evidencia: puntos con intervalo del 90 %
- Pantalla / archivo: P2 · Evidencia (`app.py`)
- Qué hay que hacer: para el género elegido en P1, graficar cada región como un punto (afinidad) con una línea (intervalo del 90 %) y una referencia en 100. Resaltar en verde la región recomendada.
- Depende de: T-10
- Criterio de aceptación (cómo compruebo a mano que está listo): con Indie, la línea de Latinoamérica queda entera por encima de 100 y las otras tres la cruzan. Si llego a P2 sin género elegido, vuelvo a P1 con el mensaje «Elige un género para ver la recomendación».
- Fuera de este ticket: probabilidades, número de registros, texto de ayuda.
- Responsable: (en blanco)
- Estado: hecho

### T-15 — P2: probabilidad, registros y guía de lectura
- Pantalla / archivo: P2 · Evidencia (`app.py`)
- Qué hay que hacer: a la derecha del gráfico, mostrar la probabilidad de ser la mejor de cada región y el número de registros que la respalda. Agregar una frase de ayuda: «Si la línea cruza 100, esa región no se distingue del promedio».
- Depende de: T-14
- Criterio de aceptación (cómo compruebo a mano que está listo): con Indie veo 93 % para Latinoamérica y «7 registros». Las cuatro probabilidades de cada género suman 100 %. La frase de ayuda es visible.
- Fuera de este ticket: nuevas métricas, descarga en PDF.
- Responsable: (en blanco)
- Estado: hecho

### T-16 — P3 Ranking por región: selector y ranking de géneros
- Pantalla / archivo: P3 · Ranking por región (`app.py`, `pipeline.py`)
- Qué hay que hacer: agregar a la izquierda un selector con las 4 regiones. Mostrar el ranking de géneros de la región elegida, con el promedio de streams y el número de registros. Resaltar en verde el género líder.
- Depende de: T-04, T-06
- Criterio de aceptación (cómo compruebo a mano que está listo): al elegir Latinoamérica veo Indie en primer lugar, en verde, con su promedio y su número de registros. Las 4 regiones muestran 10 géneros cada una.
- Fuera de este ticket: alerta de pocos datos, enlace a P1.
- Responsable: (en blanco)
- Estado: hecho

### T-17 — P3: alerta de pocos datos y enlace a la recomendación
- Pantalla / archivo: P3 · Ranking por región (`app.py`)
- Qué hay que hacer: marcar con una alerta los géneros con menos de 5 registros (ej. R&B con 4). Hacer que cada género del ranking sea clicable y lleve a P1 con ese género ya elegido.
- Depende de: T-16, T-08
- Criterio de aceptación (cómo compruebo a mano que está listo): en Latinoamérica, R&B muestra la alerta. Al tocar Indie llego a P1 con «Prioriza Latinoamérica» ya calculado, sin volver a elegir el género.
- Fuera de este ticket: validación de texto libre en P3.
- Responsable: (en blanco)
- Estado: hecho

### T-18 — Conectar el flujo completo y todos los regresos
- Pantalla / archivo: `app.py`
- Qué hay que hacer: reemplazar los botones provisionales de T-05 por la navegación real. Revisar que ninguna pantalla sea un callejón sin salida y que el enlace «← Volver» lleve siempre a la pantalla anterior.
- Depende de: T-07, T-09, T-15, T-17
- Criterio de aceptación (cómo compruebo a mano que está listo): recorro P0 → P1 → P2 → regreso → P1 → regreso → P0, y P0 → P3 → P1. Nunca me quedo atrapado y no queda ningún botón provisional.
- Fuera de este ticket: ajustes derivados de la prueba con usuarios.
- Responsable: (en blanco)
- Estado: hecho

## Cierre (semanas 13 y 14)

### T-19 — Declarar que los datos son sintéticos y la fuente
- Pantalla / archivo: pie común de `app.py`, `README.md`
- Qué hay que hacer: agregar al pie de todas las pantallas una línea: «Datos sintéticos (Kaggle, Apache 2.0). Resultados exploratorios». Verificar que el README diga lo mismo.
- Depende de: T-18
- Criterio de aceptación (cómo compruebo a mano que está listo): la línea se ve al pie de P0, P1, P2 y P3 sin invadir los resultados.
- Fuera de este ticket: pantalla «Acerca de los datos» (deseable).
- Responsable: (en blanco)
- Estado: hecho

### T-20 — Prueba con usuarios externos
- Pantalla / archivo: URL pública de la app, documento `PRUEBA_USUARIOS.md`
- Qué hay que hacer: pedir a 3 personas ajenas al equipo que cumplan la tarea de Valentina («¿en qué región lanzo un sencillo de Indie y qué tan segura es la elección?»). Observar sin ayudar y anotar dónde dudan o se equivocan. Preguntarles específicamente si se entiende el nivel de evidencia y si falta algún camino.
- Depende de: T-18
- Criterio de aceptación (cómo compruebo a mano que está listo): existe `PRUEBA_USUARIOS.md` con las observaciones de las 3 personas y una lista de ajustes propuestos.
- Fuera de este ticket: implementar los ajustes (T-21).
- Responsable: (en blanco)
- Estado: pendiente

### T-21 — Implementar los ajustes de la prueba
- Pantalla / archivo: las pantallas afectadas, `PRUEBA_USUARIOS.md`
- Qué hay que hacer: implementar los ajustes de usabilidad priorizados de T-20, solo los que caben en el tiempo y existen en el documento de funcionalidades. Anotar en `PRUEBA_USUARIOS.md` cuáles se hicieron y cuáles quedaron pendientes.
- Depende de: T-20
- Criterio de aceptación (cómo compruebo a mano que está listo): cada ajuste marcado como hecho es visible en la app. Cada ajuste no hecho tiene una razón anotada.
- Fuera de este ticket: funcionalidades nuevas o deseables.
- Responsable: (en blanco)
- Estado: pendiente

### T-22 — Publicación final y verificación
- Pantalla / archivo: Community Cloud, `README.md`
- Qué hay que hacer: confirmar que la app desplegada usa la última versión del repositorio. Agregar al README la URL pública y las instrucciones para correrla en local. Recorrer el flujo completo una vez más en la URL pública.
- Depende de: T-19, T-21
- Criterio de aceptación (cómo compruebo a mano que está listo): desde un navegador sin sesión abro la URL del README y completo el recorrido de Valentina (Indie → «Prioriza Latinoamérica» → evidencia → regreso) sin errores. La app no supera ~1 GB de RAM.
- Fuera de este ticket: funcionalidades nuevas.
- Responsable: (en blanco)
- Estado: pendiente

---

## Deseables (solo si sobra tiempo, no son parte del MVP)

Estos están en el documento de funcionalidades como deseables. Conviértanlos en tickets con el mismo formato solo si terminan T-22 antes de tiempo:
- Pantalla «Acerca de los datos».
- Tendencia de los últimos 30 días.
- Comparar dos géneros.
- Descargar la recomendación en PDF.
