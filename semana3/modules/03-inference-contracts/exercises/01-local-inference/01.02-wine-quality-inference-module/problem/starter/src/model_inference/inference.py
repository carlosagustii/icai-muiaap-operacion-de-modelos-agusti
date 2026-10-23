"""TODO: carga del .joblib e inferencia sobre características preparadas."""

# Declara DEFAULT_MODEL_PATH, load_wine_quality_model() e infer_wine_quality().
# Comprueba las características del artefacto antes de llamar al clasificador.

from pathlib import Path
import joblib
DEFAULT_MODEL_PATH = Path(r"C:\TRASTEO\icai-muiaap-operacion-de-modelos-agusti\semana3\modules\03-inference-contracts\exercises\01-local-inference\01.02-wine-quality-inference-module\problem\starter\models\wine_quality_classifier.joblib")
def load_wine_quality_model(Path = DEFAULT_MODEL_PATH): #se queda como default, si no meto ninguna ruta usa esa
    artefacto = joblib.load(Path)
    estimador = artefacto.get("estimator")
    if not hasattr(estimador, "predict_proba"):   ### PREGUNTA: no entiendo por que tengo que comprobar predict_proba
        raise ValueError("El artefacto no tiene las características necesarias" \
        "")
    return artefacto


def infer_wine_quality()
