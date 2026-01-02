import joblib
import json
import numpy as np
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACT_DIR = BASE_DIR / "artifacts"

scaler = joblib.load(ARTIFACT_DIR / "scaler.pkl")
kmeans = joblib.load(ARTIFACT_DIR / "kmeans.pkl")
gmm = joblib.load(ARTIFACT_DIR / "gmm.pkl")

with open(ARTIFACT_DIR / "feature_schema.json") as f:
    FEATURE_SCHEMA = json.load(f)

FEATURES = FEATURE_SCHEMA["features"]


def predict_customer_segment(input_dict: dict):
    """
    input_dict example:
    {
        "Recency": 30,
        "Frequency": 5,
        "Monetary": 1500,
        "TotalQuantity": 200,
        "UniqueProducts": 20
    }
    """

    df = pd.DataFrame([input_dict])

    # Schema validation
    if list(df.columns) != FEATURES:
        raise ValueError("Input features do not match training schema")

    # Scaling
    X_scaled = scaler.transform(df)

    # Predictions
    kmeans_cluster = int(kmeans.predict(X_scaled)[0])
    gmm_cluster = int(gmm.predict(X_scaled)[0])
    gmm_confidence = float(gmm.predict_proba(X_scaled).max())

    return {
        "kmeans_cluster": kmeans_cluster,
        "gmm_cluster": gmm_cluster,
        "gmm_confidence": round(gmm_confidence, 3)
    }


