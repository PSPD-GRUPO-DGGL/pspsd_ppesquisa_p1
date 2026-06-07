# Projeto de Pesquisa – Parte 1
## Aplicação Distribuída com gRPC e Kubernetes

---

**Universidade de Brasília — Campus Gama (FGA)**

**Curso:** Engenharia de Software

**Disciplina:** FGA0244 — Programação para Sistemas Paralelos e Distribuídos (60h) — Turma 02 (2026.1)

**Professor:** Fernando W. Cruz

**Integrantes:**

| #   | Nome                      | Responsabilidade Principal                                              |
| --- | ------------------------- | ----------------------------------------------------------------------- |
| 1   | Danilo Carvalho Antunes   | gRPC, ProtoBuf, Módulo A (gRPC + REST), Dockerfile e manifests K8s do A |
| 2   | Gabriel Soares dos Anjos  | HTTP/2, Módulo B (gRPC + REST), Dockerfile e manifests K8s do B         |
| 3   | Guilherme Brito de Souza  | Módulo P (API Gateway em Node.js), Dockerfile, docker-compose           |
| 4   | Luiz Gustavo Lopes Campos | Docker, Kubernetes/minikube, organização geral, relatório e slides      |

---

## 1. Introdução

Este relatório documenta o desenvolvimento de uma aplicação distribuída baseada em microserviços, realizado como atividade extraclasse da disciplina PSPD. O trabalho teve dois objetivos centrais: (i) construir e experimentar uma aplicação real usando o framework gRPC com Protocol Buffers, e (ii) implantar essa aplicação em containers utilizando Kubernetes (minikube).

A aplicação desenvolvida é um **Sistema Distribuído de Consulta e Análise de Produtos**, composta por três módulos colaborativos:

- **Módulo P** (Node.js/Express): API Gateway que recebe requisições HTTP de clientes e as traduz em chamadas gRPC para os módulos A e B;
- **Módulo A** (Python): microserviço gRPC que fornece dados básicos dos produtos (nome, categoria, preço, disponibilidade);
- **Módulo B** (Python): microserviço gRPC que fornece dados complementares (avaliação, comentário, prazo de entrega).

Os módulos A e B foram implementados em Python; o Módulo P em Node.js. As linguagens são propositalmente distintas, conforme exigido na especificação. Além da versão gRPC, foi construída uma versão alternativa com REST/JSON entre os módulos, permitindo a comparação de desempenho entre as duas abordagens.

O relatório está organizado nas seguintes seções: estudo do framework gRPC (seção 2), descrição e implementação da aplicação (seção 3), comparativo de desempenho gRPC vs REST (seção 4), infraestrutura Kubernetes (seção 5) e conclusão (seção 6).

---

## 2. Framework gRPC

### 2.1 Visão Geral

O gRPC (*gRPC Remote Procedure Calls*) é um framework de chamada de procedimento remoto de alto desempenho, originalmente desenvolvido pela Google e mantido pela CNCF (Cloud Native Computing Foundation). Ele permite que um serviço chame métodos de outro serviço remoto como se fossem chamadas locais.

Os pilares do gRPC são:

- **Contrato primeiro (IDL):** o serviço é definido em um arquivo `.proto` usando Protocol Buffers;
- **Geração de código:** o compilador `protoc` gera stubs de cliente e servidor em dezenas de linguagens a partir do mesmo contrato;
- **Transporte HTTP/2:** multiplexação de streams, suporte nativo a streaming e cabeçalhos comprimidos;
- **Serialização binária:** mensagens compactas e eficientes via Protocol Buffers.

### 2.2 Protocol Buffers (protobuf)

Protocol Buffers é a linguagem de definição de interface (IDL) e o formato de serialização binária do gRPC. Um arquivo `.proto` define os serviços (conjunto de RPCs) e as mensagens (estruturas de dados).

**Exemplo — contrato do Módulo A (`proto/produto.proto`):**

```proto
syntax = "proto3";
package produto;

service ProdutoService {
  rpc BuscarProduto(ProdutoRequest)          returns (ProdutoResponse);
  rpc ListarProdutos(ListarProdutosRequest)  returns (stream ProdutoResponse);
}

message ProdutoRequest        { int32 id = 1; }
message ListarProdutosRequest { string categoria = 1; int32 limite = 2; }
message ProdutoResponse {
  int32  id         = 1;
  string nome       = 2;
  string categoria  = 3;
  double preco      = 4;
  bool   disponivel = 5;
}
```

