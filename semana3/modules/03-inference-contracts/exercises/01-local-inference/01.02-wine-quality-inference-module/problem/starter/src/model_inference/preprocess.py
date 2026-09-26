"""TODO: transformación de una muestra validada en el vector del modelo."""
import pandas as pd
from src.model_inference.contracts import WineQualityRequest

# Este contrato se entrega ya decidido: no cambies ni los nombres ni el orden.
FEATURE_NAMES = (
    "fixed_acidity",
    "volatile_acidity",
    "citric_acid",
    "residual_sugar",
    "chlorides",
    "free_sulfur_dioxide",
    "total_sulfur_dioxide",
    "density",
    "ph",
    "sulphates",
    "alcohol",
)

# Implementa WineFeatures y preprocess_wine_request(). El orden anterior debe
# coincidir con el artefacto, no con un orden arbitrario del CSV.

def preprocess_wine_request(row):
    data = dict(zip(FEATURE_NAMES, row))
    WineQualityRequest.model_validate(data)