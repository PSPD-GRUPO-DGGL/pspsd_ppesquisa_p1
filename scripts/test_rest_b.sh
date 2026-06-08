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

BASE="http://localhost:${REST_B_PORT:-8002}"
# Aguarda o servidor ficar pronto (cold-start do Python em /mnt/c pode ser lento).
for _ in $(seq 1 40); do
  curl -s -o /dev/null -m 1 "$BASE/health" && break
  sleep 0.5
done

echo "== GET /health =="
curl -s "$BASE/health"; echo
echo "== GET /avaliacao/1 =="
curl -s "$BASE/avaliacao/1"; echo
echo "== GET /avaliacao/999 (404) =="
curl -s -o /dev/null -w "  HTTP %{http_code}\n" "$BASE/avaliacao/999"
echo "== GET /avaliacoes?ids=1,3,6 =="
curl -s "$BASE/avaliacoes?ids=1,3,6"; echo
