"""FastAPI inference server for EskomSense AI."""

from __future__ import annotations

import numpy as np
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.config import settings
from src.models.lstm import EskomLSTM

# ---------------------------------------------------------------------------
# App & model
# ---------------------------------------------------------------------------

app = FastAPI(
    title="EskomSense AI Inference API",
    version="2.0.0",
    description="Predictive load forecasting for the South African power grid.",
)

_model: EskomLSTM | None = None


def _load_model() -> EskomLSTM:
    global _model  # noqa: PLW0603
    if _model is not None:
        return _model

    _model = EskomLSTM(
        input_size=1,
        hidden_size=settings.HIDDEN_SIZE,
        num_layers=settings.NUM_LAYERS,
        dropout=settings.DROPOUT,
    )
    ckpt = settings.MODEL_PATH / "best_model.pt"
    if ckpt.exists():
        state = torch.load(ckpt, map_location="cpu", weights_only=True)
        _model.load_state_dict(state)
    _model.eval()
    return _model


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------

class PredictRequest(BaseModel):
    """Request body for ``POST /predict``."""

    sequence: list[float] = Field(
        ...,
        min_length=1,
        description="Historical load values (most recent last).",
        examples=[[4200.0, 4350.0, 4100.0]],
    )


class PredictResponse(BaseModel):
    """Response body for ``POST /predict``."""

    predicted_load: float = Field(..., description="Predicted load in MW.")
    sequence_length: int


class ModelInfoResponse(BaseModel):
    """Response body for ``GET /model/info``."""

    model_name: str
    hidden_size: int
    num_layers: int
    dropout: float
    parameter_count: int
    device: str
    checkpoint_exists: bool


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Liveness probe."""
    model = _load_model()
    return HealthResponse(status="ok", model_loaded=model is not None)


@app.get("/model/info", response_model=ModelInfoResponse)
async def model_info() -> ModelInfoResponse:
    """Return metadata about the loaded model."""
    model = _load_model()
    ckpt = settings.MODEL_PATH / "best_model.pt"
    return ModelInfoResponse(
        model_name="EskomLSTM",
        hidden_size=model.hidden_size,
        num_layers=model.num_layers,
        dropout=model.lstm.dropout if hasattr(model.lstm, "dropout") else 0.0,
        parameter_count=model.count_parameters(),
        device=str(next(model.parameters()).device),
        checkpoint_exists=ckpt.exists(),
    )


@app.post("/predict", response_model=PredictResponse)
async def predict(req: PredictRequest) -> PredictResponse:
    """Predict the next load value given a historical sequence."""
    model = _load_model()

    arr = np.array(req.sequence, dtype=np.float32)
    if arr.ndim != 1:
        raise HTTPException(status_code=422, detail="Sequence must be 1-D.")

    # Reshape to (1, seq_len, 1)
    tensor = torch.tensor(arr).unsqueeze(0).unsqueeze(-1)

    with torch.no_grad():
        pred = model(tensor).item()

    return PredictResponse(predicted_load=round(pred, 4), sequence_length=len(req.sequence))
