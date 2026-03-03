import itertools
import json
import multiprocessing as mp
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

import pandas as pd

from engine.backtester import run_backtest
from strategies.momentum import MomentumStrategy


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=['date'])
    df = df.sort_values('date').reset_index(drop=True)
    required = {'date', 'open', 'high', 'low', 'close', 'volume'}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return df


def evaluate(task: Tuple[str, dict], data: pd.DataFrame, base_capital: float) -> dict:
    name, param_dict = task
    strategy = MomentumStrategy()
    positions = strategy.generate_signals(data, param_dict)
    metrics = run_backtest(data, positions, param_dict['take_profit'], param_dict['stop_loss'], base_capital)
    metrics.update({'strategy': name, 'params': param_dict})
    return metrics


def expand_grid(strategy: MomentumStrategy) -> List[dict]:
    grid = strategy.parameter_grid()
    keys = list(grid.keys())
    combos = list(itertools.product(*[grid[k] for k in keys]))
    return [dict(zip(keys, combo)) for combo in combos]


def run_grid_search(data_path: str, base_capital: float, max_workers: int | None = None) -> List[dict]:
    data = load_data(Path(data_path))
    strategy = MomentumStrategy()
    params_list = expand_grid(strategy)

    tasks = [('momentum', p) for p in params_list]
    workers = max_workers or mp.cpu_count()

    with mp.Pool(processes=workers) as pool:
        results = pool.starmap(evaluate, [(t, data, base_capital) for t in tasks])

    ranked = sorted(results, key=lambda r: r['net_return'], reverse=True)[:10]
    return ranked


def save_outputs(results: List[dict], output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / 'optimization_results.json'
    json_path.write_text(json.dumps(results, indent=2))

    lines = ['# Daily Optimization Report', f"Generated: {datetime.utcnow().isoformat()} UTC", '']
    for i, r in enumerate(results, 1):
        lines.append(f"## Rank {i}: {r['strategy']}")
        lines.append(f"Params: {r['params']}")
        lines.append(
            'Metrics: '
            f"win_rate={r['win_rate']:.2f}, profit_factor={r['profit_factor']:.2f}, "
            f"max_dd={r['max_drawdown']:.2%}, sharpe={r['sharpe_ratio']:.2f}, "
            f"net_return={r['net_return']:.4f}, trades={r['trade_count']}"
        )
        lines.append('')

    report_path = output_dir / 'daily_report.md'
    report_path.write_text('\n'.join(lines))
    return json_path, report_path


def optimize(data_path: str, base_capital: float, output_dir: str, max_workers: int | None = None):
    results = run_grid_search(data_path, base_capital, max_workers)
    return save_outputs(results, Path(output_dir))
