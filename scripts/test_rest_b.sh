#!/usr/bin/env bash
# Sobe o Módulo B REST, faz requisições de teste e encerra o servidor.
# Uso: ./scripts/test_rest_b.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$ROOT/.venv/bin/python"
[ -x "$PY" ] || PY="python3"

cd "$ROOT/rest-version/modulo-b"

REST_B_PORT="${REST_B_PORT:-8002}" "$PY" app.py &
SRV=$!
trap 'kill "$SRV" 2>/dev/null || true' EXIT
sleep 1

BASE="http://localhost:${REST_B_PORT:-8002}"
echo "== GET /health =="
curl -s "$BASE/health"; echo
echo "== GET /avaliacao/1 =="
curl -s "$BASE/avaliacao/1"; echo
echo "== GET /avaliacao/999 (404) =="
curl -s -o /dev/null -w "  HTTP %{http_code}\n" "$BASE/avaliacao/999"
echo "== GET /avaliacoes?ids=1,3,6 =="
curl -s "$BASE/avaliacoes?ids=1,3,6"; echo
