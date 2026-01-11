#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $(basename "$0") <host-ip> [env: PORT, CORS_ORIGINS]" >&2
  exit 1
}

HOST_IP="${1:-}"
if [[ -z "$HOST_IP" ]]; then
  usage
fi

PORT="${PORT:-8000}"
DEFAULT_CORS="http://localhost:5173,http://127.0.0.1:5173,http://${HOST_IP}:5173"
export CORS_ORIGINS="${CORS_ORIGINS:-$DEFAULT_CORS}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR/Backend"

echo "Starting backend on 0.0.0.0:${PORT}"
echo "CORS_ORIGINS=${CORS_ORIGINS}"

if command -v uvicorn >/dev/null 2>&1; then
  exec uvicorn App.main:app --host 0.0.0.0 --port "$PORT"
elif command -v python >/dev/null 2>&1; then
  exec python -m uvicorn App.main:app --host 0.0.0.0 --port "$PORT"
elif command -v python3 >/dev/null 2>&1; then
  exec python3 -m uvicorn App.main:app --host 0.0.0.0 --port "$PORT"
else
  echo "Error: no se encontro uvicorn ni python en PATH." >&2
  exit 1
fi
