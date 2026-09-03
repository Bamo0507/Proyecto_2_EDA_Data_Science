"""
Etapa 0 del pipeline: PREPARACION DEL ENTORNO
------------------------------------------------------------
Una sola responsabilidad: crear el entorno e instalar dependencias.

  Lee : requirements.txt
  Hace: - crea .venv si no existe
        - instala las dependencias del proyecto
  Escribe: .venv/

Ejecutar:  python src/00_init.py
"""

import subprocess
import sys
import venv
from pathlib import Path


RAIZ = Path(__file__).resolve().parent.parent
RUTA_VENV = RAIZ / ".venv"
RUTA_REQUIREMENTS = RAIZ / "requirements.txt"


def ruta_python_venv() -> Path:
    if sys.platform == "win32":
        return RUTA_VENV / "Scripts" / "python.exe"
    return RUTA_VENV / "bin" / "python"


def main() -> None:
    if not RUTA_VENV.exists():
        print(f"[creando]   {RUTA_VENV}")
        venv.EnvBuilder(with_pip=True).create(RUTA_VENV)
    else:
        print(f"[ok]        El entorno ya existe: {RUTA_VENV}")

    print(f"[instalando] Dependencias desde {RUTA_REQUIREMENTS.name}")
    subprocess.run(
        [str(ruta_python_venv()), "-m", "pip", "install", "-r", str(RUTA_REQUIREMENTS)],
        check=True,
    )


if __name__ == "__main__":
    main()
