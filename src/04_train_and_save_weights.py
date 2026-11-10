"""
Topic 6: Real-Time Weather Data Collection and Cleaning
Step 4: Walk-Forward Validation, Multi-Horizon Autoregressive Evaluation (h = 1, 24, 72, 168h),
        Hybrid (GRU + Ridge + HistGB) + XGBoost Residual Training & Weight Serialization.

Follows ML Best Practices:
  - Stationarity (ADF) and Seasonality (24h Autocorrelation) testing
  - Expanding Walk-Forward Validation with Purge Gap (168h) to prevent label leakage
  - True Autoregressive Multi-Horizon Rollout (h = 1h, 24h, 72h, 168h) matching Dashboard logic
  - Seasonal & ENSO Regime Breakdown (La Niña vs Neutral vs El Niño)
  - Saves trained model weights & preprocessing pipeline to `models/weather_forecast_weights.joblib`
"""

import json
import sys
import time
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from statsmodels.tsa.stattools import adfuller
from xgboost import XGBRegressor

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

torch.manual_seed(42)
np.random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_DIR = BASE_DIR / "data" / "cleaned"
MODEL_DIR = BASE_DIR / "models"
FIG_DIR = BASE_DIR / "figures"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

TARGET_VARS = [
    "temperature_2m",
    "relative_humidity_2m",
    "wind_speed_10m",
    "precipitation",
    "pressure_msl",
]

LAGS = [1, 2, 3, 6, 12, 24, 48, 72]
CHRONO_LAGS = [72, 48, 24, 12, 6, 3, 2, 1]  # Ordered from oldest (t-72h) to newest (t-1h) for GRU sequence
HORIZONS = [1, 24, 72, 168]
MAX_HORIZON = max(HORIZONS)
MAX_LAG = max(LAGS)


def get_enso_phase(ts: pd.Timestamp) -> str:
    """
    Classify timestamp into NOAA Oceanic Niño Index (ONI) phases for climate robustness reporting.
    """
    ym = (ts.year, ts.month)
    if (2020, 8) <= ym <= (2023, 2):
        return "La Niña (2020-2022)"
    elif (2023, 5) <= ym <= (2024, 5):
        return "El Niño (2023-2024)"
    elif (2018, 9) <= ym <= (2019, 6):
        return "El Niño (2018-2019)"
    elif (2016, 8) <= ym <= (2018, 4):
        return "La Niña (2016-2018)"
    return "ENSO Neutral"


def get_season_label(month: int) -> str:
    if month in [12, 1, 2]:
        return "Winter (Dec-Feb)"
    elif month in [3, 4, 5]:
        return "Spring (Mar-May)"
    elif month in [6, 7, 8]:
        return "Summer (Jun-Aug)"
    return "Autumn (Sep-Nov)"


def load_weather_dataset() -> pd.DataFrame:
    """
    Automatically load multi-year .parquet archive if available; otherwise fallback to cleaned CSV.
    """
    parquet_path = CLEAN_DIR / "cleaned_weather_data.parquet"
    csv_path = CLEAN_DIR / "cleaned_weather_data.csv"

    if parquet_path.exists():
        print(f"[INFO] Loading dataset from Parquet: {parquet_path}")
        df = pd.read_parquet(parquet_path)
    else:
        print(f"[INFO] Loading dataset from CSV: {csv_path}")
        df = pd.read_csv(csv_path)

    df["timestamp"] = pd.to_datetime(df["time"] if "time" in df.columns else df["timestamp"])
    if "hour" not in df.columns:
        df["hour"] = df["timestamp"].dt.hour
    return df


