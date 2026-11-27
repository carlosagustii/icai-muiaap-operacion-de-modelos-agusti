"""Carga del modelo entrenado (TU)."""
from pathlib import Path

import joblib

from reservas.config import RUTA_MODELO
from functools import lru_cache

# TODO: el modelo debe cargarse UNA sola vez y reutilizarse en las siguientes
#   llamadas (cargarlo en cada prediccion es lento). Investiga
#   functools.lru_cache y aplicalo como decorador a esta funcion.
#   Comprobacion: tests/test_cargador.py::test_el_modelo_se_carga_una_sola_vez
@lru_cache
def cargar_modelo(ruta: Path = RUTA_MODELO):
    """Carga el joblib una sola vez y reutiliza el mismo objeto en las siguientes llamadas."""
    # TODO: si el fichero no existe, lanza FileNotFoundError con un mensaje que
    #   diga como generarlo ("uv run entrenar"). Si existe, cargalo con joblib.
    #   Comprobacion: tests/test_cargador.py::test_ruta_inexistente_da_un_error_claro
    try:
        model = joblib.load(ruta)
    except FileNotFoundError:
        raise FileNotFoundError("generar modelo con uv run entrenar")
    return model
