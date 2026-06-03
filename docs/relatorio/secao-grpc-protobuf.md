# Relatório — Seção: Framework gRPC (Danilo Carvalho Antunes)

> Rascunho da seção sob responsabilidade do Danilo Carvalho Antunes. Será integrado ao relatório final
> (estrutura completa em [`../PLANO.md`](../PLANO.md), Etapa 9).

## 3. Framework gRPC

### 3.1 Visão geral

O gRPC é um framework de RPC de alto desempenho baseado em **Protocol Buffers** (serialização
binária) e **HTTP/2** (transporte). No projeto, ele é o mecanismo de comunicação do backend
entre o Módulo P (gateway) e os microserviços A e B.

### 3.2 Protocol Buffers

Os contratos do projeto estão em `proto/`:

- `produto.proto` — `ProdutoService` (Módulo A);
- `avaliacao.proto` — `AvaliacaoService` (Módulo B).

Cada mensagem define campos com tags numéricas que identificam os dados no payload binário.
Os stubs Python são gerados com `grpc_tools.protoc` (ver `scripts/gen_protos.sh`).

> _[Inserir trecho final do produto.proto e screenshot da geração de stubs.]_

### 3.3 HTTP/2

Discutir multiplexação, streams, HPACK e comunicação binária; comparar com HTTP/1.1.
_[Conteúdo detalhado pelo Aluno 2 — integrar aqui.]_

### 3.4 Tipos de comunicação e testes

| Tipo | RPC | Status no projeto | Evidência |
|---|---|---|---|
| Unary | `BuscarProduto` | Implementado e testado | saída de `scripts/test_a.sh` |
| Server streaming | `ListarProdutos` | Implementado e testado | saída de `scripts/test_a.sh` |
| Client streaming | exemplo documentado | Documentado | `docs/grpc-protobuf.md` §4.3 |
| Bidirecional | exemplo documentado | Documentado | `docs/grpc-protobuf.md` §4.4 |

**Teste executado (unary + server streaming) — Módulo A:**

```text
== Unary: BuscarProduto(id=1) ==
  -> Notebook Ultra | Eletrônicos | R$ 3500.00 | disp=True
== Unary: BuscarProduto(id=999) deve dar NOT_FOUND ==
  -> NOT_FOUND: Produto com id=999 não encontrado
== Server streaming: ListarProdutos(categoria='Eletrônicos') ==
  -> #1 Notebook Ultra (R$ 3500.00)
  -> #2 Mouse Gamer (R$ 150.00)
  -> #4 Monitor 27" (R$ 1200.00)
  -> #6 Teclado Mecânico (R$ 320.00)
```

### 3.5 Conclusão dos tipos de comunicação

- **Unary:** ideal para consultas pontuais (ex.: buscar um produto por id).
- **Server streaming:** ideal para listagens/feeds (ex.: listar produtos por categoria).
- **Client streaming:** ideal para ingestão/upload incremental de dados.
- **Bidirecional:** ideal para interação contínua em tempo real (chat, sincronização).

> _[Fechar com parágrafo conclusivo após os testes de desempenho da Etapa 6.]_
