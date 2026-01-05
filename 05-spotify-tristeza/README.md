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

## Conceptos aplicados

**EDA estacional** — se agrupa el dataset por mes y se calcula la media del valence en cada mes. Si diciembre y enero tienen valence sistemáticamente más bajo que julio, hay un patrón estacional.

**Correlación de Pearson** — mide si valence y popularidad se mueven juntos. Una correlación negativa significaría que las canciones más tristes son más populares; cerca de 0 significaría que no hay relación lineal.

**Test de Mann-Whitney** — alternativa no paramétrica al t-test. Compara si dos grupos (canciones de invierno vs canciones de verano) tienen distribuciones distintas, sin asumir que los datos siguen una distribución normal. Devuelve un p-valor: si p < 0.05, la diferencia es estadísticamente significativa.

**Clustering K-Means** — algoritmo que agrupa canciones en k clusters según sus características de audio (valence, energy, danceability). Sin etiquetas previas, el modelo encuentra grupos naturales: por ejemplo, "canciones tristes y lentas", "canciones alegres y bailables", "canciones intensas y oscuras".

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
