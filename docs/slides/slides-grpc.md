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

---

# Demonstração — Módulo A

```text
Unary  BuscarProduto(1)  -> Notebook Ultra, R$ 3500.00
Stream ListarProdutos(Eletrônicos) -> #1 #2 #4 #6
```

- `scripts/test_a.sh` sobe o servidor e roda o cliente

---

# gRPC x REST (resumo)

- gRPC: binário, HTTP/2, contrato forte, streaming nativo
- REST/JSON: texto, HTTP/1.1, flexível, nativo no browser
- Comparação de tempo de resposta: Etapa 6

---

# Conclusão

- gRPC + ProtoBuf + HTTP/2 = comunicação eficiente entre microserviços
- Cada tipo de RPC tem seu caso de uso
- Próximos passos: integração P↔A↔B e testes de desempenho
