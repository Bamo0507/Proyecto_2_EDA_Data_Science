"""
Etapa 2 del pipeline: CONSISTENCIA OHLC
------------------------------------------------------------
Una sola responsabilidad: rechazar aperturas y cierres fuera del rango diario.

  Lee : data/processed/01_train_sin_gold.csv
         data/processed/01_test_sin_gold.csv
  Hace: - detecta aperturas y cierres fuera de [minimo, maximo]
        - reemplaza unicamente esas celdas por NaN
  Escribe: data/processed/train_eda.csv
           data/processed/test_eda.csv

Ejecutar:  python src/02_consistencia_ohlc.py
"""

import pandas as pd

from config import (
    COLUMNA_AUXILIAR_TEST,
    COLUMNAS_SIN_COBERTURA,
    ESPECIFICACIONES_OHLC,
    RECHAZOS_ESPERADOS,
    RUTA_TEST_FINAL,
    RUTA_TEST_SIN_COBERTURA,
    RUTA_TRAIN_FINAL,
    RUTA_TRAIN_SIN_COBERTURA,
)
from utils import afirmar, afirmar_date_id, banner, cargar, guardar


def rechazar_mediciones_invalidas(datos: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    resultado = datos.copy()
    conteos = {"apertura": 0, "cierre": 0}

    for especificacion in ESPECIFICACIONES_OHLC:
        sufijo_open = especificacion["open"]
        columnas_open = [
            columna for columna in resultado.columns if columna.endswith(sufijo_open)
        ]
        familias_incompletas = []

        for columna_open in columnas_open:
            instrumento = columna_open.removesuffix(sufijo_open)
            columnas_esperadas = {
                f"{instrumento}{especificacion[medicion]}"
                for medicion in ("open", "high", "low", "close")
            }
            if not columnas_esperadas.issubset(resultado.columns):
                familias_incompletas.append(instrumento)

        afirmar(
            not familias_incompletas,
            f"{especificacion['mercado']} posee familias OHLC completas",
        )

        for columna_open in columnas_open:
            instrumento = columna_open.removesuffix(sufijo_open)
            columnas = {
                medicion: f"{instrumento}{especificacion[medicion]}"
                for medicion in ("open", "high", "low", "close")
            }
            valores = resultado[list(columnas.values())].rename(
                columns={columna: medicion for medicion, columna in columnas.items()}
            )
            filas_validas = valores.notna().all(axis=1)
            apertura_invalida = filas_validas & (
                (valores["open"] < valores["low"])
                | (valores["open"] > valores["high"])
            )
            cierre_invalido = filas_validas & (
                (valores["close"] < valores["low"])
                | (valores["close"] > valores["high"])
            )

            conteos["apertura"] += int(apertura_invalida.sum())
            conteos["cierre"] += int(cierre_invalido.sum())
            resultado.loc[apertura_invalida, columnas["open"]] = pd.NA
            resultado.loc[cierre_invalido, columnas["close"]] = pd.NA

    return resultado, conteos


def contar_violaciones(datos: pd.DataFrame) -> int:
    total = 0
    for especificacion in ESPECIFICACIONES_OHLC:
        sufijo_open = especificacion["open"]
        for columna_open in [
            columna for columna in datos.columns if columna.endswith(sufijo_open)
        ]:
            instrumento = columna_open.removesuffix(sufijo_open)
            columnas = {
                medicion: f"{instrumento}{especificacion[medicion]}"
                for medicion in ("open", "high", "low", "close")
            }
            valores = datos[list(columnas.values())].rename(
                columns={columna: medicion for medicion, columna in columnas.items()}
            )
            filas_validas = valores.notna().all(axis=1)
            total += int(
                (
                    filas_validas
                    & (
                        (valores["open"] < valores["low"])
                        | (valores["open"] > valores["high"])
                        | (valores["close"] < valores["low"])
                        | (valores["close"] > valores["high"])
                    )
                ).sum()
            )
    return total


def procesar_dataset(
    nombre: str,
    ruta_entrada,
    ruta_salida,
) -> None:
    datos = cargar(ruta_entrada)
    afirmar_date_id(datos, ruta_entrada.name)
    afirmar(
        not set(COLUMNAS_SIN_COBERTURA).intersection(datos.columns),
        f"{nombre} no contiene variables US_Stock_GOLD",
    )
    if nombre == "test":
        afirmar(
            COLUMNA_AUXILIAR_TEST in datos.columns,
            "test conserva la variable auxiliar is_scored",
        )

    filas_originales = len(datos)
    columnas_originales = datos.columns.tolist()
    date_id_original = datos["date_id"].copy()
    faltantes_originales = int(datos.isna().sum().sum())

    datos_consistentes, conteos = rechazar_mediciones_invalidas(datos)
    esperados = RECHAZOS_ESPERADOS[nombre]

    afirmar(
        conteos == esperados,
        f"{nombre} rechaza las mediciones esperadas: {conteos}",
    )
    afirmar(
        len(datos_consistentes) == filas_originales,
        f"{nombre} conserva todas las filas",
    )
    afirmar(
        datos_consistentes.columns.tolist() == columnas_originales,
        f"{nombre} conserva todas las columnas recibidas",
    )
    afirmar(
        datos_consistentes["date_id"].equals(date_id_original),
        f"{nombre} conserva el orden de date_id",
    )
    afirmar(
        int(datos_consistentes.isna().sum().sum()) - faltantes_originales
        == sum(conteos.values()),
        f"{nombre} agrega NaN unicamente por mediciones OHLC invalidas",
    )
    afirmar(
        contar_violaciones(datos_consistentes) == 0,
        f"{nombre} no conserva aperturas o cierres fuera del intervalo diario",
    )

    guardar(datos_consistentes, ruta_salida)


def main() -> None:
    banner("ETAPA 2 - CONSISTENCIA OHLC")
    procesar_dataset("train", RUTA_TRAIN_SIN_COBERTURA, RUTA_TRAIN_FINAL)
    procesar_dataset("test", RUTA_TEST_SIN_COBERTURA, RUTA_TEST_FINAL)


if __name__ == "__main__":
    main()
