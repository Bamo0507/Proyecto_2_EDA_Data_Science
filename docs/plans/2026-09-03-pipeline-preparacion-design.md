# Diseno del pipeline de preparacion

## Objetivo

Generar una version estable de `train.csv` y `test.csv` para el analisis
exploratorio, aplicando solamente las decisiones justificadas durante el
diagnostico de calidad y conservando intactos los archivos originales.

## Enfoque aprobado

Se utilizara un pipeline de dos etapas porque permite separar las dos
transformaciones necesarias sin agregar pasos que no modifican los datos. Cada
etapa cargara la salida anterior, validara su contrato de entrada, aplicara una
sola responsabilidad, validara el resultado y guardara una salida reproducible
en `data/processed/`.

```text
data/raw/train.csv + data/raw/test.csv
                    |
                    v
        01_exclusion_sin_cobertura.py
                    |
                    +--> 01_train_sin_gold.csv
                    +--> 01_test_sin_gold.csv
                    |
                    v
             02_consistencia_ohlc.py
                    |
                    +--> train_eda.csv
                    +--> test_eda.csv
```

## Etapa 1: exclusion de variables sin cobertura

La primera etapa eliminara las cinco variables `US_Stock_GOLD_*` de los datos
de entrenamiento y prueba. Estas variables poseen cobertura insuficiente en
`train.csv`, se encuentran completamente vacias en `test.csv` y no forman
parte de la definicion de los targets. No se eliminara ninguna fila y el orden
de `date_id` se conservara.

## Etapa 2: consistencia OHLC

La segunda etapa revisara las familias OHLC de acciones estadounidenses y
futuros JPX. Cuando una apertura o un cierre se encuentre fuera del intervalo
definido por el minimo y el maximo del mismo instrumento y dia, se reemplazara
unicamente esa celda por `NaN`. No se modificaran el maximo, el minimo, las
otras mediciones ni la fila completa.

El diagnostico anticipa 107 rechazos en entrenamiento, correspondientes a 97
aperturas y 10 cierres. `test.csv` no presenta violaciones, pero se aplicara la
misma regla para mantener un contrato uniforme.

## Archivos complementarios

`train_labels.csv` y `target_pairs.csv` permaneceran en `data/raw/`, dado que no
requieren transformaciones. `test_eda.csv` conservara la columna auxiliar
`is_scored`.

## Validaciones de liberacion

El pipeline comprobara como minimo:

- conservacion de filas y del orden de `date_id`;
- eliminacion exclusiva de las cinco columnas `US_Stock_GOLD_*`;
- correspondencia de predictores entre entrenamiento y prueba;
- conservacion de `is_scored` en prueba;
- 107 nuevos `NaN` por invalidez OHLC en entrenamiento y ninguno en prueba;
- ausencia de aperturas o cierres fuera de su intervalo en las salidas finales;
- ausencia de modificaciones en `data/raw/`.

## Archivos de soporte

`config.py` concentrara las rutas y contratos; `utils.py` proporcionara carga,
guardado y validaciones compartidas; `run_pipeline.py` ejecutara las etapas en
orden y se detendra ante cualquier fallo; y `00_init.py` permitira recrear el
entorno a partir de `requirements.txt`.

## Documentacion

El README explicara el flujo, las etapas y su ejecucion. El codebook describira
las variables finales, las reglas aplicadas y la diferencia entre valores
ausentes en el origen y valores rechazados por invalidez.
