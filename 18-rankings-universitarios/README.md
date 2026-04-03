# Proyecto 18: ¿Son objetivos los rankings universitarios?

## Descripción

Análisis crítico de los tres principales rankings universitarios mundiales para 2024:
QS World University Rankings, Shanghai ARWU y Times Higher Education (THE).
Se comparan sus metodologías, se detectan sesgos geográficos y se evalúa si la
financiación en investigación explica las posiciones.

---

## Rankings incluidos

| Ranking | Promotor | Metodología principal |
|---|---|---|
| **QS 2024** | Quacquarelli Symonds | Reputación académica (40 %), reputación empleadores (10 %), ratio estudiante/facultad (20 %), citas por facultad (20 %), internacionalización (10 %) |
| **Shanghai ARWU 2024** | Shanghai Ranking Consultancy | Alumni Nobel/Fields (10 %), staff Nobel/Fields (20 %), HiCi researchers (20 %), artículos Nature/Science (20 %), artículos indexados (20 %), per-capita (10 %) |
| **THE 2024** | Times Higher Education | Enseñanza (29,5 %), investigación (29 %), citas (30 %), ingresos industria (4 %), perspectiva internacional (7,5 %) |

---

## Hallazgos clave

1. **Correlación entre rankings**: QS y THE correlacionan razonablemente bien
   (rho ~0.75), pero Shanghai diverge notablemente, premiando producción
   bibliométrica sobre reputación de encuesta.

2. **Sesgo geográfico**: más del 60 % de las posiciones del top 50 corresponde
   a universidades de países de habla inglesa (EE. UU., Reino Unido, Australia,
   Canadá). Las encuestas de reputación penalizan a instituciones cuya producción
   científica se publica mayoritariamente en otros idiomas.

3. **Correlación con financiación**: existe una correlación negativa moderada entre
   financiación en investigación (USD) y posición en el ranking (a mayor
   financiación, menor número de posición = mejor ranking). El Pearson r ≈ -0.53.

4. **Efecto metodológico**: universidades como ETH Zúrich, Universidad de Tokio
   o la London School of Economics muestran divergencias >20 puestos entre QS
   y Shanghai, ilustrando que cada ranking mide una cosa diferente.

5. **España en los rankings**: las universidades españolas no aparecen en el top
   100 de ninguno de los tres rankings. UB, UAB y UAM son las que mejor posición
   alcanzan (150-250 en QS y THE, 200-300 en Shanghai). UPF destaca en algunas
   áreas específicas pero no en el global.

---

## Lo que los rankings NO miden

- Calidad docente en el aula
- Empleabilidad real de los graduados en el mercado local
- Bienestar del estudiantado
- Innovación pedagógica
- Ratio coste/beneficio para el estudiante

---

## Fuentes

- QS World University Rankings 2024: https://www.topuniversities.com/world-university-rankings/2024
- Shanghai ARWU 2024: https://www.shanghairanking.com/rankings/arwu/2024
- Times Higher Education World University Rankings 2024: https://www.timeshighereducation.com/world-university-rankings/2024/world-ranking
- Research funding data: OECD MSTI 2023, university annual reports (MIT, Stanford, Harvard, etc.)

---

## Estructura

```
18-rankings-universitarios/
├── notebooks/
│   └── 01_rankings_universitarios.ipynb
├── requirements.txt
└── README.md
```

## Cómo ejecutar

```bash
pip install -r requirements.txt
jupyter notebook notebooks/01_rankings_universitarios.ipynb
```
