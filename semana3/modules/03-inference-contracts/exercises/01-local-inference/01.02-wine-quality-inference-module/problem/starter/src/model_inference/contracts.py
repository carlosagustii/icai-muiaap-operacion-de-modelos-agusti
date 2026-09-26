"""TODO: contratos de entrada y salida de la inferencia."""

# Implementa WineQualityRequest y WineQualityPrediction con Pydantic.
# Revisa los campos de assets/inference_samples.csv y prohíbe columnas extra.

class WineQualityRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    fixed_acidity: float = Field(ge=0, le=20)
    volatile_acidity: float = Field(ge=0, le=2)
    citric_acid: float = Field(ge=0, le=1)
    residual_sugar: float = Field(ge=0, le=4)
    chlorides: float = Field(ge=0, le=0.1)
    free_sulfur_dioxide: float = Field(ge=0, le=50)
    total_sulfur_dioxide: float = Field(ge=0, le=100)
    density: float = Field(ge=0, le=1)
    ph: float = Field(ge=0, le=4.5)
    sulphates: float = Field(ge=0, le=3)
    alcohol: float = Field(ge=5, le=20)


class WineQualityPrediction(BaseModel):

    prediction:float = Field(ge=0, le=1)
