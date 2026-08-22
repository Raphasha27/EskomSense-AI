"""Tests for the EskomLSTM model."""

from __future__ import annotations

import torch

from src.models.lstm import EskomLSTM


class TestEskomLSTM:
    def test_forward_shape(self) -> None:
        model = EskomLSTM(input_size=1, hidden_size=64, num_layers=2)
        x = torch.randn(8, 24, 1)  # batch=8, seq=24, features=1
        out = model(x)
        assert out.shape == (8,), f"Expected (8,), got {out.shape}"

    def test_single_sample(self) -> None:
        model = EskomLSTM()
        x = torch.randn(1, 24, 1)
        out = model(x)
        assert out.shape == (1,)

    def test_parameter_count_positive(self) -> None:
        model = EskomLSTM(hidden_size=128, num_layers=2)
        assert model.count_parameters() > 0

    def test_parameter_count_varies_with_hidden(self) -> None:
        small = EskomLSTM(hidden_size=32, num_layers=1)
        large = EskomLSTM(hidden_size=256, num_layers=3)
        assert large.count_parameters() > small.count_parameters()
