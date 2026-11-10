# Especificación de diseño visual — Mercados Musicales · Spotify 2024

> **Alcance exclusivo:** diseño de interfaz, composición, identidad visual, componentes, estados, responsive y criterios de fidelidad. No incluye lógica, algoritmos, procesamiento de datos, API ni arquitectura.

## 1. Objetivo visual

Reproducir con alta fidelidad la aplicación web de los mockups: un dashboard editorial de análisis musical con identidad inspirada en Spotify, estética limpia, contemporánea y amable, dominada por verde esmeralda, verde menta, blanco, superficies suaves y tipografía sans serif. La jerarquía es clara: encabezados contundentes, resultados destacados, gráficos legibles y navegación lateral discreta.

**Regla esencial:** los círculos rojos con números de las capturas son anotaciones externas y **NO deben aparecer** en el aplicativo. Tampoco deben aparecer las páginas de presentación, los textos explicativos externos en serif, ni etiquetas como «RECORRIDO · PASO 3 DE 3», «CAMINO SECUNDARIO» o «CAMINOS ALTERNATIVOS». Solo se replica la UI interna de las capturas.

## 2. Referencias y pantallas a reproducir

1. **Inicio:** selector de dos recorridos, «Tengo un género → ¿dónde lo promuevo?» y «Tengo un mercado → ¿qué géneros funcionan allí?».
2. **Recomendación por género:** sidebar con selector de género, recomendación protagonista, indicador de evidencia y gráfico horizontal de afinidad regional.
3. **Evidencia de recomendación:** sidebar de retorno y género, titular explicativo, indicador de evidencia y gráfico de puntos con intervalos horizontales.
4. **Ranking por región:** sidebar con región, titular del género líder y ranking de barras horizontales de streams promedio por registro.
5. **Variantes y estados:** recomendación sin región dominante, evidencia baja, alerta por muestra pequeña, entradas inválidas, ausencia de selección y retorno.

Las pantallas 3–5 aparecen dentro de diapositivas explicativas: reconstruir únicamente la interfaz que aparece incrustada, no la diapositiva completa.

## 3. Sistema de diseño

### 3.1 Paleta

Los siguientes valores HEX son **aproximaciones visuales** a partir de las capturas; afinar comparando con las imágenes originales.

| Token | HEX sugerido | Aplicación |
|---|---|---|
| `--green-primary` | `#00C96B` | Acciones principales, acentos, barras ganadoras |
| `--green-bright` | `#25E68D` | Gradientes, botones redondos y resaltes |
| `--green-deep` | `#007A4B` | Títulos resaltados y textos verdes |
| `--green-dark` | `#103A2F` | Panel oscuro destacado en inicio |
| `--mint-100` | `#E6FAF1` | Fondos de iconos, chips, secciones |
| `--mint-200` | `#CEF6E5` | Capas decorativas y fondos |
| `--canvas` | `#F3FBF7` | Fondo general |
| `--surface` | `#FFFFFF` | Navbar, sidebar, tarjetas, gráficos |
| `--ink` | `#10191D` | Titulares y valores |
| `--text-secondary` | `#626D73` | Descripciones, ayuda y metadatos |
| `--chart-neutral` | `#D0D2D4` | Barras no seleccionadas |
| `--chart-dot` | `#667078` | Puntos e intervalos secundarios |
| `--border` | `#E5EDE9` | Bordes sutiles |
| `--warning` | `#E5A33E` | Advertencia de evidencia baja |
| `--warning-bg` | `#FFF4DC` | Fondo de advertencia |

**Gradientes:** hero de resultados `linear-gradient(110deg, #F0FFF8 0%, #D8FAE9 58%, #B9F4D8 100%)`; botón principal `linear-gradient(100deg, #00B862, #27E68A)`; fondo general con manchas de menta translúcidas y suaves. No usar colores chillones fuera de esta familia.

### 3.2 Tipografía

