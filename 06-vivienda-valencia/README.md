# ¿La DANA disparó el precio del alquiler en Valencia?

Análisis del impacto de las inundaciones del 29 de octubre de 2024 en el mercado
de la vivienda en la Comunitat Valenciana. ¿Cuánto subió el alquiler? ¿Y la venta?
¿Se puede cuantificar el efecto de un desastre natural en los precios inmobiliarios?

## Dilema

Tras la DANA, miles de familias perdieron su vivienda. La demanda de alquiler
en Valencia ciudad y municipios colindantes se disparó de golpe.
¿Los datos de precios confirman ese shock? ¿Cuánto tardó en absorberse?
¿Afectó igual a todos los barrios?

## Métodos

| Análisis | Pregunta |
|---|---|
| EDA histórico | ¿Cómo evolucionaron los precios 2019–2024 en Valencia? |
| Event study (±6 meses) | ¿Cuándo y cuánto suben tras la DANA? |
| Comparativa ciudades | ¿Valencia vs Madrid/Barcelona — diverge tras octubre 2024? |
| Asequibilidad | ¿El salario medio en Valencia alcanza para pagar el alquiler? |

## Conceptos aplicados

**EDA histórico** — se visualiza la evolución del precio del alquiler en Valencia desde 2019 hasta 2024 para entender la tendencia base antes del evento. Fundamental para distinguir qué es tendencia preexistente y qué es impacto real de la DANA.

**Event study** — se toma el 29 de octubre de 2024 como evento y se mide cómo evolucionan los precios en los ±6 meses alrededor de esa fecha. Permite ver si el shock fue inmediato, gradual, o si ya se anticipaba.

**Comparativa con ciudades control** — se compara Valencia con Madrid y Barcelona, que no sufrieron la DANA. Si los precios suben en Valencia pero no en las otras ciudades en el mismo período, es más probable que la subida se deba a la DANA y no a factores generales del mercado.

**Análisis de asequibilidad** — ratio entre el precio del alquiler y el salario medio de la zona. Si el alquiler supera el 30–40% del salario neto, se considera que la vivienda no es asequible para el trabajador típico.

## Datos

- **MITMA — Ministerio de Transportes** (precios venta por municipio, gratis)
  - URL: https://www.mitma.gob.es/el-ministerio/informacion-estadistica/vivienda-y-actuaciones-urbanas/estadisticas/precios-de-suelo
- **INE — Índice de Precios del Alquiler** (por municipio, gratis)
  - URL: https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177105
- **GVA Datos Abiertos** (open data Generalitat Valenciana, gratis)
  - URL: https://dadesobertes.gva.es/
- **Salario medio**: INE Encuesta de Estructura Salarial, Comunitat Valenciana

## Uso

```bash
pip install -r requirements.txt
python src/fetch_data.py
jupyter lab notebooks/01_vivienda_dana.ipynb
```

## Stack

Python · pandas · matplotlib · scipy · statsmodels · requests
