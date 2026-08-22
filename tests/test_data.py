"""Tests for the DataPipeline."""

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.data.preprocessing import DataPipeline


@pytest.fixture()
def sample_csv(tmp_path: Path) -> Path:
    """Create a minimal CSV with a ``load_mw`` column."""
    n = 100
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range("2024-01-01", periods=n, freq="h"),
            "load_mw": np.random.uniform(3000, 5000, size=n),
        }
    )
    path = tmp_path / "sample.csv"
    df.to_csv(path, index=False)
    return path


class TestDataPipeline:
    def test_load_csv(self, sample_csv: Path) -> None:
        pipe = DataPipeline(sequence_length=24, target_column="load_mw")
        df = pipe.load_csv(sample_csv)
        assert len(df) == 100
        assert "load_mw" in df.columns

    def test_load_csv_missing_file(self) -> None:
        pipe = DataPipeline()
        with pytest.raises(FileNotFoundError):
            pipe.load_csv("/nonexistent/data.csv")

    def test_normalise_range(self, sample_csv: Path) -> None:
        pipe = DataPipeline(target_column="load_mw")
        df = pipe.load_csv(sample_csv)
        raw = df["load_mw"].values.astype(np.float32)
        normed = pipe.normalise(raw)
        assert normed.min() >= 0.0
        assert normed.max() <= 1.0

    def test_create_sequences_shape(self) -> None:
        seq_len = 24
        pipe = DataPipeline(sequence_length=seq_len, target_column="load_mw")
        values = np.arange(100, dtype=np.float32)
        X, y = pipe.create_sequences(values)
        assert X.shape == (100 - seq_len, seq_len)
        assert y.shape == (100 - seq_len,)

    def test_prepare_end_to_end(self, sample_csv: Path) -> None:
        pipe = DataPipeline(sequence_length=24, target_column="load_mw", val_split=0.2)
        X_train, y_train, X_val, y_val = pipe.prepare(sample_csv)
        assert X_train.ndim == 2
        assert X_val.ndim == 2
        assert len(X_train) > len(X_val)
