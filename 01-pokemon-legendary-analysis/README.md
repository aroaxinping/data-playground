# What makes a Pokemon legendary?

Exploratory data analysis to identify the characteristics that define a legendary Pokemon.

---

## Dataset

- 800 Pokemon (Generations 1–6)
- 65 legendaries (8% of total)
- Method: comparative statistical analysis and visualization

---

## Key findings

1. **Higher base stats** — legendaries average ~100 more total stat points
2. **Dominant types** — Psychic (14) and Dragon (12) account for 40% of legendaries
3. **Clear separation** — stat totals split visibly (legendaries >580 vs non-legendaries <540)
4. **Visual cluster** — legendaries form a distinct group in Attack vs Defense space

---

## Visualizations

- Attack vs Defense scatter plot with legendaries highlighted
- Average stat comparison by category
- Total stat distribution
- Most common types among legendaries

---

## Conceptos aplicados

**EDA (Exploratory Data Analysis)** — antes de responder cualquier pregunta, se explora el dataset: cuántos registros hay, qué variables existen, si hay valores nulos, cómo se distribuyen. Es el paso 0 obligatorio de cualquier análisis de datos.

**Estadística descriptiva** — media, mediana, desviación típica. Resumen numérico de lo que de otra forma sería una lista de 800 filas. Permiten comparar grupos de un vistazo.

**Análisis comparativo por grupos** — se calculan las estadísticas por separado para legendarios y no legendarios y se comparan. Si la diferencia entre medias es grande respecto a la variabilidad, hay un patrón real y no ruido.

**Visualización exploratoria** — scatter plots, histogramas, barras. En datos con grupos bien separados, la visualización revela el patrón antes que cualquier test estadístico.

---

## Stack

Python · pandas · matplotlib · Jupyter

## File

`analisis-pokemon-legendarios.ipynb` — full notebook with analysis and charts
