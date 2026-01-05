# Tech Salaries & Remote Work

Exploratory analysis of 89,184 developers to identify what drives salaries in tech and the impact of remote work.

---

## Questions

- How is remote work distributed?
- Does remote work pay more?
- Does experience correlate with salary?
- Which languages pay best?

---

## Dataset

Stack Overflow Developer Survey 2023 — 89,184 responses, 84 variables, global coverage.

---

## Key findings

1. **Remote dominates** — 83% work remote or hybrid, only 14% fully on-site
2. **Remote pays more** — Remote: $115K/yr vs on-site: $70K/yr (~64% difference)
3. **Experience matters** — clear positive correlation between years of experience and salary
4. **Niche languages lead** — Ada, SAS and Flow outpay mainstream languages
5. **Typical profile** — median 9 years experience, most common 5 years

---

## Visualizations

1. Work modality distribution
2. Salary comparison by modality
3. Experience vs salary correlation
4. Top 10 highest-paying languages
5. Years of experience distribution

---

## Conceptos aplicados

**EDA (Exploratory Data Analysis)** — exploración inicial del dataset para entender su estructura, distribuciones y posibles relaciones antes de hacer cualquier análisis formal.

**Correlación de Pearson** — mide si dos variables numéricas se mueven juntas y en qué dirección. r = 1 es correlación perfecta positiva, r = 0 es sin relación. Aquí se usa para ver si más años de experiencia implican mayor salario.

**Comparación de grupos** — se calcula la media salarial por modalidad de trabajo (remoto / híbrido / presencial) y se comparan. La diferencia porcentual (64%) cuantifica el efecto del trabajo remoto.

**Ranking y agregación** — agrupar por lenguaje de programación y calcular el salario mediano permite ordenar qué tecnologías pagan más, filtrando el ruido de valores extremos.

---

## Stack

Python · pandas · matplotlib · Jupyter

## File

`tech-job-satisfaction-analysis.ipynb` — full notebook with code, analysis and charts
