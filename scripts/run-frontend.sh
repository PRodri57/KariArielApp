#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $(basename "$0") <host-ip> [env: PORT, API_PORT, VITE_API_BASE_URL, VITE_USE_MOCKS]" >&2
  exit 1
}

HOST_IP="${1:-}"
if [[ -z "$HOST_IP" ]]; then
  usage
fi

PORT="${PORT:-5173}"
API_PORT="${API_PORT:-8000}"
export VITE_API_BASE_URL="${VITE_API_BASE_URL:-http://${HOST_IP}:${API_PORT}}"
export VITE_USE_MOCKS="${VITE_USE_MOCKS:-false}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR/Frontend"

echo "Starting frontend on 0.0.0.0:${PORT}"
echo "VITE_API_BASE_URL=${VITE_API_BASE_URL}"

VITE_BIN="$ROOT_DIR/Frontend/node_modules/.bin/vite"
if [[ ! -x "$VITE_BIN" ]]; then
  echo "Error: falta node_modules/.bin/vite. Ejecuta: (cd Frontend && npm install)" >&2
  echo "Nota: el paquete Python 'vite' no sirve para el frontend." >&2
  exit 1
fi

VITE_JS="$ROOT_DIR/Frontend/node_modules/vite/bin/vite.js"
if [[ -f "$VITE_JS" ]] && command -v node >/dev/null 2>&1; then
  exec node "$VITE_JS" --host 0.0.0.0 --port "$PORT"
elif command -v npm >/dev/null 2>&1; then
  exec npm run dev -- --host 0.0.0.0 --port "$PORT"
else
  echo "Error: no se encontro npm en PATH." >&2
  exit 1
fi
