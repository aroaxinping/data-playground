"""
Descarga datos de Google Trends (pytrends) e IBEX 35 (yfinance).
Ambas fuentes son gratuitas y no requieren API key.

  - pytrends: https://github.com/GeneralMills/pytrends
  - yfinance: https://github.com/ranaroussi/yfinance
"""

import time
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

KEYWORDS  = ["recesión", "crisis económica", "despido", "paro"]
GEO       = "ES"
TIMEFRAME = "2021-01-01 2024-12-31"  # 3 years to get weekly granularity from Trends
IBEX_TICKER = "^IBEX"


def fetch_google_trends():
    """Descarga interés de búsqueda semanal desde Google Trends."""
    try:
        from pytrends.request import TrendReq
    except ImportError:
        print("Instala pytrends: pip install pytrends")
        return None

    print("Descargando Google Trends...")
    pytrends = TrendReq(hl="es-ES", tz=60, timeout=(10, 25))

    all_dfs = []
    # pytrends solo acepta 5 keywords a la vez
    for kw in KEYWORDS:
        try:
            pytrends.build_payload([kw], geo=GEO, timeframe=TIMEFRAME)
            df = pytrends.interest_over_time()
            if df.empty:
                continue
            df = df[[kw]].rename(columns={kw: kw.replace(" ", "_")})
            all_dfs.append(df)
            time.sleep(2)  # evitar rate limit
        except Exception as e:
            print(f"  Error en '{kw}': {e}")

    if not all_dfs:
        return None

    trends = pd.concat(all_dfs, axis=1)
    trends.index.name = "date"
    trends = trends.reset_index()

    out = DATA_DIR / "google_trends.csv"
    trends.to_csv(out, index=False)
    print(f"Guardado: {out} ({len(trends)} semanas)")
    return trends


def fetch_ibex():
    """Descarga el IBEX 35 semanal desde Yahoo Finance."""
    try:
        import yfinance as yf
    except ImportError:
        print("Instala yfinance: pip install yfinance")
        return None

    print("Descargando IBEX 35 (Yahoo Finance)...")
    try:
        ibex = yf.download(IBEX_TICKER, start="2021-01-01", end="2024-12-31",
                           interval="1wk", progress=False, auto_adjust=True)
        # yfinance >=0.2 returns MultiIndex columns — flatten
        if isinstance(ibex.columns, pd.MultiIndex):
            ibex.columns = ibex.columns.get_level_values(0)
        ibex = ibex[["Close"]].rename(columns={"Close": "ibex_close"})
        ibex.index.name = "date"
        ibex = ibex.reset_index()

        out = DATA_DIR / "ibex35.csv"
        ibex.to_csv(out, index=False)
        print(f"Guardado: {out} ({len(ibex)} semanas)")
        return ibex
    except Exception as e:
        print(f"Error yfinance: {e}")
        return None


if __name__ == "__main__":
    trends = fetch_google_trends()
    ibex   = fetch_ibex()

    if trends is not None and ibex is not None:
        trends["date"] = pd.to_datetime(trends["date"])
        ibex["date"]   = pd.to_datetime(ibex["date"])
        # Normalize both to Monday of each week so dates align (Trends=Sunday, IBEX=Monday)
        trends["date"] = trends["date"] - pd.to_timedelta(trends["date"].dt.dayofweek, unit="D")
        ibex["date"]   = ibex["date"]   - pd.to_timedelta(ibex["date"].dt.dayofweek, unit="D")
        merged = pd.merge(trends, ibex, on="date", how="inner")
        out = DATA_DIR / "trends_ibex_merged.csv"
        merged.to_csv(out, index=False)
        print(f"\nMerge guardado: {out} ({len(merged)} semanas)")
        print(merged.tail())
    else:
        print("\nEl notebook generará datos sintéticos.")
