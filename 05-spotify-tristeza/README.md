# ¿Las canciones tristes arrasan más en invierno?

Análisis de la relación entre las características emocionales de las canciones (valence, energy)
y su popularidad según la estación del año. ¿Escuchamos música más triste cuando hace frío?

## Dilema

Spotify sabe qué tan "feliz" suena una canción (valence: 0–1).
¿El valence medio de las canciones más populares cae en noviembre y enero?
¿O la tristeza musical no tiene estación?

## Métodos

| Análisis | Pregunta |
|---|---|
| EDA estacional | ¿Cómo varía el valence medio por mes? |
| Correlación Pearson | ¿Valence y popularidad se relacionan? |
| Test de medias (Mann-Whitney) | ¿Son significativamente distintos invierno vs verano? |
| Clustering K-Means | ¿Qué emociones agrupan las canciones más populares? |

## Datos

- **Spotify Tracks Dataset** — Kaggle (600k+ canciones con audio features)
  - URL: https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset
  - Alternativa sin Kaggle: `src/fetch_data.py` descarga un subset vía Spotify API (requiere cuenta gratuita)
- **Columnas clave**: `valence`, `energy`, `danceability`, `popularity`, `track_genre`, `release_date`

## Uso

```bash
pip install -r requirements.txt

# Opción A: Kaggle (requiere kaggle CLI configurado)
kaggle datasets download maharshipandya/-spotify-tracks-dataset -p data/

# Opción B: Spotify API (requiere CLIENT_ID y CLIENT_SECRET en .env)
python src/fetch_data.py

# Si no tienes ninguno de los dos, el notebook genera datos sintéticos realistas
jupyter lab notebooks/01_spotify_tristeza.ipynb
```

## Stack

Python · pandas · matplotlib · seaborn · scipy · sklearn · spotipy
