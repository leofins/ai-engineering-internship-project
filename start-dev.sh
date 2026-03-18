#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

export NODE_ENV="${NODE_ENV:-development}"
export OAUTH_SERVER_URL="${OAUTH_SERVER_URL:-http://localhost:3000}"
export PYTHON_API_URL="${PYTHON_API_URL:-http://127.0.0.1:8000}"

if ! command -v pnpm >/dev/null 2>&1; then
  if command -v corepack >/dev/null 2>&1; then
    corepack enable >/dev/null 2>&1 || true
  fi
fi

if ! command -v pnpm >/dev/null 2>&1; then
  echo "[erro] pnpm nao encontrado. Instale Node 22+ e habilite corepack/pnpm."
  exit 1
fi

if [ -x "$ROOT_DIR/backend/.venv/bin/python" ]; then
  PYTHON_BIN="$ROOT_DIR/backend/.venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
else
  echo "[erro] Python nao encontrado. Instale Python 3.11+ ou crie backend/.venv."
  exit 1
fi

cleanup() {
  echo ""
  echo "Encerrando servicos..."
  kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
}
trap cleanup INT TERM EXIT

(
  cd "$ROOT_DIR/backend"
  "$PYTHON_BIN" -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
) &
BACKEND_PID=$!

(
  cd "$ROOT_DIR"
  pnpm exec tsx watch server/_core/index.ts
) &
FRONTEND_PID=$!

sleep 2

echo "Servicos iniciados:"
echo "  Backend : http://localhost:8000/health"
echo "  Frontend: http://localhost:3000"

if command -v open >/dev/null 2>&1; then
  open "http://localhost:3000" >/dev/null 2>&1 || true
fi

# Removido -n para compatibilidade com macOS (bash 3.2)
# wait -n "$BACKEND_PID" "$FRONTEND_PID"
wait "$BACKEND_PID" "$FRONTEND_PID"
echo "Um dos servicos finalizou. Parando o restante..."
kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
wait || true
