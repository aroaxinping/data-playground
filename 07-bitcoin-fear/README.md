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

## Conceptos aplicados

**EDA de series temporales** — exploración visual de la evolución del precio de BTC y del Fear & Greed Index a lo largo del tiempo. Se busca si las dos series se mueven juntas, en sentido contrario, o con retardo.

**Correlación con lag** — mide si el Fear & Greed de hoy predice el precio del Bitcoin de dentro de k días. Si el lag k=7 tiene correlación alta, significa que el sentimiento del mercado esta semana anticiparía el precio de la próxima.

**Event study** — se identifican todos los días históricos en que el índice cayó por debajo de 20 (pánico extremo) y se mide cómo se comportó el precio de BTC en los ±15 días alrededor de esos momentos. Responde: ¿el pánico precede a las caídas o a las recuperaciones?

**Rocket & Feather** — test de asimetría en la transmisión de señales. La hipótesis es que el miedo (caída del índice) se propaga rápido al precio, pero la recuperación de la confianza tarda más. Si es así, los bajistas tienen ventaja informativa sobre los alcistas en el corto plazo.

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
