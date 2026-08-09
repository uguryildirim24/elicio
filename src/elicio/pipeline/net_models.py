"""Compact neural-network architectures for raw-window sEMG gesture decoding.

All three networks take a raw window tensor of shape
(batch, n_channels, n_timesteps) -- sEMG signal, channel-first, as
PyTorch conv/recurrent layers expect -- and output class logits over
the gesture alphabet (17 classes: 16 gestures + rest).

Every network is small enough to train on a CPU node in a few
minutes per subject: total parameter counts are in the tens of
thousands, not millions.
"""
from __future__ import annotations

import math

import torch
import torch.nn as nn


class TemporalCNN(nn.Module):
    """A small 1-D convolutional network over the raw time series.

    Two conv blocks downsample time by 4x total, then global average
    pooling collapses time to one vector per channel-group before the
    final linear classifier.
    """

    def __init__(self, n_channels: int, n_classes: int, hidden: int = 32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv1d(n_channels, hidden, kernel_size=9, stride=2, padding=4),
            nn.BatchNorm1d(hidden),
            nn.ReLU(),
            nn.Conv1d(hidden, hidden * 2, kernel_size=9, stride=2, padding=4),
            nn.BatchNorm1d(hidden * 2),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1),
        )
        self.fc = nn.Linear(hidden * 2, n_classes)

    def forward(self, x):  # x: (batch, n_channels, n_timesteps)
        z = self.net(x).squeeze(-1)
        return self.fc(z)


class GestureGRU(nn.Module):
    """A small GRU over a downsampled raw time series.

    Time is average-pooled by 4x before the GRU so the recurrent loop
    runs about 100 steps instead of 410, which is the main CPU-time
    lever for a recurrent model.
    """

    def __init__(self, n_channels: int, n_classes: int, hidden: int = 48):
        super().__init__()
        self.pool = nn.AvgPool1d(kernel_size=4, stride=4)
        self.gru = nn.GRU(input_size=n_channels, hidden_size=hidden, batch_first=True)
        self.fc = nn.Linear(hidden, n_classes)

    def forward(self, x):  # x: (batch, n_channels, n_timesteps)
        z = self.pool(x)              # (batch, n_channels, n_timesteps/4)
        z = z.transpose(1, 2)         # (batch, n_timesteps/4, n_channels)
        _, h_n = self.gru(z)          # h_n: (1, batch, hidden)
        return self.fc(h_n[-1])


class _SinusoidalPositionalEncoding(nn.Module):
    def __init__(self, d_model: int, max_len: int = 256):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float32).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2, dtype=torch.float32) * (-math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer("pe", pe.unsqueeze(0))  # (1, max_len, d_model)

    def forward(self, x):  # x: (batch, seq_len, d_model)
        return x + self.pe[:, : x.size(1), :]


class GestureTransformer(nn.Module):
    """A small transformer encoder over a downsampled raw time series.

    Time is average-pooled by 8x (to about 51 steps) before the
    encoder, since attention cost grows with the square of sequence
    length. One encoder layer, small model width.
    """

    def __init__(self, n_channels: int, n_classes: int, d_model: int = 32, nhead: int = 4):
        super().__init__()
        self.pool = nn.AvgPool1d(kernel_size=8, stride=8)
        self.proj = nn.Linear(n_channels, d_model)
        self.posenc = _SinusoidalPositionalEncoding(d_model)
        layer = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=nhead, dim_feedforward=d_model * 2,
            batch_first=True, dropout=0.1,
        )
        self.encoder = nn.TransformerEncoder(layer, num_layers=1)
        self.fc = nn.Linear(d_model, n_classes)

    def forward(self, x):  # x: (batch, n_channels, n_timesteps)
        z = self.pool(x).transpose(1, 2)   # (batch, seq_len, n_channels)
        z = self.proj(z)                    # (batch, seq_len, d_model)
        z = self.posenc(z)
        z = self.encoder(z)                 # (batch, seq_len, d_model)
        z = z.mean(dim=1)                   # mean pool over time
        return self.fc(z)


def build_networks(n_channels: int, n_classes: int) -> dict:
    return {
        "Temporal_CNN": TemporalCNN(n_channels, n_classes),
        "GRU": GestureGRU(n_channels, n_classes),
        "Transformer": GestureTransformer(n_channels, n_classes),
    }
