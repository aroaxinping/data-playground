# ¿Las búsquedas de "recesión" predicen caídas del IBEX 35?

Análisis de la relación entre el interés de búsqueda en Google (términos de crisis económica)
y el comportamiento del índice bursátil español IBEX 35.

## Dilema

Cuando la gente empieza a buscar "recesión", "despido" o "crisis" en Google,
¿el mercado ya lo sabe antes? ¿O las búsquedas anticipan caídas del IBEX?
¿Se puede usar Google Trends como indicador adelantado de la bolsa española?

## Métodos

| Análisis | Pregunta |
|---|---|
| EDA series temporales | ¿Cómo se mueven juntas las búsquedas y el IBEX? |
| Lag correlation | ¿Las búsquedas de hoy predicen el IBEX de la próxima semana? |
| Granger Causality | ¿Búsquedas → IBEX o IBEX → búsquedas? |
| Event study | ¿Qué pasa con el IBEX en los ±30 días de un pico de búsqueda? |

## Conceptos aplicados

**EDA de series temporales** — exploración de dos series que evolucionan en el tiempo (búsquedas + IBEX). Se visualizan juntas para detectar si se mueven en la misma dirección, si una va antes que la otra, o si no tienen relación aparente.

**Correlación con lag** — la correlación de Pearson normal mide la relación entre dos series en el mismo instante. La lag correlation mide si la serie A de hoy se parece a la serie B de dentro de k semanas. Si el lag k=2 tiene la correlación más alta, significa que las búsquedas anticipan el IBEX 2 semanas.

**Causalidad de Granger** — test estadístico que responde: ¿saber el valor pasado de X mejora la predicción de Y? Si sí, se dice que X "Granger-causa" Y. Importante: no implica causalidad real, solo que X tiene información predictiva sobre Y.

**Event study** — se define un evento (pico de búsquedas de "recesión") y se mide cómo se comporta el IBEX en los ±30 días alrededor de ese evento, promediando sobre todos los eventos históricos. Muestra si el mercado reacciona antes, durante o después del pico de búsquedas.

## Datos

Ambas fuentes son gratuitas:

- **Google Trends** — vía `pytrends` (wrapper no oficial, sin API key)
  - Keywords: `"recesión"`, `"crisis económica"`, `"despido"`, `"paro"`
  - Geo: `ES` (España), frecuencia semanal

- **IBEX 35** — vía `yfinance` (Yahoo Finance, sin API key)
  - Ticker: `^IBEX`
  - Frecuencia semanal, ajustado por splits y dividendos

## Uso

```bash
pip install -r requirements.txt
python src/fetch_data.py
jupyter lab notebooks/01_trends_ibex.ipynb
```

Si pytrends falla por rate limit, el notebook genera datos sintéticos realistas.

## Stack

Python · pandas · matplotlib · scipy · statsmodels · pytrends · yfinance
