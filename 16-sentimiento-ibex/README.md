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

## Resultados

El correlograma cruzado muestra que el **lag 1** presenta la correlación más elevada (r ≈ 0.078) entre sentimiento y retorno del IBEX, consistente con la estructura del dataset sintético donde la señal fue inyectada por construcción (`sentiment[t] ~ return[t+1]`). Los lags 2–8 decaen hacia cero.

El scatter sentimiento–retorno t+1 confirma la pendiente positiva esperada. En datos reales, esta señal sería significativamente más débil.

## Metodología

- Datos sintéticos generados con `np.random.seed(2021)`
- Paseo aleatorio para precios IBEX, reescalado a rango 8200–9800
- Sentimiento construido como combinación lineal del retorno siguiente + ruido gaussiano (σ=0.3)
- Correlación cruzada calculada manualmente con `pearsonr` de scipy.stats
- Bandas de significancia al 95%: |r| > 2/√n

## Conexión con proyecto 04

Este análisis es complementario al **proyecto 04** (Google Trends vs IBEX 35). Ambos proyectos exploran si señales de comportamiento colectivo — búsquedas online, tono de noticias — anticipan movimientos del mercado español con un adelanto de ~1 semana.

## Requisitos

```
pip install -r requirements.txt
```
