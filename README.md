# ⚡ EskomSense AI - Load Shedding Predictor

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-ML-orange?style=for-the-badge&logo=pytorch)
![FastAPI](https://img.shields.io/badge/FastAPI-Inference-009688?style=for-the-badge&logo=fastapi)

An AI-powered system designed to forecast South African load shedding schedules and optimize backup energy usage using Time-Series Machine Learning (LSTM).

## Architecture
1. **Data Pipeline:** Ingests historical Eskom schedule data and extracts features (time of day, day of week, seasonal trends).
2. **ML Model (PyTorch):** An LSTM (Long Short-Term Memory) neural network trained to predict stage fluctuations 24-72 hours in advance.
3. **Inference API (FastAPI):** Exposes the trained model via a REST API for integrations with smart home systems (Home Assistant).

## Project Structure
- /src/data: Data ingestion, cleaning, and feature engineering.
- /src/models: PyTorch LSTM model definition and training loop.
- /src/api: FastAPI application serving predictions.
- /notebooks: Jupyter notebooks for Exploratory Data Analysis (EDA) and model evaluation.

## Quick Start
`ash
# Generate synthetic dataset for testing
python -m src.data.generator

# Start inference API
uvicorn src.api.main:app --reload
`
