# ¿Los estudios de Clarins Double Serum aguantan un análisis estadístico?

[![CI](https://github.com/aroaxinping/data-playground/actions/workflows/validate.yml/badge.svg)](https://github.com/aroaxinping/data-playground/actions/workflows/validate.yml)

Clarins es de las pocas marcas cosméticas que publica metodología real: tamaños de muestra,
métodos de medición, duración y tipo de estudio. Eso lo convierte en el caso ideal para analizar
si los claims de marketing se sostienen con los datos que ellos mismos declaran.

## Dilema

Clarins afirma resultados como "piel más firme en 7 días" o "hidratación instantánea".
Publican estudios con n declarado, método y duración. ¿Tienen sentido estadístico?
¿Los tamaños de muestra son suficientes? ¿Los métodos son objetivos o subjetivos?
¿Qué diferencia hay entre sus estudios instrumentales y sus estudios de autoevaluación?

## Lo que Clarins publica (punto de partida)

| Estudio | Sujetos | Duración | Método |
|---|---|---|---|
| Estudio de gemelos (epigenética) | 60+ gemelas homocigóticas (24+ pares) | — | Comparación de signos clínicos |
| Antiedad comparativo (Harungana vs Retinol) | 46 mujeres | 56 días | Medición instrumental |
| Test de consumidor | 353 mujeres (panel multiétnico) | 28 días | Escala estructurada (subjetivo) |
| Autoevaluación | 388 mujeres (panel multiétnico) | 7 días | Escala estructurada (subjetivo) |
| Cinética TEWL | 24 mujeres | 4–6 horas | Instrumental (pérdida de agua transepidérmica) |
| Cinética de hidratación | 24 mujeres | — | Instrumental |

## Preguntas

| Pregunta | Por qué importa |
|---|---|
| ¿n=24 es suficiente para claims de hidratación? | Con n pequeño, un outlier puede mover el promedio varios puntos |
| ¿Qué diferencia hay entre el 97% subjetivo y el % instrumental? | La autoevaluación siempre da números más altos que la medición objetiva |
| ¿El estudio de gemelos es el diseño correcto para lo que afirman? | Los gemelos aislan la genética, pero no el comportamiento de la piel |
| ¿56 días es suficiente para medir antiedad real? | Los cambios dérmicos profundos tardan meses |
| ¿353 vs 24 — cuál claim es más fiable? | El instrumental (n=24) vs el subjetivo (n=353): ¿cuál deberían destacar en marketing? |

## Métodos

| Análisis | Fuente |
|---|---|
| Clasificación de estudios por tipo (instrumental vs subjetivo) | Datos publicados por Clarins |
| Análisis de potencia estadística por n | Simulación con scipy (¿qué efecto detecta cada n?) |
| Comparación de claims subjetivos vs instrumentales | ¿Los % coinciden? ¿Cuál usan en el packaging? |
| Estudio de gemelos: ¿es el diseño correcto? | Literatura de gemelos en dermatología (PubMed) |
| Benchmarking vs literatura independiente | ¿Los valores de TEWL e hidratación son típicos para este tipo de producto? |

## Conceptos aplicados

**Potencia estadística** — la probabilidad de detectar un efecto real si existe. Con n=24, solo puedes detectar efectos grandes (d de Cohen > 0.8). Efectos pequeños o medianos requieren n=50-100+. Si Clarins detecta mejoras con n=24, el efecto tiene que ser muy pronunciado — o están midiendo algo que varía poco.

**Subjetivo vs instrumental** — una escala tipo "¿sientes tu piel más hidratada?" (subjetivo) siempre genera % más altos que un corneómetro (objetivo). El efecto placebo en cosméticos está documentado en +20-30 puntos porcentuales sobre el instrumental. Separar ambos tipos de evidencia es clave para interpretar los claims.

**Diseño de gemelos** — los estudios en gemelas homocigóticas son el gold standard para aislar el efecto de la genética. Pero si se usa para validar una crema, el control tiene que ser claro: ¿una gemela usa el producto y la otra no? ¿O es solo para mapear el envejecimiento? La diferencia determina si el estudio prueba algo sobre el producto.

**TEWL (Trans-Epidermal Water Loss)** — mide cuánta agua pierde la piel al evaporarse. Una crema que reduce el TEWL está actuando como oclusivo (barrera física, no activo específico). Es una métrica válida pero no diferenciadora: la vaselina también reduce el TEWL. El claim debería especificar en cuánto mejora vs un control sin nada.

**Intervalo de confianza vs valor puntual** — Clarins publica el % de mejora como número único (ej: "+X% hidratación"). Sin el intervalo de confianza no sabemos si ese número podría ser 5% o 40% en otra muestra. Un claim honesto incluiría "X% (IC 95%: A–B)".

## Datos

- Metodología publicada por Clarins en su web corporativa y fichas de producto
- PubMed: estudios independientes con TEWL y corneómetro en cremas hidratantes
- Simulación de potencia estadística con scipy.stats

## Stack

Python · pandas · scipy · matplotlib · numpy

## Fuentes

- Clarins Group R&D. *Double Serum clinical studies*. [groupeclarins.com](https://www.groupeclarins.com/en/research-and-development/)
- Clarins Double Serum product page. [clarins.com](https://www.clarins.com/double-serum)
- Draelos ZD (2010). *Active agents in common skin care products*. Plastic and Reconstructive Surgery. [PubMed](https://pubmed.ncbi.nlm.nih.gov/20048601/)
- Cohen J (1988). *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). Lawrence Erlbaum Associates.
- Clarys P et al. (2012). *Hydration measurements of the skin*. Skin Research and Technology. [PubMed](https://pubmed.ncbi.nlm.nih.gov/22564014/)
- Zhu G et al. (2011). *A genome-wide association analysis of skin aging in a discovery and replication study*. Twin Research and Human Genetics. [PubMed](https://pubmed.ncbi.nlm.nih.gov/22093225/)
- Fluhr JW et al. (2006). *Glycerol and the skin*. British Journal of Dermatology. [PubMed](https://pubmed.ncbi.nlm.nih.gov/16704648/)
