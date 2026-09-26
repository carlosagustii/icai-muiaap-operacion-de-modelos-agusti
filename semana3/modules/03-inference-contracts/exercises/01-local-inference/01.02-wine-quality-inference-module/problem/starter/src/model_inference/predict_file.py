"""TODO: script CLI que encadena contratos, preprocesado e inferencia."""
import pandas as pd
from src.model_inference.contracts import WineQualityRequest
# Implementa el comando:
# python -m model_inference.predict_file --input <csv> --output <csv>
# No dejes un archivo de salida parcial si alguna fila es inválida.
df_csv = pd.read_csv("assets/inference_samples.csv")
for index, row in df_csv:
    WineQualityRequest(row)