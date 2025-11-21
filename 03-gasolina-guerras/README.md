# Petróleo, Guerras y el Surtidor

Análisis de la relación entre conflictos geopolíticos y el precio de la gasolina en España. ¿Correlación o causalidad?

## Qué hay aquí

Un notebook de Python con cinco técnicas estadísticas aplicadas a datos reales (Brent + precios MITECO):

| Análisis | Pregunta |
|---|---|
| Correlación de Pearson | ¿Existe relación lineal? |
| Lag Correlation | ¿Con qué retardo se transmite el Brent al surtidor? |
| Granger Causality Test | ¿El Brent *predice* el precio de la gasolina? |
| Event Study | ¿Cuánto sube el precio en los 30 días de cada guerra? |
| Rocket & Feather | ¿Sube más rápido de lo que baja? |

También incluye un desglose del precio en España: cuánto es IEH, cuánto es IVA, y por qué el Estado recauda más cuando sube el crudo sin tocar ningún tipo impositivo.

## Datos

- **Brent**: [FRED – DCOILBRENTEU](https://fred.stlouisfed.org/series/DCOILBRENTEU) (Federal Reserve, gratis)
- **Precios España**: [MITECO](https://www.miteco.gob.es/es/energia/petroleo/precios/) (boletín semanal oficial)
- **EUR/USD**: [FRED – DEXUSEU](https://fred.stlouisfed.org/series/DEXUSEU)

## Uso

```bash
pip install -r requirements.txt

# Descargar datos reales (no requiere API key)
python src/fetch_data.py

# Abrir el notebook
jupyter lab notebooks/01_gasolina_guerras.ipynb
```

Si no descargas los datos, el notebook genera un dataset sintético realista con los shocks geopolíticos en sus fechas correctas.

## Stack

Python · pandas · statsmodels · matplotlib · scipy
