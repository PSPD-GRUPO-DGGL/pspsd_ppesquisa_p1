# Projeto de Pesquisa P1 — PSPD

**Disciplina:** FGA0244 — Programação para Sistemas Paralelos e Distribuídos (60h) — Turma 02 (2026.1)
**Universidade de Brasília — Campus Gama (FGA)**

---

## Sobre o Projeto

Desenvolvimento de uma **aplicação distribuída baseada em microserviços** utilizando gRPC, Protocol Buffers, HTTP/2, REST-API/JSON, containers Docker e orquestração com Kubernetes/minikube.

A aplicação implementa um **Sistema Distribuído de Consulta e Análise de Produtos**, dividido em três módulos:

| Módulo | Função |
|--------|--------|
| **Módulo P** | API Gateway / Web Server — recebe requisições HTTP e consulta os microserviços via gRPC |
| **Módulo A** | Microserviço gRPC — fornece dados básicos do produto (nome, categoria, preço, disponibilidade) |
| **Módulo B** | Microserviço gRPC — fornece dados complementares (avaliação, comentário, prazo de entrega) |

Também é implementada uma **versão alternativa REST/JSON** entre os módulos para comparação de desempenho.

---

## Arquitetura

```
Cliente Web (Browser / curl)
        |
        | HTTP/REST
        v
  ┌─────────────┐
  │  Módulo P   │  ← API Gateway + gRPC Client + Web Server
  └──────┬──────┘
         |
         | gRPC (HTTP/2 + Protocol Buffers)
    _____|_____
   |           |
   v           v
┌──────┐   ┌──────┐
│ Mod A│   │ Mod B│   ← gRPC Servers
└──────┘   └──────┘
```

### Fluxo de uma requisição

```
GET /produto/1
  → P recebe a requisição HTTP
  → P chama ProdutoService no Módulo A via gRPC
  → P chama AvaliacaoService no Módulo B via gRPC
  → P consolida as respostas
  → P retorna JSON ao cliente
```

### Exemplo de resposta final

```json
{
  "id": 1,
  "nome": "Notebook",
  "categoria": "Eletrônicos",
  "preco": 3500.00,
  "disponivel": true,
  "nota": 4.7,
  "comentario": "Produto bem avaliado",
  "prazo_entrega": 5
}
```

---

## Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| **gRPC** | Comunicação entre P, A e B |
| **Protocol Buffers (protobuf)** | Serialização das mensagens gRPC |
| **HTTP/2** | Protocolo de transporte do gRPC |
| **REST / JSON** | Versão alternativa para comparação |
| **Docker** | Containerização dos módulos |
| **Kubernetes / minikube** | Orquestração e implantação local |
| **Python** | Microserviços A e B (gRPC + REST) |
| **Node.js** | Módulo P (API Gateway) — linguagem distinta de A/B (regra do professor) |

---

## Contratos gRPC (Protocol Buffers)

Os arquivos `.proto` ficam em `proto/`. Contratos previstos:

**`proto/produto.proto`** — Serviço do Módulo A
```proto
syntax = "proto3";
package produto;

service ProdutoService {
  rpc BuscarProduto(ProdutoRequest) returns (ProdutoResponse);
}

message ProdutoRequest  { int32 id = 1; }
message ProdutoResponse {
  int32  id         = 1;
  string nome       = 2;
  string categoria  = 3;
  double preco      = 4;
  bool   disponivel = 5;
}
```

**`proto/avaliacao.proto`** — Serviço do Módulo B
```proto
syntax = "proto3";
package avaliacao;

service AvaliacaoService {
  rpc BuscarAvaliacao(AvaliacaoRequest) returns (AvaliacaoResponse);
}

message AvaliacaoRequest  { int32 id_produto = 1; }
message AvaliacaoResponse {
  int32  id_produto    = 1;
  double nota          = 2;
  string comentario    = 3;
  int32  prazo_entrega = 4;
}
```

---

## Estrutura do Repositório

```
pspsd_ppesquisa_p1/
├── docs/               ← Documentação, relatório, diagrams
├── proto/              ← Arquivos .proto (contratos gRPC)
├── modulo-p/           ← API Gateway / Web Server
├── modulo-a/           ← Microserviço A (dados básicos do produto)
├── modulo-b/           ← Microserviço B (avaliação e complemento)
├── rest-version/       ← Versão alternativa com REST/JSON
├── k8s/                ← Manifests Kubernetes (Deployments e Services)
├── testes/             ← Scripts de teste e comparação de desempenho
└── README.md
```

