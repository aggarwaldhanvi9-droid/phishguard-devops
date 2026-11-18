from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["model_loaded"] is True

def test_model_info():
    response = client.get("/model-info")
    assert response.status_code == 200
    assert "accuracy" in response.json()

def test_predict_phishing():
    response = client.post(
        "/predict",
        json={"url": "http://paypa1-secure-login-update.xyz/verify"},
    )
    assert response.status_code == 200
    assert response.json()["prediction"] == "phishing"

def test_predict_legitimate():
    response = client.post(
        "/predict",
        json={"url": "https://www.google.com"},
    )
    assert response.status_code == 200
    assert response.json()["prediction"] == "legitimate"