# Vichy Minéral 89: ¿El marketing dice lo mismo que los estudios publicados?

Vichy es una de las pocas marcas cosméticas con estudios reales en PubMed.
Corneómetro, Tewameter, Chromameter, grupos control split-face, p-values, registro NCT.
La pregunta no es si el producto funciona — es si el marketing usa esos datos honestamente.

## Dilema

Vichy afirma en su web: "mejora visiblemente el 100% de los signos de hidratación".
Sus estudios publicados son más específicos: +31-35% de hidratación en pacientes con rosácea,
medido con Corneómetro CM825, en un diseño split-face de 30 días.

¿Son el mismo claim? ¿La misma población? ¿El mismo método?
Comparar el claim de marketing con los datos publicados permite ver exactamente
dónde hay coherencia y dónde hay exageración.

## Lo que Vichy publica (estudios en PubMed)

| Estudio | PMID / PMC | Sujetos | Diseño | Instrumentos |
|---|---|---|---|---|
| Post-procedimiento y piel seca (Canadá) | PMID 33786979 | 47 adultos | Open-label, 4 semanas | Gradación clínica + síntomas subjetivos |
| Rosácea split-face | PMC7547125 | 20 sujetos | Split-face intra-individual, 30 días | Corneómetro CM825, Tewameter TM300, Chromameter CR400 |
| Rosácea con mascarilla (RCT) | PMC9843703 | Registro NCT05562661 | Ensayo controlado aleatorizado | Instrumentación + días 15 y 30 |
| Post-láser | PMID 33538111 | 51 mujeres | 28 días | Corneómetro, Tewameter, Chromameter |
| Antienvejecimiento con tretinoína | PMC9928536 | 38 mujeres | Split-face, 84 días | ELISA (IL-8, IL-1α, PGE2, SOD) + instrumental |

## Preguntas

| Pregunta | Por qué importa |
|---|---|
| ¿"100% de signos de hidratación" está respaldado por los estudios publicados? | El estudio split-face midió +31-35% en rosácea — ¿es la misma afirmación? |
| ¿Los estudios publicados son de la misma población que el marketing? | Rosácea y piel post-procedimiento no es lo mismo que "piel normal" |
| ¿El +31-35% de hidratación es instrumental u autoevaluado? | Corneómetro (objetivo) vs "¿sientes tu piel más hidratada?" |
| ¿Qué pasa con los estudios de autoevaluación que usa en marketing? | 42-53 sujetos, escala subjetiva — distinto método, mismo claim |
| ¿El diseño split-face es el control adecuado para hidratación? | La cara untreated puede verse afectada por la treated (migración de producto) |
| ¿Cómo se comparan sus valores de TEWL con literatura independiente? | -11% TEWL: ¿es grande o pequeño vs otros hidratantes? |

## Métodos

| Análisis | Fuente |
|---|---|
| Extracción de datos de estudios PubMed | PMC full text (acceso abierto) |
| Comparación claim de marketing vs datos publicados | Web Vichy USA/ES + estudios PMC |
| Análisis de la población de estudio vs claim | ¿Rosácea = "todas las pieles"? |
| Benchmarking de valores TEWL e hidratación | Literatura independiente de hidratantes |
| Evaluación del diseño split-face | Limitaciones metodológicas del control intra-individual |
| Conflicto de interés: quién financia y quién publica | Afiliación de autores en los estudios PMC |

## Conceptos aplicados

**Split-face design** — cada sujeto es su propio control: una mitad de la cara recibe el producto, la otra no. Elimina la variabilidad entre individuos. Limitación: el producto puede migrar entre zonas, contaminando el control. Para hidratación superficial, es un diseño razonable pero no perfecto.

**Corneómetro** — mide la conductancia eléctrica del estrato córneo como proxy de hidratación. Es el estándar instrumental en dermatología cosmética. Un +31% en Corneómetro es un efecto real y medible — pero solo en la capa más superficial de la piel.

**TEWL (Pérdida de agua transepidérmica)** — mide cuánta agua evapora la piel. Una reducción del TEWL indica que el producto actúa como oclusivo (barrera física). -11% TEWL puede ser estadísticamente significativo pero clínicamente modesto: la vaselina lo reduce en un 30-50%.

**Población de estudio vs claim de marketing** — los estudios publicados de Vichy M89 son casi todos en rosácea o piel post-procedimiento. La rosácea tiene una barrera cutánea comprometida con TEWL elevado. Mejorar el TEWL en esa población es más fácil que en piel sana. Usar esos datos para hacer claims sobre "cualquier piel" es un salto no respaldado.

**Conflicto de interés en estudios cosméticos** — todos los estudios de Vichy M89 están financiados por Vichy/L'Oréal. Esto no los invalida, pero sí eleva el riesgo de sesgo de publicación: los estudios negativos probablemente no se publican. Los estudios canadienses incluyen investigadores de la Universidad de British Columbia y Toronto, lo que añade algo de independencia institucional.

**Gap marketing vs evidencia** — el claim de marketing extrapola datos de una población específica (rosácea) a toda la audiencia ("visiblemente mejora el 100% de signos de hidratación"). Los estudios de autoevaluación que usa en marketing (42-53 sujetos, escala subjetiva) son metodológicamente distintos a los estudios publicados en PubMed (instrumentación, grupos control). Separar ambas fuentes es el núcleo del análisis.

## Datos

- Estudios publicados: PMC7547125, PMC9843703, PMC9928536, PMID 33786979, PMID 33538111 (acceso abierto)
- Claims de marketing: web oficial Vichy USA / España
- Literatura independiente: estudios de TEWL e hidratación en cremas de barrera (PubMed)

## Stack

Python · pandas · scipy · matplotlib · requests · BeautifulSoup (solo para claims públicos)
