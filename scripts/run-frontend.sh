#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $(basename "$0") <host-ip> [extra-host-ip ...] [env: PORT, API_PORT, VITE_USE_MOCKS]" >&2
  exit 1
}

HOST_IPS=("$@")
if [[ ${#HOST_IPS[@]} -eq 0 ]]; then
  usage
fi

PORT="${PORT:-5173}"
API_PORT="${API_PORT:-8000}"
export VITE_USE_MOCKS="${VITE_USE_MOCKS:-false}"
VITE_API_BASE_URL_OVERRIDE="${VITE_API_BASE_URL:-}"
if [[ -n "$VITE_API_BASE_URL_OVERRIDE" && ${#HOST_IPS[@]} -gt 1 ]]; then
  echo "Warning: VITE_API_BASE_URL esta definido; se usara el mismo API para todas las instancias." >&2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR/Frontend"

echo "Starting frontend on 0.0.0.0 (base port ${PORT})"

VITE_BIN="$ROOT_DIR/Frontend/node_modules/.bin/vite"
if [[ ! -x "$VITE_BIN" ]]; then
  echo "Error: falta node_modules/.bin/vite. Ejecuta: (cd Frontend && npm install)" >&2
  echo "Nota: el paquete Python 'vite' no sirve para el frontend." >&2
  exit 1
fi

PIDS=()
cleanup() {
  if [[ ${#PIDS[@]} -gt 0 ]]; then
    kill "${PIDS[@]}" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

VITE_JS="$ROOT_DIR/Frontend/node_modules/vite/bin/vite.js"
if [[ -f "$VITE_JS" ]] && command -v node >/dev/null 2>&1; then
  VITE_COMMAND=("node" "$VITE_JS")
elif command -v npm >/dev/null 2>&1; then
  VITE_COMMAND=("npm" "run" "dev" "--")
else
  echo "Error: no se encontro npm en PATH." >&2
  exit 1
fi

for index in "${!HOST_IPS[@]}"; do
  HOST_IP="${HOST_IPS[$index]}"
  FRONTEND_PORT=$((PORT + index))
  if [[ -n "$VITE_API_BASE_URL_OVERRIDE" ]]; then
    VITE_API_BASE_URL="$VITE_API_BASE_URL_OVERRIDE"
  else
    VITE_API_BASE_URL="http://${HOST_IP}:${API_PORT}"
  fi
  echo "VITE_API_BASE_URL=${VITE_API_BASE_URL} (port ${FRONTEND_PORT})"
  VITE_API_BASE_URL="$VITE_API_BASE_URL" VITE_USE_MOCKS="$VITE_USE_MOCKS" \
    "${VITE_COMMAND[@]}" --host 0.0.0.0 --port "$FRONTEND_PORT" &
  PIDS+=("$!")
done

wait "${PIDS[@]}"
