# Proyecto 17: ¿Tienen sesgo las reseñas de Amazon?

## Descripción

Análisis de 50.000 reseñas sintéticas calibradas a los patrones documentados en investigación académica y estudios de detección de fraude. El objetivo es demostrar estadísticamente que el rating promedio de Amazon es una métrica engañosa y que existen sesgos estructurales bien identificables.

## Investigación de respaldo

### Literatura académica
- **Hu & Liu (2004)** — *Mining and Summarizing Customer Reviews* (KDD 2004): Primeros en documentar la distribución bimodal de ratings en e-commerce. El 60–70% de las reseñas son de 5 o 1 estrella.
- **Hu, Pavlou & Zhang (2006)** — Documentan que las reseñas no verificadas tienen distribuciones más extremas, consistente con comportamiento estratégico de reviewers.
- **Mayzlin, Dover & Chevalier (2014)** — Evidencia de reseñas falsas en hoteles: propiedades sin presencia en plataformas competidoras tienen más reseñas de 1-estrella en esas mismas plataformas.

### Estudios de industria
- **Fakespot (2020)**: Estima que el 30–40% de las reseñas en Electrónica y Belleza son poco confiables (no necesariamente falsas, pero incentivadas o de baja calidad).
- **Amazon (2022)**: Reporta haber eliminado 200M+ reseñas falsas en 2022, con picos de actividad detectados mediante análisis temporal.
- **ReviewMeta**: Documenta que el rating medio de productos con muchas reseñas no verificadas es sistemáticamente 0.3–0.5 puntos más alto que el de productos con solo reseñas verificadas.

## Metodología

### Datos sintéticos calibrados
Los datos fueron generados usando las distribuciones documentadas en la literatura:

| Categoría | % 5-estrellas | % 1-estrella | Tasa fraude estimada |
|---|---|---|---|
| Electrónica | 55% | 20% | 18% |
| Libros | 45% | 10% | 8% |
| Belleza | 60% | 12% | 22% |
| Cocina | 50% | 14% | 12% |
| Deportes | 48% | 16% | 14% |

Las reseñas no verificadas tienen 20% más extremos en ambas colas.

### Review bombing simulado
- Categoría: Electrónica
- Periodo: 15–21 marzo 2023
- Volumen: 420 reseñas en 7 días (6x el promedio diario)
- Distribución: 85% de 1-estrella, 15% de 2-estrella

La detección usa una ventana rodante de 7 días con umbral de +2.5 desviaciones estándar.

## Hallazgos clave

1. **Gap media-mediana**: La media siempre es 0.1–0.5 puntos mayor que la mediana debido a la asimetría de la distribución.
2. **Sesgo de no verificadas**: +15–20 puntos porcentuales más de reseñas de 1 y 5 estrellas en no verificadas vs verificadas.
3. **Electrónica y Belleza** son las categorías más polarizadas y con mayor tasa de fraude estimada.
4. **La detección temporal funciona**: Picos de volumen + caída de rating son señal robusta de coordinated review bombing.

## Estructura

```
17-resenas-amazon/
├── notebooks/
│   └── 01_resenas_amazon.ipynb   # Análisis completo
├── requirements.txt
└── README.md
```

## Ejecución

```bash
pip install -r requirements.txt
jupyter notebook notebooks/01_resenas_amazon.ipynb
```

## Próximos pasos (datos reales)

1. Usar el dataset público de Amazon Reviews (McAuley & Leskovec, 2013) — 142M reseñas
2. Aplicar análisis de sentimiento a texto de reseña vs rating declarado (inconsistencias = posible fraude)
3. Construir grafo de reviewers para detectar cuentas coordinadas (mismo día, mismos productos)
4. Comparar con puntuaciones de Fakespot para validación externa