Pontos importantes sobre o formato:
- Cada campo tem um **número (tag)** que identifica o campo no payload binário — mudar ou renumerar tags quebra a compatibilidade;
- A serialização binária é significativamente **menor e mais rápida** de (de)serializar do que JSON textual;
- O mesmo arquivo `.proto` gera código em qualquer linguagem suportada, garantindo compatibilidade automática entre Python (A e B) e Node.js (P).

**Geração dos stubs no projeto (`scripts/gen_protos.sh`):**

```bash
python -m grpc_tools.protoc -I proto \
  --python_out=modulo-a --grpc_python_out=modulo-a proto/produto.proto
# gera: produto_pb2.py (mensagens) e produto_pb2_grpc.py (serviço/stubs)
```

No Módulo P (Node.js) os arquivos `.proto` são carregados dinamicamente em runtime via `@grpc/proto-loader`, sem necessidade de geração prévia de stubs:

```javascript
const produtoPackageDef = protoLoader.loadSync(produtoProtoPath, { keepCase: true });
const produtoProto = grpc.loadPackageDefinition(produtoPackageDef);
```

### 2.3 HTTP/2 — Transporte do gRPC

O gRPC utiliza HTTP/2 como protocolo de transporte. As principais melhorias em relação ao HTTP/1.1 que tornam o gRPC eficiente são:

**Multiplexação:** no HTTP/1.1 uma conexão processa uma requisição por vez (*Head-of-Line Blocking*). No HTTP/2, múltiplos streams trafegam simultaneamente na mesma conexão TCP.

```
HTTP/1.1             HTTP/2
Req1 → Resp1         Uma conexão:
Req2 → Resp2         Req1, Req2, Req3 intercalados
Req3 → Resp3         Resp1, Resp2, Resp3 intercalados
(conexões separadas) (streams independentes)
```

**Comparativo HTTP/1.1 vs HTTP/2:**

| Característica           | HTTP/1.1 | HTTP/2           |
| ------------------------ | -------- | ---------------- |
| Formato de dados         | Texto    | Binário (frames) |
| Multiplexação            | Não      | Sim              |
| Compressão de cabeçalhos | Não      | Sim (HPACK)      |
| Conexões por cliente     | Várias   | Uma              |
| Streaming bidirecional   | Não      | Sim (nativo)     |
| Latência                 | Maior    | Menor            |
| Uso pelo gRPC            | Não      | Sim              |

### 2.4 Tipos de Comunicação gRPC

O gRPC suporta quatro tipos de comunicação, todos implementados e testados neste projeto.

#### 2.4.1 Unary Call (1 request → 1 response)

O tipo mais simples: equivalente a uma chamada de função normal. Utilizado nos RPCs `BuscarProduto` (Módulo A) e `BuscarAvaliacao` (Módulo B) — o fluxo principal da aplicação.

```proto
rpc BuscarProduto(ProdutoRequest) returns (ProdutoResponse);
```

**Quando usar:** consultas pontuais, comandos com resposta imediata.

**Saída do teste (`scripts/test_a.sh`):**
```
== Unary: BuscarProduto(id=1) ==
  -> Notebook Ultra | Eletrônicos | R$ 3500.00 | disp=True
== Unary: BuscarProduto(id=999) deve dar NOT_FOUND ==
  -> NOT_FOUND: Produto com id=999 não encontrado
```

#### 2.4.2 Server Streaming (1 request → N responses)

O cliente envia uma requisição e recebe um fluxo contínuo de respostas. Utilizado em `ListarProdutos` (Módulo A) e `ListarAvaliacoes` (Módulo B).

```proto
rpc ListarProdutos(ListarProdutosRequest) returns (stream ProdutoResponse);
```

**Quando usar:** listagens grandes, feeds, exportação de dados, progresso de tarefas longas.

**Saída do teste:**
```
== Server streaming: ListarProdutos(categoria='Eletrônicos') ==
  -> #1 Notebook Ultra (R$ 3500.00)
  -> #2 Mouse Gamer (R$ 150.00)
  -> #4 Monitor 27" (R$ 1200.00)
  -> #6 Teclado Mecânico (R$ 320.00)
```

