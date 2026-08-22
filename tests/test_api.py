"""Tests for the FastAPI inference server."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from src.api.main import app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


class TestHealth:
    def test_health(self, client: TestClient) -> None:
        resp = client.get("/health")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "ok"
        assert isinstance(body["model_loaded"], bool)


class TestModelInfo:
    def test_model_info(self, client: TestClient) -> None:
        resp = client.get("/model/info")
        assert resp.status_code == 200
        body = resp.json()
        assert body["model_name"] == "EskomLSTM"
        assert body["hidden_size"] == 128
        assert body["parameter_count"] > 0


class TestPredict:
    def test_predict_valid(self, client: TestClient) -> None:
        payload = {"sequence": [4200.0] * 24}
        resp = client.post("/predict", json=payload)
        assert resp.status_code == 200
        body = resp.json()
        assert "predicted_load" in body
        assert body["sequence_length"] == 24

    def test_predict_short_sequence(self, client: TestClient) -> None:
        payload = {"sequence": [1.0, 2.0]}
        resp = client.post("/predict", json=payload)
        assert resp.status_code == 200

    def test_predict_empty_body(self, client: TestClient) -> None:
        resp = client.post("/predict", json={})
        assert resp.status_code == 422
