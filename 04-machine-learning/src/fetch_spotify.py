"""
fetch_spotify.py
================
Descarga el dataset de Spotify Tracks desde Kaggle (o genera datos sintéticos).

Uso:
    python src/fetch_spotify.py

Dataset: https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset
Si no tienes el CSV, el script genera un dataset sintético realista.
"""

import os
import numpy as np
import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
PROC_DIR = Path(__file__).parent.parent / "data" / "processed"
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROC_DIR.mkdir(parents=True, exist_ok=True)

KAGGLE_FILE = RAW_DIR / "spotify_tracks.csv"


def generate_synthetic_spotify(n: int = 5000, seed: int = 42) -> pd.DataFrame:
    """
    Genera un dataset sintético que imita la estructura del Spotify Tracks Dataset.
    Las distribuciones están calibradas con los rangos reales de la API de Spotify.
    """
    rng = np.random.default_rng(seed)

    genres = [
        "pop", "rock", "hip-hop", "electronic", "r&b", "latin",
        "indie", "jazz", "classical", "metal", "folk", "reggaeton",
    ]

    df = pd.DataFrame({
        "track_name": [f"track_{i:04d}" for i in range(n)],
        "artist": [f"artist_{rng.integers(0, 500)}" for _ in range(n)],
        "genre": rng.choice(genres, size=n),
        "danceability": rng.beta(5, 3, size=n),           # 0-1, skew right
        "energy": rng.beta(4, 3, size=n),                  # 0-1
        "loudness": rng.normal(-8, 4, size=n).clip(-30, 0),  # dB, -30 a 0
        "speechiness": rng.beta(1.5, 10, size=n),          # 0-1, skew left
        "acousticness": rng.beta(1.5, 4, size=n),          # 0-1, skew left
        "instrumentalness": rng.beta(0.5, 5, size=n),      # 0-1, muy skew left
        "liveness": rng.beta(2, 8, size=n),                 # 0-1, skew left
        "valence": rng.beta(3, 3, size=n),                  # 0-1, simétrico
        "tempo": rng.normal(120, 25, size=n).clip(50, 220),  # BPM
        "duration_ms": rng.normal(210_000, 60_000, size=n).clip(60_000, 600_000).astype(int),
        "explicit": rng.choice([0, 1], size=n, p=[0.7, 0.3]),
    })

    # Popularidad = función de features + ruido (simula relación real)
    popularity = (
        15 * df["danceability"]
        + 10 * df["energy"]
        + 8 * (df["loudness"] + 30) / 30
        + 5 * df["valence"]
        - 10 * df["acousticness"]
        - 15 * df["instrumentalness"]
        + 3 * df["explicit"]
        + rng.normal(0, 10, size=n)
    )
    df["popularity"] = popularity.clip(0, 100).round().astype(int)

    return df


def load_or_generate() -> pd.DataFrame:
    """Carga el CSV real si existe, si no genera datos sintéticos."""
    if KAGGLE_FILE.exists():
        print(f"[OK] Cargando dataset real: {KAGGLE_FILE}")
        df = pd.read_csv(KAGGLE_FILE)
        # Quedarnos solo con las columnas que necesitamos
        cols = [
            "track_name", "artists", "track_genre",
            "danceability", "energy", "loudness", "speechiness",
            "acousticness", "instrumentalness", "liveness", "valence",
            "tempo", "duration_ms", "explicit", "popularity",
        ]
        available = [c for c in cols if c in df.columns]
        df = df[available].copy()
        df = df.rename(columns={"artists": "artist", "track_genre": "genre"})
    else:
        print(f"[INFO] No se encontró {KAGGLE_FILE}")
        print("[INFO] Generando dataset sintético (5000 tracks)...")
        print("[TIP]  Descarga el real desde:")
        print("       https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset")
        print(f"       y guárdalo en {KAGGLE_FILE}")
        df = generate_synthetic_spotify()

    # Guardar procesado
    out_path = PROC_DIR / "spotify_clean.csv"
    df.to_csv(out_path, index=False)
    print(f"[OK] Dataset guardado: {out_path} ({len(df)} tracks, {df.shape[1]} columnas)")
    return df


if __name__ == "__main__":
    df = load_or_generate()
    print("\nPrimeras filas:")
    print(df.head())
    print(f"\nEstadísticas de popularity:")
    print(df["popularity"].describe())
