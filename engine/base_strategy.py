from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    @abstractmethod
    def generate_signals(self, df: pd.DataFrame, params: dict) -> pd.Series:
        """Return a pandas Series of position values (+1 long, -1 short, 0 flat)."""
        raise NotImplementedError

    @abstractmethod
    def parameter_grid(self) -> dict:
        """Return dict of parameter lists for grid search."""
        raise NotImplementedError
