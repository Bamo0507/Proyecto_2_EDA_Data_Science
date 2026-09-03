# Diseño: estadística descriptiva de los predictores

**Fecha:** 3 de septiembre de 2026  
**Estado:** aprobado

## Propósito

Describir de forma compacta los niveles y la dispersión de las variables predictoras disponibles para entrenamiento, sin realizar transformaciones logarítmicas ni inferir relaciones predictivas. Esta sección corresponde a la tarea 3.1 y antecede el análisis gráfico de distribuciones.

## Fuente y alcance

- Fuente de análisis: `data/processed/train_eda.csv`.
- Se excluye `date_id` de los cálculos descriptivos.
- Se conservan los valores observados en su escala original; no se calculan retornos ni se aplican transformaciones logarítmicas.
- Los valores faltantes estructurales y las celdas OHLC rechazadas se mantienen como `NaN`. Cada estadístico se calcula con las observaciones disponibles de su variable.

## Agrupación

Las variables se agruparán por **mercado × medición**. Esta organización evita combinar directamente magnitudes heterogéneas, como precios, volúmenes e interés abierto, y permite resumir las 552 variables predictoras sin presentar una tabla ilegible por columna.

## Resultados a incorporar al notebook

1. Una tabla descriptiva por variable con: número de observaciones disponibles, media, mediana, desviación estándar, mínimo, primer cuartil, tercer cuartil, máximo, rango e IQR.
2. Una tabla consolidada por grupo con: número de variables y la mediana de los estadísticos calculados por variable. La mediana representa una variable típica del grupo sin que un instrumento con escala elevada domine el resumen.
3. Una tabla breve de extremos de variabilidad relativa, calculada como `IQR / |mediana|` solo para mediciones cuyo nivel permite dicha comparación. Los resultados de volumen e interés abierto se mantendrán separados de los precios y no se compararán entre sí mediante esta razón.
4. Un texto interpretativo conciso sobre cobertura, tendencia central y dispersión. Se indicará expresamente que estos resultados describen niveles observados y no determinan aún qué variables se conservarán para un modelo.

## Límites de la tarea

- No se crearán gráficos; estos se reservan para la tarea 3.2 de distribuciones.
- No se excluirán variables ni filas a partir de estos resultados.
- No se imputarán ausencias ni se modificará el dataset procesado.
- No se concluirá poder predictivo; esa evaluación pertenece a etapas posteriores de selección y modelado.

## Verificación

Al ejecutar el notebook se comprobará que la tabla por variable cubra todas las columnas predictoras de `train_eda.csv`, que `date_id` no aparezca en el resumen y que los conteos de observaciones respeten la cobertura previamente diagnosticada.
