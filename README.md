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

# Guia de Configuração do Ambiente e Execução — PSPD

Este guia orienta o passo a passo de instalação das ferramentas necessárias e 
as instruções para executar a nossa aplicação de microsserviços distribuídos 
(Módulos P, A e B) localmente no Docker ou orquestrado no Kubernetes (Minikube).

---

## 1. Pré-requisitos & Ativação de Virtualização (Windows)

Antes de iniciar as instalações, certifique-se de habilitar a virtualização 
física do seu processador e os recursos do Windows.

### Passo 1.1: Ativar na Placa-Mãe (BIOS)
1. Reinicie seu computador.
2. Acesse a BIOS pressionando repetidamente a tecla correspondente à sua marca 
   (geralmente `F2`, `F12`, `F10` ou `Delete`).
3. Procure pelas seguintes opções e marque como **Enabled** (Habilitado):
   - Se for processador **Intel**: Intel Virtualization Technology (Intel VT-x).
   - Se for processador **AMD**: SVM Mode (Secure Virtual Machine).
4. Salve as alterações e inicie o Windows.

### Passo 1.2: Ativar Recursos de Máquina Virtual no Windows
Abra o **PowerShell como Administrador** e execute os dois comandos abaixo:

```powershell
# Ativa o Subsistema do Windows para Linux (WSL)
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# Ativa a Plataforma de Máquina Virtual
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

**Importante:** Reinicie o computador após a execução desses comandos. 
Ao ligar de volta, execute este comando no terminal para atualizar o kernel 
do WSL 2:

```powershell
wsl --update
```

---

## 2. Instalação das Ferramentas Obrigatórias

Abra o seu terminal e utilize o gerenciador de pacotes padrão do Windows 
(`winget`) para instalar as dependências de infraestrutura de forma automática:

```powershell
# 1. Instalar o Docker Desktop
winget install Docker.DockerDesktop

# 2. Instalar o Minikube
winget install Kubernetes.minikube

# 3. Instalar o Kubectl (CLI do Kubernetes)
winget install Kubernetes.kubectl
```

> **Atenção:** Após concluir as instalações por completo, feche todos os 
> terminais abertos ou reinicie o VS Code para que o sistema operacional 
> reconheça as novas variáveis de ambiente.

---

## 3. Rodando o Projeto com Docker Compose (Local)

O Docker Compose sobe todo o ecossistema local na sua máquina, incluindo 
as versões gRPC e REST do Módulo A e B para comparação.

1. **Abra o Docker Desktop** na sua máquina e certifique-se de que a baleia 
   no canto inferior esquerdo está verde.
2. Na raiz do projeto, execute o comando:

```bash
docker compose up --build
```

### Endpoints Disponíveis Localmente:
- **Módulo P (API Gateway):** `http://localhost:8000/produto/1`
- **Módulo A (REST):** `http://localhost:8001/produto/1`
- **Módulo B (REST):** `http://localhost:8002/avaliacao/1`

Para derrubar os containers após testar:
```bash
docker compose down
```

---

## 4. Rodando o Projeto no Kubernetes (Minikube)

Para simular o ambiente de produção orquestrado sob o Kubernetes local:

### Passo 4.1: Inicializar o nó Kubernetes
```powershell
minikube start --driver=docker
```

### Passo 4.2: Apontar contexto de build de imagem para dentro do Kubernetes
No PowerShell, execute o comando abaixo para que o seu comando `docker build` 
salve as imagens diretamente na memória do cluster:

```powershell
& minikube -p minikube docker-env --shell powershell | Invoke-Expression
```

### Passo 4.3: Compilar as imagens
Rode o comando de compilação na raiz do projeto:

```powershell
docker build -t modulo-a:latest -f modulo-a/Dockerfile .
docker build -t modulo-b:latest -f modulo-b/Dockerfile .
docker build -t modulo-p:latest -f modulo-p/Dockerfile .
```

### Passo 4.4: Aplicar as configurações no Kubernetes (Deploy)
```powershell
kubectl apply -f k8s/
```

### Passo 4.5: Monitorar o status de inicialização
Execute o comando abaixo e aguarde de 1 a 2 minutos até que o status de todos 
os 3 pods (`modulo-a-...`, `modulo-b-...` e `modulo-p-...`) mude de 
`ContainerCreating` para **`Running`**:

```powershell
kubectl get pods -w
```
*(Pressione `Ctrl + C` para sair do monitoramento contínuo).*

---

## 5. Como Testar e Fazer Requisições no Kubernetes

Como rodamos o Minikube via driver do Docker no Windows, os clusters rodam 
em uma rede isolada. Para testar, precisamos abrir um canal de ponte de rede:

1. No terminal do PowerShell, rode:
```powershell
minikube service p-service --url
```
2. **Deixe este terminal aberto em segundo plano.** Ele criará uma ponte e 
   cuspirá uma URL neste formato: `http://127.0.0.1:xxxxx` (ex: 63200).
3. Abra um navegador ou use um terminal secundário do VS Code e acesse 
   a URL gerada adicionando `/produto/1` no final:

```powershell
# Exemplo de consulta (substitua a porta de acordo com seu terminal)
curl.exe http://127.0.0.1:63200/produto/1
```

O JSON completo fundindo os dados de A e B será mostrado na tela!

---

## 6. Comandos Úteis do Kubernetes para Debug (Depuração)

- Ver logs de processamento de um pod em tempo real:
  ```powershell
  kubectl logs -f modulo-p-deployment-xxxxxx
  ```
- Excluir e limpar todos os recursos instalados do Kubernetes:
  ```powershell
  kubectl delete -f k8s/
  ```
- Desligar de forma segura o minikube:
  ```powershell
  minikube stop
  ```

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
| **Guilherme Brito de Souza** | Módulo P (API Gateway), integração gRPC e REST + scripts de testes e comparação de desempenho |
| **Luiz Gustavo Lopes Campos** | Docker, Kubernetes, minikube + consolidação do relatório, slides e vídeo final |

> Detalhamento completo por etapa disponível em [`docs/PLANO.md`](docs/PLANO.md).
