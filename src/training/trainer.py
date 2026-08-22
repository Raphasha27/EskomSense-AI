"""Training loop with early stopping, LR scheduling, and checkpointing."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import torch
import torch.nn as nn
from torch.optim import Adam
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader, TensorDataset


class Trainer:
    """Handles the full training lifecycle of an EskomLSTM model.

    Parameters
    ----------
    model : nn.Module
        The neural network to train.
    device : str | None
        ``"cuda"``, ``"cpu"``, or ``None`` for auto-detection.
    checkpoint_dir : Path
        Directory where model checkpoints are persisted.
    patience : int
        Epochs without improvement before early stopping.
    """

    def __init__(
        self,
        model: nn.Module,
        device: str | None = None,
        checkpoint_dir: Path = Path("models/checkpoints"),
        patience: int = 7,
    ) -> None:
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)

        self.model = model.to(self.device)
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.patience = patience

        self.train_losses: List[float] = []
        self.val_losses: List[float] = []
        self.best_val_loss = float("inf")
        self._wait = 0

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        epochs: int = 50,
        lr: float = 1e-3,
        batch_size: int = 32,
    ) -> Dict[str, Any]:
        """Run the full training loop.

        Returns
        -------
        dict with keys ``train_losses``, ``val_losses``, ``best_val_loss``,
        ``epochs_trained``, ``training_time_s``.
        """
        train_loader = self._make_loader(X_train, y_train, batch_size)
        val_loader = self._make_loader(X_val, y_val, batch_size, shuffle=False)

        criterion = nn.MSELoss()
        optimizer = Adam(self.model.parameters(), lr=lr)
        scheduler = ReduceLROnPlateau(
            optimizer, mode="min", factor=0.5, patience=max(patience // 2, 1)
        )

        start = time.time()

        for epoch in range(1, epochs + 1):
            train_loss = self._train_epoch(train_loader, criterion, optimizer)
            val_loss = self._validate(val_loader, criterion)

            self.train_losses.append(train_loss)
            self.val_losses.append(val_loss)

            scheduler.step(val_loss)
            current_lr = optimizer.param_groups[0]["lr"]

            print(
                f"Epoch {epoch:>3d}/{epochs} | "
                f"train_loss={train_loss:.6f} | val_loss={val_loss:.6f} | "
                f"lr={current_lr:.2e}"
            )

            if val_loss < self.best_val_loss:
                self.best_val_loss = val_loss
                self._wait = 0
                self._save_checkpoint(epoch)
            else:
                self._wait += 1
                if self._wait >= self.patience:
                    print(f"Early stopping at epoch {epoch}")
                    break

        elapsed = time.time() - start
        summary = {
            "train_losses": self.train_losses,
            "val_losses": self.val_losses,
            "best_val_loss": self.best_val_loss,
            "epochs_trained": len(self.train_losses),
            "training_time_s": round(elapsed, 2),
        }
        self._save_history(summary)
        return summary

    def load_checkpoint(self, path: Path | str) -> None:
        """Load model weights from a checkpoint file."""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"No checkpoint at {path}")
        state = torch.load(path, map_location=self.device, weights_only=True)
        self.model.load_state_dict(state)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _make_loader(
        self,
        X: np.ndarray,
        y: np.ndarray,
        batch_size: int,
        shuffle: bool = True,
    ) -> DataLoader:
        X_t = torch.tensor(X, dtype=torch.float32).to(self.device)
        y_t = torch.tensor(y, dtype=torch.float32).to(self.device)
        ds = TensorDataset(X_t, y_t)
        return DataLoader(ds, batch_size=batch_size, shuffle=shuffle)

    def _train_epoch(
        self, loader: DataLoader, criterion: nn.Module, optimizer: Adam
    ) -> float:
        self.model.train()
        running = 0.0
        for X_batch, y_batch in loader:
            optimizer.zero_grad()
            pred = self.model(X_batch)
            loss = criterion(pred, y_batch)
            loss.backward()
            nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            optimizer.step()
            running += loss.item() * len(y_batch)
        return running / len(loader.dataset)

    @torch.no_grad()
    def _validate(self, loader: DataLoader, criterion: nn.Module) -> float:
        self.model.eval()
        running = 0.0
        for X_batch, y_batch in loader:
            pred = self.model(X_batch)
            loss = criterion(pred, y_batch)
            running += loss.item() * len(y_batch)
        return running / len(loader.dataset)

    def _save_checkpoint(self, epoch: int) -> None:
        path = self.checkpoint_dir / f"best_model.pt"
        torch.save(self.model.state_dict(), path)

    def _save_history(self, summary: Dict[str, Any]) -> None:
        path = self.checkpoint_dir / "training_history.json"
        with open(path, "w") as f:
            json.dump(summary, f, indent=2)
