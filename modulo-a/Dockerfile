# Dockerfile do Módulo A (gRPC) — Python
# IMPORTANTE: o build deve usar a RAIZ do repositório como contexto, pois
# precisamos do arquivo proto/produto.proto:
#   docker build -t modulo-a:latest -f modulo-a/Dockerfile .
FROM python:3.12-slim

WORKDIR /app

# Dependências
COPY modulo-a/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Contrato proto + código do módulo
COPY proto/produto.proto ./proto/produto.proto
COPY modulo-a/*.py ./

# Gera os stubs gRPC dentro da imagem
RUN python -m grpc_tools.protoc -I proto \
    --python_out=. --grpc_python_out=. proto/produto.proto

ENV GRPC_A_PORT=50051
EXPOSE 50051

CMD ["python", "server.py"]
