# 19 · Anomaly Detection en Precios de Gasolina (España)

Detección de anomalías en precios semanales de gasolina95 en España,
usando IQR sobre la serie temporal de medias nacionales semanales + Isolation Forest.

## Datos

Datos sintéticos que simulan la salida semanal de un scraper de gasolineras:
- 50 provincias × 52 semanas
- Precios realistas: ~1.55 €/L gasolina95 (tendencia lineal 1.52 → 1.58)
- 3 picos nacionales inyectados (semanas 10, 28, 42): +0.10–0.15 €/L en todas las provincias
- 1 provincia outlier crónica: Soria (+0.12 €/L toda la serie)

## Metodología

**IQR** sobre la serie temporal de medias nacionales:
- Se calcula la media nacional por semana (serie de 52 puntos)
- IQR se aplica sobre esa serie — detecta semanas donde el precio nacional sube o baja de golpe
- Clave: NO es IQR cross-province por semana (eso detectaría heterogeneidad estructural, no picos)

**Isolation Forest** (contamination=0.05):
- Misma serie de 52 medias semanales como input
- Resultados comparados con IQR

## Resultados

- IQR e Isolation Forest **coinciden exactamente** en las 3 semanas con pico nacional inyectado (S11, S29, S43)
- **Soria** aparece como la provincia más cara en el ranking anual (+0.12 €/L de bias crónico)
- El outlier crónico provincial NO aparece en el IQR temporal (correcto: no es un pico semanal)

## Visualizaciones

1. Serie temporal de medias nacionales con anomalías destacadas en rojo
2. Ranking barh: top 10 provincias más baratas vs más caras (media anual)

## Conexión con datos reales

Este análisis está diseñado para conectarse directamente con la salida del scraper
[scraper-gasolineras-espana](https://github.com/aroaxinping/scraper-gasolineras-espana),
que genera exactamente este formato: precios semanales por provincia.
Con datos reales, las semanas anomalas corresponderían a eventos como subidas del Brent,
guerras de precios entre operadoras o cambios en la fiscalidad de carburantes.

## Ejecución

```bash
pip install -r requirements.txt
jupyter notebook notebooks/01_anomalias_gasolina.ipynb
```
