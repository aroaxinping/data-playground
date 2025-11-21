"""
fetch_data.py
=============
Descarga y prepara los datos necesarios para el análisis:
  - Precio Brent (EIA API o FRED)
  - Precio gasolina 95 y diésel A en España (CNMC / MITECO)

Uso:
    python src/fetch_data.py --eia-key TU_API_KEY

Si no tienes API key de EIA, el script descarga el Brent desde FRED (no requiere key).
Los datos de España se descargan del boletín semanal del MITECO (CSV público).
"""

import argparse
import os
import time
import requests
import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# 1. BRENT — EIA API (requiere key gratuita en eia.gov/opendata)
# ---------------------------------------------------------------------------

def fetch_brent_eia(api_key: str) -> pd.DataFrame:
    """
    Descarga precio semanal del Brent desde la API de la EIA.
    Serie: PET.RBRTE.W (Europe Brent Spot Price FOB, USD/barril, semanal)
    """
    url = (
        "https://api.eia.gov/v2/seriesid/PET.RBRTE.W"
        f"?api_key={api_key}&data[]=value&frequency=weekly"
        "&start=2000-01-01&sort[0][column]=period&sort[0][direction]=asc"
    )
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    data = r.json()["response"]["data"]
    df = pd.DataFrame(data)[["period", "value"]].rename(
        columns={"period": "fecha", "value": "brent_usd"}
    )
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["brent_usd"] = pd.to_numeric(df["brent_usd"], errors="coerce")
    return df.dropna().sort_values("fecha").reset_index(drop=True)


# ---------------------------------------------------------------------------
# 2. BRENT — FRED (Federal Reserve de St. Louis, no requiere key)
# ---------------------------------------------------------------------------

def fetch_brent_fred() -> pd.DataFrame:
    """
    Descarga precio diario del Brent desde FRED.
    Serie: DCOILBRENTEU (Crude Oil Prices: Brent, USD/barril, diario)
    """
    url = (
        "https://fred.stlouisfed.org/graph/fredgraph.csv"
        "?id=DCOILBRENTEU&vintage_date=&realtime_start=&realtime_end="
    )
    df = pd.read_csv(url, parse_dates=["DATE"])
    df.columns = ["fecha", "brent_usd"]
    df["brent_usd"] = pd.to_numeric(df["brent_usd"], errors="coerce")
    df = df.dropna().sort_values("fecha").reset_index(drop=True)
    # Resamplear a semanal (lunes) para alinear con datos de España
    df = df.set_index("fecha").resample("W-MON").mean().reset_index()
    return df


# ---------------------------------------------------------------------------
# 3. PRECIOS ESPAÑA — MITECO / CNMC
#    El Ministerio publica el boletín semanal de carburantes como CSV/Excel.
#    URL del boletín oficial (puede cambiar; verificar en:
#    https://www.miteco.gob.es/es/energia/petroleo/precios/
# ---------------------------------------------------------------------------

MITECO_URL = (
    "https://www.miteco.gob.es/content/dam/miteco/es/energia/files-1/"
    "petroleo/Precios_eess_semana.xls"
)