def build_supervised_features(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """
    Construct autoregressive lag features, rolling window statistics, cyclical temporal features,
    and spatial coordinates for each location's time series.
    """
    df = df.sort_values(["location_id", "timestamp"]).copy()

    hour = df["timestamp"].dt.hour
    doy = df["timestamp"].dt.dayofyear
    df["hour_sin"] = np.sin(2 * np.pi * hour / 24.0)
    df["hour_cos"] = np.cos(2 * np.pi * hour / 24.0)
    df["doy_sin"] = np.sin(2 * np.pi * doy / 365.25)
    df["doy_cos"] = np.cos(2 * np.pi * doy / 365.25)

    feature_cols = [
        "location_id",
        "requested_lat",
        "requested_lon",
        "elevation_m",
        "hour_sin",
        "hour_cos",
        "doy_sin",
        "doy_cos",
    ]

    grouped = df.groupby("location_id", sort=False)

    for var in TARGET_VARS:
        for lag in LAGS:
            col_name = f"{var}_lag_{lag}h"
            df[col_name] = grouped[var].shift(lag)
            feature_cols.append(col_name)

        shifted_1h = grouped[var].shift(1)
        roll24_mean = (
            shifted_1h.groupby(df["location_id"])
            .rolling(window=24, min_periods=6)
            .mean()
            .reset_index(level=0, drop=True)
        )
        roll24_std = (
            shifted_1h.groupby(df["location_id"])
            .rolling(window=24, min_periods=6)
            .std()
            .fillna(0.0)
            .reset_index(level=0, drop=True)
        )
        df[f"{var}_roll24_mean"] = roll24_mean
        df[f"{var}_roll24_std"] = roll24_std
        feature_cols.extend([f"{var}_roll24_mean", f"{var}_roll24_std"])

    df_model = df.dropna(subset=feature_cols + TARGET_VARS).reset_index(drop=True)
    return df_model, feature_cols


def get_gru_sequence_indices(feature_cols: list[str]) -> list[list[int]]:
    """
    Return a 2D index map of shape (8, 5) corresponding to chronological lags
    [t-72h, t-48h, t-24h, t-12h, t-6h, t-3h, t-2h, t-1h] across the 5 weather variables.
    """
    seq_indices = []
    for lag in CHRONO_LAGS:
        step_cols = [feature_cols.index(f"{var}_lag_{lag}h") for var in TARGET_VARS]
        seq_indices.append(step_cols)
    return seq_indices


class WeatherGRUNet(nn.Module):
    """
    PyTorch Gated Recurrent Unit (GRU) Network that processes the 8-step chronological lag tensor
    (t-72h -> ... -> t-1h across 5 variables) and combines the GRU hidden state with full covariates.
    """

    def __init__(self, seq_input_dim: int, full_dim: int, hidden_dim: int = 32):
        super().__init__()
        self.gru = nn.GRU(input_size=seq_input_dim, hidden_size=hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim + full_dim, 1)

    def forward(self, x_seq: torch.Tensor, x_full: torch.Tensor) -> torch.Tensor:
        _, h_n = self.gru(x_seq)
        h_last = h_n.squeeze(0)
        combined = torch.cat([h_last, x_full], dim=1)
        return self.fc(combined).squeeze(1)


def train_pytorch_gru_and_export_weights(
    X_scaled: np.ndarray,
    y: np.ndarray,
    seq_indices: list[list[int]],
    hidden_dim: int = 32,
    epochs: int = 16,
    batch_size: int = 512,
    lr: float = 0.004,
    max_train_samples: int = 120_000,
) -> dict:
    """
    Train PyTorch WeatherGRUNet on chronological training data and export its exact gate weights.
    Caps training samples to the most recent `max_train_samples` rows to prevent CPU bottlenecks on multi-year data.
    """
    torch.manual_seed(42)
    if len(X_scaled) > max_train_samples:
        X_scaled = X_scaled[-max_train_samples:]
        y = y[-max_train_samples:]

    seq_idx_arr = np.array(seq_indices, dtype=np.int64)  # shape (8, 5)
    X_seq = X_scaled[:, seq_idx_arr]  # shape (N, 8, 5)

    y_mean = float(np.mean(y))
    y_std = float(np.std(y)) if np.std(y) > 1e-6 else 1.0
    y_norm = (y - y_mean) / y_std

    ds = TensorDataset(
        torch.tensor(X_seq, dtype=torch.float32),
        torch.tensor(X_scaled, dtype=torch.float32),
        torch.tensor(y_norm, dtype=torch.float32),
    )
    loader = DataLoader(ds, batch_size=batch_size, shuffle=True)

    model = WeatherGRUNet(seq_input_dim=len(TARGET_VARS), full_dim=X_scaled.shape[1], hidden_dim=hidden_dim)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-3)
    criterion = nn.MSELoss()

    model.train()
    for _ in range(epochs):
        for b_seq, b_full, b_y in loader:
            optimizer.zero_grad()
            pred = model(b_seq, b_full)
            loss = criterion(pred, b_y)
            loss.backward()
            optimizer.step()

    model.eval()
    sd = model.state_dict()
    return {
        "W_ih": sd["gru.weight_ih_l0"].detach().cpu().numpy().astype(np.float64),
        "W_hh": sd["gru.weight_hh_l0"].detach().cpu().numpy().astype(np.float64),
        "b_ih": sd["gru.bias_ih_l0"].detach().cpu().numpy().astype(np.float64),
        "b_hh": sd["gru.bias_hh_l0"].detach().cpu().numpy().astype(np.float64),
        "fc_W": sd["fc.weight"].detach().cpu().numpy().astype(np.float64),
        "fc_b": sd["fc.bias"].detach().cpu().numpy().astype(np.float64),
        "hidden_dim": hidden_dim,
        "seq_indices": seq_indices,
        "y_mean": y_mean,
        "y_std": y_std,
    }


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40.0, 40.0)))


def gru_predict_from_weights(gru_w: dict, X_scaled: np.ndarray) -> np.ndarray:
    """
    Execute the exact mathematical PyTorch GRU forward pass using the saved NumPy weight matrices.
    """
    seq_idx_arr = np.array(gru_w["seq_indices"], dtype=np.int64)
    X_seq = X_scaled[:, seq_idx_arr]  # (N, 8, 5)
    N, T, _ = X_seq.shape
    H = gru_w["hidden_dim"]

    W_ih = gru_w["W_ih"]  # (3H, 5)
    W_hh = gru_w["W_hh"]  # (3H, H)
    b_ih = gru_w["b_ih"]  # (3H,)
    b_hh = gru_w["b_hh"]  # (3H,)

    h = np.zeros((N, H), dtype=np.float64)
    for t in range(T):
        x_t = X_seq[:, t, :]
        gi = x_t @ W_ih.T + b_ih
        gh = h @ W_hh.T + b_hh

        i_r, i_z, i_n = gi[:, :H], gi[:, H:2 * H], gi[:, 2 * H:]
        h_r, h_z, h_n = gh[:, :H], gh[:, H:2 * H], gh[:, 2 * H:]

        r_t = _sigmoid(i_r + h_r)
        z_t = _sigmoid(i_z + h_z)
        n_t = np.tanh(i_n + r_t * h_n)
        h = (1.0 - z_t) * n_t + z_t * h

    combined = np.hstack([h, X_scaled])  # (N, H + 58)
    out_norm = (combined @ gru_w["fc_W"].T + gru_w["fc_b"]).ravel()
    return out_norm * gru_w["y_std"] + gru_w["y_mean"]


def bootstrap_ci(y_true: np.ndarray, y_pred: np.ndarray, metric_fn, n_boot: int = 200, seed: int = 42):
    rng = np.random.default_rng(seed)
    n = len(y_true)
    if n == 0:
        return 0.0, 0.0
    scores = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        scores.append(metric_fn(y_true[idx], y_pred[idx]))
    return float(np.percentile(scores, 2.5)), float(np.percentile(scores, 97.5))


