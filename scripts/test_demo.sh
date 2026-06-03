#!/usr/bin/env bash
# Gera os stubs do demo, sobe o servidor, roda o cliente (4 tipos) e encerra.
# Uso: ./scripts/test_demo.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$ROOT/.venv/bin/python"
[ -x "$PY" ] || PY="python3"
DEMO="$ROOT/exemplos-grpc"

echo ">> Gerando stubs do demo"
"$PY" -m grpc_tools.protoc -I "$DEMO" \
  --python_out="$DEMO" --grpc_python_out="$DEMO" "$DEMO/demo.proto"

cd "$DEMO"
"$PY" servidor_demo.py &
SRV=$!
trap 'kill "$SRV" 2>/dev/null || true' EXIT
sleep 2
"$PY" cliente_demo.py
