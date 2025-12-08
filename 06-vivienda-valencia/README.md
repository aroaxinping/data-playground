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