def fit_hybrid_gru_ridge_hgb_xgboost_residual(
    X_raw: np.ndarray,
    X_scaled: np.ndarray,
    y: np.ndarray,
    seq_indices: list[list[int]],
    gru_epochs: int = 16,
) -> tuple[dict, Ridge, HistGradientBoostingRegressor, XGBRegressor]:
    """
    Two-stage Hybrid Residual Learning with GRU + Ridge + HistGradientBoosting + XGBoost Residual.
    """
    gru_w = train_pytorch_gru_and_export_weights(
        X_scaled, y, seq_indices, hidden_dim=32, epochs=gru_epochs
    )
    y_gru_pred = gru_predict_from_weights(gru_w, X_scaled)

    ridge_full = Ridge(alpha=10.0)
    ridge_full.fit(X_scaled, y)
    y_ridge_pred = ridge_full.predict(X_scaled)

    hgb_full = HistGradientBoostingRegressor(
        max_iter=250,
        learning_rate=0.05,
        max_depth=8,
        min_samples_leaf=25,
        l2_regularization=1.0,
        random_state=42,
    )
    hgb_full.fit(X_raw, y)
    y_hgb_pred = hgb_full.predict(X_raw)

    # Stage 1 Base prediction combining GRU + Ridge + HistGB
    y_base = 0.15 * y_gru_pred + 0.10 * y_ridge_pred + 0.75 * y_hgb_pred

    # Stage 2 Residual r = y - y_base
    base_residuals = y - y_base

    xgb_residual = XGBRegressor(
        n_estimators=180,
        learning_rate=0.03,
        max_depth=5,
        min_child_weight=25,
        subsample=0.85,
        colsample_bytree=0.85,
        reg_alpha=1.0,
        reg_lambda=4.0,
        random_state=42,
        n_jobs=4,
    )
    xgb_residual.fit(X_raw, base_residuals)

    return gru_w, ridge_full, hgb_full, xgb_residual


def predict_hybrid(
    gru_w: dict,
    ridge_model: Ridge,
    hgb_model: HistGradientBoostingRegressor,
    xgb_res_model: XGBRegressor,
    X_raw: np.ndarray,
    X_scaled: np.ndarray,
) -> np.ndarray:
    y_gru = gru_predict_from_weights(gru_w, X_scaled)
    y_ridge = ridge_model.predict(X_scaled)
    y_hgb = hgb_model.predict(X_raw)
    base_pred = 0.15 * y_gru + 0.10 * y_ridge + 0.75 * y_hgb
    res_pred = xgb_res_model.predict(X_raw)
    return base_pred + 0.50 * res_pred


# ==============================================================================
# WALK-FORWARD & MULTI-HORIZON AUTOREGRESSIVE ENGINE
# ==============================================================================

def generate_walk_forward_splits(
    df_feat: pd.DataFrame,
    purge_hours: int = MAX_HORIZON,
    max_train_years: int = 4,
) -> list[dict]:
    """
    Generate Walk-Forward Validation folds with a strict purge gap (168h) between Train and Test.
    - If multi-year dataset (>= 365 days): Retrains quarterly (every 3 months), tests on the next quarter.
    - If short dataset (< 365 days): Automatically creates 4 chronological expanding folds.
    """
    min_ts = df_feat["timestamp"].min()
    max_ts = df_feat["timestamp"].max()
    total_days = (max_ts - min_ts).total_seconds() / 86400.0
    purge_delta = pd.Timedelta(hours=purge_hours)

    splits = []
    if total_days >= 365:
        # Multi-year mode: Initial train window (at least 2 years, or 50% of data), step quarterly
        initial_train_days = max(365 * 2, int(total_days * 0.45))
        cursor_ts = (min_ts + pd.Timedelta(days=initial_train_days)).floor("D")

        fold_idx = 1
        while cursor_ts + purge_delta + pd.Timedelta(days=14) <= max_ts:
            train_end = cursor_ts
            train_start = max(min_ts, train_end - pd.Timedelta(days=365 * max_train_years))
            test_start = train_end + purge_delta
            test_end = min(max_ts, test_start + pd.DateOffset(months=3))

            splits.append({
                "fold": fold_idx,
                "train_start": train_start,
                "train_end": train_end,
                "test_start": test_start,
                "test_end": test_end,
                "enso_phase": get_enso_phase(test_start),
                "season": get_season_label(test_start.month),
            })
            cursor_ts = cursor_ts + pd.DateOffset(months=3)
            fold_idx += 1
    else:
        # Short dataset mode (e.g., 3-month dataset): 4 expanding folds
        unique_ts = np.sort(df_feat["timestamp"].unique())
        n_ts = len(unique_ts)
        train_fracs = [0.50, 0.62, 0.74, 0.85]
        for fold_idx, frac in enumerate(train_fracs, start=1):
            train_end = pd.Timestamp(unique_ts[int(n_ts * frac)])
            test_start = train_end + purge_delta
            next_frac = train_fracs[fold_idx] if fold_idx < len(train_fracs) else 1.0
            test_end = pd.Timestamp(unique_ts[min(n_ts - 1, int(n_ts * next_frac))])

            if test_end <= test_start + pd.Timedelta(hours=MAX_HORIZON):
                test_end = pd.Timestamp(unique_ts[-1])

            if (test_end - test_start).total_seconds() / 3600.0 >= MAX_HORIZON:
                splits.append({
                    "fold": fold_idx,
                    "train_start": min_ts,
                    "train_end": train_end,
                    "test_start": test_start,
                    "test_end": test_end,
                    "enso_phase": get_enso_phase(test_start),
                    "season": get_season_label(test_start.month),
                })

        # Deduplicate if last folds converged to the same test_end
        unique_splits = []
        seen_starts = set()
        for s in splits:
            if s["train_end"] not in seen_starts:
                unique_splits.append(s)
                seen_starts.add(s["train_end"])
        splits = unique_splits

    return splits


