# Proyecto 2 - Análisis Exploratorio

Este repositorio contiene el Proyecto 2 del curso CC3084 - Data Science. El
trabajo utiliza los datos del MITSUI&CO. Commodity Prediction Challenge para
examinar la estructura, calidad, distribución y relaciones presentes entre
instrumentos de distintos mercados.

## Dataset y problemas identificados

El conjunto reúne información de la London Metal Exchange, Japan Exchange
Group, acciones de Estados Unidos y tipos de cambio. La inspección inicial
identificó tres condiciones relevantes para preparar los datos:

- valores faltantes estructurales asociados con la disponibilidad de cada
  mercado;
- cinco variables `US_Stock_GOLD_*` sin cobertura útil para el conjunto de
  prueba;
- 97 aperturas y 10 cierres de acciones estadounidenses fuera del intervalo
  diario definido por el mínimo y el máximo.

Los valores faltantes estructurales se conservan y no se aplica imputación. Los
archivos ubicados en `data/raw/` constituyen la fuente de verdad y nunca son
modificados por el pipeline.

## Estructura

```text
src/                 Pipeline reproducible y archivos de soporte
notebooks/           Exploración y análisis exploratorio
data/raw/            Datos originales, nunca se modifican
data/processed/      Datos regenerables, no se versionan
docs/plans/          Decisiones de diseño acordadas
informe.md           Planteamiento y redacción del informe
codebook.md          Diccionario del dataset final
requirements.txt     Dependencias mínimas del proyecto
```

## Pipeline

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

| Etapa | Archivo | Responsabilidad | Entrada | Salida |
|---|---|---|---|---|
| 1 | `01_exclusion_sin_cobertura.py` | Excluir únicamente las cinco variables `US_Stock_GOLD_*` | `train.csv`, `test.csv` | `01_train_sin_gold.csv`, `01_test_sin_gold.csv` |
| 2 | `02_consistencia_ohlc.py` | Rechazar mediante `NaN` aperturas y cierres fuera del intervalo diario | Salidas de la etapa 1 | `train_eda.csv`, `test_eda.csv` |

La versión final de entrenamiento conserva las 1,961 filas y contiene 553
columnas. La versión de prueba conserva las 134 filas y contiene 554 columnas,
incluyendo `is_scored`.

## Archivos de apoyo

- `00_init.py`: crea `.venv` e instala las dependencias.
- `config.py`: centraliza rutas y contratos del pipeline.
- `utils.py`: contiene las funciones compartidas de carga, guardado y
  validación.
- `run_pipeline.py`: ejecuta las etapas en orden y se detiene si alguna
  validación falla.
- `generar_codebook.py`: regenera el diccionario de las columnas finales.

## Ejecución

Desde la raíz del proyecto:

```bash
python src/00_init.py
source .venv/bin/activate
python src/run_pipeline.py
python src/generar_codebook.py
```

En Windows, la activación del entorno se realiza con:

```powershell
.venv\Scripts\activate
```

También es posible ejecutar una etapa individual con el entorno activado:

```bash
python src/01_exclusion_sin_cobertura.py
python src/02_consistencia_ohlc.py
```

## Justificación del diseño

Se utiliza un pipeline por etapas para poder auditar cada transformación por
separado y detectar un incumplimiento en el punto donde ocurre. La primera etapa
modifica únicamente la cobertura de columnas y la segunda atiende solamente la
consistencia OHLC; de esta forma, una decisión puede revisarse sin mezclarla con
las demás. Cada etapa valida su entrada y salida, conserva `date_id` y genera
archivos intermedios reproducibles.

Las decisiones y variables del resultado se describen en [codebook.md](codebook.md).

## Reproducibilidad

La semilla única del proyecto es `123` y se encuentra centralizada en
`src/config.py`. Cualquier muestreo, separación de datos, algoritmo o
visualización que incorpore aleatoriedad deberá importar y utilizar la constante
`SEMILLA`, evitando definir valores diferentes dentro de notebooks o scripts.
