# gRPC, Protocol Buffers e HTTP/2 — Estudo (Danilo Carvalho Antunes)

> Material de estudo e referência do projeto. Base: <https://grpc.io/>.

## 1. O que é gRPC

gRPC (gRPC Remote Procedure Calls) é um framework de **chamada de procedimento remoto**
de alto desempenho, criado pela Google e mantido pela CNCF. Ele permite que uma aplicação
chame métodos de um serviço em outra máquina como se fossem locais.

Pilares do gRPC:

- **Contrato primeiro (IDL):** o serviço é definido em um arquivo `.proto` (Protocol Buffers).
- **Geração de código:** o compilador `protoc` gera stubs de cliente e servidor em várias linguagens.
- **Transporte HTTP/2:** multiplexação, streaming e cabeçalhos comprimidos.
- **Serialização binária:** mensagens compactas e rápidas via Protocol Buffers.

## 2. Protocol Buffers (protobuf)

É a linguagem de definição de interface (IDL) e o formato de serialização binária do gRPC.

```proto
syntax = "proto3";
package produto;

service ProdutoService {
  rpc BuscarProduto(ProdutoRequest) returns (ProdutoResponse);
}

message ProdutoRequest  { int32 id = 1; }
message ProdutoResponse {
  int32  id         = 1;   // o número é a TAG do campo no formato binário
  string nome       = 2;
  string categoria  = 3;
  double preco      = 4;
  bool   disponivel = 5;
}
```

Pontos importantes:

- Cada campo tem um **número (tag)** que identifica o campo no payload binário — por isso a ordem
  no código não importa, mas **mudar/renumerar tags quebra compatibilidade**.
- Tipos comuns: `int32`, `int64`, `double`, `float`, `bool`, `string`, `bytes`, `repeated` (listas), `enum`, `message` aninhada.
- A serialização binária é **menor e mais rápida** de (de)serializar do que JSON textual.

Geração de stubs Python (usada neste projeto):

```bash
python -m grpc_tools.protoc -I proto \
  --python_out=. --grpc_python_out=. proto/produto.proto
# gera: produto_pb2.py (mensagens) e produto_pb2_grpc.py (serviço/stubs)
```

## 3. HTTP/2 — por que o gRPC usa

| Recurso HTTP/2 | Benefício para o gRPC |
|---|---|
| **Multiplexação** | Vários RPCs simultâneos em **uma única conexão TCP** (sem head-of-line blocking do HTTP/1.1) |
| **Streams bidirecionais** | Permite os tipos *streaming* (server/client/bidirecional) |
| **Cabeçalhos comprimidos (HPACK)** | Menos overhead por requisição |
| **Comunicação binária** | Combina com o payload binário do protobuf |

Comparado ao HTTP/1.1 (texto, uma requisição por vez por conexão), o HTTP/2 reduz latência e
aumenta a vazão, o que é essencial para comunicação entre microserviços.

## 4. Os quatro tipos de comunicação gRPC

### 4.1 Unary call (1 request → 1 response)

O tipo mais simples, equivalente a uma chamada de função. **Implementado no Módulo A** (`BuscarProduto`).

```proto
rpc BuscarProduto(ProdutoRequest) returns (ProdutoResponse);
```
```python
# servidor
def BuscarProduto(self, request, context):
    return _to_response(dados.buscar_por_id(request.id))
# cliente
resp = stub.BuscarProduto(produto_pb2.ProdutoRequest(id=1))
```
**Quando usar:** consultas/comandos simples (buscar um registro, validar um dado).

### 4.2 Server streaming (1 request → N responses)

O cliente envia uma requisição e recebe um **fluxo** de respostas. **Implementado no Módulo A** (`ListarProdutos`).

```proto
rpc ListarProdutos(ListarProdutosRequest) returns (stream ProdutoResponse);
```
```python
# servidor
def ListarProdutos(self, request, context):
    for p in dados.listar(request.categoria, request.limite):
        yield _to_response(p)
# cliente
for item in stub.ListarProdutos(pedido):
    print(item.nome)
```
**Quando usar:** listagens grandes, resultados paginados, feeds, exportação de dados, progresso de tarefa.

### 4.3 Client streaming (N requests → 1 response)

O cliente envia um **fluxo** de mensagens e o servidor responde uma única vez (ex.: ao final).

```proto
rpc EnviarLote(stream ProdutoResponse) returns (ResumoLote);
```
```python
# servidor
def EnviarLote(self, request_iterator, context):
    total = sum(1 for _ in request_iterator)
    return ResumoLote(quantidade=total)
# cliente
resumo = stub.EnviarLote(iter_de_produtos())
```
**Quando usar:** upload de dados em partes, ingestão de telemetria, agregação de muitas entradas.

### 4.4 Bidirecional streaming (N requests ↔ N responses)

Cliente e servidor trocam fluxos independentes simultaneamente sobre a mesma conexão HTTP/2.

```proto
rpc Conversar(stream Mensagem) returns (stream Mensagem);
```
```python
# servidor
def Conversar(self, request_iterator, context):
    for msg in request_iterator:
        yield Mensagem(texto=f"eco: {msg.texto}")
```
**Quando usar:** chats, jogos em tempo real, sincronização contínua, pipelines interativos.

## 5. Resumo dos tipos

| Tipo | Request | Response | Exemplo no projeto |
|---|---|---|---|
| Unary | 1 | 1 | `BuscarProduto` (Módulo A) + `exemplos-grpc` |
| Server streaming | 1 | N | `ListarProdutos` (Módulo A) + `exemplos-grpc` |
| Client streaming | N | 1 | `exemplos-grpc` (`ClientStream`, executável) |
| Bidirecional | N | N | `exemplos-grpc` (`BidiStream`, executável) |

> Os quatro tipos têm **código executável** em [`../exemplos-grpc/`](../exemplos-grpc/) — rode `./scripts/test_demo.sh`.

## 6. gRPC/ProtoBuf x REST/JSON (visão geral)

| Critério | gRPC/ProtoBuf | REST/JSON |
|---|---|---|
| Formato | binário (compacto) | texto (legível) |
| Transporte | HTTP/2 | normalmente HTTP/1.1 |
| Contrato | `.proto` (forte, tipado) | OpenAPI/convenção (mais flexível) |
| Streaming | nativo (4 tipos) | limitado |
| Browser direto | precisa de proxy (grpc-web) | nativo |
| Performance | tende a ser maior | menor overhead de adoção |

> A comparação quantitativa (tempo de resposta) é feita na Etapa 6 com as duas versões da aplicação.

## 7. Referências

- gRPC — <https://grpc.io/docs/>
- Protocol Buffers — <https://protobuf.dev/>
- HTTP/2 (RFC 9113) — <https://httpwg.org/specs/rfc9113.html>
