# Módulo A — Serviço de Produtos (Danilo Carvalho Antunes)

Microserviço responsável pelos **dados básicos do produto** (nome, categoria, preço, disponibilidade).
Implementa o `ProdutoService` definido em [`proto/produto.proto`](../proto/produto.proto).

| Item | Valor |
|---|---|
| Linguagem | Python 3.12 |
| RPC unary | `BuscarProduto(ProdutoRequest) -> ProdutoResponse` |
| RPC server streaming | `ListarProdutos(ListarProdutosRequest) -> stream ProdutoResponse` |
| Porta gRPC | `50051` (env `GRPC_A_PORT`) |
| Versão REST | [`../rest-version/modulo-a/`](../rest-version/modulo-a/) (porta `8001`) |

## Pré-requisitos

```bash
# a partir da raiz do repositório
python3 -m venv .venv
./.venv/bin/python -m pip install -r modulo-a/requirements.txt
```

## Gerar os stubs gRPC

```bash
./scripts/gen_protos.sh
# gera modulo-a/produto_pb2.py e modulo-a/produto_pb2_grpc.py (não versionados)
```

## Executar

```bash
# Servidor gRPC
cd modulo-a && ../.venv/bin/python server.py

# Em outro terminal: cliente de teste (unary + server streaming)
cd modulo-a && ../.venv/bin/python client_test.py
```

Ou tudo de uma vez:

```bash
./scripts/test_a.sh
```

### Saída esperada

```text
[Modulo A] ProdutoService gRPC ouvindo em 0.0.0.0:50051
== Unary: BuscarProduto(id=1) ==
  -> Notebook Ultra | Eletrônicos | R$ 3500.00 | disp=True
== Unary: BuscarProduto(id=999) deve dar NOT_FOUND ==
  -> NOT_FOUND: Produto com id=999 não encontrado
== Server streaming: ListarProdutos(categoria='Eletrônicos') ==
  -> #1 Notebook Ultra (R$ 3500.00)
  ...
```

## Versão REST (para comparação de desempenho)

```bash
./scripts/test_rest_a.sh
# ou: cd rest-version/modulo-a && ../../.venv/bin/python app.py
```

| Método | Rota | Equivalente gRPC |
|---|---|---|
| GET | `/produto/<id>` | `BuscarProduto` |
| GET | `/produtos?categoria=&limite=` | `ListarProdutos` |
| GET | `/health` | — |

## Docker

```bash
# build a partir da RAIZ do repositório (precisa do proto/)
docker build -t modulo-a:latest -f modulo-a/Dockerfile .
docker run --rm -p 50051:50051 modulo-a:latest
```

## Kubernetes

Manifests em [`../k8s/a-deployment.yaml`](../k8s/a-deployment.yaml) e [`../k8s/a-service.yaml`](../k8s/a-service.yaml).
O `a-service` é `ClusterIP` (acessado internamente pelo Módulo P).
