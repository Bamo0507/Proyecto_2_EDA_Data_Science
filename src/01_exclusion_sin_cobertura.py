"""
Etapa 1 del pipeline: EXCLUSION DE VARIABLES SIN COBERTURA
------------------------------------------------------------
Una sola responsabilidad: excluir las variables US_Stock_GOLD.

  Lee : data/raw/train.csv y data/raw/test.csv
  Hace: - valida que las cinco variables esperadas existan
        - excluye unicamente las variables US_Stock_GOLD
  Escribe: data/processed/01_train_sin_gold.csv
           data/processed/01_test_sin_gold.csv

Ejecutar:  python src/01_exclusion_sin_cobertura.py
"""

from config import (
    COLUMNA_AUXILIAR_TEST,
    COLUMNAS_SIN_COBERTURA,
    RUTA_TARGET_PAIRS,
    RUTA_TEST_CRUDO,
    RUTA_TEST_SIN_COBERTURA,
    RUTA_TRAIN_CRUDO,
    RUTA_TRAIN_LABELS,
    RUTA_TRAIN_SIN_COBERTURA,
)
from utils import afirmar, afirmar_date_id, banner, cargar, guardar


def main() -> None:
    banner("ETAPA 1 - EXCLUSION DE VARIABLES SIN COBERTURA")

    train = cargar(RUTA_TRAIN_CRUDO)
    test = cargar(RUTA_TEST_CRUDO)
    train_labels = cargar(RUTA_TRAIN_LABELS)
    target_pairs = cargar(RUTA_TARGET_PAIRS)

    afirmar_date_id(train, "train.csv")
    afirmar_date_id(test, "test.csv")
    afirmar(
        set(COLUMNAS_SIN_COBERTURA).issubset(train.columns),
        "train.csv contiene las cinco variables US_Stock_GOLD",
    )
    afirmar(
        set(COLUMNAS_SIN_COBERTURA).issubset(test.columns),
        "test.csv contiene las cinco variables US_Stock_GOLD",
    )
    afirmar(
        COLUMNA_AUXILIAR_TEST in test.columns,
        "test.csv contiene la variable auxiliar is_scored",
    )
    afirmar(
        train["date_id"].equals(train_labels["date_id"]),
        "train.csv y train_labels.csv poseen los mismos date_id",
    )
    afirmar(
        set(train_labels.columns) - {"date_id"} == set(target_pairs["target"]),
        "train_labels.csv y target_pairs.csv documentan los mismos targets",
    )
    instrumentos_target = {
        instrumento
        for par in target_pairs["pair"]
        for instrumento in par.split(" - ")
    }
    afirmar(
        instrumentos_target.issubset(train.columns),
        "train.csv contiene todos los instrumentos utilizados por los targets",
    )
    afirmar(
        not instrumentos_target.intersection(COLUMNAS_SIN_COBERTURA),
        "las variables US_Stock_GOLD no participan en la definicion de targets",
    )

    date_id_train = train["date_id"].copy()
    date_id_test = test["date_id"].copy()
    columnas_train_esperadas = [
        columna for columna in train.columns if columna not in COLUMNAS_SIN_COBERTURA
    ]
    columnas_test_esperadas = [
        columna for columna in test.columns if columna not in COLUMNAS_SIN_COBERTURA
    ]

    train_sin_cobertura = train.drop(columns=COLUMNAS_SIN_COBERTURA)
    test_sin_cobertura = test.drop(columns=COLUMNAS_SIN_COBERTURA)

    afirmar(
        train_sin_cobertura.columns.tolist() == columnas_train_esperadas,
        "train conserva todas las columnas excepto US_Stock_GOLD",
    )
    afirmar(
        test_sin_cobertura.columns.tolist() == columnas_test_esperadas,
        "test conserva todas las columnas excepto US_Stock_GOLD",
    )
    afirmar(
        train_sin_cobertura["date_id"].equals(date_id_train),
        "train conserva todas las filas y el orden de date_id",
    )
    afirmar(
        test_sin_cobertura["date_id"].equals(date_id_test),
        "test conserva todas las filas y el orden de date_id",
    )

    predictores_train = set(train_sin_cobertura.columns) - {"date_id"}
    predictores_test = set(test_sin_cobertura.columns) - {
        "date_id",
        COLUMNA_AUXILIAR_TEST,
    }
    afirmar(
        predictores_train == predictores_test,
        "train y test conservan el mismo conjunto de predictores",
    )

    guardar(train_sin_cobertura, RUTA_TRAIN_SIN_COBERTURA)
    guardar(test_sin_cobertura, RUTA_TEST_SIN_COBERTURA)


if __name__ == "__main__":
    main()
