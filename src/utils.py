"""Utilidades compartidas de carga, guardado y validacion."""

import sys
from pathlib import Path

import pandas as pd


def banner(titulo: str) -> None:
    """Muestra el inicio de una etapa."""
    separador = "=" * 60
    print(f"\n{separador}\n{titulo}\n{separador}")


def cargar(ruta: Path, **kwargs) -> pd.DataFrame:
    """Carga un CSV y reporta sus dimensiones."""
    if not ruta.exists():
        print(f"[FALLO] No existe el archivo: {ruta}")
        sys.exit(1)

    datos = pd.read_csv(ruta, **kwargs)
    print(
        f"[cargado]  {ruta.name:<30} -> "
        f"{len(datos):,} filas, {datos.shape[1]:,} columnas"
    )
    return datos


def guardar(datos: pd.DataFrame, ruta: Path) -> None:
    """Guarda un CSV reproducible sin incluir el indice."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    datos.to_csv(ruta, index=False)
    print(
        f"[guardado] {ruta.name:<30} -> "
        f"{len(datos):,} filas, {datos.shape[1]:,} columnas"
    )


def afirmar(condicion: bool, mensaje: str) -> None:
    """Detiene el pipeline cuando un contrato no se cumple."""
    if not condicion:
        print(f"[FALLO] {mensaje}")
        sys.exit(1)
    print(f"[ok]      {mensaje}")


def afirmar_date_id(datos: pd.DataFrame, nombre: str) -> None:
    """Valida presencia, unicidad y orden de date_id."""
    afirmar("date_id" in datos.columns, f"{nombre} contiene date_id")
    afirmar(datos["date_id"].notna().all(), f"{nombre} no posee date_id ausentes")
    afirmar(datos["date_id"].is_unique, f"{nombre} posee date_id unicos")
    afirmar(datos["date_id"].is_monotonic_increasing, f"{nombre} esta ordenado por date_id")