- Interfaz: **Inter** o una sans serif geométrica similar (fallback: `Arial, sans-serif`). No utilizar serif en la aplicación.
- Marca: 16–18 px, peso 700–800.
- Titular de inicio: 48–58 px desktop, peso 800–900, interlineado 1.05–1.12.
- Titular de recomendación: 48–58 px desktop, peso 800–900, interlineado 1.05–1.12.
- Titular en vistas compactas: 30–42 px, peso 800.
- Títulos de gráficos: 20–24 px, peso 700–800.
- Texto de botones principales: 19–24 px, peso 700.
- Texto general: 15–18 px, peso 400–500.
- Etiquetas y metadatos: 12–14 px, peso 400–600.
- Valores de gráficos: 14–16 px, peso 700.
- Resaltar **solo** la palabra o región clave en verde; mantener el resto del titular casi negro.

### 3.3 Espaciado, bordes y sombras

- Escala de espaciado: 4, 8, 12, 16, 20, 24, 32, 40, 48 y 64 px.
- Contenedor máximo de contenido: 1440 px; padding horizontal desktop: 24–40 px.
- Navbar: borde muy redondeado, 20–36 px de radio, altura 60–72 px.
- Tarjetas principales: radio 16–22 px.
- Botones circulares: 52–64 px de diámetro.
- Inputs: radio 7–10 px.
- Sombras suaves, difusas y de poca opacidad: `0 12px 35px rgba(17,64,43,.07)`.
- Bordes discretos de 1 px o ausentes; evitar contornos gruesos salvo en botón secundario delineado.
- Mucho espacio en blanco y separación clara entre secciones.

### 3.4 Recursos gráficos

- Logo circular verde de Spotify con ondas blancas a la izquierda de la marca. Usar un recurso vectorial autorizado, no un emoji.
- Fotografía de público en concierto, monocromática o teñida de verde, con manos levantadas y alto contraste, dentro de un recorte curvo/circular en la esquina derecha de los banners.
- Decoración: círculos de gran radio recortados en los bordes, ondas semicirculares y columnas verticales que evocan un ecualizador de música.
- Iconos de línea sencillos: nota musical, barras de ranking, flechas hacia la derecha e izquierda, globo, información, advertencia y cursor. Usar un conjunto consistente (p. ej., Lucide).
- Los recursos decorativos nunca deben competir con los datos ni impedir la lectura.

## 4. Estructura global de las pantallas

### 4.1 Barra superior

En todas las vistas aparece una barra blanca flotante con esquinas redondeadas, casi a todo el ancho, con margen superior y lateral.

- **Izquierda:** logo Spotify verde + «Mercados Musicales · Spotify 2024» en negrita.
- **Centro:** nombre de la vista: «Inicio», «Recomendación por género», «Evidencia de la recomendación» o «Ranking por región».
- **Derecha:** «Acerca de los datos» en gris y pequeño icono de información circular.
- La pestaña central activa tiene una pequeña línea horizontal verde debajo.
- Alineación vertical centrada; espaciado amplio; la barra no debe verse como menú denso.
- En la pantalla inicial, el indicador central es «Inicio».

### 4.2 Fondo y contenedores

Fondo casi blanco con ligero tinte verde. Figuras geométricas grandes verde menta y transparencias en esquinas. El contenido vive sobre superficies blancas, con márgenes generosos. En pantallas internas, composición de **dos columnas**: sidebar izquierda de aproximadamente 25–27 % y panel principal de aproximadamente 73–75 %, con gap de 24–30 px. En el mockup de referencia, la sidebar es un panel blanco alto con bordes redondeados y el área derecha contiene banner de resultado y tarjeta de gráfico.

## 5. Pantalla A — Inicio

### Composición

- Barra superior flotante a 24–28 px de los lados.
- Área principal centrada horizontalmente y situada en la zona media-alta.
- Titular grande: «¿Qué quieres **decidir hoy**?»; las palabras «decidir hoy» aparecen en verde oscuro/gradiente verde.
- Subtítulo gris centrado: «Elige el punto de partida de tu decisión de promoción.»
- Debajo, dos tarjetas de elección horizontales apiladas, ancho aproximado de 790–850 px, altura 120–130 px y separación 22–26 px.

### Primera tarjeta

