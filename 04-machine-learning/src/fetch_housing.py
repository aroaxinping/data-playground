"""
fetch_housing.py
================
Carga el California Housing dataset de sklearn (o genera datos sintéticos).

Uso:
    python src/fetch_housing.py

Dataset: sklearn.datasets.fetch_california_housing
No requiere descarga externa ni API key.
"""

import numpy as np
import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
PROC_DIR = Path(__file__).parent.parent / "data" / "processed"
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROC_DIR.mkdir(parents=True, exist_ok=True)


def fetch_california_housing() -> pd.DataFrame:
    """Carga California Housing desde sklearn."""
    try:
        from sklearn.datasets import fetch_california_housing
        data = fetch_california_housing(as_frame=True)
        df = data.frame
        print(f"[OK] California Housing cargado: {len(df)} bloques censales")
        return df
    except Exception as e:
        print(f"[WARN] Error cargando dataset: {e}")
        return pd.DataFrame()


def generate_synthetic_housing(n: int = 5000, seed: int = 42) -> pd.DataFrame:
    """
    Genera un dataset sintético que imita California Housing.
    8 features + target (MedHouseVal en $100k).
    """
    rng = np.random.default_rng(seed)

    df = pd.DataFrame({
        "MedInc": rng.lognormal(1.2, 0.5, n).clip(0.5, 15),
        "HouseAge": rng.integers(1, 52, size=n).astype(float),
        "AveRooms": rng.lognormal(1.6, 0.3, n).clip(1, 50),
        "AveBedrms": rng.lognormal(0.0, 0.2, n).clip(0.5, 10),
        "Population": rng.lognormal(6.5, 1.0, n).clip(100, 30000),
        "AveOccup": rng.lognormal(1.0, 0.4, n).clip(1, 20),
        "Latitude": rng.uniform(32.5, 42, n),
        "Longitude": rng.uniform(-124.5, -114, n),
    })

    # Target: relación con income + rooms + location noise
    target = (
        0.8 * df["MedInc"]
        + 0.02 * df["AveRooms"]
        - 0.01 * df["HouseAge"]
        - 0.05 * df["AveOccup"]
        + 0.3 * (df["Latitude"] - 34).clip(0, 5)
        + rng.normal(0, 0.5, n)
    )
    df["MedHouseVal"] = target.clip(0.15, 5.0).round(3)

    return df


def load_or_generate() -> pd.DataFrame:
    """Intenta cargar desde sklearn, si no genera sintético."""
    df = fetch_california_housing()
    if df.empty:
        print("[INFO] Generando dataset sintético...")
        df = generate_synthetic_housing()

    # Feature engineering
    df["RoomsPerPerson"] = df["AveRooms"] / df["AveOccup"].clip(lower=0.1)
    df["BedroomRatio"] = df["AveBedrms"] / df["AveRooms"].clip(lower=0.1)

    out_path = PROC_DIR / "housing_clean.csv"
    df.to_csv(out_path, index=False)
    print(f"[OK] Dataset guardado: {out_path} ({len(df)} muestras, {df.shape[1]} columnas)")
    return df


if __name__ == "__main__":
    df = load_or_generate()
    print("\nPrimeras filas:")
    print(df.head())
    print(f"\nEstadísticas del target (MedHouseVal, en $100k):")
    print(df["MedHouseVal"].describe())
