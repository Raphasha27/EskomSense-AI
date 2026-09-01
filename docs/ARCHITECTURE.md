# EskomSense AI — Architecture

## System Overview

EskomSense AI is a production-grade machine learning pipeline that forecasts South African electricity demand 24 hours ahead using an LSTM (Long Short-Term Memory) neural network. The system ingests historical Eskom load data, trains a sequence model, and exposes predictions via a FastAPI REST endpoint.

## Architecture Diagram

```
┌───────────────┐    ┌────────────────┐    ┌──────────────┐    ┌──────────┐    ┌───────────┐
│ Data Pipeline │───►│ Preprocessing  │───►│ LSTM Model   │───►│ FastAPI  │───►│ Dashboard │
│  (CSV load)   │    │ (MinMaxScaler) │    │  (PyTorch)   │    │   REST   │    │  / Client │
│  pandas       │    │  sequence gen  │    │  GPU/CPU     │    │  :8000   │    │           │
└───────────────┘    └────────────────┘    └──────────────┘    └──────────┘    └───────────┘
                            │                    │
                     ┌──────▼──────┐      ┌──────▼──────┐
                     │  Synthetic  │      │  Model      │
                     │  Data Gen   │      │  Checkpoint │
                     └─────────────┘      └─────────────┘
```

## Model Architecture

```
Input (sequence_length, 1)
        │
        ▼
Linear(1 → hidden_size)
        │
        ▼
LSTM(hidden_size, num_layers, batch_first=True)
        │
        ▼
Dropout(dropout)
        │
        ▼
Linear(hidden_size → 1)
        │
        ▼
Output: predicted_load (MW)
```

**Default Hyperparameters:** hidden_size=128, num_layers=2, dropout=0.2, learning_rate=1e-3

## Technology Stack

| Component      | Technology            | Version |
|----------------|-----------------------|---------|
| Language       | Python                | 3.12    |
| ML Framework   | PyTorch               | 2.x     |
| API            | FastAPI + Uvicorn     | —       |
| Data Processing| pandas, NumPy         | —       |
| Preprocessing  | scikit-learn (MinMaxScaler) | — |
| Testing        | pytest, pytest-cov    | —       |
| Linting        | ruff                  | —       |
| CI/CD          | GitHub Actions        | —       |

## Directory Structure

```
EskomSense-AI/
├── .github/workflows/ci.yml       # CI pipeline
├── scripts/
│   ├── train.py                    # CLI training entrypoint
│   └── predict.py                  # CLI prediction entrypoint
├── src/
│   ├── __init__.py
│   ├── config.py                   # Centralised settings (dataclass)
│   ├── data/
│   │   ├── preprocessing.py        # DataPipeline: load, normalise, split
│   │   └── generator.py            # Synthetic data generator
│   ├── models/
│   │   └── lstm.py                 # EskomLSTM model definition
│   ├── training/
│   │   └── trainer.py              # Training loop with early stopping
│   ├── api/
│   │   └── main.py                 # FastAPI inference server
│   └── evaluation/
│       └── metrics.py              # MAE, RMSE, MAPE, R2
├── tests/
│   ├── test_data.py
│   ├── test_model.py
│   └── test_api.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Data Flow

### Training Pipeline
1. **Data Generation**: `src/data/generator.py` creates synthetic Eskom load data (MW values over time).
2. **Preprocessing**: `DataPipeline` loads CSV, applies MinMaxScaler normalization, creates sliding window sequences.
3. **Training**: `Trainer` runs epoch loop with MSE loss, Adam optimizer, early stopping on validation loss.
4. **Checkpoint**: Best model saved to disk; training metrics (MAE, RMSE, MAPE, R2) logged.

### Inference Pipeline
1. **Request**: Client sends `POST /predict` with a sequence of historical load values.
2. **Preprocessing**: Input sequence normalized with fitted scaler.
3. **Prediction**: LSTM model forward pass returns predicted MW load.
4. **Response**: JSON with `predicted_load` and `sequence_length`.

## Security

- **No authentication by default**: Add JWT/API key auth for production.
- **Model integrity**: Checksums on saved model files to detect tampering.
- **Input validation**: Pydantic models validate sequence length and data types.
- **Environment variables**: Sensitive config (model paths, API keys) loaded from env.

## Deployment

### Local Development

```bash
pip install -r requirements.txt
python -m src.data.generator          # Generate training data
python scripts/train.py --epochs 50   # Train model
uvicorn src.api.main:app --reload     # Start API
```

### API Endpoints

| Endpoint     | Method | Description                              |
|--------------|--------|------------------------------------------|
| `/health`    | GET    | Liveness probe                           |
| `/model/info`| GET    | Model metadata (architecture, param count) |
| `/predict`   | POST   | Accepts sequence, returns predicted MW   |

## Scaling Considerations

- **GPU acceleration**: PyTorch automatically uses CUDA when available; set `device` in config.
- **Batch predictions**: Extend API to accept multiple sequences in a single request.
- **Model versioning**: Save checkpoints with timestamps; implement model registry.
- **Data pipeline**: Replace CSV with streaming pipeline (Kafka) for real-time Eskom data.
- **Horizontal scaling**: Stateless API behind load balancer; model loaded once per worker.
- **A/B testing**: Deploy multiple model versions, route traffic by percentage.

## Decision Records

| Decision | Rationale |
|----------|-----------|
| LSTM over Transformer | Sequential time series data; LSTM is simpler and sufficient for 24h forecast horizon |
| PyTorch over TensorFlow | More Pythonic API, dynamic computation graph, easier debugging |
| FastAPI for serving | Auto-generated OpenAPI docs, async support, native Pydantic validation |
| MinMaxScaler | LSTM sensitive to input scale; normalization ensures stable training |
| Early stopping | Prevents overfitting on small synthetic datasets |
| Synthetic data | No public Eskom API; synthetic data demonstrates pipeline without licensing issues |
