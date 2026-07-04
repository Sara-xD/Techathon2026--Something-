#!/usr/bin/env bash
# One-command launcher: starts the backend, dashboard, and bot together.
# Prerequisite: run setup once first (see README) so the venvs and node_modules
# exist:
#   python -m venv backend/.venv && backend/.venv/bin/pip install -r backend/requirements.txt
#   python -m venv bot/.venv     && bot/.venv/bin/pip install -r bot/requirements.txt
#   npm --prefix dashboard install
#
# Usage: ./run.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"

cleanup() { echo; echo "Stopping all services..."; kill 0 2>/dev/null || true; }
trap cleanup EXIT INT TERM

echo "▶ backend   → http://localhost:8000"
( cd "$ROOT/backend" && . .venv/bin/activate && uvicorn app.main:app --port 8000 ) &

echo "▶ dashboard → http://localhost:5173"
( cd "$ROOT/dashboard" && npm run dev ) &

echo "▶ bot       → Discord if DISCORD_TOKEN is set, otherwise a local mock CLI"
( cd "$ROOT/bot" && . .venv/bin/activate && python bot.py ) &

wait
