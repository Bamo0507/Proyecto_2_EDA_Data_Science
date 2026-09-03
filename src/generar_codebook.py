"""Regenera el diccionario de datos a partir de la version final."""

from config import (
    COLUMNA_AUXILIAR_TEST,
    COLUMNAS_SIN_COBERTURA,
    RAIZ,
    RUTA_TEST_FINAL,
    RUTA_TRAIN_FINAL,
)
from utils import afirmar, cargar


RUTA_CODEBOOK = RAIZ / "codebook.md"

MEDICIONES = {
    "_adj_open": "precio ajustado de apertura",
    "_adj_high": "precio máximo ajustado",
    "_adj_low": "precio mínimo ajustado",
    "_adj_close": "precio ajustado de cierre",
    "_adj_volume": "volumen ajustado",
    "_Open": "precio de apertura",
    "_High": "precio máximo",
    "_Low": "precio mínimo",
    "_Close": "precio de cierre",
    "_Volume": "volumen negociado",
    "_Open Interest": "interés abierto",
    "_Settlement Price": "precio de liquidación",
}


def descripcion_variable(variable: str) -> tuple[str, str]:
    if variable == "date_id":
        return (
            "Identificador ordinal de la secuencia temporal.",
            "Entero único, ordenado y sin valores faltantes.",
        )

    if variable.startswith("FX_"):
        par = variable.removeprefix("FX_")
        return (
            f"Tipo de cambio de cierre para el par {par}.",
            "Valor numérico positivo o NaN cuando no existe una observación disponible.",
        )

    for sufijo, medicion in MEDICIONES.items():
        if variable.endswith(sufijo):
            instrumento = variable.removesuffix(sufijo)
            if variable.startswith("US_Stock_"):
                mercado = "acciones de Estados Unidos"
            elif variable.startswith("JPX_"):
                mercado = "futuros de Japan Exchange Group"
            else:
                mercado = "London Metal Exchange"
            nota = "Valor numérico o NaN cuando no existe una observación disponible."
            if sufijo in {"_adj_open", "_adj_close"}:
                nota += " Los valores que incumplen el intervalo OHLC se rechazan como NaN."
            return (
                f"{medicion.capitalize()} de {instrumento}, perteneciente a {mercado}.",
                nota,
            )

    return (
        "Variable numérica histórica proporcionada por el reto.",
        "Valor numérico o NaN cuando no existe una observación disponible.",
    )


def construir_codebook(train, test) -> str:
    lineas = [
        "# Codebook",
        "",
        "Este diccionario documenta `data/processed/train_eda.csv`, generado a partir de "
        "`data/raw/train.csv` mediante `01_exclusion_sin_cobertura.py` y "
        "`02_consistencia_ohlc.py`. `test_eda.csv` conserva el mismo conjunto de "
        "predictores y agrega la variable auxiliar `is_scored`.",
        "",
        "## Variables",
        "",
        "| Variable | Tipo pandas | Descripción | Valores válidos / notas |",
        "|---|---|---|---|",
    ]

    for variable in train.columns:
        descripcion, notas = descripcion_variable(variable)
        lineas.append(
            f"| `{variable}` | `{train[variable].dtype}` | {descripcion} | {notas} |"
        )

    lineas.extend(
        [
            "",
            "### Variable exclusiva de prueba",
            "",
            "| Variable | Tipo pandas | Descripción | Valores válidos / notas |",
            "|---|---|---|---|",
            f"| `{COLUMNA_AUXILIAR_TEST}` | `{test[COLUMNA_AUXILIAR_TEST].dtype}` | "
            "Indica si la fila será considerada por el mecanismo de evaluación. | "
            "Valor lógico proporcionado por el reto. |",
            "",
            "## Reglas de preparación aplicadas",
            "",
            "- Se conservaron las 1,961 filas y el orden original de `date_id`.",
            "- Se excluyeron las cinco variables `US_Stock_GOLD_*` debido a su cobertura "
            "insuficiente en entrenamiento y ausencia completa en prueba.",
            "- Se rechazaron como `NaN` 97 aperturas y 10 cierres ubicados fuera del "
            "intervalo definido por el mínimo y el máximo del mismo instrumento y día.",
            "- No se eliminaron filas, no se imputaron valores y no se modificaron los "
            "máximos o mínimos para forzar la consistencia OHLC.",
            "",
            "## Política de valores faltantes",
            "",
            "Los `NaN` se clasifican en dos grupos. Los **ausentes en el origen** "
            "corresponden principalmente a diferencias de disponibilidad entre mercados y "
            "se conservan porque las demás variables de la fila todavía pueden aportar "
            "información. Los **rechazados por invalidez** corresponden a las 107 mediciones "
            "OHLC que existían en el origen, pero incumplían una regla objetiva y no podían "
            "reconstruirse sin inventar un valor.",
            "",
            "La preparación no utiliza media, mediana, relleno hacia adelante, relleno hacia "
            "atrás ni otro método de imputación. Cada análisis debe trabajar con las "
            "observaciones disponibles para las variables que utiliza y reportar la cantidad "
            "de pares válidos.",
            "",
            "## Diferencias respecto al archivo original",
            "",
            "| Dataset | Filas | Columnas | Diferencia principal |",
            "|---|---:|---:|---|",
            "| `data/raw/train.csv` | 1,961 | 558 | Fuente original sin modificaciones. |",
            "| `data/processed/train_eda.csv` | 1,961 | 553 | Cinco columnas excluidas y 107 mediciones rechazadas como `NaN`. |",
            "| `data/raw/test.csv` | 134 | 559 | Fuente original con `is_scored`. |",
            "| `data/processed/test_eda.csv` | 134 | 554 | Cinco columnas excluidas; no se encontraron violaciones OHLC. |",
            "",
            "## Fuente",
            "",
            "Demkin, M., Takano, N., Rai, R., Dane, S., & Kitayama, T. (2025). "
            "*MITSUI&CO. Commodity Prediction Challenge*. Kaggle. "
            "https://www.kaggle.com/competitions/mitsui-commodity-prediction-challenge",
            "",
        ]
    )
    return "\n".join(lineas)


def main() -> None:
    train = cargar(RUTA_TRAIN_FINAL)
    test = cargar(RUTA_TEST_FINAL)
    afirmar(
        list(train.columns)
        == [
            columna
            for columna in test.columns
            if columna != COLUMNA_AUXILIAR_TEST
        ],
        "train_eda y test_eda poseen los mismos predictores y el mismo orden",
    )
    afirmar(
        not set(COLUMNAS_SIN_COBERTURA).intersection(train.columns),
        "el dataset final no contiene las variables US_Stock_GOLD",
    )

    RUTA_CODEBOOK.write_text(construir_codebook(train, test), encoding="utf-8")
    print(
        f"[guardado] {RUTA_CODEBOOK.name} -> "
        f"{len(train.columns):,} variables documentadas"
    )


if __name__ == "__main__":
    main()
