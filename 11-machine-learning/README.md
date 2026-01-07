# Data Playground: Machine Learning de 0 a Viral

5 proyectos de ML progresivos: desde regresión lineal hasta un predictor de viralidad para TikTok e Instagram con mis propios datos.

## Proyectos

| # | Proyecto | Técnica | Dataset |
|---|----------|---------|---------|
| 1 | Popularidad en Spotify | Regresión Lineal | Kaggle Spotify Tracks |
| 2 | Fuga de talento tech | Regresión Logística | IBM HR Attrition |
| 3 | Calidad del vino | Decision Tree + Random Forest | UCI Wine Quality |
| 4 | Precio de vivienda | XGBoost + Tuning | Ames Housing |
| 5 | Predictor viral TikTok+IG | Pipeline completo | Datos propios @aroaxinping |

## Uso

```bash
pip install -r requirements.txt

# Descargar datos del proyecto que quieras
python src/fetch_spotify.py
python src/fetch_attrition.py
python src/fetch_wine.py
python src/fetch_housing.py

# Abrir el notebook
jupyter lab notebooks/01_regresion_lineal_spotify.ipynb
```

Si no descargas los datos, cada notebook genera un dataset sintético para que funcione igualmente.

## Stack

Python · pandas · scikit-learn · xgboost · shap · matplotlib · seaborn
