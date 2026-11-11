"""Pipeline de Mercados Musicales.

Funciones del notebook del proyecto (PROYECTO_ANALITICA_APLICADA_Entrega3.ipynb),
reutilizadas en la app. Lee la tabla precalculada ``data/resultados_app.csv``
(40 filas = 10 géneros x 4 regiones), que el notebook genera con el índice de
afinidad y 5.000 remuestreos bootstrap (semilla 42).
"""

from __future__ import annotations

import difflib
import unicodedata
from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).parent / "data" / "resultados_app.csv"

# Los 10 géneros de la base Spotify 2024 (mismos nombres que la columna Genre).
GENEROS = [
    "Indie",
    "Hip Hop",
    "EDM",
    "Jazz",
    "K-pop",
    "Pop",
    "R&B",
    "Reggaeton",
    "Classical",
    "Rock",
]

REGIONES = ["Latinoamérica", "Anglosajón", "Asia", "Europa continental"]

# Solo los 20 países que existen en la base, en español y en inglés.
# Un país que no está en la base (p. ej. Colombia) no se traduce: la app
# muestra la lista de opciones, porque no hay datos que lo respalden.
PAIS_A_REGION = {
    # Anglosajón
    "estados unidos": "Anglosajón", "united states": "Anglosajón", "usa": "Anglosajón",
    "canada": "Anglosajón",
    "reino unido": "Anglosajón", "united kingdom": "Anglosajón", "uk": "Anglosajón",
    "australia": "Anglosajón",
    "sudafrica": "Anglosajón", "south africa": "Anglosajón",
    # Latinoamérica
    "mexico": "Latinoamérica",
    "brasil": "Latinoamérica", "brazil": "Latinoamérica",
    "argentina": "Latinoamérica",
    # Asia
    "corea del sur": "Asia", "corea": "Asia", "south korea": "Asia",
    "japon": "Asia", "japan": "Asia",
    "indonesia": "Asia",
    "india": "Asia",
    # Europa continental
    "italia": "Europa continental", "italy": "Europa continental",
    "espana": "Europa continental", "spain": "Europa continental",
    "francia": "Europa continental", "france": "Europa continental",
    "alemania": "Europa continental", "germany": "Europa continental",
    "paises bajos": "Europa continental", "holanda": "Europa continental",
    "netherlands": "Europa continental",
    "suecia": "Europa continental", "sweden": "Europa continental",
    "rusia": "Europa continental", "russia": "Europa continental",
    "turquia": "Europa continental", "turkey": "Europa continental",
}

# Variantes frecuentes de escritura (clave ya limpia, ver _clave).
ALIAS = {
    "kpop": "K-pop",
    "hiphop": "Hip Hop",
    "rap": "Hip Hop",
    "rnb": "R&B",
    "randb": "R&B",
    "regueton": "Reggaeton",
    "reggeaton": "Reggaeton",
    "electronica": "EDM",
    "clasica": "Classical",
    "musicaclasica": "Classical",
    "latam": "Latinoamérica",
    "latinoamerica": "Latinoamérica",
    "americalatina": "Latinoamérica",
    "anglo": "Anglosajón",
    "europa": "Europa continental",
}

_df_cache: pd.DataFrame | None = None


def _cargar_tabla() -> pd.DataFrame:
    global _df_cache
    if _df_cache is None:
        _df_cache = pd.read_csv(DATA_PATH)
    return _df_cache


def _sin_tildes(texto: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn"
    )


def _clave(texto: str) -> str:
    """Minúsculas, sin tildes y solo letras y números ('Hip-Hop' -> 'hiphop')."""
    return "".join(c for c in _sin_tildes(str(texto).lower()) if c.isalnum())


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
    clave = _clave(t)

    # Coincidencia ignorando mayúsculas, tildes, espacios y guiones.
    for g in GENEROS:
        if clave == _clave(g):
            return {"tipo": "genero", "valor": g}
    for r in REGIONES:
        if clave == _clave(r):
            return {"tipo": "region", "valor": r}

    # Variantes conocidas (kpop, hip-hop, reguetón, latam...).
    if clave in ALIAS:
        valor = ALIAS[clave]
        return {"tipo": "genero" if valor in GENEROS else "region", "valor": valor}

    # País de la base -> su región.
    pais = _sin_tildes(t.lower()).strip()
    if pais in PAIS_A_REGION:
        return {"tipo": "region", "valor": PAIS_A_REGION[pais]}

    # Sugerencia por cercanía (error de escritura), ej. "Jaz" -> Jazz.
    # Cutoff 0.75: permite "Jaz"->"Jazz" (0.86) pero no "Salsa"->"Asia".
    candidatos = GENEROS + REGIONES
    candidatos_low = [c.lower() for c in candidatos]
    cerca = difflib.get_close_matches(t.lower(), candidatos_low, n=1, cutoff=0.75)
    if cerca:
        original = candidatos[candidatos_low.index(cerca[0])]
        return {
            "tipo": "sugerencia",
            "mensaje": f"¿Quisiste decir {original}?",
            "valor": original,
        }

    # Valor que no está en la base -> lista de disponibles.
    return {
        "tipo": "lista",
        "mensaje": f"«{t}» no está en la base. Elige uno de los géneros disponibles:",
        "generos": GENEROS,
    }


def recomendar_region(genero: str) -> dict:
    """Recomienda la región para un género.

    Las regiones se ordenan por índice de afinidad, igual que en el notebook
    (posición 1 = recomendada, posición 2 = segunda opción). El nivel de
    evidencia sale de la probabilidad bootstrap de la región recomendada.
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
    sub = sub.sort_values("afinidad", ascending=False).reset_index(drop=True)

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
