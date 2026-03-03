# Agent Onboarding

Read in this order:
1) README.md — overview, topology, how to run.
2) docker-compose.yml — volumes/binds and container entrypoint.
3) engine/optimizer.py — grid search + reporting pipeline.
4) engine/backtester.py — metrics and equity logic.
5) strategies/momentum.py — example strategy and parameter grid.
6) CHANGELOG.md — update on every change.

## Change policy
- Every change must add a dated bullet to CHANGELOG.md.
- Do not commit secrets or large proprietary datasets. `.env` and real data stay local.
- Keep cron time and worker count defaults unless requirements change.

## Development notes
- DATA_FILE must be reachable inside container; bind-mount real datasets to `./data`.
- Multiprocessing defaults to CPU count; set `MAX_WORKERS` in `.env` to limit.
- Reports are written to `/app/data` (host `./data`).

## Relationship to other components
- Optimizer informs strategy selection for Nova Pulse.
- Alert Relay Node (~/horizon/alert-relay) delivers live signals; keep contracts stable between backtest outputs and live alert formats.