#### 2.4.3 Client Streaming (N requests → 1 response)

O cliente envia um fluxo de mensagens e o servidor responde uma única vez ao final. Implementado no `DemoService` do diretório `exemplos-grpc/`.

```proto
rpc ClientStream(stream Echo) returns (Resumo);
```

**Quando usar:** upload em partes, ingestão de telemetria, agregação de muitas entradas.

**Saída do teste (`scripts/test_demo.sh`):**
```
== 3) CLIENT STREAMING ==
  total=3 | concat='alpha | beta | gama'
```

#### 2.4.4 Bidirecional Streaming (N requests ↔ N responses)

Cliente e servidor trocam fluxos independentes simultaneamente sobre a mesma conexão HTTP/2. Implementado no `DemoService`.

```proto
rpc BidiStream(stream Echo) returns (stream Echo);
```

**Quando usar:** chats em tempo real, jogos multiplayer, sincronização contínua, pipelines interativos.

**Saída do teste:**
```
== 4) BIDIRECTIONAL STREAMING ==
  recebido: eco[alpha]
  recebido: eco[beta]
  recebido: eco[gama]
```

### 2.5 Resumo dos Tipos

| Tipo             | Request | Response | Implementado em                                                             |
| ---------------- | ------- | -------- | --------------------------------------------------------------------------- |
| Unary            | 1       | 1        | Módulo A (`BuscarProduto`), Módulo B (`BuscarAvaliacao`), `exemplos-grpc`   |
| Server streaming | 1       | N        | Módulo A (`ListarProdutos`), Módulo B (`ListarAvaliacoes`), `exemplos-grpc` |
| Client streaming | N       | 1        | `exemplos-grpc` (`ClientStream`)                                            |
| Bidirecional     | N       | N        | `exemplos-grpc` (`BidiStream`)                                              |

> Todos os quatro tipos têm código executável em `exemplos-grpc/`. Executar: `./scripts/test_demo.sh`.

---

## 3. Aplicação Distribuída

### 3.1 Descrição da Aplicação

A aplicação implementa um **Sistema de Consulta e Análise de Produtos**. O usuário faz uma requisição HTTP ao Módulo P informando o ID do produto, e recebe uma resposta JSON consolidada com dados básicos (fornecidos pelo Módulo A) e dados de avaliação (fornecidos pelo Módulo B).

**Exemplo de resposta final:**
```json
{
  "id": 1,
  "nome": "Notebook Ultra",
  "categoria": "Eletrônicos",
  "preco": 3500.0,
  "disponivel": true,
  "nota": 4.7,
  "comentario": "Excelente desempenho e bateria duradoura.",
  "prazo_entrega": 5
}
```

### 3.2 Arquitetura

```
Cliente Web (browser / curl)
        |
        | HTTP (porta 8000)
        v
┌──────────────────────────────────┐
│         Módulo P (Node.js)       │  API Gateway — Express + gRPC Client
│         porta 8000               │
└──────────────┬───────────────────┘
               |
               | gRPC (HTTP/2 + Protocol Buffers)
         ______|______
        |             |
        v             v
┌─────────────┐  ┌─────────────┐
│  Módulo A   │  │  Módulo B   │
│  (Python)   │  │  (Python)   │
│  porta 50051│  │  porta 50052│
│ ProdutoSvc  │  │ AvaliacaoSvc│
└─────────────┘  └─────────────┘
```

**Fluxo de uma requisição gRPC:**
```
GET /produto/1
 → P recebe a requisição HTTP
 → P chama ProdutoService.BuscarProduto(id=1) em A via gRPC
 → P chama AvaliacaoService.BuscarAvaliacao(id_produto=1) em B via gRPC
 → P consolida as respostas e retorna JSON ao cliente
```

### 3.3 Implementação dos Módulos

#### Módulo A — ProdutoService (Python, gRPC :50051 | REST :8001)

Implementa dois RPCs do contrato `produto.proto`:
- `BuscarProduto` (unary): retorna dados de um produto pelo ID;
- `ListarProdutos` (server streaming): emite produtos filtráveis por categoria.