def prepare_rollout_origins(
    df_full: pd.DataFrame,
    test_start: pd.Timestamp,
    test_end: pd.Timestamp,
    stride_hours: int = 24,
) -> dict | None:
    """
    Extract batch matrices of history (72h before origin) and future ground-truth (168h after origin)
    across all 20 cities so multi-horizon autoregressive rollout can run in 100% vectorized NumPy.
    """
    context_start = test_start - pd.Timedelta(hours=MAX_LAG)
    df_slice = (
        df_full[(df_full["timestamp"] >= context_start) & (df_full["timestamp"] <= test_end)]
        .sort_values(["location_id", "timestamp"])
        .copy()
    )

    static_list = []
    hist_list = []
    fut_temp_list = []
    fut_time_list = []
    origin_ts_list = []

    for loc_id, group in df_slice.groupby("location_id", sort=False):
        ts_arr = group["timestamp"].to_numpy()
        vals_arr = group[TARGET_VARS].to_numpy(dtype=np.float64)
        n_rows = len(group)

        if n_rows < MAX_LAG + MAX_HORIZON:
            continue

        static_vec = np.array(
            [
                float(loc_id),
                float(group["requested_lat"].iloc[0]),
                float(group["requested_lon"].iloc[0]),
                float(group["elevation_m"].iloc[0]),
            ],
            dtype=np.float64,
        )

        # Precompute cyclical time features for the entire location slice
        hours = group["timestamp"].dt.hour.to_numpy(dtype=np.float64)
        doys = group["timestamp"].dt.dayofyear.to_numpy(dtype=np.float64)
        time_feats = np.column_stack([
            np.sin(2 * np.pi * hours / 24.0),
            np.cos(2 * np.pi * hours / 24.0),
            np.sin(2 * np.pi * doys / 365.25),
            np.cos(2 * np.pi * doys / 365.25),
        ])

        for idx in range(MAX_LAG, n_rows - MAX_HORIZON + 1, stride_hours):
            t0 = pd.Timestamp(ts_arr[idx])
            if t0 < test_start:
                continue
            # Ensure contiguous hourly timestamps without missing gaps
            if (pd.Timestamp(ts_arr[idx + MAX_HORIZON - 1]) - t0) != pd.Timedelta(hours=MAX_HORIZON - 1):
                continue
            if (t0 - pd.Timestamp(ts_arr[idx - MAX_LAG])) != pd.Timedelta(hours=MAX_LAG):
                continue

            static_list.append(static_vec)
            hist_list.append(vals_arr[idx - MAX_LAG : idx])  # (72, 5): t-72h .. t-1h
            fut_temp_list.append(vals_arr[idx : idx + MAX_HORIZON, 0])  # (168,) temperature_2m
            fut_time_list.append(time_feats[idx : idx + MAX_HORIZON])  # (168, 4)
            origin_ts_list.append(t0)

    if not static_list:
        return None

    return {
        "static_mat": np.array(static_list, dtype=np.float64),        # (B, 4)
        "hist_buffer": np.array(hist_list, dtype=np.float64),         # (B, 72, 5)
        "fut_temp_true": np.array(fut_temp_list, dtype=np.float64),   # (B, 168)
        "fut_time_feats": np.array(fut_time_list, dtype=np.float64),  # (B, 168, 4)
        "origin_timestamps": pd.to_datetime(origin_ts_list),
    }


def rollout_multi_horizon_vectorized(
    batch_data: dict,
    scaler: StandardScaler,
    step_Predictors: dict,
) -> dict[str, dict[int, np.ndarray]]:
    """
    Perform 168-step autoregressive rollout simultaneously across all origins in `batch_data`.
    At each step h in 1..168, predicted values are appended to the history buffer and used as
    lag_1h, lag_2h, ..., roll24_mean, roll24_std for step h+1.
    """
    static_mat = batch_data["static_mat"]
    fut_time_feats = batch_data["fut_time_feats"]
    B = static_mat.shape[0]
    n_vars = len(TARGET_VARS)

    # Precompute buffer indices for LAGS = [1, 2, 3, 6, 12, 24, 48, 72] inside a 72-step window
    lag_buf_indices = [MAX_LAG - lag for lag in LAGS]

    results = {}
    for model_name, pred_fn in step_Predictors.items():
        # Copy initial 72-hour true history buffer: shape (B, 72, 5)
        buf = batch_data["hist_buffer"].copy()
        horizon_preds = {}

        for step_idx in range(MAX_HORIZON):
            h = step_idx + 1
            if model_name == "Seasonal Naive":
                # Seasonal Naive repeats the last 24h cycle from the autoregressive buffer
                next_vals = buf[:, -24, :].copy()
            else:
                # Assemble exact 58-column feature matrix for all B origins at step h
                X_step = np.empty((B, 58), dtype=np.float64)
                X_step[:, 0:4] = static_mat
                X_step[:, 4:8] = fut_time_feats[:, step_idx, :]

                col_Include = 8
                for v_idx in range(n_vars):
                    # 8 Lags for variable v_idx
                    for b_idx in lag_buf_indices:
                        X_step[:, col_Include] = buf[:, b_idx, v_idx]
                        col_Include += 1
                    # 24h Rolling Mean and Std (sample std ddof=1 matching pandas .std())
                    recent_24 = buf[:, -24:, v_idx]
                    X_step[:, col_Include] = np.mean(recent_24, axis=1)
                    X_step[:, col_Include + 1] = np.std(recent_24, axis=1, ddof=1)
                    col_Include += 2

                X_step_scaled = scaler.transform(X_step)
                next_vals = pred_fn(X_step, X_step_scaled)

                # Apply physical bounds for stability over 168 autoregressive steps
                next_vals[:, 0] = np.clip(next_vals[:, 0], -5.0, 50.0)    # temperature_2m
                next_vals[:, 1] = np.clip(next_vals[:, 1], 0.0, 100.0)    # relative_humidity_2m
                next_vals[:, 2] = np.clip(next_vals[:, 2], 0.0, 150.0)    # wind_speed_10m
                next_vals[:, 3] = np.clip(next_vals[:, 3], 0.0, 500.0)    # precipitation
                next_vals[:, 4] = np.clip(next_vals[:, 4], 950.0, 1060.0) # pressure_msl

            if h in HORIZONS:
                horizon_preds[h] = next_vals[:, 0].copy()  # Store temperature_2m forecast at horizon h

            # Slide 72h buffer forward by 1 hour and append new prediction
            buf[:, :-1, :] = buf[:, 1:, :]
            buf[:, -1, :] = next_vals

        results[model_name] = horizon_preds

    return results


