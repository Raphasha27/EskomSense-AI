from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_areas_endpoint():
    response = client.get("/api/v1/areas")
    assert response.status_code == 200
    data = response.json()
    assert "areas" in data
    assert len(data["areas"]) > 0

def test_schedule_endpoint():
    response = client.get("/api/v1/schedule?area=Sandton")
    assert response.status_code == 200
    data = response.json()
    assert "schedule" in data or "stages" in data or "predictions" in data
