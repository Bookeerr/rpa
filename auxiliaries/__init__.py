"""Auxiliares acotados: no navegan ni coordinan el robot."""
from pathlib import Path
import sys

# Rocketbot usa su propio Python; estas dependencias puras viajan con el proyecto.
# Nunca agregar todo el site-packages del venv (puede contener binarios incompatibles).
_vendor = str(Path(__file__).resolve().parent / '_vendor')
if Path(_vendor).is_dir() and _vendor not in sys.path:
    sys.path.insert(0, _vendor)