def run_walk_forward_multi_horizon_evaluation(
    df_feat: pd.DataFrame,
    feature_cols: list[str],
    seq_indices: list[list[int]],
) -> dict:
    """
    Execute expanding Walk-Forward Validation across all folds and evaluate all 5 models
    at forecast horizons h = 1h, 24h, 72h, and 168h.
    """
    splits = generate_walk_forward_splits(df_feat, purge_hours=MAX_HORIZON)
    model_names = [
        "Seasonal Naive",
        "Ridge Autoregressive",
        "GRU Neural Network",
        "HistGradientBoosting",
        "Hybrid GRU + XGBoost Residual",
    ]

    print(f"\n2. Walk-Forward Multi-Horizon Validation ({len(splits)} Folds, Purge Gap = {MAX_HORIZON}h):")
    for s in splits:
        print(
            f"   - Fold {s['fold']:>2}: Train [{s['train_start'].strftime('%Y-%m-%d')} -> {s['train_end'].strftime('%Y-%m-%d')}] "
            f"| Test [{s['test_start'].strftime('%Y-%m-%d')} -> {s['test_end'].strftime('%Y-%m-%d')}] "
            f"| {s['enso_phase']}"
        )

    # Storage for out-of-sample predictions across all walk-forward folds
    y_true_by_h = {h: [] for h in HORIZONS}
    y_pred_by_model_h = {m: {h: [] for h in HORIZONS} for m in model_names}
    meta_records = []  # Tracks month, season, ENSO phase for each forecast origin
    train_times = {m: [] for m in model_names}
    train_times["Seasonal Naive"] = [0.001]

    for s in splits:
        t_fold_start = time.perf_counter()
        df_tr = df_feat[
            (df_feat["timestamp"] >= s["train_start"]) & (df_feat["timestamp"] <= s["train_end"])
        ]

        # Determine stride so each fold samples ~120-200 origins across the 20 cities
        test_hours = (s["test_end"] - s["test_start"]).total_seconds() / 3600.0
        stride_h = 24 if test_hours <= 24 * 45 else 72

        batch_data = prepare_rollout_origins(df_feat, s["test_start"], s["test_end"], stride_hours=stride_h)
        if batch_data is None:
            continue

        scaler = StandardScaler()
        X_tr_raw = df_tr[feature_cols].to_numpy(dtype=np.float64)
        X_tr_scaled = scaler.fit_transform(X_tr_raw)

        # Train all 5 target variables per model family so multi-step rollout updates all 5 covariates
        ridge_vars, gru_vars, hgb_vars, hyb_vars = {}, {}, {}, {}
        t_ridge, t_gru, t_hgb, t_hyb = 0.0, 0.0, 0.0, 0.0

        for v_idx, target in enumerate(TARGET_VARS):
            y_tr = df_tr[target].to_numpy(dtype=np.float64)

            # 1. Ridge
            t0 = time.perf_counter()
            r_mod = Ridge(alpha=10.0)
            r_mod.fit(X_tr_scaled, y_tr)
            t_ridge += time.perf_counter() - t0
            ridge_vars[target] = r_mod

            # 2. HistGB
            t0 = time.perf_counter()
            h_mod = HistGradientBoostingRegressor(
                max_iter=200,
                learning_rate=0.05,
                max_depth=7,
                min_samples_leaf=30,
                l2_regularization=1.5,
                random_state=42,
            )
            h_mod.fit(X_tr_raw, y_tr)
            t_hgb += time.perf_counter() - t0
            hgb_vars[target] = h_mod

            # 3. GRU (Fewer epochs on intermediate folds for speed, full convergence on temperature)
            t0 = time.perf_counter()
            g_epochs = 12 if target == "temperature_2m" else 8
            g_w = train_pytorch_gru_and_export_weights(
                X_tr_scaled, y_tr, seq_indices, hidden_dim=32, epochs=g_epochs
            )
            t_gru += time.perf_counter() - t0
            gru_vars[target] = g_w

            # 4. Hybrid (Reuses trained GRU, Ridge, HistGB + fits XGBoost Residual)
            t0 = time.perf_counter()
            y_base = (
                0.15 * gru_predict_from_weights(g_w, X_tr_scaled)
                + 0.10 * r_mod.predict(X_tr_scaled)
                + 0.75 * h_mod.predict(X_tr_raw)
            )
            xgb_res = XGBRegressor(
                n_estimators=150,
                learning_rate=0.03,
                max_depth=5,
                min_child_weight=25,
                subsample=0.85,
                colsample_bytree=0.85,
                reg_alpha=1.0,
                reg_lambda=4.0,
                random_state=42,
                n_jobs=4,
            )
            xgb_res.fit(X_tr_raw, y_tr - y_base)
            t_hyb += (time.perf_counter() - t0)
            hyb_vars[target] = (g_w, r_mod, h_mod, xgb_res)

        train_times["Ridge Autoregressive"].append(t_ridge / len(TARGET_VARS))
        train_times["HistGradientBoosting"].append(t_hgb / len(TARGET_VARS))
        train_times["GRU Neural Network"].append(t_gru / len(TARGET_VARS))
        train_times["Hybrid GRU + XGBoost Residual"].append(
            (t_ridge + t_hgb + t_gru + t_hyb) / len(TARGET_VARS)
        )

        # Define batch step predictors returning (B, 5) across all 5 TARGET_VARS
        step_predictors = {
            "Seasonal Naive": None,
            "Ridge Autoregressive": lambda X_r, X_s: np.column_stack(
                [ridge_vars[v].predict(X_s) for v in TARGET_VARS]
            ),
            "GRU Neural Network": lambda X_r, X_s: np.column_stack(
                [gru_predict_from_weights(gru_vars[v], X_s) for v in TARGET_VARS]
            ),
            "HistGradientBoosting": lambda X_r, X_s: np.column_stack(
                [hgb_vars[v].predict(X_r) for v in TARGET_VARS]
            ),
            "Hybrid GRU + XGBoost Residual": lambda X_r, X_s: np.column_stack(
                [predict_hybrid(*hyb_vars[v], X_r, X_s) for v in TARGET_VARS]
            ),
        }

        rollout_preds = rollout_multi_horizon_vectorized(batch_data, scaler, step_predictors)

        for h in HORIZONS:
            y_true_by_h[h].append(batch_data["fut_temp_true"][:, h - 1])
            for m_name in model_names:
                y_pred_by_model_h[m_name][h].append(rollout_preds[m_name][h])

        for ts in batch_data["origin_timestamps"]:
            meta_records.append({
                "fold": s["fold"],
                "origin_ts": ts,
                "year_month": ts.strftime("%Y-%m"),
                "season": get_season_label(ts.month),
                "enso_phase": get_enso_phase(ts),
            })

        fold_elapsed = time.perf_counter() - t_fold_start
        fold_mae_h1 = mean_absolute_error(
            batch_data["fut_temp_true"][:, 0],
            rollout_preds["Hybrid GRU + XGBoost Residual"][1],
        )
        fold_mae_h24 = mean_absolute_error(
            batch_data["fut_temp_true"][:, 23],
            rollout_preds["Hybrid GRU + XGBoost Residual"][24],
        )
        fold_mae_h168 = mean_absolute_error(
            batch_data["fut_temp_true"][:, 167],
            rollout_preds["Hybrid GRU + XGBoost Residual"][168],
        )
        print(
            f"     -> Fold {s['fold']:>2} Done ({len(batch_data['origin_timestamps']):>4} origins, {fold_elapsed:.1f}s) "
            f"| Hybrid MAE: h=1h: {fold_mae_h1:.3f}°C | h=24h: {fold_mae_h24:.3f}°C | h=168h: {fold_mae_h168:.3f}°C"
        )

    # Concatenate all Walk-Forward folds
    y_true_concat = {h: np.concatenate(y_true_by_h[h]) for h in HORIZONS}
    y_pred_concat = {
        m: {h: np.concatenate(y_pred_by_model_h[m][h]) for h in HORIZONS}
        for m in model_names
    }
    meta_df = pd.DataFrame(meta_records)

    # 1. Multi-Horizon Summary per Model
    horizon_summary = {}
    model_comparison_compat = {}

    for m_name in model_names:
        horizon_summary[m_name] = {}
        for h in HORIZONS:
            yt = y_true_concat[h]
            yp = y_pred_concat[m_name][h]
            mae = float(mean_absolute_error(yt, yp))
            rmse = float(root_mean_squared_error(yt, yp))
            r2 = float(r2_score(yt, yp))
            ci_low, ci_high = bootstrap_ci(yt, yp, mean_absolute_error)
            horizon_summary[m_name][f"h_{h}h"] = {
                "mae": round(mae, 4),
                "mae_95ci": [round(ci_low, 4), round(ci_high, 4)],
                "rmse": round(rmse, 4),
                "r2": round(r2, 4),
            }

        # Populate backward-compatible `model_comparison` dictionary (h=1h as test, h=24h as val)
        h1_metrics = horizon_summary[m_name]["h_1h"]
        h24_metrics = horizon_summary[m_name]["h_24h"]
        h72_metrics = horizon_summary[m_name]["h_72h"]
        h168_metrics = horizon_summary[m_name]["h_168h"]

        model_comparison_compat[m_name] = {
            "val_mae": h24_metrics["mae"],
            "val_rmse": h24_metrics["rmse"],
            "val_r2": h24_metrics["r2"],
            "test_mae": h1_metrics["mae"],
            "test_mae_95ci": h1_metrics["mae_95ci"],
            "test_rmse": h1_metrics["rmse"],
            "test_r2": h1_metrics["r2"],
            "mae_h1h": h1_metrics["mae"],
            "mae_h24h": h24_metrics["mae"],
            "mae_h72h": h72_metrics["mae"],
            "mae_h168h": h168_metrics["mae"],
            "train_time_sec": round(float(np.mean(train_times[m_name])), 4),
        }

    # 2. Monthly Distribution, Seasonal & ENSO Breakdown for Hybrid Model (at h=24h and h=168h)
    for h in [1, 24, 72, 168]:
        meta_df[f"abs_err_h{h}"] = np.abs(
            y_true_concat[h] - y_pred_concat["Hybrid GRU + XGBoost Residual"][h]
        )

    monthly_mae = meta_df.groupby("year_month")[["abs_err_h1", "abs_err_h24", "abs_err_h72", "abs_err_h168"]].mean()
    monthly_distribution = {}
    for h in HORIZONS:
        col = f"abs_err_h{h}"
        worst_ym = str(monthly_mae[col].idxmax())
        monthly_distribution[f"h_{h}h"] = {
            "mean_monthly_mae": round(float(monthly_mae[col].mean()), 4),
            "std_monthly_mae": round(float(monthly_mae[col].std(ddof=0)), 4),
            "p90_monthly_mae": round(float(np.percentile(monthly_mae[col], 90)), 4),
            "worst_month": worst_ym,
            "worst_month_mae": round(float(monthly_mae[col].max()), 4),
        }

    seasonal_breakdown = (
        meta_df.groupby("season")[["abs_err_h1", "abs_err_h24", "abs_err_h72", "abs_err_h168"]]
        .mean()
        .round(4)
        .rename(columns=lambda c: c.replace("abs_err_", "mae_"))
        .to_dict(orient="index")
    )

    enso_breakdown = (
        meta_df.groupby("enso_phase")[["abs_err_h1", "abs_err_h24", "abs_err_h72", "abs_err_h168"]]
        .mean()
        .round(4)
        .rename(columns=lambda c: c.replace("abs_err_", "mae_"))
        .to_dict(orient="index")
    )

    return {
        "num_folds": len(splits),
        "total_forecast_origins": len(meta_df),
        "horizons_evaluated": HORIZONS,
        "model_comparison_compat": model_comparison_compat,
        "multi_horizon_summary": horizon_summary,
        "monthly_mae_distribution": monthly_distribution,
        "seasonal_mae_breakdown": seasonal_breakdown,
        "enso_phase_mae_breakdown": enso_breakdown,
    }