Mantém 7 produtos em memória (`modulo-a/dados.py`) simulando um banco de dados. Os stubs são gerados pelo script `scripts/gen_protos.sh`.

#### Módulo B — AvaliacaoService (Python, gRPC :50052 | REST :8002)

Implementa dois RPCs do contrato `avaliacao.proto`:
- `BuscarAvaliacao` (unary): retorna nota, comentário e prazo de entrega de um produto;
- `ListarAvaliacoes` (server streaming): emite avaliações de uma lista de IDs.

Os IDs de produto espelham os do Módulo A para que o Módulo P possa combinar as respostas.

#### Módulo P — API Gateway (Node.js, HTTP :8000)

Implementado em Node.js com Express. Não usa stubs gerados — carrega os arquivos `.proto` dinamicamente via `@grpc/proto-loader` em runtime.

Expõe três endpoints:
- `GET /` — health check;
- `GET /produto/:id` — consulta A e B via **gRPC**, retorna JSON consolidado;
- `GET /rest/produto/:id` — consulta A e B via **HTTP REST**, retorna JSON consolidado.

Os endereços dos serviços são configuráveis por variáveis de ambiente (`URL_MODULO_A`, `URL_MODULO_B`, `MODULO_A_URL`, `MODULO_B_URL`), permitindo uso local e em containers sem alteração de código.

### 3.4 Saída dos Testes de Integração

Todos os serviços foram levantados localmente e testados via `curl`:

**GET /produto/1 (via gRPC):**
```json
{
  "id": 1,
  "nome": "Notebook Ultra",
  "categoria": "Eletrônicos",
  "preco": 3500,
  "disponivel": true,
  "nota": 4.7,
  "comentario": "Excelente desempenho e bateria duradoura.",
  "prazo_entrega": 5
}
```

**GET /produto/3 (via gRPC — produto indisponível):**
```json
{
  "id": 3,
  "nome": "Cadeira Ergonômica",
  "categoria": "Móveis",
  "preco": 980.5,
  "disponivel": false,
  "nota": 3.8,
  "comentario": "Boa qualidade, mas montagem demorada.",
  "prazo_entrega": 10
}
```

**GET /rest/produto/1 (via REST):**
```json
{
  "id": 1,
  "nome": "Notebook Ultra",
  "categoria": "Eletrônicos",
  "preco": 3500,
  "disponivel": true,
  "nota": 4.7,
  "comentario": "Excelente desempenho e bateria duradoura.",
  "prazo_entrega": 5
}
```

### 3.5 Dificuldades Encontradas

- **Conversão de linguagem do Módulo P:** o módulo foi inicialmente desenvolvido em Python (FastAPI) e depois migrado para Node.js para atender ao requisito de linguagens distintas. A migração exigiu reescrever a lógica de cliente gRPC usando `@grpc/grpc-js` e `@grpc/proto-loader` (carregamento dinâmico de `.proto`, sem geração de stubs).
- **Caminho dos arquivos `.proto` nos containers:** o Dockerfile do Módulo P usa build multi-stage e copia os `.proto` para `/usr/src/proto/`, alinhado ao caminho resolvido em runtime pelo `grpcClient.js`.
- **Coordenação entre módulos:** os contratos `.proto` foram definidos antecipadamente pelo Aluno 1 para desbloquear o desenvolvimento paralelo de A, B e P.

---

## 4. Comparativo de Desempenho: gRPC/ProtoBuf vs REST/JSON

### 4.1 Versão REST Alternativa

Além da versão gRPC, foi implementada uma versão alternativa onde o Módulo P consulta A e B via HTTP/REST/JSON:

- **REST A** (`rest-version/modulo-a/app.py`, porta 8001): expõe `GET /produto/{id}`;
- **REST B** (`rest-version/modulo-b/app.py`, porta 8002): expõe `GET /avaliacao/{id}`;
- **Módulo P** (`src/restClient.js`): chama A e B via HTTP usando axios, consolidando as respostas.

A lógica de negócio é idêntica entre as versões; apenas o protocolo de comunicação entre P, A e B difere.

### 4.2 Metodologia dos Testes

