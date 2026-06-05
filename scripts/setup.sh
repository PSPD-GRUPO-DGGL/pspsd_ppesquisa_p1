#!/usr/bin/env bash
# Prepara o ambiente Python do projeto: cria o venv, instala dependencias e gera os stubs.
# Uso (a partir da raiz do repositorio): ./scripts/setup.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo ">> [1/3] Criando ambiente virtual em .venv"
if ! python3 -m venv .venv 2>/dev/null; then
  echo "ERRO: 'python3 -m venv' falhou."
  echo "      No Ubuntu, instale o pacote: sudo apt update && sudo apt install -y python3-venv python3-pip"
  exit 1
fi

echo ">> [2/3] Instalando dependencias (modulo-a e modulo-b)"
./.venv/bin/python -m pip install --quiet --upgrade pip
./.venv/bin/python -m pip install --quiet -r modulo-a/requirements.txt
./.venv/bin/python -m pip install --quiet -r modulo-b/requirements.txt

echo ">> [3/3] Gerando stubs gRPC"
./scripts/gen_protos.sh

echo ">> Setup concluido. Rode: ./scripts/test_all.sh"
