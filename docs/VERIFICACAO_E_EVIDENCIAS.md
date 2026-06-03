# Verificação e Evidências — Entregas do Danilo Carvalho Antunes

> Documento de rastreabilidade: liga cada requisito do enunciado e do `PLANO.md`
> às entregas implementadas e às **evidências de execução** (saídas reais de teste).
> Ambiente: WSL2 Ubuntu 24.04, Python 3.12.3, `grpcio` 1.64.1.

## 1. Rastreabilidade — requisito → entrega → status

| Origem | Requisito (Danilo Carvalho Antunes) | Entrega | Status |
|---|---|---|---|
| PLANO Etapa 1 | Estudar gRPC; documentar funcionamento | `docs/grpc-protobuf.md` | OK |
| PLANO Etapa 1 | Exemplos de unary e server streaming | Módulo A + `exemplos-grpc/` | OK |
| Enunciado B.1 | Demonstrar os 4 tipos de comunicação | `exemplos-grpc/` (executável) | OK |
| PLANO Etapa 3 | Contrato `.proto` do serviço A | `proto/produto.proto` | OK |
| PLANO Etapa 4 | Implementar microserviço A (gRPC) + testes | `modulo-a/server.py`, `client_test.py` | OK |
| PLANO Etapa 5 | Versão REST do serviço A | `rest-version/modulo-a/` | OK |
| PLANO Etapa 7 | Dockerfile do módulo A | `modulo-a/Dockerfile` | OK (build a validar pelo Aluno 4) |
| PLANO Etapa 8 | Manifests K8s do módulo A | `k8s/a-deployment.yaml`, `k8s/a-service.yaml` | OK (deploy a validar pelo Aluno 4) |
| PLANO Etapa 9 | Seção de relatório gRPC/ProtoBuf | `docs/relatorio/secao-grpc-protobuf.md` | Rascunho |
| PLANO Etapa 10 | Slides gRPC/ProtoBuf/HTTP/2 | `docs/slides/slides-grpc.md` | Rascunho |

## 2. Conformidade com as regras do professor

| Regra | Situação |
|---|---|
| A e B em linguagem distinta de P | **OK** — A/B em Python, P em Node.js |
| A e B diferentes entre si (funcionalidade) | **OK** — A: dados básicos; B: avaliação/entrega |
| P expõe interface web/REST ao cliente | Responsabilidade do Aluno 3 (Módulo P) |
| Backend colaborativo (P consulta A e B) | Contratos prontos em `proto/`; integração no Módulo P |

## 3. Como reproduzir as verificações

```bash
# 1. Ambiente (uma vez)
python3 -m venv .venv
./.venv/bin/python -m pip install -r modulo-a/requirements.txt

# 2. Gerar stubs
./scripts/gen_protos.sh

# 3. Testes
./scripts/test_a.sh        # Módulo A gRPC (unary + server streaming)
./scripts/test_rest_a.sh   # Módulo A REST
./scripts/test_demo.sh     # 4 tipos de comunicação gRPC
```

## 4. Evidências capturadas

### 4.1 Geração de stubs (`protoc`)

```text
>> Gerando stubs do Módulo A (produto.proto) em modulo-a/
>> Gerando stubs do Módulo B (avaliacao.proto) em modulo-b/
>> Stubs gerados com sucesso.
```

### 4.2 Módulo A gRPC — unary + server streaming (`scripts/test_a.sh`)

```text
[Modulo A] ProdutoService gRPC ouvindo em 0.0.0.0:50051
== Unary: BuscarProduto(id=1) ==
  -> Notebook Ultra | Eletrônicos | R$ 3500.00 | disp=True
== Unary: BuscarProduto(id=999) deve dar NOT_FOUND ==
  -> NOT_FOUND: Produto com id=999 não encontrado
== Server streaming: ListarProdutos(categoria='Eletrônicos') ==
  -> #1 Notebook Ultra (R$ 3500.00)
  -> #2 Mouse Gamer (R$ 150.00)
  -> #4 Monitor 27" (R$ 1200.00)
  -> #6 Teclado Mecânico (R$ 320.00)
OK: testes do Módulo A concluídos.
```

### 4.3 Módulo A REST (`scripts/test_rest_a.sh`)

```text
== GET /health ==
{"status": "ok", "modulo": "A", "tipo": "rest"}
== GET /produto/1 ==
{"id": 1, "nome": "Notebook Ultra", "categoria": "Eletrônicos", "preco": 3500.0, "disponivel": true}
== GET /produto/999 (404) ==
  HTTP 404
== GET /produtos?categoria=Eletrônicos ==
[{"id": 1, ...}, {"id": 2, ...}, {"id": 4, ...}, {"id": 6, ...}]
```

### 4.4 Quatro tipos de comunicação (`scripts/test_demo.sh`)

```text
== 1) UNARY ==
  resposta: recebi: ola
== 2) SERVER STREAMING ==
  recebido: item #1 / item #2 / item #3
== 3) CLIENT STREAMING ==
  total=3 | concat='alpha | beta | gama'
== 4) BIDIRECTIONAL STREAMING ==
  recebido: eco[alpha] / eco[beta] / eco[gama]
```

## 5. Equivalência gRPC × REST (base para a comparação de desempenho)

As duas versões do Módulo A retornam **os mesmos dados** para a mesma consulta,
o que valida a comparação justa exigida na Etapa 6:

| Consulta | gRPC (`BuscarProduto`/`ListarProdutos`) | REST (`/produto`/`/produtos`) |
|---|---|---|
| `id=1` | Notebook Ultra, R$ 3500.00 | `{"id":1,"nome":"Notebook Ultra","preco":3500.0,...}` |
| `categoria=Eletrônicos` | #1, #2, #4, #6 | ids 1, 2, 4, 6 |

> A medição de tempo de resposta (tabela da Etapa 6) será feita pelo Aluno 3, usando
> estas duas versões equivalentes do serviço A (e as do B).

## 6. Decisões de projeto registradas

- **`produto.proto` estendido:** além do `BuscarProduto` (unary) previsto no PLANO,
  adicionei `ListarProdutos` (server streaming) para cumprir o requisito de exemplos
  de unary **e** server streaming do Danilo Carvalho Antunes, mantendo compatibilidade com o contrato original.
- **Portas padronizadas:** A gRPC `50051`, A REST `8001`, B gRPC `50052`, B REST `8002`, P `8080`
  (configuráveis por variáveis de ambiente — facilita Docker/K8s).
- **Stubs não versionados:** `*_pb2*.py` são gerados por `scripts/gen_protos.sh` (ver `.gitignore`).
- **Fim de linha LF:** `.gitattributes` força LF para scripts/código (projeto roda em Linux).

## 7. Pendências que dependem de outros (destravadas)

- **Build/deploy** do Dockerfile e dos manifests K8s: requer Docker + minikube (Aluno 4).
- **Integração P↔A↔B:** contratos prontos; implementação do P em Node.js (Aluno 3).
- **Módulo B:** contrato `proto/avaliacao.proto` pronto; implementação (Aluno 2).
