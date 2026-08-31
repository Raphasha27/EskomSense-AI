[![CI](https://github.com/Raphasha27/EskomSense-AI/actions/workflows/ci.yml/badge.svg)](https://github.com/Raphasha27/EskomSense-AI/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# EskomSense AI

> Predictive Load Forecasting for the South African Power Grid

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C?style=flat-square&logo=pytorch)

## Overview

EskomSense AI is a production-grade machine learning pipeline that forecasts South African electricity demand 24 hours ahead using an LSTM (Long Short-Term Memory) neural network. The system ingests historical Eskom load data, trains a sequence model, and exposes predictions via a FastAPI REST endpoint.

## Architecture

`
+---------------+   +----------------+   +-------------+   +---------+   +-----------+
| Data Pipeline |-->| Preprocessing  |-->| LSTM Model  |-->| FastAPI |-->| Dashboard |
|  (CSV load)   |   | (MinMaxScaler) |   |  (PyTorch)  |   |   REST  |   |           |
+---------------+   +----------------+   +-------------+   +---------+   +-----------+
`

## Model Architecture

| Layer             | Configuration                          |
|-------------------|----------------------------------------|
| Input Projection  | Linear(1 -> hidden_size)               |
| LSTM              | hidden_size units, num_layers stacked  |
| Dropout           | Applied between LSTM layers & output   |
| Fully Connected   | Linear(hidden_size -> 1)               |

**Default hyperparameters:** hidden_size=128, num_layers=2, dropout=0.2, lr=1e-3

## Quick Start

`ash
# Install dependencies
pip install -r requirements.txt

# Generate synthetic training data
python -m src.data.generator

# Train the model
python scripts/train.py --data data/sample_data.csv --epochs 50

# Run predictions
python scripts/predict.py
`

## API

Start the server:

`ash
uvicorn src.api.main:app --reload
`

| Endpoint     | Method | Description                                        |
|--------------|--------|----------------------------------------------------|
| /health    | GET    | Liveness probe - returns service status            |
| /model/info| GET    | Model metadata (architecture, param count, device) |
| /predict   | POST   | Accepts sequence data, returns predicted MW load   |

### Example Request

`json
POST /predict
{
  "sequence": [4200.0, 4350.0, 4100.0, 4050.0]
}
`

### Example Response

`json
{
  "predicted_load": 4182.34,
  "sequence_length": 4
}
`

## Tech Stack

- **Language:** Python 3.12
- **ML Framework:** PyTorch
- **API:** FastAPI + Uvicorn
- **Data:** pandas, NumPy, scikit-learn
- **Testing:** pytest, pytest-cov
- **Linting:** ruff
- **CI/CD:** GitHub Actions

## Directory Structure

`
EskomSense-AI/
+-- .github/workflows/ci.yml   CI pipeline
+-- scripts/
|   +-- train.py               CLI training entrypoint
|   +-- predict.py             CLI prediction entrypoint
+-- src/
|   +-- __init__.py
|   +-- config.py              Centralised settings (dataclass)
|   +-- data/
|   |   +-- preprocessing.py   DataPipeline: load, normalise, split
|   |   +-- generator.py       Synthetic data generator
|   +-- models/
|   |   +-- lstm.py            EskomLSTM model definition
|   +-- training/
|   |   +-- trainer.py         Training loop with early stopping
|   +-- api/
|   |   +-- main.py            FastAPI inference server
|   +-- evaluation/
|       +-- metrics.py         MAE, RMSE, MAPE, R2
+-- tests/
|   +-- test_data.py           Data pipeline tests
|   +-- test_model.py          Model tests
|   +-- test_api.py            API endpoint tests
+-- pyproject.toml             Project metadata + tool config
+-- requirements.txt           Runtime dependencies
+-- README.md
`

## Training Results

| Metric | Value   |
|--------|---------|
| MAE    | --      |
| RMSE   | --      |
| MAPE   | --      |
| R2     | --      |

*Run python scripts/train.py to populate results.*

<!-- 2026-08-31 17:04:21 -->