def fetch_precios_espana() -> pd.DataFrame:
    """
    Descarga el boletín semanal de precios de carburantes del MITECO.
    Devuelve precios medios nacionales de gasolina 95 y diésel A (€/litro).

    NOTA: Si el MITECO cambia la URL o el formato, descarga manualmente desde:
    https://www.miteco.gob.es/es/energia/petroleo/precios/
    y guarda el archivo en data/raw/precios_espana_raw.xls
    """
    out_path = RAW_DIR / "precios_espana_raw.xls"

    # Intentar descarga automática
    try:
        r = requests.get(MITECO_URL, timeout=60)
        r.raise_for_status()
        out_path.write_bytes(r.content)
        print(f"[OK] Precios España descargados en {out_path}")
    except Exception as e:
        print(f"[WARN] No se pudo descargar automáticamente: {e}")
        if out_path.exists():
            print(f"[INFO] Usando archivo existente: {out_path}")
        else:
            print("[ERROR] Descarga manual necesaria. Ver docstring de fetch_precios_espana().")
            return pd.DataFrame()

    # Parsear Excel — las columnas y filas de cabecera varían según año
    # Ajustar skiprows si el formato cambia
    try:
        df = pd.read_excel(out_path, skiprows=3, header=0)
        # Buscar columnas de fecha, gasolina 95 y gasóleo A por nombre parcial
        fecha_col = [c for c in df.columns if "fecha" in str(c).lower() or "date" in str(c).lower()]
        g95_col   = [c for c in df.columns if "95" in str(c)]
        diesel_col = [c for c in df.columns if "gas" in str(c).lower() and "a" in str(c).lower()]

        if not fecha_col or not g95_col:
            print("[WARN] Columnas no identificadas automáticamente. Revisar el Excel manualmente.")
            print("Columnas disponibles:", df.columns.tolist())
            return df

        result = df[[fecha_col[0], g95_col[0]]].copy()
        result.columns = ["fecha", "gasolina95_eur"]
        if diesel_col:
            result["diesel_eur"] = df[diesel_col[0]].values
        result["fecha"] = pd.to_datetime(result["fecha"], errors="coerce")
        result = result.dropna(subset=["fecha"]).sort_values("fecha").reset_index(drop=True)
        return result

    except Exception as e:
        print(f"[ERROR] Parseando Excel: {e}")
        return pd.DataFrame()


# ---------------------------------------------------------------------------
# 4. TIPO DE CAMBIO EUR/USD — FRED (para convertir Brent a euros)
# ---------------------------------------------------------------------------

def fetch_eurusd_fred() -> pd.DataFrame:
    """Descarga tipo de cambio EUR/USD diario desde FRED."""
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXUSEU"
    df = pd.read_csv(url, parse_dates=["DATE"])
    df.columns = ["fecha", "eurusd"]
    df["eurusd"] = pd.to_numeric(df["eurusd"], errors="coerce")
    df = df.dropna().set_index("fecha").resample("W-MON").mean().reset_index()
    return df


# ---------------------------------------------------------------------------
# 5. Pipeline principal: descarga, limpia y guarda todo en /data/processed
# ---------------------------------------------------------------------------

def build_dataset(eia_key: str = None) -> pd.DataFrame:
    PROC_DIR = RAW_DIR.parent / "processed"
    PROC_DIR.mkdir(exist_ok=True)

    print("--- Descargando Brent ---")
    if eia_key:
        brent = fetch_brent_eia(eia_key)
        print(f"[EIA] {len(brent)} observaciones")
    else:
        brent = fetch_brent_fred()
        print(f"[FRED] {len(brent)} observaciones semanales")

    print("\n--- Descargando tipo de cambio EUR/USD ---")
    fx = fetch_eurusd_fred()
    brent = brent.merge(fx, on="fecha", how="left")
    brent["brent_eur"] = brent["brent_usd"] / brent["eurusd"]

    print("\n--- Descargando precios España ---")
    espana = fetch_precios_espana()

    if espana.empty:
        print("[INFO] Sin datos de España. Solo se guarda el Brent.")
        out = brent
    else:
        # Merge por semana más cercana (merge_asof)
        brent_s = brent.sort_values("fecha")
        espana_s = espana.sort_values("fecha")
        out = pd.merge_asof(
            espana_s, brent_s,
            on="fecha", direction="nearest", tolerance=pd.Timedelta("7 days")
        )

    out_path = PROC_DIR / "dataset_gasolina_brent.csv"
    out.to_csv(out_path, index=False)
    print(f"\n[OK] Dataset guardado: {out_path} ({len(out)} filas, {out.columns.tolist()})")
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Descarga datos para el análisis gasolina-guerras")
    parser.add_argument("--eia-key", default=None, help="API key de EIA (opcional)")
    args = parser.parse_args()

    df = build_dataset(eia_key=args.eia_key)
    print("\nPrimeras filas:")
    print(df.head())
