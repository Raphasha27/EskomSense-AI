"""Centralised configuration for EskomSense AI."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Immutable application settings with sensible defaults."""

    SEQUENCE_LENGTH: int = 24
    HIDDEN_SIZE: int = 128
    NUM_LAYERS: int = 2
    DROPOUT: float = 0.2
    LEARNING_RATE: float = 1e-3
    EPOCHS: int = 50
    BATCH_SIZE: int = 32
    VAL_SPLIT: float = 0.2
    EARLY_STOP_PATIENCE: int = 7
    SEED: int = 42

    MODEL_PATH: Path = field(default_factory=lambda: Path("models/"))
    DATA_PATH: Path = field(default_factory=lambda: Path("data/"))
    DEVICE: str = "auto"

    def __post_init__(self) -> None:
        self.MODEL_PATH.mkdir(parents=True, exist_ok=True)
        self.DATA_PATH.mkdir(parents=True, exist_ok=True)


settings = Settings()
