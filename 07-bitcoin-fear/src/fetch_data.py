"""
Descarga datos de Bitcoin y Fear & Greed Index.
Ambas fuentes son gratuitas y no requieren API key.

Fuentes:
  - Bitcoin: CoinGecko API  https://www.coingecko.com/en/api
  - Fear & Greed: Alternative.me  https://alternative.me/crypto/fear-and-greed-index/
"""

import requests
import pandas as pd
import time
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
FNG_URL       = "https://api.alternative.me/fng/?limit=2000&format=json"

DAYS = 730  # 2 años de histórico


def fetch_bitcoin_price():
    """Descarga precio diario de Bitcoin desde CoinGecko (sin API key)."""
    print("Descargando Bitcoin (CoinGecko)...")
    try:
        r = requests.get(
            COINGECKO_URL,
            params={"vs_currency": "usd", "days": DAYS, "interval": "daily"},
            timeout=30,
            headers={"accept": "application/json"},
        )
        r.raise_for_status()
        data = r.json()

        prices = data["prices"]
        df = pd.DataFrame(prices, columns=["timestamp_ms", "price_usd"])
        df["date"] = pd.to_datetime(df["timestamp_ms"], unit="ms").dt.normalize()
        df = df[["date", "price_usd"]].drop_duplicates("date")
        df = df.sort_values("date").reset_index(drop=True)

        out = DATA_DIR / "btc_price.csv"
        df.to_csv(out, index=False)
        print(f"Guardado: {out} ({len(df)} días)")
        return df

    except Exception as e:
        print(f"Error CoinGecko: {e}")
        return None


def fetch_fear_greed():
    """Descarga el Fear & Greed Index desde Alternative.me (sin API key)."""
    print("Descargando Fear & Greed Index (alternative.me)...")
    try:
        r = requests.get(FNG_URL, timeout=30)
        r.raise_for_status()
        data = r.json()["data"]

        df = pd.DataFrame(data)
        df["date"]  = pd.to_datetime(df["timestamp"].astype(int), unit="s").dt.normalize()
        df["fng"]   = df["value"].astype(int)
        df["label"] = df["value_classification"]
        df = df[["date", "fng", "label"]].sort_values("date").reset_index(drop=True)

        out = DATA_DIR / "fear_greed.csv"
        df.to_csv(out, index=False)
        print(f"Guardado: {out} ({len(df)} días)")
        return df

    except Exception as e:
        print(f"Error Alternative.me: {e}")
        return None


if __name__ == "__main__":
    btc = fetch_bitcoin_price()
    time.sleep(1)
    fng = fetch_fear_greed()

    if btc is not None and fng is not None:
        merged = pd.merge(btc, fng, on="date", how="inner")
        out = DATA_DIR / "btc_fng_merged.csv"
        merged.to_csv(out, index=False)
        print(f"\nMerge guardado: {out} ({len(merged)} días con ambas series)")
        print(merged.tail())
    else:
        print("\nNo se pudieron descargar todos los datos.")
        print("El notebook generará un dataset sintético.")
