# Spotify Wrapped pero Real

Análisis del historial de escucha de Spotify que el Wrapped oficial no hace. Patrones temporales, sesiones, clustering de épocas musicales, y la verdad sobre el shuffle.

## Qué hay aquí

Un notebook de Python con análisis aplicados a los datos extendidos de streaming de Spotify:

| Análisis | Pregunta |
|---|---|
| Patrones temporales | ¿A qué hora y qué día escucho más? |
| Top artistas y canciones | ¿Quiénes son mis top por tiempo real, no por plays? |
| Sesiones de escucha | ¿Sesiones largas y enfocadas o cortas y dispersas? |
| Clustering de épocas | ¿Se pueden detectar "eras" en mi historial? |
| Shuffle y skips | ¿Cuánto controlo yo vs cuánto decide el algoritmo? |

## Datos

Spotify permite descargar tu historial extendido de streaming desde [Configuración de privacidad](https://www.spotify.com/account/privacy/). Llega como archivos `endsong_*.json`.

## Uso

```bash
pip install -r requirements.txt

# Procesar datos reales (colocar endsong_*.json en data/raw/)
python src/fetch_spotify_data.py

# Abrir el notebook
jupyter lab notebooks/01_spotify_wrapped_real.ipynb
```

Si no tienes los datos reales, el notebook genera un dataset sintético realista.

## Stack

Python · pandas · scikit-learn · matplotlib · seaborn
