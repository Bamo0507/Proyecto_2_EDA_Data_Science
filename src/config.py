"""Rutas y contratos compartidos del pipeline."""

from pathlib import Path


RAIZ = Path(__file__).resolve().parent.parent
DIR_RAW = RAIZ / "data" / "raw"
DIR_PROCESSED = RAIZ / "data" / "processed"

# Semilla unica para cualquier procedimiento estocastico del proyecto.
SEMILLA = 123

RUTA_TRAIN_CRUDO = DIR_RAW / "train.csv"
RUTA_TEST_CRUDO = DIR_RAW / "test.csv"
RUTA_TRAIN_LABELS = DIR_RAW / "train_labels.csv"
RUTA_TARGET_PAIRS = DIR_RAW / "target_pairs.csv"

RUTA_TRAIN_SIN_COBERTURA = DIR_PROCESSED / "01_train_sin_gold.csv"
RUTA_TEST_SIN_COBERTURA = DIR_PROCESSED / "01_test_sin_gold.csv"
RUTA_TRAIN_FINAL = DIR_PROCESSED / "train_eda.csv"
RUTA_TEST_FINAL = DIR_PROCESSED / "test_eda.csv"

COLUMNA_ID = "date_id"
COLUMNA_AUXILIAR_TEST = "is_scored"

COLUMNAS_SIN_COBERTURA = [
    "US_Stock_GOLD_adj_open",
    "US_Stock_GOLD_adj_high",
    "US_Stock_GOLD_adj_low",
    "US_Stock_GOLD_adj_close",
    "US_Stock_GOLD_adj_volume",
]

ESPECIFICACIONES_OHLC = [
    {
        "mercado": "Acciones de Estados Unidos",
        "open": "_adj_open",
        "high": "_adj_high",
        "low": "_adj_low",
        "close": "_adj_close",
    },
    {
        "mercado": "Futuros JPX",
        "open": "_Open",
        "high": "_High",
        "low": "_Low",
        "close": "_Close",
    },
]

RECHAZOS_ESPERADOS = {
    "train": {"apertura": 97, "cierre": 10},
    "test": {"apertura": 0, "cierre": 0},
}
