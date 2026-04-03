# A/B Testing: Checkout Button Experiment

Analisis completo de un experimento A/B en e-commerce. Desde la generacion de datos hasta la decision de si lanzar o no el cambio.

## Por que este proyecto

En data science aplicada, el A/B testing es la herramienta estandar para tomar decisiones con datos. No basta con ver que un numero es mas alto que otro — necesitas saber si la diferencia es real o ruido estadistico, si tienes suficientes datos para confiar en el resultado, y si el efecto es igual para todos los segmentos de usuarios.

Este notebook recorre todo el proceso como se haria en una empresa real.

## Que se aprende

| Seccion | Concepto | Por que importa |
|---|---|---|
| Exploracion | Balance checks entre grupos | Verificar que la aleatorizacion funciono antes de analizar resultados |
| Test de hipotesis | Z-test para proporciones, p-value, intervalo de confianza | Cuantificar si la diferencia es estadisticamente significativa |
| Power analysis | Tamano de muestra, effect size (Cohen's h) | Saber si el experimento tenia suficientes datos para detectar el efecto |
| Segmentacion | Conversion por device y pais, chi-square tests | El efecto global puede esconder diferencias importantes por segmento |
| Metricas secundarias | Mann-Whitney U test | Evaluar si el cambio afecta otras metricas ademas de la principal |
| Errores comunes | Peeking, Bonferroni, Simpson's paradox | Trampas clasicas que invalidan conclusiones si no las conoces |

## Datos

- **Experimento simulado**: Boton de checkout en e-commerce (Control vs Treatment)
- **~20,000 usuarios** (~10k por grupo), conversion ~3.2% control vs ~3.6% treatment
- Los datos incluyen un **Simpson's paradox real**: treatment gana overall pero pierde en desktop — causado por distribucion desigual de dispositivos entre grupos
- **Fallback**: Generador sintetico incluido (`src/fetch_ab_data.py`)

## Uso

```bash
pip install -r requirements.txt
python src/fetch_ab_data.py
jupyter lab notebooks/01_ab_testing.ipynb
```

## Stack

Python · pandas · numpy · scipy · statsmodels · matplotlib
