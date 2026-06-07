# Plano de Aplicação do Projeto de Pesquisa — PSPD

**Disciplina:** FGA0244 — Programação para Sistemas Paralelos e Distribuídos (60h) — Turma 02 (2026.1)

---

## Tema Geral do Projeto

Desenvolvimento de uma aplicação distribuída baseada em microserviços usando gRPC, Protocol Buffers, HTTP/2, REST-API/JSON, containers e Kubernetes/minikube.

A aplicação será composta por três módulos principais:

- **Módulo P:** API-Gateway/web server, responsável por receber requisições HTTP de usuários e consultar os serviços gRPC.
- **Módulo A:** microserviço gRPC responsável por uma parte da lógica da aplicação.
- **Módulo B:** microserviço gRPC responsável por outra parte complementar da lógica da aplicação.

Também será criada uma versão alternativa usando REST-API/JSON entre P, A e B, para permitir comparação de desempenho.

## Sugestão de Aplicação

Sistema distribuído de consulta e análise de produtos.

O usuário acessa o módulo P por uma interface HTTP. O módulo P consulta dois microserviços:

- **Serviço A:** retorna informações básicas dos produtos, como nome, categoria, preço e disponibilidade.
- **Serviço B:** retorna informações complementares, como avaliação, tempo estimado de entrega, desconto ou recomendação.

O módulo P junta as respostas de A e B e devolve ao usuário uma resposta única.

---

## Etapa 1 — Estudo e Pesquisa Inicial

### Objetivo

Entender os conceitos principais necessários para desenvolver o projeto.

### Conteúdos a estudar

1. gRPC
2. Protocol Buffers
3. HTTP/2
4. Tipos de comunicação gRPC:
   - Unary call
   - Server streaming
   - Client streaming
   - Bidirectional streaming
5. REST-API e JSON
6. Comparação entre gRPC/ProtoBuf e REST/JSON
7. Docker e containers
8. Kubernetes e minikube
9. Cloud Native e arquitetura de microserviços

### Entregáveis

- Resumo sobre gRPC, ProtoBuf e HTTP/2.
- Exemplos simples dos quatro tipos de comunicação gRPC.
- Resumo sobre Kubernetes, containers e minikube.
- Definição da aplicação que será implementada.

### Divisão entre os alunos

**Danilo Carvalho Antunes:**
- Estudar gRPC.
- Levantar exemplos de unary call e server streaming.
- Documentar o funcionamento geral do gRPC.

**Aluno 2:**
- Estudar Protocol Buffers.
- Criar exemplos simples de arquivos `.proto`.
- Documentar mensagens, serviços e geração de código.

**Aluno 3:**
- Estudar HTTP/2.
- Explicar multiplexação, headers comprimidos e comunicação binária.
- Comparar HTTP/2 com HTTP/1.1.
- Estudar REST-API/JSON e levantar critérios de comparação com gRPC.
- Planejar como medir tempo de resposta nas duas versões.

**Aluno 4:**
- Estudar Docker, containers e minikube.
- Levantar comandos básicos de criação, build e execução.
- Preparar anotações sobre implantação local.

---

## Etapa 2 — Acesso ao Ambiente e Preparação das Ferramentas

### Objetivo

Garantir que todos os alunos consigam acessar o ambiente de trabalho e executar os comandos necessários.

### Atividades

1. Acessar o servidor da disciplina via SSH.
2. Trocar a senha no primeiro login.
3. Verificar ambiente Linux disponível.
4. Instalar ou verificar ferramentas:
   - Git
   - Docker
   - minikube
   - kubectl
   - compilador/ambiente da linguagem escolhida
   - ferramentas gRPC
   - Protocol Buffers compiler
5. Criar um repositório do grupo.
6. Definir estrutura inicial do projeto.

### Organização sugerida do repositório

```text
projeto-pspd/
├── docs/
├── proto/
├── modulo-p/
├── modulo-a/
├── modulo-b/
├── rest-version/
├── k8s/
├── testes/
└── README.md
```

### Divisão entre os alunos

**Danilo Carvalho Antunes:**
- Testar acesso SSH e documentar o passo a passo de entrada no servidor.

**Aluno 2:**
- Preparar o repositório Git e organizar a estrutura de pastas.

**Aluno 3:**
- Instalar/testar ferramentas gRPC e ProtoBuf.
- Criar um documento de comandos usados e problemas encontrados.