def train_and_save_weights():
    print("=" * 86)
    print("STEP 4: WALK-FORWARD MULTI-HORIZON EVALUATION & HYBRID MODEL SERIALIZATION")
    print("=" * 86)

    df_clean = load_weather_dataset()

    # 1. Stationarity & Seasonality Check
    hcm_series = (
        df_clean[df_clean["city"] == "Ho Chi Minh City"]
        .sort_values("timestamp")["temperature_2m"]
        .dropna()
    )
    adf_stat, adf_pval, _, _, _, _ = adfuller(hcm_series.iloc[-50000:], maxlag=24)
    autocorr_24h = float(hcm_series.autocorr(lag=24))
    print("1. Time-Series Diagnostics:")
    print(f"   - Total Rows Loaded : {len(df_clean):,}")
    print(f"   - Date Range        : {df_clean['timestamp'].min()} -> {df_clean['timestamp'].max()}")
    print(f"   - ADF Statistic     : {adf_stat:.4f} (p-value: {adf_pval:.4e})")
    print(f"   - 24h Autocorrel.   : {autocorr_24h:.4f}")

    # 2. Build Supervised Features & Run Walk-Forward Multi-Horizon Validation
    df_feat, feature_cols = build_supervised_features(df_clean)
    seq_indices = get_gru_sequence_indices(feature_cols)

    wf_results = run_walk_forward_multi_horizon_evaluation(df_feat, feature_cols, seq_indices)
    model_comparison = wf_results["model_comparison_compat"]

    print("\n3. Walk-Forward Multi-Horizon MAE Comparison on Temperature_2m (°C):")
    print(f"   {'Model Name':<30} | {'h = 1h':>8} | {'h = 24h':>8} | {'h = 72h':>8} | {'h = 168h':>8}")
    print("   " + "-" * 74)
    for m_name, metrics in model_comparison.items():
        print(
            f"   {m_name:<30} | {metrics['mae_h1h']:>7.3f}° | {metrics['mae_h24h']:>7.3f}° | "
            f"{metrics['mae_h72h']:>7.3f}° | {metrics['mae_h168h']:>7.3f}°"
        )

    print("\n   [Climate & Seasonal Robustness - Hybrid Model MAE (°C)]:")
    for phase, p_metrics in wf_results["enso_phase_mae_breakdown"].items():
        print(
            f"   - ENSO [{phase:<20}] -> h=1h: {p_metrics['mae_h1']:.3f}°C | "
            f"h=24h: {p_metrics['mae_h24']:.3f}°C | h=168h: {p_metrics['mae_h168']:.3f}°C"
        )

    # 4. Final Production Model Training on Most Recent Window (up to last 4 years)
    print("\n4. Training Final Production Hybrid Models for All 5 Variables...")
    unique_times = np.sort(df_feat["timestamp"].unique())
    n_times = len(unique_times)
    test_Split_ts = unique_times[int(n_times * 0.85)]

    # Cap production training window to the most recent 500,000 rows (~3 years across 20 cities)
    df_train_val = df_feat[df_feat["timestamp"] <= test_Split_ts].iloc[-500_000:].copy()
    df_test = df_feat[df_feat["timestamp"] > test_Split_ts].copy()

    X_train_val_raw = df_train_val[feature_cols].to_numpy(dtype=np.float64)
    X_test_raw = df_test[feature_cols].to_numpy(dtype=np.float64)

    production_scaler = StandardScaler()
    X_train_val_scaled = production_scaler.fit_transform(X_train_val_raw)
    X_test_prod_scaled = production_scaler.transform(X_test_raw)

    trained_gru_weights = {}
    trained_hgb_models = {}
    trained_ridge_models = {}
    trained_xgb_residual_models = {}
    multi_target_metrics = {}

    for target in TARGET_VARS:
        y_tv = df_train_val[target].to_numpy(dtype=np.float64)
        y_te = df_test[target].to_numpy(dtype=np.float64)

        g_w, r_mod, h_mod, xgb_res_mod = fit_hybrid_gru_ridge_hgb_xgboost_residual(
            X_train_val_raw, X_train_val_scaled, y_tv, seq_indices, gru_epochs=16
        )
        trained_gru_weights[target] = g_w
        trained_ridge_models[target] = r_mod
        trained_hgb_models[target] = h_mod
        trained_xgb_residual_models[target] = xgb_res_mod

        preds_te = predict_hybrid(g_w, r_mod, h_mod, xgb_res_mod, X_test_raw, X_test_prod_scaled)
        if target in ["relative_humidity_2m", "wind_speed_10m", "precipitation"]:
            preds_te = np.clip(preds_te, 0.0, 100.0 if target == "relative_humidity_2m" else None)

        mae = float(mean_absolute_error(y_te, preds_te))
        rmse = float(root_mean_squared_error(y_te, preds_te))
        r2 = float(r2_score(y_te, preds_te))
        multi_target_metrics[target] = {
            "test_mae": round(mae, 4),
            "test_rmse": round(rmse, 4),
            "test_r2": round(r2, 4),
        }
        print(f"   - Target [{target:<21}] -> 1h MAE: {mae:>6.3f} | RMSE: {rmse:>6.3f} | R²: {r2:>6.4f}")

    hourly_climatology = (
        df_clean.groupby(["location_id", "hour"], as_index=False)[TARGET_VARS]
        .mean()
        .round(2)
    )
    city_metadata_df = (
        df_clean.groupby(["location_id", "city", "region"], as_index=False)[
            ["requested_lat", "requested_lon", "elevation_m"]
        ]
        .first()
        .sort_values("location_id")
    )

    # 5. Serialize Model Weights & Walk-Forward Metadata Bundle to Disk (.joblib)
    weights_bundle = {
        "model_name": "Hybrid (GRU + Ridge + HistGradientBoosting) + XGBoost Residual Forecaster",
        "version": "5.0-WalkForward-MultiHorizon",
        "trained_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        "feature_cols": feature_cols,
        "target_vars": TARGET_VARS,
        "lags": LAGS,
        "seq_indices": seq_indices,
        "gru_weights": trained_gru_weights,
        "hgb_models": trained_hgb_models,
        "ridge_models": trained_ridge_models,
        "xgb_residual_models": trained_xgb_residual_models,
        "scaler": production_scaler,
        "hourly_climatology": hourly_climatology.to_dict(orient="records"),
        "locations": city_metadata_df.to_dict(orient="records"),
        "model_comparison": model_comparison,
        "walk_forward_evaluation": wf_results,
        "multi_target_test_metrics": multi_target_metrics,
        "stationarity_diagnostics": {
            "adf_statistic": round(float(adf_stat), 4),
            "adf_pvalue": float(adf_pval),
            "lag24_autocorrelation": round(autocorr_24h, 4),
        },
    }

    weights_path = MODEL_DIR / "weather_forecast_weights.joblib"
    joblib.dump(weights_bundle, weights_path, compress=3)

    eval_report_path = MODEL_DIR / "model_evaluation_report.json"
    with open(eval_report_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "model_name": weights_bundle["model_name"],
                "version": weights_bundle["version"],
                "trained_at": weights_bundle["trained_at"],
                "total_rows": int(len(df_feat)),
                "num_features": len(feature_cols),
                "stationarity_diagnostics": weights_bundle["stationarity_diagnostics"],
                "temperature_model_comparison": model_comparison,
                "walk_forward_multi_horizon": wf_results,
                "multi_target_test_metrics": multi_target_metrics,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    # 6. Plot Figure 7: Multi-Horizon Error Degradation Curve & Test Forecast Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17.0, 6.4), dpi=180)

    palette = {
        "Seasonal Naive": ("#7f8c8d", ":", "o"),
        "Ridge Autoregressive": ("#f39c12", "--", "s"),
        "GRU Neural Network": ("#2b8cbe", "-.", "^"),
        "HistGradientBoosting": ("#27ae60", "--", "D"),
        "Hybrid GRU + XGBoost Residual": ("#d73027", "-", "P"),
    }

    x_pos = np.arange(len(HORIZONS))
    for m_name, (color, ls, marker) in palette.items():
        maes_h = [
            wf_results["multi_horizon_summary"][m_name][f"h_{h}h"]["mae"]
            for h in HORIZONS
        ]
        lw = 2.6 if "Hybrid" in m_name else 1.8
        ax1.plot(
            x_pos, maes_h, label=m_name, color=color, linestyle=ls,
            marker=marker, markersize=7, linewidth=lw
        )
        if "Hybrid" in m_name or "Naive" in m_name:
            for idx_h, val in enumerate(maes_h):
                ax1.annotate(
                    f"{val:.2f}°C",
                    xy=(x_pos[idx_h], val),
                    xytext=(0, 6),
                    textcoords="offset points",
                    ha="center",
                    fontsize=8.5,
                    fontweight="bold",
                    color=color,
                )

    ax1.set_xticks(x_pos)
    ax1.set_xticklabels([f"h = {h}h\n({h // 24 if h >= 24 else 0}d)" for h in HORIZONS], fontsize=10, fontweight="bold")
    ax1.set_ylabel("Walk-Forward MAE (°C)", fontsize=11, fontweight="bold")
    ax1.set_title("Sai số MAE theo Tầm dự báo (Walk-Forward Multi-Horizon)", fontsize=12.5, fontweight="bold")
    ax1.grid(True, linestyle="--", alpha=0.4)
    ax1.legend(frameon=True, fontsize=9.5)

    # Right panel: Recent 14-day Actual vs Predicted Temperature at Ho Chi Minh City
    hcm_test = df_test[df_test["city"] == "Ho Chi Minh City"].sort_values("timestamp").iloc[-336:].copy()
    hcm_X_raw = hcm_test[feature_cols].to_numpy(dtype=np.float64)
    hcm_X_scl = production_scaler.transform(hcm_X_raw)
    hcm_pred_hybrid = predict_hybrid(
        trained_gru_weights["temperature_2m"],
        trained_ridge_models["temperature_2m"],
        trained_hgb_models["temperature_2m"],
        trained_xgb_residual_models["temperature_2m"],
        hcm_X_raw,
        hcm_X_scl,
    )
    hcm_pred_gru = gru_predict_from_weights(trained_gru_weights["temperature_2m"], hcm_X_scl)

    ax2.plot(hcm_test["timestamp"], hcm_test["temperature_2m"], color="black", linewidth=2.2, label="Thực tế")
    ax2.plot(hcm_test["timestamp"], hcm_pred_hybrid, color="#d73027", linestyle="--", linewidth=1.9, label="Hybrid GRU + XGBoost Residual")
    ax2.plot(hcm_test["timestamp"], hcm_pred_gru, color="#2b8cbe", linestyle=":", linewidth=1.6, label="GRU Neural Network")
    ax2.set_title("Nhiệt độ Thực tế và Dự báo tại Ho Chi Minh City (14 ngày cuối)", fontsize=12.5, fontweight="bold")
    ax2.set_xlabel("Ngày/Tháng/Năm", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Nhiệt độ - °C", fontsize=11, fontweight="bold")
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y"))
    plt.setp(ax2.get_xticklabels(), rotation=12, ha="right", fontsize=9.5)
    ax2.grid(True, linestyle="--", alpha=0.4)
    ax2.legend(frameon=True, fontsize=10)

    plt.tight_layout()
    fig7_path = FIG_DIR / "fig7_model_training_and_forecast_eval.png"
    fig.savefig(fig7_path, bbox_inches="tight", dpi=180)
    plt.close(fig)

    print("=" * 86)
    print(f"Saved Trained Model Weights to : {weights_path} ({weights_path.stat().st_size / 1024:.1f} KB)")
    print(f"Saved Evaluation Report to     : {eval_report_path}")
    print(f"Saved Model Evaluation Plot to : {fig7_path}")
    print("=" * 86)


if __name__ == "__main__":
    train_and_save_weights()