# ¿El "89% más hidratación" de Olay es real?

Deconstrucción estadística del claim de marketing más famoso de la industria cosmética.
Olay afirma en packaging y publicidad "89% más hidratación". ¿Qué significa ese número realmente?

## Dilema

Un porcentaje sin contexto no significa nada. ¿89% más que qué?
¿Más que no aplicar nada? ¿Más que agua? ¿Más que el peor resultado del grupo?
¿En cuántos sujetos? ¿Cómo midieron "hidratación"? ¿Partían de piel sana o patológicamente seca?

Este análisis no tiene acceso al estudio original (Olay/P&G no lo publica).
Lo que sí se puede hacer: **deconstruir el claim con lo que está disponible públicamente**
y compararlo con estándares de la literatura dermatológica independiente.

## Preguntas

| Pregunta | Por qué importa |
|---|---|
| ¿89% más que qué baseline? | El baseline determina si el número es impresionante o trivial |
| ¿Cuántos sujetos? | n=20 con piel seca severa no es lo mismo que n=200 piel normal |
| ¿Cómo se mide hidratación? | Corneómetro (objetivo) vs cuestionario subjetivo vs foto |
| ¿Hubo control group? | Sin placebo, cualquier crema hidrata — el efecto es oclusivo |
| ¿Es outlier vs la literatura? | ¿Otros estudios independientes encuentran valores similares? |

## Métodos

| Análisis | Fuente |
|---|---|
| Deconstrucción del claim | Packaging, web oficial, anuncios |
| Estándares de medición de hidratación cutánea | Literatura dermatológica (PubMed) |
| Comparativa de claims similares en la industria | Otras marcas, mismas palabras |
| Simulación estadística | ¿Qué n hace falta para que 89% sea significativo? |
| Análisis de sesgo de selección | ¿Qué tipo de piel maximiza el % de mejora? |

## Conceptos aplicados

**Baseline manipulation** — el porcentaje de mejora depende completamente del punto de partida. Si el control (sin crema) da hidratación 10 y la crema da 18.9, el resultado es "89% más". Si el control da 50 y la crema da 94.5, el porcentaje es el mismo pero el contexto es radicalmente distinto.

**Tamaño de muestra y significancia estadística** — con n=20, un outlier en el grupo puede mover el promedio varios puntos porcentuales. La mayoría de estudios cosméticos no publican intervalos de confianza.

**Sesgo de selección** — si reclutan sujetos con piel ya deshidratada, la mejora porcentual es mayor que en piel normal. La piel seca tiene más margen de mejora.

**Corneómetro vs percepción subjetiva** — el corneómetro mide conductancia eléctrica de la piel (proxy de agua en el estrato córneo). Es objetivo pero mide solo la capa más superficial. Un cuestionario "¿sientes tu piel más hidratada?" es subjetivo pero clínicamente relevante.

**Efecto oclusivo** — cualquier crema con petrolato, glicerina o ceramidas mejora la hidratación medida por corneómetro simplemente porque reduce la pérdida de agua transepidérmica (TEWL). El ingrediente activo del claim puede no ser el responsable.

## Datos

- Texto exacto del claim en web/packaging (scrapeable)
- PubMed: estudios de hidratación cutánea con corneómetro (literatura independiente)
- Comparativa de claims de marcas competidoras

## Stack

Python · pandas · matplotlib · requests · BeautifulSoup (solo para claim scraping público)
