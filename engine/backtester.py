import numpy as np
import pandas as pd


def compute_metrics(df: pd.DataFrame, equity_curve: pd.Series) -> dict:
    returns = df["strategy_returns"]
    trades = df.loc[df["positions"].diff().abs() > 0]
    wins = (returns > 0).sum()
    losses = (returns < 0).sum()
    gross_profit = returns[returns > 0].sum()
    gross_loss = -returns[returns < 0].sum()

    max_drawdown = ((equity_curve.cummax() - equity_curve) / equity_curve.cummax()).max()
    sharpe = 0.0
    if returns.std() > 1e-9:
        sharpe = (returns.mean() / returns.std()) * np.sqrt(252)

    profit_factor = gross_profit / gross_loss if gross_loss > 0 else np.inf
    net_return = equity_curve.iloc[-1] - equity_curve.iloc[0]

    return {
        "win_rate": wins / max(1, (wins + losses)),
        "profit_factor": profit_factor,
        "max_drawdown": max_drawdown,
        "sharpe_ratio": sharpe,
        "net_return": net_return,
        "trade_count": trades.shape[0],
    }


def run_backtest(df: pd.DataFrame, positions: pd.Series, take_profit: float, stop_loss: float, base_capital: float) -> dict:
    df = df.copy()
    df["positions"] = positions.shift(1).fillna(0)
    returns = df["close"].pct_change().fillna(0)
    df["strategy_returns"] = returns * df["positions"]

    # Apply TP/SL on returns per bar (simplified)
    df["strategy_returns"] = df["strategy_returns"].clip(lower=-stop_loss, upper=take_profit)

    equity_curve = (1 + df["strategy_returns"]).cumprod() * base_capital
    metrics = compute_metrics(df, equity_curve)
    metrics["equity_final"] = equity_curve.iloc[-1]
    metrics["equity_curve"] = equity_curve.values.tolist()
    return metrics
