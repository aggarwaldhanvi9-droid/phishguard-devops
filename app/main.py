import json
from pathlib import Path
import joblib
from fastapi import FastAPI
from pydantic import BaseModel
from app.features import extract_features

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "model.joblib"
METRICS_PATH = BASE_DIR / "model" / "metrics.json"

model = joblib.load(MODEL_PATH)
metrics = json.loads(METRICS_PATH.read_text()) if METRICS_PATH.exists() else {}

app = FastAPI(title="PhishGuard ML API", version="1.0.0")

class URLRequest(BaseModel):
    url: str

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}

@app.get("/model-info")
def model_info():
    return metrics

@app.post("/predict")
def predict(payload: URLRequest):
    features = [extract_features(payload.url)]
    pred = int(model.predict(features)[0])
    prob = float(model.predict_proba(features)[0][1])
    return {
        "url": payload.url,
        "prediction": "phishing" if pred == 1 else "legitimate",
        "phishing_probability": round(prob, 4),
    }