**Aluno 4:**
- Instalar/testar Docker, minikube e kubectl.

---

## Etapa 3 — Definição da Arquitetura e dos Contratos gRPC

### Objetivo

Definir claramente os serviços, mensagens e responsabilidades dos módulos P, A e B.

### Arquitetura planejada

```text
Cliente Web
    |
    | HTTP/REST
    v
Módulo P - API Gateway / Web Server / gRPC Client
    |
    | gRPC
    |--------------------|
    v                    v
Módulo A              Módulo B
gRPC Server          gRPC Server
```

### Responsabilidade dos módulos

**Módulo P:**
- Receber requisições HTTP do usuário.
- Chamar os serviços gRPC A e B.
- Consolidar as respostas.
- Retornar resultado final ao cliente web.

**Módulo A:**
- Implementar o primeiro serviço gRPC.
- Responder com dados básicos.

**Módulo B:**
- Implementar o segundo serviço gRPC.
- Responder com dados complementares.

### Linguagens sugeridas

- Módulo P: Node.js ou Python
- Módulo A: Python ou Go
- Módulo B: Java ou Go

O importante é que A e B sejam implementados em linguagem diferente da usada em P.

### Arquivos ProtoBuf sugeridos

**`proto/produto.proto`:**

```proto
syntax = "proto3";

package produto;

service ProdutoService {
  rpc BuscarProduto(ProdutoRequest) returns (ProdutoResponse);
}

message ProdutoRequest {
  int32 id = 1;
}

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
  rpc BuscarAvaliacao(AvaliacaoRequest) returns (AvaliacaoResponse);
}

message AvaliacaoRequest {
  int32 id_produto = 1;
}

message AvaliacaoResponse {
  int32  id_produto    = 1;
  double nota          = 2;
  string comentario    = 3;
  int32  prazo_entrega = 4;
}
```

### Divisão entre os alunos

**Danilo Carvalho Antunes:** Definir e implementar o contrato `.proto` do serviço A.
**Aluno 2:** Definir e implementar o contrato `.proto` do serviço B.
**Aluno 3:** Projetar o módulo P como API Gateway.
**Aluno 4:** Planejar a comunicação entre P, A e B + documentar a arquitetura e criar o diagrama da solução.

---

## Etapa 4 — Implementação da Versão gRPC

### Objetivo

Construir a aplicação distribuída usando gRPC.

### Atividades

1. Criar os arquivos `.proto`.
2. Gerar os códigos gRPC a partir dos arquivos `.proto`.
3. Implementar o servidor gRPC A.
4. Implementar o servidor gRPC B.
5. Implementar o módulo P como cliente gRPC e servidor HTTP.
6. Testar chamadas isoladas (P→A e P→B).
7. Testar fluxo completo (Cliente HTTP → P → A e B → resposta consolidada).

### Fluxo esperado

```text
GET /produto/1

P recebe a requisição HTTP
P chama ProdutoService no módulo A
P chama AvaliacaoService no módulo B
P junta as respostas
P retorna JSON final ao usuário
```

### Exemplo de resposta final de P

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

### Divisão entre os alunos

**Danilo Carvalho Antunes:** Implementar microserviço A e criar testes diretos para A.
**Aluno 2:** Implementar microserviço B e criar testes diretos para B.
**Aluno 3:** Implementar módulo P com web server e cliente gRPC.
**Aluno 4:** Integrar P, A e B; resolver problemas de comunicação + criar testes de uso, registrar resultados e documentar execução.

---

## Etapa 5 — Implementação da Versão REST-API/JSON

### Objetivo

Criar uma versão alternativa da aplicação usando REST-API/JSON entre P, A e B.

### Atividades

1. Criar serviço REST A.
2. Criar serviço REST B.
3. Adaptar P para chamar A e B usando HTTP/JSON.
4. Manter a mesma lógica da versão gRPC.
5. Garantir que as respostas finais sejam equivalentes.

### Divisão entre os alunos

**Danilo Carvalho Antunes:** Adaptar o serviço A para REST.
**Aluno 2:** Adaptar o serviço B para REST.
**Aluno 3:** Adaptar o módulo P para consumir REST.
**Aluno 4:** Garantir equivalência funcional entre as versões REST e gRPC + criar os testes comparativos entre as duas versões.

---

## Etapa 6 — Testes de Desempenho

### Objetivo

Comparar o tempo de resposta entre a versão gRPC/ProtoBuf e a versão REST/JSON.

