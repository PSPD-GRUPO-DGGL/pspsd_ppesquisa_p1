#!/usr/bin/env bash
# Gera os stubs Python a partir dos arquivos .proto.
# Uso: ./scripts/gen_protos.sh   (executar a partir da raiz do repositório)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROTO_DIR="$ROOT/proto"

# Usa o python do venv se existir, senão o python3 do sistema.
PY="$ROOT/.venv/bin/python"
[ -x "$PY" ] || PY="python3"

echo ">> Gerando stubs do Módulo A (produto.proto) em modulo-a/"
"$PY" -m grpc_tools.protoc \
  -I "$PROTO_DIR" \
  --python_out="$ROOT/modulo-a" \
  --grpc_python_out="$ROOT/modulo-a" \
  "$PROTO_DIR/produto.proto"

echo ">> Gerando stubs do Módulo B (avaliacao.proto) em modulo-b/"
"$PY" -m grpc_tools.protoc \
  -I "$PROTO_DIR" \
  --python_out="$ROOT/modulo-b" \
  --grpc_python_out="$ROOT/modulo-b" \
  "$PROTO_DIR/avaliacao.proto"

echo ">> Stubs gerados com sucesso."
