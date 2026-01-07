"""
fetch_spotify_data.py
=====================
Carga y procesa el historial extendido de streaming de Spotify.

Los datos se solicitan en: https://www.spotify.com/account/privacy/
Spotify envía un ZIP con archivos endsong_0.json, endsong_1.json, etc.
Colocar los JSON en data/raw/ antes de ejecutar.

Uso:
    python src/fetch_spotify_data.py

Si no hay archivos endsong_*.json en data/raw/, genera un dataset sintético.
"""

import json
import os
import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
PROC_DIR = Path(__file__).parent.parent / "data" / "processed"
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROC_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# 1. CARGAR datos reales de Spotify (endsong_*.json)
# ---------------------------------------------------------------------------

def load_endsong_files() -> pd.DataFrame:
    """
    Lee todos los archivos endsong_*.json de data/raw/ y extrae
    los campos relevantes para el análisis.
    """
    json_files = sorted(RAW_DIR.glob("endsong_*.json"))
    if not json_files:
        return pd.DataFrame()

    all_records = []
    for f in json_files:
        with open(f, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            all_records.extend(data)

    print(f"[OK] {len(all_records)} registros cargados de {len(json_files)} archivo(s)")

    df = pd.DataFrame(all_records)

    # Campos del extended streaming history
    cols_map = {
        "ts": "timestamp",
        "master_metadata_track_name": "track",
        "master_metadata_album_artist_name": "artist",
        "master_metadata_album_album_name": "album",
        "ms_played": "ms_played",
        "reason_start": "reason_start",
        "reason_end": "reason_end",
        "shuffle": "shuffle",
        "skipped": "skipped",
    }

    available = {k: v for k, v in cols_map.items() if k in df.columns}
    df = df[list(available.keys())].rename(columns=available)

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["ms_played"] = pd.to_numeric(df["ms_played"], errors="coerce").fillna(0).astype(int)

    # Filtrar entradas sin track (podcasts, etc.)
    df = df.dropna(subset=["track"]).reset_index(drop=True)

    return df


# ---------------------------------------------------------------------------
# 2. GENERADOR de datos sintéticos realistas
# ---------------------------------------------------------------------------

def generate_synthetic_data(
    n_events: int = 5000,
    n_artists: int = 50,
    n_tracks: int = 200,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Genera un dataset sintético con patrones realistas de escucha.
    - Más actividad por la tarde/noche, menos por la madrugada
    - Distribución tipo power law en plays por canción
    - Sesiones de escucha agrupadas
    """
    rng = np.random.default_rng(seed)
    random.seed(seed)

    # --- Artistas y canciones ---
    genres = [
        "indie", "pop", "electro", "hip-hop", "rock", "r&b", "latin",
        "metal", "jazz", "ambient", "folk", "reggaeton", "techno", "soul",
    ]
    artists = [f"Artist_{i:02d}" for i in range(n_artists)]
    artist_genre = {a: random.choice(genres) for a in artists}

    # Cada artista tiene 2-8 canciones
    tracks = []
    track_artist = {}
    track_album = {}
    for a in artists:
        n = rng.integers(2, 9)
        for j in range(n):
            t = f"{a}_Track_{j:02d}"
            tracks.append(t)
            track_artist[t] = a
            track_album[t] = f"{a}_Album_{j // 4}"
    tracks = tracks[:n_tracks]

    # Popularidad: power law (pocas canciones con muchos plays)
    popularity = rng.pareto(1.5, size=len(tracks)) + 1
    popularity = popularity / popularity.sum()

    # --- Timestamps con patrón realista ---
    start_date = datetime(2025, 10, 1)
    end_date = datetime(2026, 3, 31)
    total_days = (end_date - start_date).days

    # Distribución de hora del día: pico 18-23h, mínimo 3-7h
    hour_weights = np.array([
        0.3, 0.2, 0.1, 0.05, 0.05, 0.05, 0.1, 0.3,  # 0-7
        0.5, 0.7, 0.8, 0.9, 1.0, 0.9, 0.8, 0.9,      # 8-15
        1.2, 1.5, 1.8, 2.0, 2.0, 1.8, 1.3, 0.7,       # 16-23
    ])
    hour_weights = hour_weights / hour_weights.sum()

    # Generar sesiones (bloques de escucha consecutiva)
    events = []
    current_time = start_date
    while len(events) < n_events:
        # Nueva sesión
        day_offset = rng.integers(0, total_days)
        hour = rng.choice(24, p=hour_weights)
        minute = rng.integers(0, 60)
        session_start = start_date + timedelta(days=int(day_offset), hours=int(hour), minutes=int(minute))

        # Duración de sesión: 3-30 tracks
        session_length = int(rng.exponential(8)) + 3
        session_length = min(session_length, n_events - len(events))

        t = session_start
        # En una sesión, hay tendencia a repetir artista
        session_artist = rng.choice(artists)
        for _ in range(session_length):
            # 40% probabilidad de canción del artista de sesión, 60% general
            if rng.random() < 0.4:
                artist_tracks = [tr for tr in tracks if track_artist[tr] == session_artist]
                if artist_tracks:
                    track = rng.choice(artist_tracks)
                else:
                    track = rng.choice(tracks, p=popularity)
            else:
                track = rng.choice(tracks, p=popularity)

            # ms_played: mayoría escucha completa (~200k ms), algunos skips
            is_skip = rng.random() < 0.15
            if is_skip:
                ms = int(rng.integers(3000, 30000))
            else:
                ms = int(rng.integers(150000, 300000))

            shuffle = bool(rng.random() < 0.35)
            reason_start = rng.choice(["trackdone", "fwdbtn", "clickrow", "appload", "playbtn"],
                                       p=[0.5, 0.1, 0.25, 0.05, 0.1])
            reason_end = "endplay" if not is_skip else rng.choice(["fwdbtn", "endplay", "logout"],
                                                                    p=[0.7, 0.2, 0.1])

            events.append({
                "timestamp": t,
                "track": track,
                "artist": track_artist[track],
                "album": track_album[track],
                "ms_played": ms,
                "reason_start": reason_start,
                "reason_end": reason_end,
                "shuffle": shuffle,
                "skipped": is_skip,
            })

            # Siguiente canción: 0-30 segundos después
            gap = timedelta(seconds=int(rng.integers(0, 30)) + ms / 1000)
            t = t + gap

    df = pd.DataFrame(events[:n_events])
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df


# ---------------------------------------------------------------------------
# 3. Pipeline principal
# ---------------------------------------------------------------------------

def build_dataset() -> pd.DataFrame:
    print("--- Cargando historial de Spotify ---")
    df = load_endsong_files()

    if df.empty:
        print("[INFO] No se encontraron archivos endsong_*.json en data/raw/")
        print("[INFO] Generando dataset sintético (~5000 eventos, 6 meses)")
        df = generate_synthetic_data()
        print(f"[OK] Dataset sintético: {len(df)} eventos")
    else:
        print(f"[OK] Dataset real: {len(df)} eventos")

    out_path = PROC_DIR / "spotify_history.csv"
    df.to_csv(out_path, index=False)
    print(f"\n[OK] Dataset guardado: {out_path}")
    print(f"     {len(df)} filas, {df['artist'].nunique()} artistas, {df['track'].nunique()} canciones")
    print(f"     Periodo: {df['timestamp'].min()} — {df['timestamp'].max()}")
    return df


if __name__ == "__main__":
    df = build_dataset()
    print("\nPrimeras filas:")
    print(df.head().to_string())
