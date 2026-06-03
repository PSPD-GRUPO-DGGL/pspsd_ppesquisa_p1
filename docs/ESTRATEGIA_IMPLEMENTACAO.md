# Estratégia de Implementação — PSPD P1

> Documento de trabalho criado pelo **Danilo Carvalho Antunes** para organizar a execução do projeto
> e destravar o trabalho dos demais. Pode ser ajustado conforme a necessidade.

## 1. Decisões de Arquitetura (definidas)

| Item | Decisão | Motivo |
|---|---|---|
| Linguagem Módulo P | **Node.js** (Express + `@grpc/grpc-js`) | API Gateway / web; diferente de A e B (regra do professor) |
| Linguagem Módulo A | **Python** (`grpcio`) | Danilo Carvalho Antunes; melhor tooling para demonstrar tipos de comunicação |
| Linguagem Módulo B | **Python** (`grpcio`) | Acelera o grupo; A e B continuam ≠ de P (regra atendida) |
| Versão REST | mesma lógica via HTTP/JSON | Comparação de desempenho (Etapa 6) |
| Orquestração | Docker + minikube (K8s host único) | Requisito B.3 |

**Regra atendida:** os microserviços A e B (Python) usam linguagem **distinta** do gRPC Stub P (Node.js).

## 2. Ambiente (WSL2 Ubuntu 24.04)

Estado inicial: apenas `git` e `python3 3.12`. A instalar conforme as etapas:
`python3-venv` (ok via ensurepip), `grpcio`/`grpcio-tools` (pip), depois `node`, `docker`, `kubectl`, `minikube`.

> Trabalhamos no WSL local; o servidor do professor (`kiriland.unb.br`) é usado para a entrega/replicação.

## 3. Contratos gRPC

- `proto/produto.proto` — `ProdutoService` (Módulo A): `BuscarProduto` (unary) + `ListarProdutos` (server streaming).
- `proto/avaliacao.proto` — `AvaliacaoService` (Módulo B): `BuscarAvaliacao` (unary) + `ListarAvaliacoes` (server streaming).

Geração de stubs Python via `scripts/gen_protos.sh` (não versionar os `*_pb2*.py`).

## 4. Fluxo de execução local (alvo)

```text
GET /produto/1  ->  P (Node)  --gRPC-->  A (Python)  : dados básicos
                            \--gRPC-->  B (Python)  : avaliação/entrega
P consolida -> JSON ao cliente
```

## 5. O que o Danilo Carvalho Antunes já entrega nesta fase

- [x] Contratos `.proto` (A e B).
- [x] Módulo A em Python: server gRPC (unary + server streaming) com dataset de produtos.
- [x] Cliente de teste do Módulo A.
- [x] Versão REST do Módulo A.
- [x] Dockerfile + manifests K8s do Módulo A.
- [x] Documentação gRPC/ProtoBuf + exemplos dos 4 tipos de comunicação.
- [x] Esqueleto do relatório (seção gRPC/ProtoBuf) e dos slides.

## 6. Tarefas destravadas para os próximos alunos

- **Aluno 2 (Módulo B):** implementar `modulo-b/server.py` seguindo `proto/avaliacao.proto` (mesmo padrão do A). Dataset de avaliações por `id_produto`.
- **Aluno 3 (Módulo P):** implementar `modulo-p/` em Node.js consumindo A e B via gRPC; expor REST. Usar `proto/` como contrato.
- **Aluno 4 (Infra):** instalar Docker/minikube, validar build das imagens e `kubectl apply -f k8s/`.

## 7. Convenções

- Portas: A gRPC `50051`, B gRPC `50052`, A REST `8001`, B REST `8002`, P HTTP `8080`.
- Variáveis de ambiente para endereços (`GRPC_A_ADDR`, etc.) — facilita Docker/K8s.
- Toda execução documentada em formato Linux (bash).
