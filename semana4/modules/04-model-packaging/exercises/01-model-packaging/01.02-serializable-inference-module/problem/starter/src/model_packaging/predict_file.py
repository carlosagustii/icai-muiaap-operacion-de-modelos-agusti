"""Punto de extensión del CLI de inferencia sobre un bundle."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from model_packaging.artifact import (
    DEFAULT_BUNDLE_PATH,
    infer_wine_quality,
    load_model_bundle,
)
from model_packaging.contracts import WineQualityRequest

OUTPUT_COLUMNS = (
    "sample_id",
    "quality_band",
    "confidence",
    "model_version",
    "preprocessing_version",
)


def predict_file(
    input_path: Path,
    output_path: Path,
    bundle_path: Path,
) -> int:
    """TODO: valida todas las filas y escribe el CSV solo al final."""

    bundle = load_model_bundle(bundle_path)

    rows = []
    with input_path.open(newline="", encoding="utf-8") as source:
        for row in csv.DictReader(source):
            sample_id = row.pop("sample_id", "")
            if not sample_id.strip():
                raise ValueError("Cada fila necesita un sample_id")
            try:
                request = WineQualityRequest.model_validate(row)
                prediction = infer_wine_quality(bundle, request)
            except ValueError as error:
                raise ValueError(f"Fila {sample_id} invalida: {error}") from error #igual que en S3, se dice que fila falla
            rows.append({"sample_id": sample_id, **prediction.model_dump()})

    # solo se escribe si todas las filas son validas, asi no queda un CSV a medias
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def parse_args() -> argparse.Namespace:
    """Declara la interfaz del comando público."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--bundle", default=DEFAULT_BUNDLE_PATH, type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    raise SystemExit(
        predict_file(
            input_path=arguments.input,
            output_path=arguments.output,
            bundle_path=arguments.bundle,
        )
    )