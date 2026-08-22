#!/usr/bin/env python3
"""CLI entrypoint: train the EskomLSTM model."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import torch

from src.config import settings
from src.data.preprocessing import DataPipeline
from src.evaluation.metrics import compute_metrics
from src.models.lstm import EskomLSTM
from src.training.trainer import Trainer


def set_seed(seed: int) -> None:
    """Ensure reproducibility."""
    import random
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Train EskomLSTM load forecaster.")
    p.add_argument(
        "--data",
        type=str,
        default=str(settings.DATA_PATH / "sample_data.csv"),
        help="Path to CSV training data.",
    )
    p.add_argument(
        "--target-col",
        type=str,
        default="load_mw",
        help="Name of the target column.",
    )
    p.add_argument("--epochs", type=int, default=settings.EPOCHS)
    p.add_argument("--lr", type=float, default=settings.LEARNING_RATE)
    p.add_argument("--batch-size", type=int, default=settings.BATCH_SIZE)
    p.add_argument("--seq-len", type=int, default=settings.SEQUENCE_LENGTH)
    p.add_argument("--hidden", type=int, default=settings.HIDDEN_SIZE)
    p.add_argument("--layers", type=int, default=settings.NUM_LAYERS)
    p.add_argument("--dropout", type=float, default=settings.DROPOUT)
    p.add_argument("--patience", type=int, default=settings.EARLY_STOP_PATIENCE)
    p.add_argument("--seed", type=int, default=settings.SEED)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    set_seed(args.seed)

    print("=" * 60)
    print("  EskomSense AI — Model Training")
    print("=" * 60)
    print(f"  Data      : {args.data}")
    print(f"  Epochs    : {args.epochs}")
    print(f"  Hidden    : {args.hidden}  |  Layers: {args.layers}")
    print(f"  LR        : {args.lr}  |  Batch: {args.batch_size}")
    print(f"  Seed      : {args.seed}")
    print("=" * 60)

    # Data
    pipe = DataPipeline(
        sequence_length=args.seq_len,
        target_column=args.target_col,
        val_split=settings.VAL_SPLIT,
    )
    X_train, y_train, X_val, y_val = pipe.prepare(args.data)
    print(f"  Train samples: {len(X_train)}  |  Val samples: {len(X_val)}")

    # Model
    model = EskomLSTM(
        input_size=1,
        hidden_size=args.hidden,
        num_layers=args.layers,
        dropout=args.dropout,
    )
    print(f"  Parameters  : {model.count_parameters():,}")

    # Train
    trainer = Trainer(
        model=model,
        checkpoint_dir=settings.MODEL_PATH / "checkpoints",
        patience=args.patience,
    )
    summary = trainer.train(
        X_train, y_train, X_val, y_val,
        epochs=args.epochs,
        lr=args.lr,
        batch_size=args.batch_size,
    )

    # Save final model
    final_path = settings.MODEL_PATH / "best_model.pt"
    torch.save(model.state_dict(), final_path)
    print(f"\n  Model saved to {final_path}")

    # Evaluate on validation set
    model.eval()
    with torch.no_grad():
        X_val_t = torch.tensor(X_val, dtype=torch.float32)
        preds = model(X_val_t).numpy()
    metrics = compute_metrics(y_val, preds)
    print("\n  Validation metrics:")
    for k, v in metrics.items():
        print(f"    {k:>6s}: {v:.4f}")

    print(f"\n  Training time: {summary['training_time_s']:.1f}s")
    print(f"  Best val loss: {summary['best_val_loss']:.6f}")
    print(f"  Epochs trained: {summary['epochs_trained']}")


if __name__ == "__main__":
    main()
