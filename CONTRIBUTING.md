# Contributing to EskomSense AI

Welcome and thank you for your interest in contributing to **EskomSense AI**! Every contribution helps improve power grid forecasting for South Africa.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Development Setup](#development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Architecture Reference](#architecture-reference)
- [Release Process](#release-process)

---

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you are expected to uphold this code. Please report unacceptable behavior to **raphasha27@github.com**.

---

## Development Setup

### Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.12+ | Runtime |
| pip | Latest | Dependency management |
| Docker | 24.x+ | Optional containerized development |

### Step-by-Step Setup

1. **Fork and clone** the repository:
   ```bash
   git clone https://github.com/<your-username>/EskomSense-AI.git
   cd EskomSense-AI
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate sample data**:
   ```bash
   python -m src.data.generator
   ```

5. **Train the model**:
   ```bash
   python scripts/train.py --data data/sample_data.csv --epochs 50
   ```

6. **Start the API server**:
   ```bash
   uvicorn src.api.main:app --reload --port 8000
   ```

7. **Verify the API**:
   - Swagger UI: `http://localhost:8000/docs`

8. **Run linter locally** (optional):
   ```bash
   ruff check .
   ruff format .
   ```

---

## Code Style Guidelines

### Python (PyTorch + FastAPI)

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guide.
- Use **Ruff** for linting and formatting — CI enforces this.
- Maximum line length: **88 characters**.
- Use type hints on all function signatures.
- Use docstrings for all public functions and classes.

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Functions | `snake_case` | `load_training_data` |
| Classes | `PascalCase` | `LSTMForecaster` |
| Constants | `UPPER_SNAKE_CASE` | `DEFAULT_SEQUENCE_LENGTH` |
| API routes | `kebab-case` | `/api/v1/predict` |
| Model files | `snake_case` | `lstm_model_v1.pt` |

### ML-Specific Guidelines

- Save model checkpoints with descriptive names and version numbers.
- Document hyperparameters in training scripts.
- Use reproducible random seeds for train/validation splits.
- Log training metrics (loss, MAE, RMSE) at regular intervals.
- Keep data preprocessing pipelines deterministic.

### General

- Write meaningful variable and function names.
- Add comments for complex mathematical or statistical logic.
- Keep functions focused and under 40 lines.
- No hardcoded secrets — use environment variables.

---

## Testing Requirements

| Type | Framework | Coverage Target |
|------|-----------|-----------------|
| Unit tests | pytest | 85%+ |
| Model tests | pytest | All model components |
| API tests | FastAPI TestClient | All endpoints |

- Every new feature **must** include tests.
- Bug fixes **must** include a regression test.
- Run the full test suite before pushing:
  ```bash
  pytest tests/ -v --cov=src --cov-report=term-missing
  ```
- Model tests should verify input/output shapes and gradient flow.

---

## Pull Request Process

1. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines above.

3. **Write or update tests** to cover your changes.

4. **Commit with a conventional message**:
   ```
   feat: add multi-step prediction support
   fix: correct data normalization for inference
   docs: update LSTM architecture documentation
   test: add tests for early stopping logic
   chore: update PyTorch dependencies
   ```

5. **Push and open a PR** against `main`.

6. **PR checklist** (all must pass before merge):
   - [ ] CI pipeline passes (linting, tests)
   - [ ] Code reviewed by at least one maintainer
   - [ ] No merge conflicts with `main`
   - [ ] Documentation updated (if applicable)
   - [ ] Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)

---

## Issue Guidelines

### Bug Reports

- Check [existing issues](../../issues) first to avoid duplicates.
- Include a clear, descriptive title.
- Provide steps to reproduce, expected vs. actual behavior.
- Include environment details: Python version, PyTorch version, OS.
- Attach training logs or error traces if relevant.

### Feature Requests

- Describe the feature and its motivation.
- Explain the use case for power grid forecasting.
- Propose an implementation approach if possible.

### Labels

| Label | Description |
|-------|-------------|
| `bug` | Something is broken |
| `enhancement` | New feature or improvement |
| `good-first-issue` | Ideal for first-time contributors |
| `model` | Related to LSTM model |
| `help-wanted` | Community help appreciated |

---

## Architecture Reference

For detailed system design, data flow diagrams, and model architecture, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

Key components to understand:
- **Data Pipeline** — CSV loading, normalization, train/validation splitting
- **LSTM Model** — 2-layer PyTorch LSTM for sequential demand forecasting
- **FastAPI Server** — REST API for real-time prediction requests
- **Evaluation** — MAE, RMSE, MAPE, R2 scoring with visualization

---

## Release Process

1. All changes merge to `main` via PR with passing CI.
2. Semantic versioning is used: `MAJOR.MINOR.PATCH`.
3. Tags are created for each release: `git tag v1.x.x`.
4. Model artifacts are versioned alongside code releases.
5. Release notes are generated from conventional commit messages.

---

## Questions?

Open a [discussion](../../discussions) or reach out to **raphasha27@github.com**.

Thank you for contributing to EskomSense AI!
