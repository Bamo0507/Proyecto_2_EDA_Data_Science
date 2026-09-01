# Diseno del diagnostico de calidad

## Decision general

La calidad se evaluara mediante un diagnostico por capas que permita obtener
una vision suficientemente completa sin producir reportes extensos y dificiles
de interpretar. `train.csv` recibira el analisis profundo; los otros archivos
se revisaran principalmente como piezas necesarias para interpretar o utilizar
la informacion de entrenamiento.

## Restriccion principal

El tiempo disponible es limitado. Por esta razon, cada capa producira resumenes
priorizados y mostrara detalle solamente para variables afectadas. No se
utilizara un perfilador automatico ni se imprimiran tablas exhaustivas con todas
las columnas cuando una agrupacion sea mas informativa.

## Capas del diagnostico

1. Compatibilidad de los archivos complementarios.
   - Alineacion de `date_id` entre `train.csv` y `train_labels.csv`.
   - Correspondencia entre las columnas objetivo y `target_pairs.csv`.
   - Existencia en `train.csv` de los instrumentos usados en `pair`.
   - Compatibilidad de los predictores de `test.csv` con los de `train.csv`.
   - Presencia de columnas auxiliares necesarias.
2. Valores faltantes en `train.csv`.
   - Cantidad y porcentaje por variable.
   - Resumen por mercado y medicion.
   - Concentracion temporal y variables mas afectadas.
3. Duplicados.
   - Filas completas, identificadores temporales y columnas duplicadas.
4. Tipos y valores sospechosos.
   - Infinidades, valores no numericos y valores imposibles segun la medicion.
5. Variabilidad.
   - Columnas constantes, casi constantes y periodos prolongados sin cambios.
6. Cobertura temporal.
   - Primera y ultima observacion disponible, huecos y diferencias entre
     mercados.
7. Diagnostico consolidado.
   - Problema, variables afectadas, magnitud, posible causa y candidato de
     tratamiento.

## Forma de trabajo

Las capas se incorporaran una por una en
`notebooks/01_analisis_exploratorio.ipynb`. Despues de ejecutar cada capa se
revisaran sus hallazgos antes de continuar. Durante el diagnostico no se
modificaran los archivos crudos, no se imputaran valores y no se eliminaran
filas o columnas.

## Primera implementacion

La primera adicion al notebook se limitara a la compatibilidad de los archivos.
Presentara una tabla compacta de comprobaciones, su estado y un detalle
interpretable. Los valores faltantes se abordaran solamente despues de revisar
esta primera capa.
