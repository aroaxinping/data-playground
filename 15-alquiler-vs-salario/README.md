# Alquiler vs Salario en España

## Descripción

Análisis de asequibilidad de la vivienda en España, cruzando salarios medianos por Comunidad Autónoma (fuente: INE) con precios de alquiler medios por ciudad (datos conocidos 2024, basados en Idealista y portales inmobiliarios).

## Fuentes de datos

### Salarios — INE (Instituto Nacional de Estadística)
- Encuesta de Estructura Salarial
- API JSON pública (sin clave): `https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/10882?nult=5`
- Si la API no está disponible, se usan salarios hardcodeados de los informes publicados INE 2024

### Alquiler — Datos conocidos 2024
- Idealista, Fotocasa, portales inmobiliarios
- No existe API pública, se usan valores de referencia documentados:
  - Madrid: ~1.800 €/mes
  - Barcelona: ~1.700 €/mes
  - Palma: ~1.300 €/mes
  - Bilbao: ~1.200 €/mes
  - Málaga: ~1.100 €/mes
  - Valencia: ~1.000 €/mes
  - Sevilla: ~900 €/mes
  - Zaragoza: ~750 €/mes
  - Murcia: ~650 €/mes

## Metodología

### Métrica de asequibilidad
- **Ratio renta/salario** = (alquiler mensual × 12) / salario anual neto estimado
- **Umbral crítico**: >30% del ingreso mensual destinado a alquiler = vivienda inasequible (estándar ONU/Banco Mundial)

### Análisis comparativo 2019 vs 2024
- Muestra la evolución del esfuerzo económico en 5 ciudades principales
- Fuentes: histórico Idealista + INE anteriores años

## Hallazgos Clave

- Barcelona y Madrid son las ciudades más inasequibles, seguidas de Palma de Mallorca y Málaga
- El ratio alquiler/salario supera el 40% en varias ciudades — muy por encima del umbral saludable del 30%
- La brecha ha empeorado significativamente entre 2019 y 2024
- País Vasco, a pesar de tener los salarios más altos, no escapa a la presión inmobiliaria en Bilbao

## Uso

```bash
pip install -r requirements.txt
# Descargar datos INE (opcional, el notebook funciona sin conexión)
python src/fetch_data.py
# Ejecutar análisis
jupyter notebook notebooks/01_alquiler_salario.ipynb
```
