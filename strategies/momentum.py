import pandas as pd

from engine.base_strategy import BaseStrategy

class MomentumStrategy(BaseStrategy):
    def parameter_grid(self) -> dict:
        return {
            "fast_window": [5, 10, 15],
            "slow_window": [20, 30, 50],
            "take_profit": [0.02, 0.04],
            "stop_loss": [0.01, 0.02],
        }

    def generate_signals(self, df: pd.DataFrame, params: dict) -> pd.Series:
        fast = df["close"].rolling(params["fast_window"]).mean()
        slow = df["close"].rolling(params["slow_window"]).mean()
        signal = (fast > slow).astype(int) - (fast < slow).astype(int)
        return signal.fillna(0)
