# 16 — Sentimiento en Titulares Económicos vs IBEX 35

Análisis de la relación entre el sentimiento de titulares económicos semanales y la evolución del IBEX 35.

## Descripción

Este proyecto explora si el tono de las noticias económicas tiene capacidad predictiva sobre los movimientos del mercado bursátil español. Se utilizan datos sintéticos semanales (2021–2024, 156 semanas).

## Datos

- **IBEX 35**: serie de precios semanales (paseo aleatorio, rango 8200–9800)
- **Sentiment score**: puntuación de sentimiento agregado de titulares económicos (–1 a 1)
- Periodo: enero 2021 – diciembre 2024

## Análisis

- Distribución del sentimiento (histograma + semanas positivas vs negativas)
- Serie temporal dual: precio IBEX vs sentimiento semanal
- Correlograma cruzado: pearsonr en lags 0–8
- Scatter: sentimiento en t vs retorno IBEX en t+1

## Metodología

TBD

## Requisitos

```
pip install -r requirements.txt
```
