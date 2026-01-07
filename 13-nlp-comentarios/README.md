# NLP de Comentarios TikTok / Instagram

Analisis de texto de los comentarios de mis redes. Limpieza, sentimiento, topics y frases frecuentes.

## Que hay aqui

Un notebook de Python con NLP aplicado a comentarios reales (o sinteticos si no tienes el export):

| Analisis | Pregunta |
|---|---|
| Limpieza de texto | Como limpiar comentarios de redes sociales para analisis? |
| Exploratorio | De que habla mi audiencia? |
| Sentimiento | Mi audiencia es positiva, negativa o neutra? |
| Topic modeling | Se pueden detectar temas recurrentes en los comentarios? |
| N-gramas | Cuales son las frases mas repetidas? |

## Datos

- **TikTok**: Export de datos personales (Settings > Privacy > Download your data > JSON)
- **Instagram**: Export de datos (Settings > Your Activity > Download your information)
- **Fallback**: Generador sintetico de ~500 comentarios realistas en espanol

## Uso

```bash
pip install -r requirements.txt

# Opcion 1: usar export real de TikTok
# Coloca el JSON en data/raw/ y ejecuta:
python src/fetch_comments.py --source tiktok --file data/raw/user_data.json

# Opcion 2: generar datos sinteticos
python src/fetch_comments.py --synthetic

# Abrir el notebook
jupyter lab notebooks/01_nlp_comentarios.ipynb
```

Si no tienes el export, el notebook genera automaticamente un dataset sintetico.

## Stack

Python · pandas · nltk · scikit-learn · wordcloud · matplotlib
