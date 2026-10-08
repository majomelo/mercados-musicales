"""Mercados Musicales — app Streamlit (tickets T-02 a T-05)."""

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Mercados Musicales", layout="wide")


@st.cache_data
def cargar_datos() -> pd.DataFrame:
    """Lee la tabla precalculada (40 filas). Cacheada para no releer al recargar."""
    return pd.read_csv("data/resultados_app.csv")


# --- Navegación (T-05): pantalla actual en session_state, inicia en P0 ---
if "pantalla" not in st.session_state:
    st.session_state.pantalla = "P0"


def ir_a(pantalla: str) -> None:
    st.session_state.pantalla = pantalla


def pantalla_inicio() -> None:
    st.title("Mercados Musicales")
    st.write("Hola mundo: app para decidir en qué región promover un género musical.")
    df = cargar_datos()
    # T-04: muestra temporal del número de filas.
    st.caption(f"{len(df)} filas")
    st.subheader("P0 · Inicio (provisional)")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Ir a P1 Recomendación [provisional]"):
            ir_a("P1")
    with col2:
        if st.button("Ir a P3 Ranking [provisional]"):
            ir_a("P3")
    if st.button("Ir a P2 Evidencia [provisional]"):
        ir_a("P2")


def pantalla_recomendacion() -> None:
    st.title("P1 · Recomendación (provisional)")
    st.write("Hola mundo: aquí irá la región recomendada para el género elegido.")
    df = cargar_datos()
    st.caption(f"{len(df)} filas")
    if st.button("Ir a P2 Evidencia [provisional]"):
        ir_a("P2")
    if st.button("Ir a P0 Inicio [provisional]"):
        ir_a("P0")
    if st.button("Ir a P3 Ranking [provisional]"):
        ir_a("P3")


def pantalla_evidencia() -> None:
    st.title("P2 · Evidencia (provisional)")
    st.write("Hola mundo: aquí irá qué tan segura es la recomendación.")
    df = cargar_datos()
    st.caption(f"{len(df)} filas")
    if st.button("Ir a P1 Recomendación [provisional]"):
        ir_a("P1")
    if st.button("Ir a P0 Inicio [provisional]"):
        ir_a("P0")
    if st.button("Ir a P3 Ranking [provisional]"):
        ir_a("P3")


def pantalla_ranking() -> None:
    st.title("P3 · Ranking por región (provisional)")
    st.write("Hola mundo: aquí irá el ranking de géneros de la región elegida.")
    df = cargar_datos()
    st.caption(f"{len(df)} filas")
    if st.button("Ir a P1 Recomendación [provisional]"):
        ir_a("P1")
    if st.button("Ir a P0 Inicio [provisional]"):
        ir_a("P0")
    if st.button("Ir a P2 Evidencia [provisional]"):
        ir_a("P2")


# Enrutador principal
if st.session_state.pantalla == "P0":
    pantalla_inicio()
elif st.session_state.pantalla == "P1":
    pantalla_recomendacion()
elif st.session_state.pantalla == "P2":
    pantalla_evidencia()
elif st.session_state.pantalla == "P3":
    pantalla_ranking()
else:
    st.session_state.pantalla = "P0"
    pantalla_inicio()
