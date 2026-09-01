"""Edge case and extended tests for EskomSense AI."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import torch

from src.evaluation.metrics import compute_metrics
from src.models.lstm import EskomLSTM


# ── Metrics edge cases ──


class TestComputeMetrics:
    def test_perfect_predictions(self):
        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        result = compute_metrics(y, y)
        assert result["mae"] == 0.0
        assert result["rmse"] == 0.0
        assert result["r2"] == pytest.approx(1.0)

    def test_empty_arrays_raises(self):
        with pytest.raises(ValueError, match="empty"):
            compute_metrics(np.array([]), np.array([]))

    def test_mismatched_lengths_raises(self):
        with pytest.raises(ValueError, match="same length"):
            compute_metrics(np.array([1.0, 2.0]), np.array([1.0]))

    def test_all_zero_targets(self):
        y_true = np.array([0.0, 0.0, 0.0])
        y_pred = np.array([1.0, 2.0, 3.0])
        result = compute_metrics(y_true, y_pred)
        assert math.isnan(result["mape"])

    def test_single_element(self):
        result = compute_metrics(np.array([10.0]), np.array([12.0]))
        assert result["mae"] == pytest.approx(2.0)
        assert result["rmse"] == pytest.approx(2.0)

    def test_large_values(self):
        y_true = np.array([1e9, 2e9, 3e9])
        y_pred = np.array([1.1e9, 2.1e9, 3.1e9])
        result = compute_metrics(y_true, y_pred)
        assert result["mae"] == pytest.approx(1e8)

    def test_negative_values(self):
        y_true = np.array([-5.0, -3.0, -1.0])
        y_pred = np.array([-4.0, -3.0, -2.0])
        result = compute_metrics(y_true, y_pred)
        assert result["mae"] == pytest.approx(0.6667, abs=1e-3)

    def test_mixed_sign_values(self):
        y_true = np.array([-10.0, 0.0, 10.0])
        y_pred = np.array([-8.0, 1.0, 9.0])
        result = compute_metrics(y_true, y_pred)
        assert result["mae"] == pytest.approx(1.3333, abs=1e-3)

    def test_r2_all_same_predictions(self):
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([2.0, 2.0, 2.0])
        result = compute_metrics(y_true, y_pred)
        assert result["r2"] == pytest.approx(0.0)

    def test_known_mape(self):
        y_true = np.array([100.0, 200.0, 300.0])
        y_pred = np.array([110.0, 190.0, 330.0])
        result = compute_metrics(y_true, y_pred)
        expected_mape = (10 / 100 + 10 / 200 + 30 / 300) / 3 * 100
        assert result["mape"] == pytest.approx(expected_mape)


# ── Model edge cases ──


class TestEskomLSTMEdge:
    def test_different_input_sizes(self):
        for input_size in [1, 2, 5]:
            model = EskomLSTM(input_size=input_size, hidden_size=32, num_layers=1)
            x = torch.randn(2, 10, input_size)
            out = model(x)
            assert out.shape == (2,)

    def test_single_layer_no_dropout(self):
        model = EskomLSTM(hidden_size=32, num_layers=1, dropout=0.0)
        x = torch.randn(4, 12, 1)
        out = model(x)
        assert out.shape == (4,)

    def test_gradient_flows(self):
        model = EskomLSTM(hidden_size=32, num_layers=1)
        x = torch.randn(2, 10, 1, requires_grad=False)
        out = model(x)
        loss = out.sum()
        loss.backward()
        for param in model.parameters():
            assert param.grad is not None

    def test_model_eval_mode(self):
        model = EskomLSTM(hidden_size=32, num_layers=2, dropout=0.5)
        model.eval()
        x = torch.randn(1, 10, 1)
        out1 = model(x)
        out2 = model(x)
        # In eval mode, dropout is off, so repeated calls should give same output
        assert torch.allclose(out1, out2, atol=1e-6)


# ── DataPipeline edge cases ──


class TestDataPipelineEdge:
    def test_load_csv_missing_target_column(self, tmp_path: Path):
        df = pd.DataFrame(
            {"timestamp": pd.date_range("2024-01-01", periods=10, freq="h"), "other_col": range(10)}
        )
        csv_path = tmp_path / "bad.csv"
        df.to_csv(csv_path, index=False)

        from src.data.preprocessing import DataPipeline

        pipe = DataPipeline(target_column="load_mw")
        with pytest.raises(ValueError, match="not in"):
            pipe.load_csv(csv_path)

    def test_normalise_single_value(self):
        from src.data.preprocessing import DataPipeline

        pipe = DataPipeline()
        result = pipe.normalise(np.array([5.0]))
        assert result[0] == pytest.approx(0.0) or result[0] == pytest.approx(1.0)

    def test_normalise_constant_values(self):
        from src.data.preprocessing import DataPipeline

        pipe = DataPipeline()
        result = pipe.normalise(np.array([5.0, 5.0, 5.0]))
        assert all(v >= 0.0 and v <= 1.0 for v in result)

    def test_create_sequences_too_few_values(self):
        from src.data.preprocessing import DataPipeline

        pipe = DataPipeline(sequence_length=24)
        values = np.arange(10, dtype=np.float32)
        X, y = pipe.create_sequences(values)
        assert X.shape[0] == 0
        assert y.shape[0] == 0

    def test_train_val_split_single_sample(self):
        from src.data.preprocessing import DataPipeline

        pipe = DataPipeline(val_split=0.2)
        X = np.array([[1, 2, 3]])
        y = np.array([4.0])
        X_train, y_train, X_val, y_val = pipe.train_val_split(X, y)
        assert len(X_train) + len(X_val) == 1

    def test_prepare_with_small_dataset(self, tmp_path: Path):
        n = 30
        df = pd.DataFrame(
            {
                "timestamp": pd.date_range("2024-01-01", periods=n, freq="h"),
                "load_mw": np.random.uniform(3000, 5000, size=n),
            }
        )
        csv_path = tmp_path / "small.csv"
        df.to_csv(csv_path, index=False)

        from src.data.preprocessing import DataPipeline

        pipe = DataPipeline(sequence_length=24, target_column="load_mw", val_split=0.2)
        X_train, y_train, X_val, y_val = pipe.prepare(csv_path)
        assert X_train.ndim == 2
        assert X_val.ndim == 2


# ── API edge cases ──


class TestAPIEdge:
    def test_predict_negative_sequence(self, client):
        payload = {"sequence": [-100.0, -200.0, -300.0]}
        resp = client.post("/predict", json=payload)
        assert resp.status_code == 200
        assert "predicted_load" in resp.json()

    def test_predict_single_value(self, client):
        resp = client.post("/predict", json={"sequence": [4200.0]})
        assert resp.status_code == 200
        assert resp.json()["sequence_length"] == 1

    def test_predict_large_sequence(self, client):
        resp = client.post("/predict", json={"sequence": [4200.0] * 100})
        assert resp.status_code == 200
        assert resp.json()["sequence_length"] == 100

    def test_model_info_all_fields(self, client):
        resp = client.get("/model/info")
        assert resp.status_code == 200
        body = resp.json()
        required_fields = [
            "model_name",
            "hidden_size",
            "num_layers",
            "dropout",
            "parameter_count",
            "device",
            "checkpoint_exists",
        ]
        for field in required_fields:
            assert field in body, f"Missing field: {field}"