### Cenários de teste

1. Uma única requisição.
2. Dez requisições sequenciais.
3. Cem requisições sequenciais.
4. Requisições com payload pequeno.
5. Requisições com payload maior.
6. Requisições repetidas para avaliar estabilidade.

### Métrica principal

- Tempo médio de resposta em milissegundos.

### Tabela esperada no relatório

| Cenário         | gRPC/ProtoBuf | REST/JSON | Diferença observada |
| --------------- | ------------: | --------: | ------------------- |
| 1 requisição    |               |           |                     |
| 10 requisições  |               |           |                     |
| 100 requisições |               |           |                     |
| Payload pequeno |               |           |                     |
| Payload maior   |               |           |                     |

### Divisão entre os alunos

**Danilo Carvalho Antunes:** Executar testes da versão gRPC.
**Aluno 2:** Executar testes da versão REST.
**Aluno 3:** Criar script de medição de tempo + organizar resultados em tabela.
**Aluno 4:** Escrever análise conclusiva dos resultados.

---

## Etapa 7 — Containerização da Aplicação

### Objetivo

Preparar os módulos P, A e B para execução em containers.

### Atividades

1. Criar Dockerfile para o módulo P.
2. Criar Dockerfile para o módulo A.
3. Criar Dockerfile para o módulo B.
4. Criar imagens Docker.
5. Testar os containers individualmente.
6. Testar a comunicação entre containers.

### Divisão entre os alunos

**Danilo Carvalho Antunes:** Criar Dockerfile do módulo A.
**Aluno 2:** Criar Dockerfile do módulo B.
**Aluno 3:** Criar Dockerfile do módulo P.
**Aluno 4:** Testar execução dos containers + documentar comandos de build e execução.

---

## Etapa 8 — Implantação com Kubernetes/minikube

### Objetivo

Implantar a aplicação distribuída em Kubernetes usando minikube.

### Componentes esperados

Para cada módulo: Deployment + Service (total de 6 manifests YAML).

### Estrutura sugerida

```text
k8s/
├── p-deployment.yaml
├── p-service.yaml
├── a-deployment.yaml
├── a-service.yaml
├── b-deployment.yaml
└── b-service.yaml
```

### Fluxo no Kubernetes

```text
Browser / Cliente HTTP
        |
        v
Service P
        |
        v
Pod P
   |          |
   v          v
Service A   Service B
   |          |
   v          v
Pod A       Pod B
```

### Comandos esperados

```bash
minikube start
kubectl apply -f k8s/
kubectl get pods
kubectl get services
kubectl logs <pod>
minikube service p-service
```

### Divisão entre os alunos

**Danilo Carvalho Antunes:** Criar arquivos Kubernetes do módulo A.
**Aluno 2:** Criar arquivos Kubernetes do módulo B.
**Aluno 3:** Criar arquivos Kubernetes do módulo P.
**Aluno 4:** Testar implantação no minikube + documentar comandos, erros e soluções.

---

## Etapa 9 — Relatório Final

### Estrutura do relatório

1. **Capa** — Título, curso, disciplina, turma, professor, integrantes.
2. **Introdução** — Objetivo, visão geral, tecnologias.
3. **Framework gRPC** — O que é gRPC, ProtoBuf, HTTP/2, tipos de comunicação, testes.
4. **Aplicação distribuída** — Descrição, arquitetura P/A/B, arquivos `.proto`, execução, dificuldades.
5. **Comparação gRPC/ProtoBuf x REST/JSON** — Versão REST, cenários, tabela de resultados, análise.
6. **Kubernetes e minikube** — Conceitos, arquitetura, Dockerfiles, YAML, comandos, testes, dificuldades.
7. **Conclusão** — Conclusão geral, aprendizados individuais, autoavaliação.
8. **Apêndices/Anexos** — Arquivos `.proto`, trechos de código, comandos, prints.

### Divisão entre os alunos

**Danilo Carvalho Antunes:** Seção de gRPC e ProtoBuf.
**Aluno 2:** Seção da aplicação e microserviços A e B.
**Aluno 3:** Seção do módulo P, integração e testes/comparação de desempenho.
**Aluno 4:** Seção de Kubernetes/minikube + conclusão + organização geral do relatório.

---

## Etapa 10 — Slides e Apresentação

### Estrutura sugerida dos slides

