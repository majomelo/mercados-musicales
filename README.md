# Mercados Musicales

App en Streamlit que optimiza una decisión de promoción: compara cada región cultural con el promedio de su género (índice de afinidad) y simula 5.000 escenarios bootstrap para estimar la probabilidad de que cada región sea la mejor. Responde «¿En qué región lanzo el sencillo de Indie, y qué tan segura es esa elección?».

## Datos

- Base original: 500 registros sintéticos de Spotify 2024 (Kaggle, licencia Apache 2.0), agrupados en 4 regiones culturales: Latinoamérica, Anglosajón, Asia y Europa continental.
- Tabla `data/resultados_app.csv`: 40 filas (10 géneros × 4 regiones) precalculada para la app (sin recalcular el bootstrap en vivo).
- Datos sintéticos (Kaggle, Apache 2.0). Resultados exploratorios, no describen el mercado real.

### Columnas de `resultados_app.csv`

- `genero`: género musical (10 valores, ej. Indie, Hip Hop, Jazz).
- `region`: región cultural (Latinoamérica, Anglosajón, Asia, Europa continental).
- `afinidad`: índice de afinidad (100 = promedio del género; ej. 134 = +34 % frente al promedio).
- `prob_mejor`: probabilidad de ser la mejor región para ese género (0 a 1, las 4 regiones de cada género suman 1).
- `evidencia`: nivel de evidencia derivado de `prob_mejor` (Alta ≥ 0.70, Media 0.40–0.70, Baja < 0.40).
- `n_registros`: número de registros originales que respaldan la combinación género-región.
- `promedio_streams`: promedio de streams de la combinación género-región.
- `intervalo_inf` / `intervalo_sup`: límites del intervalo del 90 % de los escenarios simulados para la afinidad.

## Cómo correr en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Estructura

- `app.py`: interfaz Streamlit, navegación y pantallas (P0 Inicio, P1 Recomendación, P2 Evidencia, P3 Ranking por región).
- `pipeline.py`: funciones reutilizadas del notebook (`recomendar_region`, `nivel_evidencia`, `ranking_por_region`, `normalizar_entrada`).
- `data/resultados_app.csv`: tabla de 40 filas para la app.
