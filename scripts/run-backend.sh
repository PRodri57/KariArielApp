#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $(basename "$0") <host-ip> [extra-host-ip ...] [env: PORT, FRONTEND_PORT_BASE, CORS_ORIGINS]" >&2
  exit 1
}

HOST_IPS=("$@")
if [[ ${#HOST_IPS[@]} -eq 0 ]]; then
  usage
fi

PORT="${PORT:-8000}"
FRONTEND_PORT_BASE="${FRONTEND_PORT_BASE:-5173}"
DEFAULT_CORS_PARTS=(
  "http://localhost:${FRONTEND_PORT_BASE}"
  "http://127.0.0.1:${FRONTEND_PORT_BASE}"
)
for index in "${!HOST_IPS[@]}"; do
  HOST_IP="${HOST_IPS[$index]}"
  FRONTEND_PORT=$((FRONTEND_PORT_BASE + index))
  DEFAULT_CORS_PARTS+=("http://${HOST_IP}:${FRONTEND_PORT}")
done
DEFAULT_CORS="$(IFS=,; echo "${DEFAULT_CORS_PARTS[*]}")"
export CORS_ORIGINS="${CORS_ORIGINS:-$DEFAULT_CORS}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="$ROOT_DIR/.venv"
REQ_FILE="$ROOT_DIR/requirements.txt"

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  echo "Creando virtualenv en $VENV_DIR"
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
  elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
  else
    echo "Error: no se encontro python para crear el virtualenv." >&2
    exit 1
  fi
  "$PYTHON_BIN" -m venv "$VENV_DIR"
  "$VENV_DIR/bin/python" -m ensurepip --upgrade
  "$VENV_DIR/bin/python" -m pip install --upgrade pip
  if [[ -f "$REQ_FILE" ]]; then
    "$VENV_DIR/bin/python" -m pip install -r "$REQ_FILE"
  fi
else
  if ! "$VENV_DIR/bin/python" -c "import uvicorn" >/dev/null 2>&1; then
    echo "Uvicorn no encontrado en $VENV_DIR; reinstalando dependencias."
    "$VENV_DIR/bin/python" -m ensurepip --upgrade
    "$VENV_DIR/bin/python" -m pip install --upgrade pip
    if [[ -f "$REQ_FILE" ]]; then
      "$VENV_DIR/bin/python" -m pip install -r "$REQ_FILE"
    fi
  fi
fi

cd "$ROOT_DIR/Backend"

echo "Starting backend on 0.0.0.0:${PORT}"
echo "CORS_ORIGINS=${CORS_ORIGINS}"

if [[ -x "$ROOT_DIR/.venv/bin/python" ]]; then
  export VIRTUAL_ENV="$ROOT_DIR/.venv"
  export PATH="$VIRTUAL_ENV/bin:$PATH"
  exec "$VIRTUAL_ENV/bin/python" -m uvicorn App.main:app --host 0.0.0.0 --port "$PORT"
elif command -v uvicorn >/dev/null 2>&1; then
  exec uvicorn App.main:app --host 0.0.0.0 --port "$PORT"
elif command -v python >/dev/null 2>&1; then
  exec python -m uvicorn App.main:app --host 0.0.0.0 --port "$PORT"
elif command -v python3 >/dev/null 2>&1; then
  exec python3 -m uvicorn App.main:app --host 0.0.0.0 --port "$PORT"
else
  echo "Error: no se encontro uvicorn ni python en PATH." >&2
  exit 1
fi