- Fondo verde casi negro con leve gradiente y formas verdes semitransparentes a la derecha.
- Icono de nota musical verde brillante sobre cuadrado verde oscuro redondeado a la izquierda.
- Texto: «Tengo un género» seguido de flecha fina verde y «¿dónde lo promuevo?» en blanco.
- Extremo derecho: botón circular verde brillante con flecha negra hacia la derecha.
- Sombra tenue; texto grande y contundente; apariencia de opción protagonista.

### Segunda tarjeta

- Fondo blanco y sombra suave.
- Icono de tres barras ascendentes verde oscuro sobre cuadrado menta claro.
- Texto: «Tengo un mercado» seguido de flecha verde y «¿qué géneros funcionan allí?» en gris oscuro.
- Extremo derecho: círculo menta pálido con flecha verde.

### Decoración específica

- Lado izquierdo: dos tarjetas de portada musical inclinadas, parcialmente fuera de pantalla; una con retrato/silueta verde y otra con paisaje montañoso verde, ambas con pequeño logo Spotify.
- Lado derecho: gran recorte circular de fotografía de concierto verde.
- Ecualizadores verticales decorativos a izquierda y derecha.
- Círculos menta muy claros parcialmente cortados en bordes.
- Pie inferior centrado, muy pequeño y gris: «Basado en 500 registros de Spotify 2024 agrupados en 4 regiones · Datos sintéticos (Kaggle, licencia Apache 2.0)».
- El pie puede tener líneas horizontales finas a sus lados.

## 6. Pantalla B — Recomendación por género

### Sidebar

Panel blanco vertical con esquinas redondeadas.

1. Arriba: flecha izquierda y texto «Inicio».
2. Etiqueta gris «Género».
3. Selector blanco con borde gris suave, opción visible «Indie» y chevrón descendente oscuro.
4. Separador horizontal fino.
5. Etiqueta gris «Segunda opción».
6. Texto «Anglosajón (afinidad 97)».
7. Cerca del pie: botón secundario de ancho completo «Ver evidencia →», fondo blanco, borde oscuro de 1.5–2 px, radio pequeño, texto centrado en negrita.
8. Debajo: acceso con icono de globo y texto gris «Explorar por región».

Los elementos inferiores deben quedar cerca del fondo del panel en escritorio, sin que la sidebar parezca una lista amontonada.

### Banner principal

- Rectángulo ancho con radio 16–20 px, altura aproximada de 220–240 px en escritorio.
- Fondo menta luminoso con gradiente y capas circulares verdes suaves.
- A la derecha, imagen de concierto en recorte de curva grande.
- A la izquierda, titular: «Prioriza **Latinoamérica**», con «Latinoamérica» en verde intenso.
- Debajo: «Indie tiene +34 % de streams por registro frente a su promedio global».
- Debajo: chip horizontal blanco/translúcido con borde verde menta, sombra suave e icono de barras verdes. Texto: «**Evidencia alta** · mejor región en 93 % de 5.000 escenarios simulados».
- Banner con jerarquía: titular primero, afirmación numérica segundo, evidencia tercero.

### Tarjeta de gráfico

- Tarjeta blanca grande debajo del banner, con radio 18–20 px y padding generoso.
- Encabezado a la izquierda: «Índice de afinidad por región».
- Nota superior derecha en gris: «promedio del género = 100».
- Gráfico horizontal de cuatro barras, con etiquetas de región a la izquierda y valores al final.
- Orden y valores visibles de la referencia:

| Región | Afinidad | Registros | Estilo |
|---|---:|---:|---|
| Latinoamérica | 134 | 7 | Verde brillante |
| Anglosajón | 97 | 14 | Gris neutro |
| Europa continental | 95 | 21 | Gris neutro |
| Asia | 89 | 8 | Gris neutro |

- Las barras tienen extremos ligeramente redondeados y altura 40–46 px; separación vertical de unos 20–24 px.
- Línea vertical de referencia discontinua en el valor 100, gris oscuro sutil.
- Al final de cada barra: número en negrita y `(n=...)` en gris.
- La barra ganadora debe resaltar sin usar un color distinto para cada categoría.
- No incluir leyenda innecesaria ni cuadrículas intensas.

## 7. Pantalla C — Evidencia de la recomendación

### Sidebar