- **Ambiente:** máquina local Linux (Pop!_OS 24.04), todos os serviços em `localhost`;
- **Ferramenta:** script Python com `requests` + `time.perf_counter()`;
- **Aquecimento:** 1 requisição descartada antes de cada série para estabilizar conexões;
- **Cenários:** 1, 10 e 100 requisições sequenciais para `GET /produto/1` (gRPC) e `GET /rest/produto/1` (REST);
- **Métrica:** tempo médio de resposta em milissegundos (ms) e RPS (*requests per second*).

### 4.3 Resultados

| Cenário                 | gRPC — médio (ms) | REST — médio (ms) | Δ (REST − gRPC) |
| ----------------------- | ----------------: | ----------------: | --------------: |
| 1 requisição            |              6,23 |              5,60 |        −0,62 ms |
| 10 requisições — média  |              4,91 |              4,64 |        −0,27 ms |
| 100 requisições — média |          **4,36** |          **4,92** |    **+0,56 ms** |

**Detalhes — série de 100 requisições:**

| Métrica            |   gRPC |   REST |
| ------------------ | -----: | -----: |
| Mínimo (ms)        |   2,66 |   3,05 |
| Máximo (ms)        |  14,99 |   7,30 |
| Mediana (ms)       |   4,20 |   4,75 |
| Desvio padrão (ms) |   1,27 |   0,96 |
| RPS                | 229,11 | 203,08 |

### 4.4 Análise dos Resultados

Os resultados mostram tempos muito próximos entre gRPC e REST quando executados em `localhost`, com diferença média inferior a 1 ms. Isso é esperado por três razões:

1. **Ausência de latência de rede:** em ambiente local, o overhead de rede é negligenciável; em produção (serviços em máquinas distintas), o gRPC tende a se destacar mais devido à serialização binária compacta e à multiplexação HTTP/2.

2. **Payload pequeno:** com mensagens de poucos campos, a vantagem de compressão do Protocol Buffers sobre JSON é pouco perceptível. Para payloads maiores (listas longas, campos de texto extensos), a diferença cresce.

3. **Conexão gRPC serial:** o `grpcClient.js` atual abre o canal para B *após* receber a resposta de A (chamadas sequenciais). Em uma implementação com chamadas paralelas (`Promise.all`), o gRPC seria ainda mais rápido.

**Na série de 100 requisições**, o gRPC apresentou RPS superior (229 vs 203 req/s) e mediana menor (4,20 ms vs 4,75 ms), evidenciando a maior eficiência do protocolo em carga sustentada — tendência que se acentuaria com payloads maiores ou ambiente de rede real.

**Conclusão:** para microserviços em produção com comunicação intra-cluster (como é o caso no Kubernetes), gRPC oferece melhor desempenho e contrato mais forte. REST continua sendo a melhor escolha para APIs públicas voltadas a browsers e integrações externas — exatamente o papel que o Módulo P desempenha no projeto.

---

## 5. Infraestrutura com Kubernetes (minikube)

### 5.1 Visão Geral do Kubernetes

Kubernetes (K8s) é uma plataforma de orquestração de containers que automatiza implantação, escalonamento e gerenciamento de aplicações em containers. Para este projeto usamos o **minikube**, uma versão local de host único do Kubernetes.

Conceitos utilizados:

- **Pod:** unidade mínima de execução; agrupa um ou mais containers;
- **Deployment:** gerencia os Pods (criação, reinício, escalonamento);
- **Service:** expõe um Deployment para outros Pods (ClusterIP — interno) ou para o exterior (NodePort);
- **Namespace:** isolamento lógico de recursos.

### 5.2 Distribuição dos Módulos

```
┌─────────────────── Cluster minikube ──────────────────┐
│                                                        │
│   ┌────────────────────────────────────────────┐       │
│   │  Pod P (Node.js)  ←── NodePort :8000       │       │
│   │  API Gateway                               │◄──── externo
│   └───────────┬─────────────────┬──────────────┘       │
│               │ ClusterIP       │ ClusterIP             │
│        a-service:50051   b-service:50052                │
│               │                 │                       │
│   ┌───────────▼──────┐  ┌──────▼──────────────┐        │
│   │  Pod A (Python)  │  │  Pod B (Python)      │        │
│   │  ProdutoService  │  │  AvaliacaoService    │        │
│   └──────────────────┘  └──────────────────────┘        │
└────────────────────────────────────────────────────────┘
```

