# Exemplos gRPC — 4 tipos de comunicação (Danilo Carvalho Antunes)

Demonstração executável e autocontida dos **quatro tipos de comunicação** do gRPC,
exigidos pelo enunciado (seção B.1). Não faz parte do backend P/A/B — é material de
estudo e evidência para o relatório.

| # | Tipo | RPC | Padrão |
|---|---|---|---|
| 1 | Unary | `Unary` | 1 request → 1 response |
| 2 | Server streaming | `ServerStream` | 1 request → N responses |
| 3 | Client streaming | `ClientStream` | N requests → 1 response |
| 4 | Bidirectional streaming | `BidiStream` | N requests ↔ N responses |

Contrato: [`demo.proto`](demo.proto).

## Executar

```bash
# a partir da raiz do repositório
./scripts/test_demo.sh
```

O script gera os stubs, sobe `servidor_demo.py` e roda `cliente_demo.py`.

### Saída esperada

```text
== 1) UNARY ==
  resposta: recebi: ola
== 2) SERVER STREAMING ==
  recebido: item #1
  recebido: item #2
  recebido: item #3
== 3) CLIENT STREAMING ==
  total=3 | concat='alpha | beta | gama'
== 4) BIDIRECTIONAL STREAMING ==
  recebido: eco[alpha]
  recebido: eco[beta]
  recebido: eco[gama]
```

## Quando usar cada tipo

- **Unary:** consultas/comandos simples (buscar um registro).
- **Server streaming:** listagens, feeds, exportação, progresso de tarefa.
- **Client streaming:** upload em partes, ingestão de telemetria, agregação.
- **Bidirecional:** chat, jogos em tempo real, sincronização contínua.
