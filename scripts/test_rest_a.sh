#!/usr/bin/env bash
# Sobe o Módulo A REST, faz requisições de teste e encerra o servidor.
# Uso: ./scripts/test_rest_a.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$ROOT/.venv/bin/python"
[ -x "$PY" ] || PY="python3"

cd "$ROOT/rest-version/modulo-a"

REST_A_PORT="${REST_A_PORT:-8001}" "$PY" app.py &
SRV=$!
trap 'kill "$SRV" 2>/dev/null || true' EXIT

BASE="http://localhost:${REST_A_PORT:-8001}"
# Aguarda o servidor ficar pronto (cold-start do Python em /mnt/c pode ser lento).
for _ in $(seq 1 40); do
  curl -s -o /dev/null -m 1 "$BASE/health" && break
  sleep 0.5
done

echo "== GET /health =="
curl -s "$BASE/health"; echo
echo "== GET /produto/1 =="
curl -s "$BASE/produto/1"; echo
echo "== GET /produto/999 (404) =="
curl -s -o /dev/null -w "  HTTP %{http_code}\n" "$BASE/produto/999"
echo "== GET /produtos?categoria=Eletrônicos =="
curl -s "$BASE/produtos?categoria=Eletr%C3%B4nicos"; echo