Os Serviços A e B usam `ClusterIP` (apenas acessíveis internamente pelo Módulo P). O Serviço P usa `NodePort` para expor a API REST ao cliente externo.

### 5.3 Arquivos de Configuração

**`k8s/a-deployment.yaml`** — Deployment do Módulo A:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: modulo-a
spec:
  replicas: 1
  selector:
    matchLabels: { app: modulo-a }
  template:
    spec:
      containers:
        - name: modulo-a
          image: modulo-a:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 50051
          env:
            - name: GRPC_A_PORT
              value: "50051"
```

**`k8s/a-service.yaml`** — Service ClusterIP do Módulo A:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: a-service
spec:
  type: ClusterIP
  selector: { app: modulo-a }
  ports:
    - name: grpc
      port: 50051
      targetPort: 50051
```

Os arquivos para o Módulo B seguem a mesma estrutura, com porta 50052 e nome `b-service`.

**`k8s/p-deployment.yaml`** — Deployment do Módulo P:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: modulo-p
spec:
  replicas: 1
  selector:
    matchLabels: { app: modulo-p }
  template:
    spec:
      containers:
        - name: modulo-p
          image: modulo-p:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8000
          env:
            - name: PORT
              value: "8000"
            - name: URL_MODULO_A
              value: "a-service:50051"
            - name: URL_MODULO_B
              value: "b-service:50052"
```

**`k8s/p-service.yaml`** — Service NodePort do Módulo P:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: p-service
spec:
  type: NodePort
  selector: { app: modulo-p }
  ports:
    - name: http
      port: 8000
      targetPort: 8000
      nodePort: 30080
```

O `p-deployment.yaml` usa `URL_MODULO_A` e `URL_MODULO_B` com os nomes dos Services K8s (`a-service:50051`, `b-service:50052`), garantindo que o Módulo P encontre A e B dentro do cluster sem alterar o código.

### 5.4 Passos para Implantação no minikube

```bash
# 1. Iniciar o minikube
minikube start

# 2. Apontar o Docker para o daemon do minikube (build local)
eval $(minikube docker-env)

# 3. Construir as imagens dentro do minikube
docker build -t modulo-a:latest -f modulo-a/Dockerfile .
docker build -t modulo-b:latest -f modulo-b/Dockerfile .
docker build -t modulo-p:latest -f modulo-p/Dockerfile .

# 4. Aplicar os manifests
kubectl apply -f k8s/

# 5. Verificar os pods
kubectl get pods
kubectl get services

# 6. Acessar o serviço P (abre no browser ou retorna URL)
minikube service p-service

# 7. Ver logs de um pod
kubectl logs <nome-do-pod>
```

### 5.5 Comandos Úteis

| Comando                         | Finalidade                         |
| ------------------------------- | ---------------------------------- |
| `kubectl get pods`              | Lista todos os pods e seus estados |
| `kubectl get services`          | Lista os serviços e suas portas    |
| `kubectl describe pod <nome>`   | Detalhes e eventos de um pod       |
| `kubectl logs <nome>`           | Logs do container                  |
| `kubectl exec -it <nome> -- sh` | Shell interativo no container      |
| `minikube dashboard`            | Interface web do cluster           |
| `minikube stop`                 | Para o cluster                     |

### 5.6 Dificuldades Encontradas

- **Imagens locais no minikube:** por padrão o Kubernetes tenta baixar imagens de registries externos. A solução foi executar `eval $(minikube docker-env)` para apontar o Docker local ao daemon do minikube antes do build, combinado com `imagePullPolicy: IfNotPresent`.
- **Comunicação intra-cluster:** os endereços `localhost:50051/50052` usados no desenvolvimento local não funcionam em K8s. A solução foi utilizar os nomes dos Services (`a-service:50051`, `b-service:50052`) configurados via variáveis de ambiente no Deployment do Módulo P.
- **Nomenclatura de variáveis de ambiente (REST via Docker Compose):** o `docker-compose.yml` passa `URL_REST_A`/`URL_REST_B` para o Módulo P, mas o `restClient.js` lê `MODULO_A_URL`/`MODULO_B_URL`. No ambiente Docker, a rota `GET /rest/produto/:id` usa os defaults `localhost:8001/8002` internamente ao container. O caminho gRPC (`GET /produto/:id`) não é afetado. Para execução local (sem container), ambas as rotas funcionam normalmente.

