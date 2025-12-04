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
