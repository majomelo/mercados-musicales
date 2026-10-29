"""Mercados Musicales — app Streamlit (tickets T-02 a T-19).

Responde «¿En qué región lanzo el sencillo de Indie, y qué tan segura es esa
elección?» comparando cada región cultural con el promedio de su género.
"""

from __future__ import annotations

import altair as alt
import pandas as pd
import streamlit as st

from pipeline import (
    GENEROS,
    REGIONES,
    nivel_evidencia,
    normalizar_entrada,
    ranking_por_region,
    recomendar_region,
)

st.set_page_config(
    page_title="Mercados Musicales",
    layout="wide",
)

# --- Paleta común (T-06) ---
VERDE = "#1DB954"
VERDE_SUAVE = "#E8F8EE"
GRIS = "#C4C4C4"
GRIS_OSCURO = "#6B6B6B"
TEXTO = "#191414"
FONDO = "#FFFFFF"
FUENTE = "Datos sintéticos (Kaggle, Apache 2.0). Resultados exploratorios."

st.markdown(
    f"""
    <style>
        html, body, [class*="css"] {{ color: {TEXTO}; }}
        .block-container {{ padding-top: 1.2rem; padding-bottom: 1rem; }}
        .mm-barra {{
            display: flex; align-items: center; justify-content: space-between;
            border-bottom: 1px solid #EEEEEE; padding-bottom: 0.4rem; margin-bottom: 1.2rem;
        }}
        .mm-marca {{ font-size: 1.05rem; font-weight: 700; letter-spacing: 0.2px; }}
        .mm-tarjeta {{
            border: 1px solid #EEEEEE; border-radius: 14px; padding: 1.4rem 1.6rem;
            box-shadow: 0 1px 4px rgba(0,0,0,0.05); background: {FONDO};
        }}
        .mm-titular {{ font-size: 30px; font-weight: 800; line-height: 1.15; margin: 0; }}
        .mm-titular-verde {{ color: {VERDE}; }}
        .mm-titular-gris {{ color: {TEXTO}; }}
        .mm-secundaria {{ font-size: 0.82rem; color: {GRIS_OSCURO}; text-transform: uppercase;
            letter-spacing: 0.6px; margin-bottom: 0.25rem; }}
        .mm-secundaria-valor {{ font-size: 1.05rem; font-weight: 600; }}
        .mm-dato {{ font-size: 1.05rem; margin-top: 0.55rem; }}
        .mm-evidencia {{ font-weight: 700; }}
        .mm-pie {{ border-top: 1px solid #EEEEEE; margin-top: 2.5rem; padding-top: 0.7rem;
            color: {GRIS_OSCURO}; font-size: 0.78rem; }}
        .mm-fila {{ display: flex; align-items: center; padding: 0.55rem 0.2rem;
            border-bottom: 1px solid #F2F2F2; }}
        .mm-genero {{ font-weight: 700; font-size: 1.02rem; }}
        .mm-lider {{ color: {VERDE}; }}
        .mm-streams {{ font-variant-numeric: tabular-nums; }}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def cargar_datos() -> pd.DataFrame:
    """Lee la tabla precalculada (40 filas). Cacheada para no releer al recargar."""
    return pd.read_csv("data/resultados_app.csv")


# --- Navegación (T-05 / T-18): pantalla actual + historial para «Volver» ---
if "pantalla" not in st.session_state:
    st.session_state.pantalla = "P0"
if "historial" not in st.session_state:
    st.session_state.historial = []
if "genero" not in st.session_state:
    st.session_state.genero = None
if "entrada_texto" not in st.session_state:
    st.session_state.entrada_texto = ""
if "flash" not in st.session_state:
    st.session_state.flash = None


def navegar(destino: str) -> None:
    """Cambia de pantalla guardando la anterior para el enlace «← Volver»."""
    actual = st.session_state.pantalla
    if actual != destino:
        st.session_state.historial.append(actual)
        st.session_state.pantalla = destino
    st.rerun()


def volver() -> None:
    historial = st.session_state.historial
    st.session_state.pantalla = historial.pop() if historial else "P0"
    st.rerun()


def abrir_recomendacion(genero: str | None = None) -> None:
    if genero:
        st.session_state.genero = genero
        st.session_state.sel_genero = genero
        st.session_state.entrada_texto = ""
    navegar("P1")


def porcentaje(valor: float) -> str:
    return f"{valor:+.0f} %"


def barra_superior(mostrar_volver: bool) -> None:
    """Barra común: marca, enlace de regreso y «Acerca de los datos» (T-06/T-19)."""
    izq, centro, der = st.columns([1, 4, 1.4])
    with izq:
        if mostrar_volver:
            if st.button("← Volver", key=f"volver_{st.session_state.pantalla}"):
                volver()
    with der:
        with st.popover("Acerca de los datos", width="stretch"):
            st.markdown(
                "**Mercados Musicales** compara 10 géneros en 4 regiones culturales "
                "(Latinoamérica, Anglosajón, Asia y Europa continental).\n\n"
                "- Base: 500 registros sintéticos de Spotify 2024 (Kaggle, Apache 2.0).\n"
                "- Índice de afinidad: 100 = promedio del género.\n"
                "- Probabilidad: 5.000 escenarios bootstrap precalculados.\n\n"
                "Los datos son sintéticos y los resultados son exploratorios: "
                "no describen el mercado real."
            )
    st.markdown("<div class='mm-barra'></div>", unsafe_allow_html=True)


def pie() -> None:
    st.markdown(f"<div class='mm-pie'>{FUENTE}</div>", unsafe_allow_html=True)


def mostrar_flash() -> None:
    if st.session_state.flash:
        st.info(st.session_state.flash)
        st.session_state.flash = None


# --- P0 · Inicio (T-07) ---
def pantalla_inicio() -> None:
    barra_superior(mostrar_volver=False)
    mostrar_flash()

    st.markdown("## ¿Qué quieres decidir hoy?")
    st.write(
        "Compara cada región cultural con el promedio de su género y descubre "
        "dónde lanzar tu sencillo con mayor afinidad."
    )

    col1, col2, _ = st.columns([1.1, 1.1, 2])
    with col1:
        if st.button("Tengo un género", type="primary", width="stretch"):
            abrir_recomendacion()
    with col2:
        if st.button("Tengo un mercado", width="stretch"):
            navegar("P3")

    st.write("")
    st.caption(
        "Ejemplo: «¿En qué región lanzo el sencillo de Indie, "
        "y qué tan segura es esa elección?»"
    )


def _cambiar_genero() -> None:
    st.session_state.genero = st.session_state.sel_genero
    st.session_state.entrada_texto = ""


def _aceptar_genero(valor: str) -> None:
    """Callback: aplica una sugerencia antes de que exista el selector."""
    st.session_state.genero = valor
    st.session_state.sel_genero = valor
    st.session_state.entrada_texto = ""


# --- P1 · Recomendación (T-08 a T-13) ---
def pantalla_recomendacion() -> None:
    barra_superior(mostrar_volver=True)
    mostrar_flash()

    filtros, resultados = st.columns([1, 2.4])

    with filtros:
        st.markdown("### Elige un género")
        if "sel_genero" not in st.session_state and st.session_state.genero:
            st.session_state.sel_genero = st.session_state.genero
        st.selectbox(
            "Género",
            GENEROS,
            index=None,
            key="sel_genero",
            placeholder="Elige un género",
            on_change=_cambiar_genero,
            label_visibility="collapsed",
        )
        with st.form("buscar_genero", clear_on_submit=False):
            texto = st.text_input(
                "O escribe un género, país o región",
                placeholder="Ej. Jaz, México, Asia",
            )
            buscar = st.form_submit_button("Buscar", width="stretch")
        if buscar:
            st.session_state.entrada_texto = texto

        st.caption("También puedes escribir «Indie», «Jaz» o un país como «México».")

    genero = None
    with resultados:
        entrada = (st.session_state.entrada_texto or "").strip()
        if entrada:
            norm = normalizar_entrada(entrada)
            tipo = norm["tipo"]

            if tipo in ("genero", "sugerencia"):
                valor = norm["valor"]
                if tipo == "sugerencia":
                    st.warning(norm["mensaje"])
                    st.button(
                        f"Sí, usar {valor}",
                        type="primary",
                        on_click=_aceptar_genero,
                        args=(valor,),
                    )
                    genero = None
                else:
                    genero = valor
                    st.session_state.genero = valor
            elif tipo == "region":
                region = norm["valor"]
                st.info(f"«{entrada}» corresponde a la región {region}.")
                if st.button(f"Ver ranking de {region}", type="primary"):
                    st.session_state.sel_region = region
                    st.session_state.entrada_texto = ""
                    navegar("P3")
                genero = None
            elif tipo == "vacio":
                st.info("Elige un género para ver la recomendación")
                genero = None
            else:
                st.error(norm["mensaje"])
                st.write(", ".join(norm["generos"]))
                genero = None
        else:
            genero = st.session_state.get("sel_genero") or st.session_state.get("genero")
            if not genero:
                st.info("Elige un género para ver la recomendación")

        if genero:
            _tarjeta_recomendacion(genero)
            st.write("")
            _grafico_afinidad(genero)
            st.write("")
            if st.button("Ver evidencia"):
                navegar("P2")


def _tarjeta_recomendacion(genero: str) -> None:
    rec = recomendar_region(genero)
    detalle = rec["detalle"]
    baja = rec["evidencia"] == "Baja"

    if baja:
        primera = detalle[0]["region"]
        segunda = detalle[1]["region"]
        titular = f"Sin región dominante, compara {primera} y {segunda}"
        clase = "mm-titular-gris"
    else:
        titular = f"Prioriza {rec['region_recomendada']}"
        clase = "mm-titular-verde"

    afinidad_txt = porcentaje(rec["afinidad"] - 100)
    segunda_txt = rec["segunda_opcion"] or "—"

    st.markdown(
        f"""
        <div class="mm-tarjeta">
          <div style="display:flex; gap:1.8rem; align-items:flex-start;">
            <div style="min-width:150px;">
              <div class="mm-secundaria">Segunda opción</div>
              <div class="mm-secundaria-valor">{segunda_txt}</div>
            </div>
            <div style="flex:1;">
              <div class="mm-titular {clase}">{titular}</div>
              <div class="mm-dato">{afinidad_txt} frente al promedio del género</div>
              <div class="mm-dato">Evidencia:
                <span class="mm-evidencia" style="color:{'' if baja else VERDE}">
                  {rec['evidencia']}
                </span>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    n = detalle[0]["n_registros"]
    if n < 5:
        st.warning("Pocos datos: interpreta este resultado con cautela.")


def _grafico_afinidad(genero: str) -> None:
    rec = recomendar_region(genero)
    detalle = rec["detalle"]
    baja = rec["evidencia"] == "Baja"
    recomendada = rec["region_recomendada"]

    filas = []
    for i, fila in enumerate(sorted(detalle, key=lambda d: d["afinidad"], reverse=True)):
        if baja:
            color = GRIS_OSCURO if i < 2 else GRIS
        else:
            color = VERDE if fila["region"] == recomendada else GRIS
        filas.append(
            {
                "region": fila["region"],
                "afinidad": fila["afinidad"],
                "color": color,
            }
        )
    df = pd.DataFrame(filas)
    orden = df["region"].tolist()
    tope = float(df["afinidad"].max()) + 30

    base = alt.Chart(df).encode(
        x=alt.X("region:N", sort=orden, title=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y(
            "afinidad:Q",
            title=None,
            scale=alt.Scale(domain=[0, tope]),
            axis=None,
        ),
    )
    barras = base.mark_bar(size=72, cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
        color=alt.Color("color:N", scale=None, legend=None),
    )
    etiquetas = base.mark_text(dy=-8, fontSize=14, fontWeight="bold").encode(
        text=alt.Text("afinidad:Q", format=".0f"),
        color=alt.Color("color:N", scale=None, legend=None),
    )
    referencia = (
        alt.Chart(pd.DataFrame({"valor": [100]}))
        .mark_rule(color=GRIS_OSCURO, strokeDash=[5, 4], strokeWidth=1.5)
        .encode(y="valor:Q")
    )

    st.altair_chart(
        (barras + etiquetas + referencia)
        .properties(height=300, padding={"top": 10})
        .configure_view(strokeWidth=0)
        .configure_axis(grid=False),
        width="stretch",
    )


# --- P2 · Evidencia (T-14 / T-15) ---
def pantalla_evidencia() -> None:
    barra_superior(mostrar_volver=True)
    mostrar_flash()

    genero = st.session_state.get("genero")
    if not genero:
        st.session_state.pantalla = "P1"
        st.rerun()
        return

    rec = recomendar_region(genero)
    detalle = rec["detalle"]
    recomendada = rec["region_recomendada"]

    st.markdown(f"## Evidencia · {genero}")
    st.write(
        "Cada punto es la afinidad de la región; la línea muestra el rango del 90 % "
        "de los 5.000 escenarios simulados."
    )

    grafico, datos = st.columns([2, 1])

    with grafico:
        filas = []
        for fila in detalle:
            filas.append(
                {
                    "region": fila["region"],
                    "afinidad": fila["afinidad"],
                    "intervalo_inf": fila["intervalo_inf"],
                    "intervalo_sup": fila["intervalo_sup"],
                    "color": VERDE if fila["region"] == recomendada else GRIS_OSCURO,
                }
            )
        df = pd.DataFrame(filas)
        orden = df["region"].tolist()
        eje_y = alt.Y("region:N", sort=orden, title=None, axis=alt.Axis(labelLimit=200))

        lineas = (
            alt.Chart(df)
            .mark_rule(strokeWidth=4, opacity=0.35)
            .encode(
                y=eje_y,
                x=alt.X("intervalo_inf:Q", title="Afinidad"),
                x2="intervalo_sup:Q",
                color=alt.Color("color:N", scale=None, legend=None),
            )
        )
        puntos = (
            alt.Chart(df)
            .mark_point(size=150, filled=True, stroke="#FFFFFF", strokeWidth=2)
            .encode(
                y=eje_y,
                x="afinidad:Q",
                color=alt.Color("color:N", scale=None, legend=None),
            )
        )
        etiquetas = (
            alt.Chart(df)
            .mark_text(dy=-14, fontSize=13, fontWeight="bold")
            .encode(
                y=eje_y,
                x="afinidad:Q",
                text=alt.Text("afinidad:Q", format=".0f"),
                color=alt.Color("color:N", scale=None, legend=None),
            )
        )
        referencia = (
            alt.Chart(pd.DataFrame({"valor": [100]}))
            .mark_rule(color=VERDE, strokeDash=[5, 4], strokeWidth=1.5)
            .encode(x="valor:Q")
        )

        st.altair_chart(
            (lineas + puntos + etiquetas + referencia)
            .properties(height=320)
            .configure_view(strokeWidth=0)
            .configure_axis(grid=False),
            width="stretch",
        )

    with datos:
        st.markdown("### Probabilidad de ser la mejor")
        for fila in detalle:
            color = VERDE if fila["region"] == recomendada else GRIS_OSCURO
            st.markdown(
                f"""
                <div class="mm-fila" style="justify-content:space-between;">
                  <span class="mm-genero" style="color:{color};">{fila['region']}</span>
                  <span class="mm-streams" style="font-weight:700;color:{color};">
                    {fila['prob_mejor'] * 100:.0f} %
                  </span>
                </div>
                <div class="mm-secundaria" style="margin:0.25rem 0 0.6rem 0;">
                  {fila['n_registros']} registros
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.info(
            "Si la línea cruza 100, esa región no se distingue del promedio del género."
        )


# --- P3 · Ranking por región (T-16 / T-17) ---
def pantalla_ranking() -> None:
    barra_superior(mostrar_volver=True)
    mostrar_flash()

    filtros, resultados = st.columns([1, 2.4])

    with filtros:
        st.markdown("### Elige una región")
        st.selectbox(
            "Región",
            REGIONES,
            index=None,
            key="sel_region",
            placeholder="Elige una región",
            label_visibility="collapsed",
        )
        st.caption("Si escribes un país, se traduce a su región cultural.")

    with resultados:
        region = st.session_state.get("sel_region")
        if not region:
            st.info("Elige una región para ver el ranking")
            return

        ranking = ranking_por_region(region)
        lider = ranking.iloc[0]["genero"]

        st.markdown(f"## Ranking · {region}")
        st.write(
            f"El género líder es **{lider}**. Toca un género para ver su recomendación."
        )

        encabezado = st.columns([2.2, 1.4, 1.1, 1.2])
        encabezado[0].caption("Género")
        encabezado[1].caption("Promedio de streams")
        encabezado[2].caption("Registros")
        encabezado[3].caption("")

        for _, fila in ranking.iterrows():
            genero = fila["genero"]
            n = int(fila["n_registros"])
            es_lider = genero == lider
            color = VERDE if es_lider else TEXTO
            c1, c2, c3, c4 = st.columns([2.2, 1.4, 1.1, 1.2])

            with c1:
                st.markdown(
                    f"<span class='mm-genero' style='color:{color};'>{genero}</span>",
                    unsafe_allow_html=True,
                )
                if n < 5:
                    st.caption("Pocos datos: interpreta con cautela.")
            with c2:
                st.markdown(
                    f"<span class='mm-streams'>{fila['promedio_streams']:,.0f}</span>",
                    unsafe_allow_html=True,
                )
            with c3:
                st.markdown(f"<span class='mm-streams'>{n}</span>", unsafe_allow_html=True)
            with c4:
                if st.button("Ver recomendación", key=f"ir_{genero}", width="stretch"):
                    abrir_recomendacion(genero)


# --- Enrutador principal (T-18) ---
PANTALLAS = {
    "P0": pantalla_inicio,
    "P1": pantalla_recomendacion,
    "P2": pantalla_evidencia,
    "P3": pantalla_ranking,
}

pantalla = st.session_state.pantalla
if pantalla not in PANTALLAS:
    st.session_state.pantalla = "P0"
    pantalla = "P0"

PANTALLAS[pantalla]()
pie()

