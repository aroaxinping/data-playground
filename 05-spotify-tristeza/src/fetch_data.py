"""
Descarga datos de Spotify vía API oficial.
Requiere CLIENT_ID y CLIENT_SECRET en un archivo .env en la raíz del proyecto.

Alternativa: descarga el dataset de Kaggle manualmente y colócalo en data/
  https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset
"""

import os
import time
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# Géneros a analizar (variedad emocional)
GENRES = [
    "sad", "melancholy", "blues", "emo",          # tristes
    "happy", "dance", "pop", "latin",              # alegres
    "acoustic", "folk", "classical",               # intermedios
    "metal", "rock", "punk",                       # energéticos
]

TRACKS_PER_GENRE = 50  # máx 50 por llamada a la API


def fetch_via_spotipy():
    """Descarga tracks con audio features usando spotipy."""
    try:
        import spotipy
        from spotipy.oauth2 import SpotifyClientCredentials
        from dotenv import load_dotenv
    except ImportError:
        print("Instala dependencias: pip install spotipy python-dotenv")
        return None

    load_dotenv()
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("Faltan SPOTIFY_CLIENT_ID y SPOTIFY_CLIENT_SECRET en el .env")
        return None

    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret,
        )
    )

    all_tracks = []

    for genre in GENRES:
        print(f"  Descargando genre: {genre}...")
        try:
            results = sp.search(
                q=f"genre:{genre}",
                type="track",
                limit=TRACKS_PER_GENRE,
                market="ES",
            )
            track_ids = [t["id"] for t in results["tracks"]["items"] if t]

            # Audio features en batch (máx 100 por llamada)
            features = sp.audio_features(track_ids)

            for track, feat in zip(results["tracks"]["items"], features):
                if feat is None:
                    continue
                all_tracks.append({
                    "track_id":       track["id"],
                    "track_name":     track["name"],
                    "artist":         track["artists"][0]["name"],
                    "popularity":     track["popularity"],
                    "release_date":   track["album"]["release_date"],
                    "genre":          genre,
                    "valence":        feat["valence"],
                    "energy":         feat["energy"],
                    "danceability":   feat["danceability"],
                    "acousticness":   feat["acousticness"],
                    "instrumentalness": feat["instrumentalness"],
                    "speechiness":    feat["speechiness"],
                    "tempo":          feat["tempo"],
                    "loudness":       feat["loudness"],
                    "duration_ms":    feat["duration_ms"],
                })

            time.sleep(0.3)  # respetar rate limit

        except Exception as e:
            print(f"  Error en genre {genre}: {e}")
            continue

    if not all_tracks:
        return None

    df = pd.DataFrame(all_tracks)
    out = DATA_DIR / "spotify_tracks.csv"
    df.to_csv(out, index=False)
    print(f"\nGuardado: {out} ({len(df)} tracks)")
    return df


def load_kaggle_dataset():
    """Carga el dataset de Kaggle si ya está descargado."""
    candidates = list(DATA_DIR.glob("*.csv"))
    if candidates:
        df = pd.read_csv(candidates[0])
        print(f"Dataset cargado: {candidates[0]} ({len(df):,} filas)")
        return df
    return None


if __name__ == "__main__":
    print("Buscando dataset de Kaggle en data/...")
    df = load_kaggle_dataset()

    if df is None:
        print("No encontrado. Intentando Spotify API...")
        df = fetch_via_spotipy()

    if df is None:
        print("\nNi Kaggle ni API disponibles.")
        print("El notebook generará datos sintéticos realistas.")
    else:
        print(f"\nColumnas: {list(df.columns)}")
        print(df.head(3))