---

## 6. Conclusão

### 6.1 Conclusão Geral

Este projeto demonstrou na prática os benefícios e os desafios de sistemas distribuídos baseados em microserviços. O gRPC mostrou-se uma tecnologia madura e eficiente para comunicação intra-serviço: o contrato `.proto` garantiu interoperabilidade automática entre Python e Node.js sem qualquer adaptação manual, e o suporte nativo a streaming permitiu implementar os quatro tipos de comunicação com código limpo e direto.

A comparação com REST/JSON mostrou que, em ambiente local, as diferenças de desempenho são pequenas — ambas as versões responderam em torno de 4-5 ms. Em cenários reais (rede com latência, payloads maiores), a serialização binária e a multiplexação HTTP/2 do gRPC tendem a ampliar essa vantagem. A manutenção de uma versão REST alternativa também demonstrou que as duas abordagens podem coexistir no mesmo gateway (Módulo P), cada uma com seu papel: gRPC para comunicação interna eficiente, REST para a API pública voltada ao browser.

O Kubernetes trouxe a experiência de implantar e gerenciar a aplicação em containers isolados, tornando cada módulo independente e substituível — essência da arquitetura de microserviços.

### 6.2 Aprendizados Individuais

**Danilo Carvalho Antunes:**
> [Preencher depois]
> Nota de autoavaliação: [X/10]

**[Aluno 2]:**
> [Preencher depois]
> Nota de autoavaliação: [X/10]

**[Aluno 3]:**
> [Preencher depois]
> Nota de autoavaliação: [X/10]

**Luiz Gustavo Lopes Campos:**
Desafios de Desenvolvimento Encontrados e Soluções
  - Suporte à Virtualização: Identifiquei incompatibilidade inicial no Docker Desktop no Windows devido ao 
    suporte de virtualização estar desativado na placa-mãe (BIOS). 
    A correção envolveu a ativação do modo SVM/VT-x e instalação do subsistema WSL 2.
  - Disponibilidade de Imagens no Minikube: Como as imagens criadas do projeto eram locais, 
    o Kubernetes acusava falha de download. A solução adotada foi chavear o shell do terminal do Windows 
    com as variáveis do daemon interno do Minikube via link 'minikube docker-env', construindo os artefatos 
    direto no registro local.
> Nota de autoavaliação: [8/10]

---

## Apêndice A — Arquivos Proto Completos

**`proto/produto.proto`:**
```proto
syntax = "proto3";
package produto;

service ProdutoService {
  rpc BuscarProduto(ProdutoRequest)         returns (ProdutoResponse);
  rpc ListarProdutos(ListarProdutosRequest) returns (stream ProdutoResponse);
}

message ProdutoRequest        { int32 id = 1; }
message ListarProdutosRequest { string categoria = 1; int32 limite = 2; }
message ProdutoResponse {
  int32  id         = 1;
  string nome       = 2;
  string categoria  = 3;
  double preco      = 4;
  bool   disponivel = 5;
}
```

**`proto/avaliacao.proto`:**
```proto
syntax = "proto3";
package avaliacao;

service AvaliacaoService {
  rpc BuscarAvaliacao(AvaliacaoRequest)       returns (AvaliacaoResponse);
  rpc ListarAvaliacoes(ListarAvaliacoesRequest) returns (stream AvaliacaoResponse);
}

message AvaliacaoRequest         { int32 id_produto = 1; }
message ListarAvaliacoesRequest  { repeated int32 ids_produto = 1; }
message AvaliacaoResponse {
  int32  id_produto    = 1;
  double nota          = 2;
  string comentario    = 3;
  int32  prazo_entrega = 4;
}
```

---

## Apêndice B — Instruções de Execução

### Pré-requisitos

- Python 3.12+ e `python3-venv`
- Node.js 20+
- Docker e docker-compose (para execução em containers)
- minikube e kubectl (para execução em Kubernetes)

### Execução Local (sem containers)

