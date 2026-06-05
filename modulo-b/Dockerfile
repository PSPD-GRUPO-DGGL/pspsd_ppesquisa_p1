# Dockerfile do Módulo B (gRPC) — Python
# IMPORTANTE: o build deve usar a RAIZ do repositório como contexto, pois
# precisamos do arquivo proto/avaliacao.proto:
#   docker build -t modulo-b:latest -f modulo-b/Dockerfile .
FROM python:3.12-slim

WORKDIR /app

# Dependências
COPY modulo-b/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Contrato proto + código do módulo
COPY proto/avaliacao.proto ./proto/avaliacao.proto
COPY modulo-b/server.py modulo-b/dados.py modulo-b/client_test.py ./

# Gera os stubs gRPC dentro da imagem
RUN python -m grpc_tools.protoc -I proto \
    --python_out=. --grpc_python_out=. proto/avaliacao.proto

ENV GRPC_B_PORT=50052
EXPOSE 50052

CMD ["python", "server.py"]
