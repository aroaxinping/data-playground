# ¿Cuando el mercado tiene pánico, el Bitcoin sube o cae?

Análisis de la relación entre el índice Fear & Greed del mercado crypto y el precio del Bitcoin.
¿El pánico extremo predice una caída… o una recuperación?

## Dilema

El Fear & Greed Index mide el sentimiento del mercado (0 = pánico extremo, 100 = codicia extrema).
La teoría contraria dice que cuando todos tienen miedo es el momento de comprar.
¿Los datos lo confirman? ¿O el miedo simplemente acompaña a las caídas sin predecirlas?

## Métodos

| Análisis | Pregunta |
|---|---|
| EDA series temporales | ¿Cómo se mueven BTC y Fear & Greed juntos? |
| Lag correlation | ¿El F&G predice el precio T+k días? |
| Event study | ¿Qué pasa con el precio en los ±15 días de Fear Extremo (<20)? |
| Rocket & Feather | ¿El miedo cae más rápido de lo que se recupera la confianza? |

## Datos

Ambas fuentes son gratuitas y no requieren API key:

- **Bitcoin precio** — CoinGecko API
  - Endpoint: `https://api.coingecko.com/api/v3/coins/bitcoin/market_chart`
  - Sin key, límite: 30 llamadas/minuto (plan free)

- **Fear & Greed Index** — Alternative.me
  - Endpoint: `https://api.alternative.me/fng/?limit=2000`
  - Sin key, sin límite relevante

## Uso

```bash
pip install -r requirements.txt

# Descarga datos reales (sin API key)
python src/fetch_data.py

# O abre directamente el notebook (genera datos sintéticos si falla la API)
jupyter lab notebooks/01_bitcoin_fear.ipynb
```

## Stack

Python · pandas · matplotlib · scipy · statsmodels · requests