- Mismo panel blanco y proporciones que en recomendación.
- Enlace superior «← Volver a la recomendación».
- Etiqueta «Género» y selector «Indie».
- Espacio inferior despejado; se permite una decoración de ecualizador menta y círculos translúcidos cerca de la base.

### Banner

- Misma identidad de banner verde menta con fotografía de concierto recortada a la derecha.
- Titular en dos líneas: «¿Qué tan segura es la recomendación para **Indie**?».
- Texto explicativo: «Latinoamérica es la mejor región en 93 % de los escenarios simulados · evidencia alta».
- Chip con barras verdes y texto «Evidencia alta · mejor región en 93 % de 5.000 escenarios simulados».
- En pantallas estrechas, permitir tres líneas de titular sin superponerlo a la imagen.

### Gráfico de evidencia

- Tarjeta blanca debajo del banner.
- Título: «Índice de afinidad por región».
- Gráfico horizontal de **puntos e intervalos**, no de barras sólidas.
- Eje X con escala aproximada 70–160 y título «Índice de afinidad (intervalo del 90 %)».
- Línea vertical de referencia en 100.
- Cada fila tiene: nombre de región a la izquierda, segmento horizontal de intervalo y punto central de afinidad.
- Latinoamérica: segmento verde brillante con punto verde grande alrededor de 134; el intervalo se muestra completamente a la derecha de 100.
- Anglosajón, Europa continental y Asia: segmentos y puntos grises, alrededor de 97, 95 y 89 respectivamente, con intervalos que cruzan o se aproximan a 100.
- A la derecha de cada fila, texto pequeño: «mejor región en 93 % · n=7», «mejor región en 4 % · n=14», «mejor región en 2 % · n=21», «mejor región en 1 % · n=8».
- Espaciado amplio entre filas, ejes discretos, línea base fina y valores bien alineados.
- Debajo: pequeña nota informativa con icono `i` circular: «Cómo leerlo: el punto es la afinidad observada; la línea, el rango en el 90 % de los 5.000 remuestreos. Si la línea cruza 100, la región no se distingue claramente del promedio del género.»
- Nota final pequeña y gris: «Datos sintéticos (Kaggle, Apache 2.0). Resultados exploratorios, no representan el mercado real.»

## 8. Pantalla D — Ranking por región

### Sidebar

- Enlace «← Inicio».
- Etiqueta «Región» y selector blanco «Latinoamérica».
- Texto de ayuda con icono de cursor/mano: «Toca un género para ver en qué región conviene promoverlo».
- Aviso con triángulo: «△ = menos de 5 registros; interpretar con cautela».
- Decoración de ecualizador menta y círculos transparentes en la parte inferior.

### Banner

- Fondo gradiente menta con foto de concierto a la derecha.
- Titular de dos líneas: «En Latinoamérica lidera **Indie**»; «Indie» en verde intenso.
- No necesita el chip de evidencia del recorrido por género.

### Gráfico de ranking

- Tarjeta blanca grande, título: «Promedio de Total Streams por registro (millones)».
- Barras horizontales ordenadas de mayor a menor.
- Primera barra verde brillante, las demás gris azulado pálido.
- Valores en formato numérico visible junto al extremo derecho de cada barra, con `n=` en gris.

| Género | Promedio (millones) | n |
|---|---:|---:|
| Indie | 3,559 | 7 |
| Pop | 2,911 | 12 |
| Jazz | 2,817 | 9 |
| Rock | 2,701 | 10 |
| K-pop | 2,698 | 11 |
| Classical | 2,558 | 10 |
| R&B | 2,400 | 4 |
| Hip Hop | 2,100 | 6 |
| EDM | 1,853 | 6 |
| Reggaeton | 1,610 | 6 |

- En la fila R&B mostrar símbolo de advertencia y texto `△ n<5` (además de `n=4`), con tratamiento visual discreto.
- Etiquetas de géneros alineadas a la izquierda; valores a la derecha, evitando que se monten sobre las barras.
- Las filas deben tener separación suficiente para leer las diez categorías.
- Las barras deben percibirse como opciones explorables mediante hover/focus, sin cambiar el estilo base.

## 9. Pantalla E — Variantes, estados y mensajes

