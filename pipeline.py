"""Pipeline de Mercados Musicales.

Funciones ya probadas en el notebook; se reutilizan sin reescribir.
Lee la tabla precalculada ``data/resultados_app.csv`` (40 filas).
"""

from __future__ import annotations

import difflib
from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).parent / "data" / "resultados_app.csv"

GENEROS = [
    "Indie",
    "Hip Hop",
    "Jazz",
    "Rock",
    "R&B",
    "Reggaeton",
    "Pop",
    "Electronic",
    "Classical",
    "Country",
]

REGIONES = ["Latinoamérica", "Anglosajón", "Asia", "Europa continental"]

# País (minúsculas, sin tildes) -> región. Solo para normalizar entradas.
PAIS_A_REGION = {
    # Latinoamérica
    "mexico": "Latinoamérica",
    "colombia": "Latinoamérica",
    "argentina": "Latinoamérica",
    "peru": "Latinoamérica",
    "chile": "Latinoamérica",
    "brasil": "Latinoamérica",
    "venezuela": "Latinoamérica",
    "ecuador": "Latinoamérica",
    # Anglosajón
    "usa": "Anglosajón",
    "estados unidos": "Anglosajón",
    "united states": "Anglosajón",
    "reino unido": "Anglosajón",
    "uk": "Anglosajón",
    "canada": "Anglosajón",
    "australia": "Anglosajón",
    # Asia
    "china": "Asia",
    "japon": "Asia",
    "japan": "Asia",
    "corea": "Asia",
    "india": "Asia",
    # Europa continental
    "espana": "Europa continental",
    "españa": "Europa continental",
    "francia": "Europa continental",
    "alemania": "Europa continental",
    "italia": "Europa continental",
    "portugal": "Europa continental",
}

_df_cache: pd.DataFrame | None = None


def _cargar_tabla() -> pd.DataFrame:
    global _df_cache
    if _df_cache is None:
        _df_cache = pd.read_csv(DATA_PATH)
    return _df_cache


def nivel_evidencia(probabilidad: float) -> str:
    """Devuelve Alta (>=70 %), Media (40-70 %) o Baja (<40 %).

    Acepta probabilidad en 0-1 o en 0-100.
    """
    p = float(probabilidad)
    if p > 1:
        p = p / 100.0
    if p >= 0.70:
        return "Alta"
    if p >= 0.40:
        return "Media"
    return "Baja"


def normalizar_entrada(texto: str | None) -> dict:
    """Normaliza texto libre a género o región válida.

    Devuelve un dict con tipo: genero | region | sugerencia | lista | vacio.
    """
    if texto is None or str(texto).strip() == "":
        return {
            "tipo": "vacio",
            "mensaje": "Elige un género para ver la recomendación",
            "generos": GENEROS,
        }

    t = str(texto).strip()
    t_low = t.lower()

    # Coincidencia exacta insensible a mayúsculas para géneros.
    for g in GENEROS:
        if t_low == g.lower():
            return {"tipo": "genero", "valor": g}

    # Coincidencia exacta para regiones.
    for r in REGIONES:
        if t_low == r.lower():
            return {"tipo": "region", "valor": r}

    # País -> región.
    import unicodedata

    def _sin_tildes(s: str) -> str:
        return "".join(
            c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
        )

    t_norm = _sin_tildes(t_low).strip()
    if t_norm in PAIS_A_REGION:
        return {"tipo": "region", "valor": PAIS_A_REGION[t_norm]}

    # Sugerencia por cercanía (error de escritura), ej. "Jaz" -> Jazz.
    # Cutoff 0.75: permite "Jaz"->"Jazz" (0.86) pero no "Salsa"->"Asia".
    candidatos = GENEROS + REGIONES
    candidatos_low = [c.lower() for c in candidatos]
    cerca = difflib.get_close_matches(t_low, candidatos_low, n=1, cutoff=0.75)
    if cerca:
        original = candidatos[candidatos_low.index(cerca[0])]
        if original in GENEROS:
            return {
                "tipo": "sugerencia",
                "mensaje": f"¿Quisiste decir {original}?",
                "valor": original,
            }
        return {
            "tipo": "sugerencia",
            "mensaje": f"¿Quisiste decir {original}?",
            "valor": original,
        }

    # Género inexistente -> lista de disponibles.
    return {
        "tipo": "lista",
        "mensaje": "Género no encontrado. Elige uno de la lista:",
        "generos": GENEROS,
    }


def recomendar_region(genero: str) -> dict:
    """Recomienda la región para un género.

    Devuelve región recomendada, afinidad, probabilidad, evidencia y segunda opción,
    más el detalle por región (afinidad, intervalo 90 %, probabilidad, registros).
    """
    df = _cargar_tabla()
    norm = normalizar_entrada(genero)
    if norm["tipo"] == "genero":
        genero_ok = norm["valor"]
    elif norm["tipo"] == "sugerencia" and norm.get("valor") in GENEROS:
        genero_ok = norm["valor"]
    else:
        raise ValueError(norm.get("mensaje", "Género no válido"))

    sub = df[df["genero"] == genero_ok].copy()
    if sub.empty:
        raise ValueError(f"Género no encontrado: {genero_ok}")
    sub = sub.sort_values("prob_mejor", ascending=False).reset_index(drop=True)

    top = sub.iloc[0]
    segunda = sub.iloc[1] if len(sub) > 1 else None
    evidencia = nivel_evidencia(float(top["prob_mejor"]))

    detalle = []
    for _, fila in sub.iterrows():
        detalle.append(
            {
                "region": fila["region"],
                "afinidad": float(fila["afinidad"]),
                "prob_mejor": float(fila["prob_mejor"]),
                "evidencia": str(fila["evidencia"]),
                "n_registros": int(fila["n_registros"]),
                "promedio_streams": float(fila["promedio_streams"]),
                "intervalo_inf": float(fila["intervalo_inf"]),
                "intervalo_sup": float(fila["intervalo_sup"]),
            }
        )

    return {
        "genero": genero_ok,
        "region_recomendada": str(top["region"]),
        "afinidad": float(top["afinidad"]),
        "prob_mejor": float(top["prob_mejor"]),
        "evidencia": evidencia,
        "segunda_opcion": str(segunda["region"]) if segunda is not None else None,
        "detalle": detalle,
    }


def ranking_por_region(region: str) -> pd.DataFrame:
    """Devuelve el ranking de géneros de una región con promedio y registros."""
    df = _cargar_tabla()
    norm = normalizar_entrada(region)
    if norm["tipo"] == "region":
        region_ok = norm["valor"]
    elif norm["tipo"] == "sugerencia" and norm.get("valor") in REGIONES:
        region_ok = norm["valor"]
    else:
        raise ValueError("Región no válida. Elige una de: " + ", ".join(REGIONES))

    sub = df[df["region"] == region_ok].copy()
    sub = sub.sort_values("promedio_streams", ascending=False).reset_index(drop=True)
    return sub[["genero", "promedio_streams", "n_registros", "afinidad", "prob_mejor"]]
