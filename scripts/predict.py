#!/usr/bin/env python3
"""CLI entrypoint: run predictions with a trained EskomLSTM."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch

from src.config import settings
from src.models.lstm import EskomLSTM


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Predict load with trained EskomLSTM.")
    p.add_argument("--model", type=str, default=str(settings.MODEL_PATH / "best_model.pt"))
    p.add_argument("--hidden", type=int, default=settings.HIDDEN_SIZE)
    p.add_argument("--layers", type=int, default=settings.NUM_LAYERS)
    p.add_argument("--input", type=str, default=None, help="JSON file or inline JSON array.")
    return p.parse_args()


def load_model(path: str, hidden: int, layers: int) -> EskomLSTM:
    model = EskomLSTM(input_size=1, hidden_size=hidden, num_layers=layers)
    ckpt = Path(path)
    if not ckpt.exists():
        print(f"Error: checkpoint not found at {ckpt}", file=sys.stderr)
        sys.exit(1)
    state = torch.load(ckpt, map_location="cpu", weights_only=True)
    model.load_state_dict(state)
    model.eval()
    return model


def read_sequence(source: str | None) -> list[float]:
    if source is None:
        print("Enter sequence as JSON array (e.g. [4200, 4350, 4100]):")
        raw = input("> ").strip()
    elif Path(source).exists():
        raw = Path(source).read_text()
    else:
        raw = source

    try:
        seq = json.loads(raw)
        return [float(x) for x in seq]
    except (json.JSONDecodeError, TypeError) as exc:
        print(f"Invalid input: {exc}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    args = parse_args()
    model = load_model(args.model, args.hidden, args.layers)
    seq = read_sequence(args.input)

    tensor = torch.tensor(seq, dtype=torch.float32).unsqueeze(0).unsqueeze(-1)
    with torch.no_grad():
        pred = model(tensor).item()

    print(f"\n  Input length : {len(seq)}")
    print(f"  Predicted MW : {pred:.2f}")
    print(json.dumps({"predicted_load_mw": round(pred, 4), "sequence_length": len(seq)}))


if __name__ == "__main__":
    main()
