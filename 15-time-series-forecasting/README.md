# Time Series Forecasting

Descomposicion, estacionariedad y tres modelos de prediccion sobre series temporales reales y sinteticas.

## Por que este proyecto

Las series temporales estan en todas partes: precios, ventas, trafico web, metricas de redes sociales. Predecir el futuro a partir del pasado requiere entender conceptos como estacionariedad, estacionalidad y autocorrelacion — sin eso, cualquier modelo que entrenes va a dar resultados sin sentido.

Este notebook va desde lo basico (que es una serie temporal y como descomponerla) hasta entrenar y comparar tres modelos clasicos de forecasting.

## Que se aprende

| Seccion | Concepto | Por que importa |
|---|---|---|
| Descomposicion | Trend, seasonality, residual (aditivo vs multiplicativo) | Entender la anatomia de una serie antes de modelar |
| Estacionariedad | Tests ADF y KPSS, diferenciacion, log transform | ARIMA necesita series estacionarias — si no lo verificas, el modelo no sirve |
| ACF / PACF | Autocorrelacion y autocorrelacion parcial | Identificar los ordenes p y q del modelo ARIMA |
| ARIMA | Grid search de (p,d,q), forecast, intervalos de confianza | Modelo clasico para series sin estacionalidad fuerte |
| SARIMA | Extension estacional de ARIMA con (P,D,Q,s) | Captura patrones que se repiten cada 12 meses |
| Prophet | Modelo de Meta/Facebook para forecasting | Alternativa moderna que maneja estacionalidad multiple automaticamente |
| Comparacion | RMSE, MAE, MAPE entre los 3 modelos | No hay modelo universal — cada uno tiene sus ventajas segun los datos |

## Datasets

| Dataset | Fuente | Registros |
|---|---|---|
| Airline Passengers | statsmodels (clasico Box-Jenkins, 1949-1960) | 144 meses |
| Ventas diarias sinteticas | Generado con trend + estacionalidad semanal/mensual + ruido | ~1095 dias (3 anos) |

## Uso

```bash
pip install -r requirements.txt
python src/fetch_ts_data.py
jupyter lab notebooks/01_time_series_forecasting.ipynb
```

Si no descargas los datos, el notebook genera datasets sinteticos automaticamente.

## Stack

Python · pandas · statsmodels · scipy · prophet · scikit-learn · matplotlib
