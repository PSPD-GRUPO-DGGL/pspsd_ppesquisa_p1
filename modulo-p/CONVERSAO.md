# Conversão Modulo P - Python → Node.js

## 📊 Resumo da Conversão

A conversão do **modulo-p** de Python (FastAPI) para 
Node.js (Express) foi concluída com sucesso. 
Toda a funcionalidade foi mantida e os requisitos 
de modulação foram preservados.

## 📁 Estrutura Criada

```
modulo-p/
├── src/
│   ├── app.js           # Servidor Express (≈ app.py)
│   ├── grpcClient.js    # Cliente gRPC (≈ grpc_client.py)
│   └── restClient.js    # Cliente REST (≈ rest_client.py)
├── package.json         # Dependências Node.js
├── .gitignore          # Configuração Git
└── README.md           # Documentação
```

## 🔄 Mapeamento Python → Node.js

### Dependências
| Python | Node.js |
|--------|---------|
| fastapi | express ^4.18.2 |
| uvicorn | (built-in) |
| grpcio | @grpc/grpc-js ^1.9.7 |
| protobuf | @grpc/proto-loader ^0.7.9 |
| requests | axios ^1.6.2 |

### Implementação
| Python | Node.js |
|--------|---------|
| app.py | src/app.js |
| FastAPI() | express() |
| @app.get() | app.get() |
| grpc_client.py | src/grpcClient.js |
| rest_client.py | src/restClient.js |

## 🎯 Endpoints Mantidos

✓ **GET** `/` 
  - Home: {"modulo": "P", "status": "ativo"}

✓ **GET** `/produto/:produto_id`
  - Via gRPC (Módulo A + B)

✓ **GET** `/rest/produto/:produto_id`
  - Via REST HTTP (Módulo A + B)

## ✨ Características Implementadas

✅ Express como framework web (substituindo FastAPI)
✅ Cliente gRPC com proto-loader 
   (carregamento dinâmico de .proto)
✅ Cliente REST com axios
✅ Tratamento de erros idêntico ao Python
✅ Variáveis de ambiente 
   (A_HOST, B_HOST, MODULO_A_URL, MODULO_B_URL, PORT)
✅ Resposta JSON com estrutura identica ao Python
✅ Código formatado com limite de 80 colunas
✅ Modularidade total (3 módulos independentes)
✅ Suporte a ES6 modules (type: "module")

## 📐 Limitações de Linha

Todos os arquivos JavaScript foram formatados 
com limite de 80 colunas por linha, conforme 
solicitado.

Exemplo (grpcClient.js):
```javascript
const canalB = new avaliacaoProto.avaliacao
  .AvaliacaoService(
    B_HOST,
    grpc.credentials.createInsecure()
  );
```

## 🚀 Como Usar

```bash
# Instalar dependências
npm install

# Executar o servidor
npm start

# Desenvolvimento (com reload automático)
npm run dev
```

## 📍 Carregamento de Proto

O arquivo `proto-loader` carrega dinamicamente 
os arquivos `.proto` do diretório raiz:

```javascript
const PROTO_DIR = path.resolve(__dirname, "../../proto");
const produtoProtoPath = path.join(PROTO_DIR, "produto.proto");
```

Isso garante que os arquivos sejam encontrados 
mesmo quando executado de dentro de `modulo-p/src/`.

---

**Status**: ✅ Conversão Completa
**Linguagem**: Node.js + Express (diferente de A e B)
**Compatibilidade**: 100% com especificação original