### 9.1 Género sin región dominante (ejemplo Rock)

- Mantener exactamente la misma plantilla de recomendación por género: navbar, sidebar, banner y tarjeta de barras.
- En selector, «Rock».
- Sidebar: «Segunda opción: Anglosajón (afinidad 103)».
- Banner: «**Sin región dominante:** compara **Latinoamérica** y **Anglosajón**».
- Mensaje: «Rock tiene +6 % de streams por registro frente a su promedio global».
- Chip de evidencia en tono ámbar suave: «Evidencia baja · mejor región en 37 % de los 5.000 escenarios simulados».
- Gráfico: Latinoamérica 106 (n=10), Anglosajón 103 (n=13), Asia 102 (n=10), Europa continental 95 (n=25).
- Las dos primeras barras en verde, las restantes grises; evitar presentar una sola ganadora indiscutible.
- La jerarquía sigue siendo limpia y el mensaje es informativo, no alarmista.

### 9.2 Entrada escrita con error

- Si existe campo editable/autocompletado, mostrar sugerencia pequeña bajo el control, por ejemplo: «¿Quisiste decir Jazz?».
- Estilo de sugerencia: fondo blanco, borde sutil, icono de búsqueda o información y texto gris/verde.
- No convertir la sugerencia en un modal invasivo.

### 9.3 País escrito en vez de región

- Mostrar una indicación de equivalencia clara: «México → Latinoamérica».
- Puede aparecer como ayuda contextual o pequeña etiqueta verde menta junto al selector.

### 9.4 Género inexistente

- Mostrar un estado vacío contenido en tarjeta blanca: icono musical tenue, título «Género no disponible», descripción «Selecciona un género de la lista».
- Mantener la navegación y el control disponibles.

### 9.5 Pocos registros

- Mostrar advertencia compacta con triángulo ámbar cuando `n < 5`.
- Texto: «Menos de 5 registros · interpretar con cautela».
- No ocultar necesariamente la fila; conservar el dato con una advertencia visual evidente pero discreta.

### 9.6 Sin selección

- En panel de resultado: «Elige un género para ver la recomendación».
- Ilustración tenue o icono musical centrado, sin gráfico vacío que parezca contener resultados.

### 9.7 Navegación de retorno

- Los enlaces de retorno siempre aparecen en la esquina superior izquierda de la sidebar, con flecha izquierda y texto gris oscuro.
- Mantener misma altura y alineación entre pantallas para evitar saltos visuales.

## 10. Catálogo de componentes reutilizables

| Componente visual | Apariencia y reglas |
|---|---|
| `TopNavigation` | Barra blanca redondeada, logo/marca izquierda, sección activa centro, info derecha |
| `PageBackground` | Fondo blanco-menta con círculos y ecualizadores translúcidos |
| `JourneyCard` | Tarjeta grande de inicio; variante oscura y variante blanca |
| `SidebarPanel` | Panel blanco alto, radio 20 px, distribución vertical |
| `BackLink` | Flecha izquierda + texto pequeño |
| `FieldLabel` | Texto gris de 13–14 px |
| `SelectField` | Selector blanco, borde fino y chevrón |
| `ResultHero` | Banner menta, gran titular, fotografía de concierto recortada |
| `EvidenceChip` | Píldora blanca/menta o ámbar, icono de barras, texto compacto |
| `ChartCard` | Tarjeta blanca con título y visualización |
| `AffinityBar` | Barra horizontal con extremo redondeado, valor y n |
| `ReferenceLine` | Línea vertical discontinua gris en 100 |
| `ConfidenceIntervalRow` | Segmento horizontal y punto central con etiqueta de región |
| `RankingBarRow` | Género + barra + promedio + conteo + advertencia opcional |
| `OutlineButton` | Botón blanco, borde oscuro, texto centrado y flecha |
| `TextAction` | Enlace de texto gris con icono de globo |
| `InfoNote` | Icono de información y texto de apoyo discreto |
| `WarningNote` | Triángulo ámbar y texto legible |
| `EmptyState` | Icono suave, título y descripción sin datos |

**Consistencia:** no crear estilos independientes para el mismo componente en cada página. Usar el mismo radio, altura, tipografía, espaciado, iconos y sombra en todas las vistas.

