#!/usr/bin/env bash
# Roda TODOS os testes do que ja foi implementado (Modulo A gRPC + REST + demo dos 4 tipos).
# Pre-requisito: ./scripts/setup.sh executado antes.
# Uso (a partir da raiz do repositorio): ./scripts/test_all.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [ ! -x ".venv/bin/python" ]; then
  echo "ERRO: ambiente nao preparado. Rode primeiro: ./scripts/setup.sh"
  exit 1
fi

echo "########################################"
echo "# 1) MODULO A - gRPC (unary + streaming)"
echo "########################################"
./scripts/test_a.sh

echo
echo "########################################"
echo "# 2) MODULO A - REST/JSON"
echo "########################################"
./scripts/test_rest_a.sh

echo
echo "########################################"
echo "# 3) MODULO B - gRPC (unary + streaming)"
echo "########################################"
./scripts/test_b.sh

echo
echo "########################################"
echo "# 4) MODULO B - REST/JSON"
echo "########################################"
./scripts/test_rest_b.sh

echo
echo "########################################"
echo "# 5) DEMO - 4 tipos de comunicacao gRPC"
echo "########################################"
./scripts/test_demo.sh

echo
echo ">> TODOS OS TESTES CONCLUIDOS COM SUCESSO."
