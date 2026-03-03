# Horizon Strategy Optimization Engine

CPU-optimized backtesting + parameter sweep engine running nightly on Raspberry Pi 5 (8GB) in Docker.

## Capabilities
- Loads OHLCV CSV data, runs vectorized backtests.
- Grid search across strategy parameters using multiprocessing.
- Ranks top 10 configs by net return.
- Outputs `/app/data/optimization_results.json` and `/app/data/daily_report.md`.
- Nightly cron inside container (configurable via `.env` `CRON_TIME`).

## Deployment topology
- Host: Raspberry Pi 5
  - LAN IP: `192.168.1.20`
  - External IP: `203.0.113.10`
- Container: `optimizer` (cron + Python runner).
- Data binds: `./data`, `./reports`, `./logs` mounted into container.

## Nova / Horizon context
- Marketing site: `horizonsvc.com` → `203.0.113.193`
- Nova bot endpoint: `nova.horizonsvc.com` → `198.51.100.68`
- Horizon API: `api.horizonsvc.com` (DNS unresolved at time of writing).
- This optimizer feeds strategy selection for Nova Pulse; relay node (other repo) delivers live alerts.

## Quick start
```bash
cd ~/horizon/optimizer
cp .env.example .env   # edit DATA_FILE, BASE_CAPITAL, CRON_TIME
docker compose build
docker compose up -d
```

Manual run:
```bash
docker exec optimizer-optimizer-1 python /app/run_once.py
```

Outputs land in `data/optimization_results.json` and `data/daily_report.md` (bind-mounted to host `~/horizon/optimizer/data`).

## Strategy implementation
- BaseStrategy in `engine/base_strategy.py`
- Example: `strategies/momentum.py` (fast/slow MAs + TP/SL)
- Backtester in `engine/backtester.py` computes win rate, profit factor, max drawdown, Sharpe, net return, trade count.
- Optimizer in `engine/optimizer.py` builds grid, multiprocessing pool (workers = `MAX_WORKERS` env or CPU count).

## Scheduling
- Cron inside container (`CRON_TIME`, default `0 2 * * *`).
- Logs: `/app/logs/cron.log` (bind to host `./logs` if desired).

## Current status (2026-03-03)
- Image built and container running; manual run completes (~0.15s on sample data).
- Sample dataset: `data/sample_ohlcv.csv` bundled for smoke tests.

## Troubleshooting
- Ensure DATA_FILE path exists (inside container). Use bind mount for real datasets.
- If cron not firing, check `/app/logs/cron.log` and `service cron status` inside container.
- For heavy datasets, set `MAX_WORKERS` to a sensible core count to avoid memory pressure (8GB RAM total).

## Fit with relay node
- Optimizer selects best parameter sets daily; relay node (~/horizon/alert-relay) ingests live Nova Pulse signals and delivers alerts.