## 11. Estados de interacción visual

- **Normal:** superficies y colores según referencia.
- **Hover en tarjeta:** elevar 2–3 px, aumentar sombra muy suavemente; no transformar excesivamente.
- **Hover en barra:** ligero aumento de contraste o fondo de fila menta muy tenue.
- **Focus:** anillo verde visible de 2–3 px alrededor del control, separado 2 px.
- **Active:** botón con ligero oscurecimiento, sin desplazamientos bruscos.
- **Disabled:** opacidad moderada, cursor coherente, mantener legibilidad.
- **Dropdown abierto:** lista blanca con sombra, radio 10 px, opción activa en menta y texto oscuro.
- **Tooltip gráfico:** tarjeta pequeña blanca con sombra, nombre de región/género, valor y n; texto legible.
- **Loading visual:** skeleton gris menta de los banners y barras, respetando dimensiones finales para evitar saltos.
- **Warning:** chip ámbar claro con texto oscuro, nunca solo cambio de color sin icono/texto.
- Transiciones de 150–220 ms, suaves, respetando `prefers-reduced-motion`.

## 12. Responsive

### Desktop grande (≥ 1200 px)

- Navbar completa en una sola línea.
- Inicio con tarjetas de máximo ~820 px y decoración lateral.
- Internas con sidebar 290–340 px y panel flexible.
- Banner con texto a la izquierda y foto a la derecha.
- Gráficos con etiquetas, valores y conteos alineados sin recortes.

### Laptop / tablet horizontal (900–1199 px)

- Sidebar 240–280 px; panel derecho flexible.
- Reducir títulos a 34–44 px.
- Banner más compacto; imagen de concierto ocupa menos espacio.
- Gráficos ajustan paddings y longitud de barras.

### Tablet vertical (600–899 px)

- Sidebar encima del contenido o en panel horizontal compacto; no forzar columnas estrechas.
- Navbar conserva marca y vista; «Acerca de los datos» puede pasar a icono con etiqueta accesible.
- Banner a ancho completo; foto como adorno en extremo derecho con opacidad/recorte controlados.
- Gráficos a ancho completo; permitir scroll horizontal interno solo si es indispensable.

### Móvil (< 600 px)

- Padding lateral de 16 px; tarjetas con radio 14–18 px.
- Inicio: titular 32–38 px, subtítulo 15–16 px; tarjetas de decisión apiladas con texto que puede ocupar dos líneas.
- Reducir/ocultar portadas musicales inclinadas y grandes círculos que estorben.
- Barra superior compacta; marca puede abreviarse visualmente sin perder identidad.
- Sidebar convertida en bloque superior con selector, retorno y acciones accesibles.
- Banner: titular 28–34 px, chip de evidencia adaptable a dos líneas; foto decorativa en área pequeña o detrás con contraste suficiente.
- Gráficos: etiquetas de regiones visibles, valores fuera de barras cuando sea posible; no reducir texto por debajo de 12 px.
- Ranking de diez filas: usar barras más compactas y un bloque de valores alineado; preservar legibilidad de R&B y su advertencia.
- Botones y controles con área táctil mínima de 44×44 px.

## 13. Accesibilidad visual

- Contraste mínimo objetivo WCAG AA: 4.5:1 para texto normal y 3:1 para texto grande e indicadores no textuales relevantes.
- El verde brillante no debe ser el único medio para transmitir «mejor»; incluir etiquetas, valores y/o iconos.
- Mantener foco visible en teclado.
- Iconos con etiqueta accesible cuando su significado no sea obvio.
- Decoraciones y fotografía de concierto son secundarias; nunca contienen información indispensable.
- Evitar texto blanco sobre menta muy clara; preferir tinta oscura.
- Los gráficos deben acompañarse de etiquetas y números visibles.
- Respetar zoom del navegador y tamaños de fuente aumentados.

## 14. Detalles de fidelidad que NO se deben omitir

