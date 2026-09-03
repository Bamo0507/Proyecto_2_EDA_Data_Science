"""Ejecuta las etapas del pipeline en orden y se detiene ante un fallo."""

import subprocess
import sys
from pathlib import Path


DIR_SRC = Path(__file__).resolve().parent
ETAPAS = [
    "01_exclusion_sin_cobertura.py",
    "02_consistencia_ohlc.py",
]


def main() -> None:
    for etapa in ETAPAS:
        ruta_etapa = DIR_SRC / etapa
        print(f"\n[ejecutando] {etapa}", flush=True)
        subprocess.run([sys.executable, str(ruta_etapa)], check=True)
    print("\n[ok] Pipeline completado correctamente", flush=True)


if __name__ == "__main__":
    main()