```bash
# 1. Preparar ambiente Python
./scripts/setup.sh

# 2. Instalar dependências do Módulo P (Node.js)
cd modulo-p && npm install && cd ..

# 3. Terminal 1 — Módulo A (gRPC :50051)
cd modulo-a && ../.venv/bin/python server.py

# 4. Terminal 2 — Módulo B (gRPC :50052)
cd modulo-b && ../.venv/bin/python server.py

# 5. Terminal 3 — REST A (:8001)
cd modulo-a && ../.venv/bin/uvicorn rest_server:app --host 0.0.0.0 --port 8001

# 6. Terminal 4 — REST B (:8002)
cd modulo-b && ../.venv/bin/uvicorn rest_server:app --host 0.0.0.0 --port 8002

# 7. Terminal 5 — Módulo P (:3000)
cd modulo-p && PORT=3000 node src/app.js

# 8. Testar
curl http://localhost:3000/produto/1        # via gRPC
curl http://localhost:3000/rest/produto/1   # via REST
```

### Testes Automatizados dos Módulos

```bash
./scripts/test_all.sh       # A gRPC + REST, B gRPC + REST, demo 4 tipos
./scripts/test_a.sh         # Apenas Módulo A (gRPC)
./scripts/test_rest_a.sh    # Apenas Módulo A (REST)
./scripts/test_b.sh         # Apenas Módulo B (gRPC)
./scripts/test_rest_b.sh    # Apenas Módulo B (REST)
./scripts/test_demo.sh      # Demo dos 4 tipos de comunicação gRPC
```

### Execução com Docker Compose

```bash
# Build e subida de todos os serviços
docker compose up --build

# Testar (P na porta 8000)
curl http://localhost:8000/produto/1
curl http://localhost:8000/rest/produto/1

# Encerrar
docker compose down
```

### Execução no Kubernetes (minikube)

```bash
minikube start
eval $(minikube docker-env)

docker build -t modulo-a:latest -f modulo-a/Dockerfile .
docker build -t modulo-b:latest -f modulo-b/Dockerfile .
docker build -t modulo-p:latest -f modulo-p/Dockerfile .

kubectl apply -f k8s/
kubectl get pods
kubectl get services
minikube service p-service
```

---

## Apêndice C — Estrutura do Repositório

```
pspsd_ppesquisa_p1/
├── proto/                    ← Contratos gRPC (.proto)
│   ├── produto.proto
│   └── avaliacao.proto
│
├── modulo-a/                 ← Microserviço A (Python)
│   ├── server.py             ← gRPC server
│   ├── rest_server.py        ← REST server (FastAPI)
│   ├── dados.py              ← dados em memória
│   ├── client_test.py        ← cliente de teste
│   ├── requirements.txt
│   └── Dockerfile
│
├── modulo-b/                 ← Microserviço B (Python)
│   ├── server.py
│   ├── rest_server.py
│   ├── dados.py
│   ├── client_test.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── modulo-p/                 ← API Gateway (Node.js)
│   ├── src/
│   │   ├── app.js            ← Express server
│   │   ├── grpcClient.js     ← cliente gRPC (A e B)
│   │   └── restClient.js     ← cliente REST (A e B)
│   ├── package.json
│   └── Dockerfile
│
├── rest-version/             ← Versão alternativa REST
│   ├── modulo-a/app.py
│   └── modulo-b/app.py
│
├── exemplos-grpc/            ← Demo dos 4 tipos de comunicação
│   ├── demo.proto
│   ├── servidor_demo.py
│   └── cliente_demo.py
│
├── k8s/                      ← Manifests Kubernetes
│   ├── a-deployment.yaml
│   ├── a-service.yaml
│   ├── b-deployment.yaml
│   └── b-service.yaml
│
├── scripts/                  ← Scripts de setup e teste
│   ├── setup.sh
│   ├── gen_protos.sh
│   ├── test_all.sh
│   ├── test_a.sh / test_b.sh / test_demo.sh
│   └── test_rest_a.sh / test_rest_b.sh
│
├── docs/                     ← Documentação
│   ├── PLANO.md
│   ├── grpc-protobuf.md
│   └── relatorio/
│       └── relatorio-final.md   ← este arquivo
│
├── docker-compose.yml
└── README.md
```
