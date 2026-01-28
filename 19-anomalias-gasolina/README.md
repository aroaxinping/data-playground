# 19 · Anomaly Detection en Precios de Gasolina (España)

Detección de anomalías en precios semanales de gasolina95 y diésel en España,
usando IQR sobre la serie temporal de medias nacionales semanales + Isolation Forest.

## Datos

Datos sintéticos que simulan la salida semanal de un scraper de gasolineras:
- 50 provincias × 52 semanas
- Precios realistas: ~1.55 €/L gasolina95, ~1.45 €/L diésel
- 3 picos nacionales inyectados (semanas 10, 28, 42)
- 1 provincia outlier crónica: Soria (+0.12 €/L toda la serie)

## Metodología

- **IQR** aplicado sobre la serie temporal de medias nacionales semanales
  (no cross-province por semana — detecta picos nacionales, no heterogeneidad entre provincias)
- **Isolation Forest** (contamination=0.05) sobre la misma serie
- Comparación de resultados entre ambos métodos

## Ejecución

```bash
pip install -r requirements.txt
jupyter notebook notebooks/01_anomalias_gasolina.ipynb
```

## Estado

Draft — en construcción.