> O plano completo de desenvolvimento está em [`docs/PLANO.md`](docs/PLANO.md).

---

## Como Executar

### Pré-requisitos

- Docker instalado e em execução
- minikube instalado
- kubectl instalado
- Compilador protobuf (`protoc`) + plugins da linguagem escolhida

### 1. Clonar o repositório

```bash
git clone <url-do-repositório>
cd pspsd_ppesquisa_p1
```

### 2. Gerar o código a partir dos arquivos `.proto`

> Comandos específicos por linguagem serão documentados em cada `modulo-*/README.md` conforme a implementação avança.

```bash
# Exemplo para Python
protoc --python_out=. --grpc_python_out=. proto/produto.proto
protoc --python_out=. --grpc_python_out=. proto/avaliacao.proto
```

### 3. Executar localmente (sem containers)

```bash
# Terminal 1 — Módulo A
cd modulo-a && python server.py

# Terminal 2 — Módulo B
cd modulo-b && python server.py

# Terminal 3 — Módulo P
cd modulo-p && python server.py
```

### 4. Build das imagens Docker

```bash
docker build -t modulo-a:latest ./modulo-a
docker build -t modulo-b:latest ./modulo-b
docker build -t modulo-p:latest ./modulo-p
```

### 5. Implantar no Kubernetes com minikube

```bash
minikube start
kubectl apply -f k8s/
kubectl get pods
kubectl get services
minikube service p-service   # abre o serviço P no browser
```

### 6. Verificar logs

```bash
kubectl logs <nome-do-pod>
```

---

## Testes de Desempenho

Os scripts de teste estão em `testes/`. A comparação mede o tempo médio de resposta (ms) entre as versões **gRPC/ProtoBuf** e **REST/JSON**:

| Cenário | gRPC/ProtoBuf | REST/JSON | Diferença |
|---|---|---|---|
| 1 requisição | — | — | — |
| 10 requisições | — | — | — |
| 100 requisições | — | — | — |
| Payload pequeno | — | — | — |
| Payload maior | — | — | — |

> Tabela será preenchida com os resultados obtidos ao longo do desenvolvimento.

---

## Acesso ao Ambiente da Disciplina (Servidor SSH)

Para exercícios no servidor da disciplina (uso de GPUs e ambiente remoto):

```bash
ssh -p 10200 a<sua_matrícula>@kiriland.unb.br
```

**Exemplo:** para matrícula `26123456`, o usuário é `a26123456`.

> **Atenção:** No **primeiro login**, o sistema solicitará troca de senha.
> Repita a senha atual quando pedida e insira sua nova senha desejada com cuidado.

---

## Entregáveis do Projeto

1. Código-fonte — versão gRPC
2. Código-fonte — versão REST/JSON
3. Arquivos `.proto`
4. Dockerfiles
5. Manifests YAML do Kubernetes
6. Relatório final
7. Tabela de testes de desempenho
8. Slides de apresentação
9. Vídeo com participação dos 4 integrantes
10. Este README

---

## Cronograma

| Semana | Foco |
|--------|------|
| 1 | Estudo de gRPC, ProtoBuf, HTTP/2, REST, Docker, Kubernetes — Definição da arquitetura |
| 2 | Implementação da versão gRPC (módulos P, A e B) |
| 3 | Implementação da versão REST/JSON e testes comparativos |
| 4 | Containerização (Dockerfiles) e implantação no minikube |
| 5 | Relatório, slides, vídeo e revisão final |

---

## Divisão de Responsabilidades

| Integrante | Responsabilidade Principal |
|---|---|
| **Danilo Carvalho Antunes** | gRPC, ProtoBuf, Microserviço A + Dockerfile e manifests K8s do módulo A |
| **Aluno 2** | HTTP/2, Microserviço B, versão REST do serviço B + Dockerfile e manifests K8s do módulo B |
| **Aluno 3** | Módulo P (API Gateway), integração gRPC e REST + scripts de testes e comparação de desempenho |
| **Luiz Gustavo Lopes Campos** | Docker, Kubernetes, minikube + consolidação do relatório, slides e vídeo final |

> Detalhamento completo por etapa disponível em [`docs/PLANO.md`](docs/PLANO.md).