1. Título e integrantes.
2. Objetivo do projeto.
3. Tecnologias utilizadas.
4. Visão geral de gRPC, ProtoBuf e HTTP/2.
5. Arquitetura da aplicação.
6. Explicação do módulo P.
7. Explicação do módulo A.
8. Explicação do módulo B.
9. Demonstração do fluxo da aplicação.
10. Comparação gRPC x REST.
11. Kubernetes/minikube.
12. Resultados dos testes.
13. Dificuldades encontradas.
14. Conclusão.
15. Divisão de trabalho.

### Divisão entre os alunos

**Danilo Carvalho Antunes:** Slides sobre gRPC, ProtoBuf e HTTP/2.
**Aluno 2:** Slides sobre serviços A e B.
**Aluno 3:** Slides sobre módulo P, integração e comparação gRPC x REST.
**Aluno 4:** Slides sobre Kubernetes, testes, resultados e conclusão.

---

## Etapa 11 — Vídeo do Projeto

### Objetivo

Gravar um vídeo com a participação de todos os membros (~20 minutos, ~5 min por aluno).

### Estrutura sugerida

**Danilo Carvalho Antunes:** Objetivo do trabalho + gRPC, ProtoBuf e HTTP/2.
**Aluno 2:** Microserviços A e B + arquivos `.proto`.
**Aluno 3:** Módulo P, API Gateway, integração HTTP/gRPC e testes comparativos gRPC x REST.
**Aluno 4:** Docker, Kubernetes/minikube, resultados dos testes e conclusão.

### Demonstrações no vídeo

1. Subir os serviços localmente.
2. Fazer uma requisição ao módulo P.
3. Mostrar P chamando A e B.
4. Mostrar a resposta final.
5. Mostrar containers/pods no Kubernetes.
6. Mostrar teste comparativo entre gRPC e REST.

---

## Cronograma Sugerido

| Semana | Atividades |
|--------|-----------|
| **1** | Estudo de gRPC, ProtoBuf, HTTP/2, REST, Docker, Kubernetes — Escolha da aplicação — Definição da arquitetura — Criação inicial dos arquivos `.proto` |
| **2** | Implementação da versão gRPC — Módulos P, A e B — Testes locais de comunicação |
| **3** | Implementação da versão REST/JSON — Testes comparativos — Medição de desempenho |
| **4** | Criação dos Dockerfiles — Implantação no minikube — Ajustes finais |
| **5** | Relatório — Slides — Vídeo — Revisão final |

---

## Divisão Geral entre os 4 Alunos

### Danilo Carvalho Antunes — gRPC, ProtoBuf e Microserviço A
- Estudar gRPC e ProtoBuf.
- Criar os arquivos `.proto` do serviço A.
- Implementar o microserviço A (versão gRPC e REST).
- Criar o Dockerfile e os manifests Kubernetes do módulo A.
- Documentar o serviço A.
- Apresentar gRPC, ProtoBuf, HTTP/2 e serviço A no vídeo.

### Aluno 2 — HTTP/2, Microserviço B e REST equivalente
- Estudar HTTP/2 e comparação com HTTP/1.1.
- Implementar o microserviço B (versão gRPC e REST).
- Criar o Dockerfile e os manifests Kubernetes do módulo B.
- Documentar o serviço B.
- Apresentar HTTP/2 e serviços A e B no vídeo.

### Aluno 3 — Módulo P, API Gateway e Testes
- Implementar o módulo P (web server + cliente gRPC + cliente REST).
- Criar o Dockerfile e os manifests Kubernetes do módulo P.
- Criar scripts de medição de tempo e testes comparativos gRPC x REST.
- Organizar tabelas de resultados e análise conclusiva.
- Apresentar o módulo P, integração e testes comparativos no vídeo.

### Luiz Gustavo — Docker, Kubernetes, minikube e Organização Final
- Configurar e testar execução de todos os containers Docker.
- Configurar minikube e testar implantação completa no Kubernetes.
- Documentar comandos, erros e soluções.
- Consolidar o relatório final e organizar slides e vídeo.
- Apresentar a infraestrutura, resultados e conclusão no vídeo.

---

## Entregáveis Finais

1. Código-fonte da versão gRPC
2. Código-fonte da versão REST/JSON
3. Arquivos `.proto`
4. Dockerfiles
5. Arquivos YAML do Kubernetes
6. Relatório final
7. Tabela de testes de desempenho
8. Slides de apresentação
9. Vídeo com participação dos 4 alunos
10. README com instruções de execução
