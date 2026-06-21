"""
fetch_wine.py
=============
Descarga el Wine Quality Dataset de UCI (o genera datos sintéticos).

Uso:
    python src/fetch_wine.py

Dataset: https://archive.ics.uci.edu/dataset/186/wine+quality
Descarga directa desde UCI (sin API key).
"""

import numpy as np
import pandas as pd
import requests
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
PROC_DIR = Path(__file__).parent.parent / "data" / "processed"
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROC_DIR.mkdir(parents=True, exist_ok=True)

URLS = {
    "red": "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv",
    "white": "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv",
}


def fetch_uci_wine() -> pd.DataFrame:
    """Descarga ambos datasets (red + white) desde UCI."""
    frames = []
    for wine_type, url in URLS.items():
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            path = RAW_DIR / f"winequality-{wine_type}.csv"
            path.write_text(r.text)
            df = pd.read_csv(path, sep=";")
            df["wine_type"] = wine_type
            frames.append(df)
            print(f"[OK] {wine_type}: {len(df)} muestras descargadas")
        except Exception as e:
            print(f"[WARN] Error descargando {wine_type}: {e}")
    if frames:
        return pd.concat(frames, ignore_index=True)
    return pd.DataFrame()


def generate_synthetic_wine(n: int = 6497, seed: int = 42) -> pd.DataFrame:
    """
    Genera un dataset sintético que imita UCI Wine Quality.
    Distribuciones calibradas con los rangos reales.
    """
    rng = np.random.default_rng(seed)

    n_red = int(n * 0.245)  # proporción real
    n_white = n - n_red

    def make_wine(n_samples, is_red):
        df = pd.DataFrame({
            "fixed acidity": rng.normal(8.3 if is_red else 6.9, 1.7, n_samples).clip(4, 16),
            "volatile acidity": rng.normal(0.53 if is_red else 0.28, 0.18, n_samples).clip(0.1, 1.6),
            "citric acid": rng.normal(0.27 if is_red else 0.33, 0.19, n_samples).clip(0, 1),
            "residual sugar": rng.lognormal(0.7 if is_red else 1.5, 0.6, n_samples).clip(0.9, 65),
            "chlorides": rng.normal(0.087 if is_red else 0.046, 0.03, n_samples).clip(0.01, 0.6),
            "free sulfur dioxide": rng.normal(16 if is_red else 35, 10, n_samples).clip(1, 72),
            "total sulfur dioxide": rng.normal(46 if is_red else 138, 33, n_samples).clip(6, 289),
            "density": rng.normal(0.997 if is_red else 0.994, 0.002, n_samples).clip(0.99, 1.004),
            "pH": rng.normal(3.31 if is_red else 3.19, 0.15, n_samples).clip(2.7, 4.0),
            "sulphates": rng.normal(0.66 if is_red else 0.49, 0.17, n_samples).clip(0.3, 2.0),
            "alcohol": rng.normal(10.4 if is_red else 10.5, 1.1, n_samples).clip(8, 15),
        })
        # Quality como función de features + ruido
        quality = (
            0.3 * df["alcohol"]
            - 2.0 * df["volatile acidity"]
            + 0.5 * df["citric acid"]
            + 0.1 * df["sulphates"]
            - 0.05 * df["total sulfur dioxide"] / 50
            + rng.normal(0, 0.5, n_samples)
        )
        # Escalar a 3-9
        quality = ((quality - quality.min()) / (quality.max() - quality.min()) * 6 + 3)
        df["quality"] = quality.round().astype(int).clip(3, 9)
        df["wine_type"] = "red" if is_red else "white"
        return df

    red = make_wine(n_red, is_red=True)
    white = make_wine(n_white, is_red=False)
    return pd.concat([red, white], ignore_index=True)


def load_or_generate() -> pd.DataFrame:
    """Descarga de UCI → si falla → sintético."""
    # Intentar descargar
    df = fetch_uci_wine()
    if df.empty:
        print("[INFO] Descarga fallida. Generando dataset sintético...")
        df = generate_synthetic_wine()

    # Crear target binario: bueno (quality >= 7) vs regular
    df["is_good"] = (df["quality"] >= 7).astype(int)

    out_path = PROC_DIR / "wine_clean.csv"
    df.to_csv(out_path, index=False)
    good_pct = df["is_good"].mean() * 100
    print(f"[OK] Dataset guardado: {out_path} ({len(df)} vinos, {good_pct:.1f}% buenos)")
    return df


if __name__ == "__main__":
    df = load_or_generate()
    print("\nPrimeras filas:")
    print(df.head())
    print(f"\nDistribución de quality:\n{df['quality'].value_counts().sort_index()}")