1. Marca «Mercados Musicales · Spotify 2024» siempre visible en desktop.
2. Barra superior flotante blanca con pestaña activa subrayada en verde.
3. Fondo verde casi blanco, círculos translúcidos y pequeños ecualizadores decorativos.
4. Inicio con dos grandes rutas, primera oscura y segunda blanca.
5. Portadas musicales inclinadas solo como decoración del inicio.
6. Fotografía de concierto verdosa con recorte circular/curvo en los banners.
7. Sidebar blanca de altura generosa en pantallas internas.
8. Titulares grandes en negro con una región/género clave en verde.
9. Chip de evidencia en banner, con variante verde y variante ámbar.
10. Gráfico de afinidad con línea de referencia en 100.
11. Barra ganadora verde y barras restantes grises.
12. Etiquetas de `n=` junto a los valores de los gráficos.
13. Pantalla de evidencia con **puntos + intervalos**, no barras.
14. Ranking regional con diez géneros y advertencia visual para R&B.
15. Variante «Sin región dominante» con dos barras resaltadas.
16. Botón delineado «Ver evidencia →» al pie de la sidebar.
17. Enlace secundario «Explorar por región» con icono de globo.
18. Márgenes amplios, sombras muy suaves y superficies redondeadas.
19. Ausencia total de círculos rojos numerados y de textos externos de las diapositivas.
20. Diseño responsive sin superposiciones, truncamientos importantes ni pérdida de jerarquía.

## 15. Lo que NO debe agregarse

- Círculos rojos con números de las capturas.
- Títulos de diapositivas como «Revisa qué tan segura es», «¿Y si ya tengo un mercado?» o «Lo que un usuario nuevo preguntaría» fuera de la UI.
- Bloques explicativos serif de las presentaciones.
- Menús, tablas, paneles o indicadores no presentes en el diseño, salvo los estados visuales necesarios especificados aquí.
- Colores arcoíris en los gráficos, gradientes excesivos o estética neón.
- Fondos negros en las pantallas de análisis (el oscuro se reserva para la primera tarjeta del inicio).
- Bordes gruesos en todas las tarjetas.
- Animaciones llamativas, imágenes decorativas dominantes o efectos glassmorphism intensos.
- Elementos de marca no relacionados con la interfaz.

## 16. Checklist de aceptación visual

- [ ] Las cinco vistas/variantes reproducen el layout descrito.
- [ ] No aparecen círculos rojos numerados ni anotaciones de presentación.
- [ ] La navbar es consistente entre pantallas.
- [ ] Inicio presenta exactamente dos tarjetas de decisión, oscura y blanca.
- [ ] Sidebar, banner y gráfico conservan jerarquía y proporciones.
- [ ] Tipografía sans serif, pesos y tamaños coherentes.
- [ ] Colores, gradientes, sombras y radios siguen el sistema de diseño.
- [ ] Los gráficos tienen etiquetas, valores, `n=` y resaltados correctos.
- [ ] El gráfico de evidencia usa intervalos horizontales con puntos.
- [ ] El ranking regional muestra diez filas y advertencia en R&B.
- [ ] La variante Rock muestra «Sin región dominante» y evidencia baja.
- [ ] Estados vacíos, advertencias y ayudas mantienen el mismo lenguaje visual.
- [ ] No hay superposición entre textos, foto de concierto y adornos.
- [ ] Desktop, tablet y móvil conservan legibilidad.
- [ ] Los controles tienen foco visible y áreas táctiles adecuadas.

## 17. Instrucción de ejecución para un diseñador o asistente de código

**Implementa únicamente la capa visual de «Mercados Musicales · Spotify 2024» siguiendo esta especificación y las cinco capturas de referencia. Prioriza fidelidad visual sobre reinterpretación. Construye un sistema coherente de tokens, componentes reutilizables y layouts responsive. Reproduce inicio, recomendación por género, evidencia, ranking regional y variantes visuales. Mantén los textos y valores ilustrados como contenido de referencia para verificar el diseño. No agregues lógica de negocio, algoritmos, endpoints, bases de datos ni nuevas funcionalidades. No incluyas los círculos rojos numerados ni el contenido externo de las diapositivas.**

---

*Nota: las medidas, colores y proporciones son estimaciones visuales orientativas; la comparación lado a lado con los mockups originales tiene prioridad para el ajuste fino.*
