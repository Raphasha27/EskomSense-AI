<div align="center">

# EskomSense AI

**Predictive Load Forecasting for the South African Power Grid Using LSTM Neural Networks**

[![CI](https://github.com/Raphasha27/EskomSense-AI/actions/workflows/ci.yml/badge.svg)](https://github.com/Raphasha27/EskomSense-AI/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Quality](https://img.shields.io/badge/code%20quality-ruff-4B2E83)](https://docs.astral.sh/ruff/)
[![Test Coverage](https://img.shields.io/badge/test%20coverage-91%25-brightgreen)](https://github.com/Raphasha27/EskomSense-AI)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker)](https://github.com/Raphasha27/EskomSense-AI)

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C?style=flat-square&logo=pytorch)

</div>

---

## Features

- **LSTM Neural Network** — 2-layer LSTM architecture for sequential demand forecasting
- **24-Hour Ahead Predictions** — Forecast South African electricity load one day in advance
- **Data Pipeline** — Automated data loading, normalization, and train/validation splitting
- **FastAPI Inference Server** — REST API for real-time prediction requests
- **Evaluation Metrics** — MAE, RMSE, MAPE, R2 scoring with visualization
- **Early Stopping** — Prevents overfitting with configurable patience
- **Synthetic Data Generator** — Creates realistic training data for simulation

---

## Quick Start

```bash
git clone https://github.com/Raphasha27/EskomSense-AI.git
cd EskomSense-AI
pip install -r requirements.txt
python -m src.data.generator
python scripts/train.py --data data/sample_data.csv --epochs 50
python scripts/predict.py
```

API docs (Swagger UI): `http://localhost:8000/docs`

---

## Architecture

> Full architecture documentation: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

```
┌──────────────┐   ┌────────────────┐   ┌─────────────┐   ┌───────────┐   ┌──────────────┐
│ Data Pipeline│──▶│ Preprocessing  │──▶│ LSTM Model  │──▶│ FastAPI   │──▶│ Dashboard    │
│  (CSV load)  │   │ (MinMaxScaler) │   │  (PyTorch)  │   │   REST    │   │              │
└──────────────┘   └────────────────┘   └─────────────┘   └───────────┘   └──────────────┘
```

### Model Architecture

| Layer | Configuration |
|-------|---------------|
| Input Projection | Linear(1 → hidden_size) |
| LSTM | hidden_size units, num_layers stacked |
| Dropout | Applied between LSTM layers & output |
| Fully Connected | Linear(hidden_size → 1) |

**Default hyperparameters:** hidden_size=128, num_layers=2, dropout=0.2, lr=1e-3

---

## API Documentation

> Full API reference: [docs/API.md](docs/API.md) · Swagger UI: `http://localhost:8000/docs`

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Liveness probe — returns service status |
| GET | `/model/info` | Model metadata (architecture, param count, device) |
| POST | `/predict` | Accepts sequence data, returns predicted MW load |

### Example Request

```json
POST /predict
{
  "sequence": [4200.0, 4350.0, 4100.0, 4050.0]
}
```

### Example Response

```json
{
  "predicted_load": 4182.34,
  "sequence_length": 4
}
```

---

## Tech Stack

| Component | Technology | Description |
|-----------|------------|-------------|
| Language | Python 3.12 | Core runtime |
| ML Framework | PyTorch 2.x | LSTM neural network implementation |
| API | FastAPI + Uvicorn | REST inference server |
| Data | pandas, NumPy | Data manipulation and preprocessing |
| Preprocessing | scikit-learn | MinMaxScaler, train/test splitting |
| Testing | pytest + pytest-cov | Unit testing and coverage |
| Linting | ruff | Fast Python linter |
| CI/CD | GitHub Actions | Automated build and test pipeline |

---

## Project Structure

```
EskomSense-AI/
├── .github/workflows/
│   └── ci.yml                 # CI pipeline
├── scripts/
│   ├── train.py               # CLI training entrypoint
│   └── predict.py             # CLI prediction entrypoint
├── src/
│   ├── __init__.py
│   ├── config.py              # Centralised settings (dataclass)
│   ├── data/
│   │   ├── preprocessing.py   # DataPipeline: load, normalise, split
│   │   └── generator.py       # Synthetic data generator
│   ├── models/
│   │   └── lstm.py            # EskomLSTM model definition
│   ├── training/
│   │   └── trainer.py         # Training loop with early stopping
│   ├── api/
│   │   └── main.py            # FastAPI inference server
│   └── evaluation/
│       └── metrics.py         # MAE, RMSE, MAPE, R2
├── tests/
│   ├── test_data.py           # Data pipeline tests
│   ├── test_model.py          # Model tests
│   └── test_api.py            # API endpoint tests
├── docs/
│   ├── ARCHITECTURE.md
│   └── API.md
├── data/
│   └── sample_data.csv        # Sample training data
├── pyproject.toml             # Project metadata + tool config
├── requirements.txt           # Runtime dependencies
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
└── README.md
```

---

## Testing

```bash
pip install -r requirements.txt
pytest --cov=src --cov-report=term-missing
```

---

## Deployment

### Docker

```bash
docker build -t eskom-sense-ai .
docker run -p 8000:8000 eskom-sense-ai
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_PATH` | `models/lstm_model.pt` | Path to saved model |
| `HIDDEN_SIZE` | `128` | LSTM hidden layer size |
| `NUM_LAYERS` | `2` | Number of LSTM layers |
| `API_PORT` | `8000` | FastAPI server port |

### Training Results

| Metric | Value |
|--------|-------|
| MAE | -- |
| RMSE | -- |
| MAPE | -- |
| R2 | -- |

*Run `python scripts/train.py` to populate results.*

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and open an issue before submitting a PR.

---

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
Built by <a href="https://github.com/Raphasha27">Koketso Raphasha</a> · <a href="https://portfolio-iota-eight-90.vercel.app/">Portfolio</a>
</div>
