#!/usr/bin/env bash
# Sobe o servidor gRPC do Módulo A, roda o cliente de teste e encerra o servidor.
# Uso: ./scripts/test_a.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$ROOT/.venv/bin/python"

cd "$ROOT/modulo-a"

"$PY" server.py &
SRV=$!
trap 'kill "$SRV" 2>/dev/null || true' EXIT

sleep 2
"$PY" client_test.py
