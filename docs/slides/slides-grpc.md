---
marp: true
title: gRPC, ProtoBuf e HTTP/2 — PSPD P1
paginate: true
---

# gRPC, Protocol Buffers e HTTP/2
## Projeto PSPD P1 — Danilo Carvalho Antunes

Sistema Distribuído de Consulta e Análise de Produtos

---

# Objetivo do trabalho

- Construir uma aplicação distribuída com **microserviços gRPC** (módulos P, A, B)
- Comparar **gRPC/ProtoBuf** x **REST/JSON**
- Implantar com **Docker + Kubernetes (minikube)**

Status atual: **implementado e validado**.

---

# O que é gRPC

- Framework de **RPC** de alto desempenho (Google / CNCF)
- Contrato-primeiro via **Protocol Buffers** (`.proto`)
- Transporte **HTTP/2**, payload **binário**
- Geração de stubs cliente/servidor com `protoc`

---

# Protocol Buffers

```proto
service ProdutoService {
  rpc BuscarProduto(ProdutoRequest) returns (ProdutoResponse);
}
message ProdutoResponse {
  int32 id = 1; string nome = 2; double preco = 4;
}
```

- Campos identificados por **tags numéricas**
- Serialização **binária**: compacta e rápida

---

# HTTP/2 (por que o gRPC usa)

- **Multiplexação**: vários RPCs em 1 conexão TCP
- **Streams**: habilita comunicação em fluxo
- **HPACK**: cabeçalhos comprimidos
- Binário (combina com o protobuf)

vs HTTP/1.1: texto, 1 requisição por vez

---

# Os 4 tipos de comunicação

| Tipo | Req | Resp |
|---|---|---|
| Unary | 1 | 1 |
| Server streaming | 1 | N |
| Client streaming | N | 1 |
| Bidirecional | N | N |

Módulo A implementa **Unary** e **Server streaming**.

Os 4 tipos foram testados em `exemplos-grpc/` via `scripts/test_demo.sh`.

---

# Demonstração — Arquitetura completa

```text
GET /produto/1      -> P consulta A e B via gRPC (ok)
GET /rest/produto/1 -> P consulta A e B via REST (ok)
```

- Validação prática concluída em Docker Compose e minikube

---

# gRPC x REST (resumo)

- gRPC: binário, HTTP/2, contrato forte, streaming nativo
- REST/JSON: texto, HTTP/1.1, flexível, nativo no browser
- Resultado (100 req): gRPC **4,36 ms** vs REST **4,92 ms**
- RPS (100 req): gRPC **229,11** vs REST **203,08**

Conclusão: em carga sustentada, gRPC teve melhor eficiência.

---

# Conclusão

- gRPC + ProtoBuf + HTTP/2 = comunicação eficiente entre microserviços
- Cada tipo de RPC tem seu caso de uso
- Projeto funcional com P↔A↔B em gRPC e REST
- Kubernetes/minikube validado no ambiente local com 5 pods (A, B, P, REST-A, REST-B)
