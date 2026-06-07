# Modulo P - API Gateway (Node.js)

## Instalação

```bash
npm install
```

## Execução

```bash
npm start
```

## Desenvolvimento (com watch)

```bash
npm run dev
```

## Endpoints

### Home
- **GET** `/` - Status do módulo P

### Produto com gRPC
- **GET** `/produto/:produto_id` 
  - Retorna produto de A + avaliação de B 
    via gRPC

### Produto com REST
- **GET** `/rest/produto/:produto_id` 
  - Retorna produto de A + avaliação de B 
    via HTTP REST

## Configuração de Ambiente

As seguintes variáveis de ambiente podem ser 
configuradas:

- `PORT` - Porta do servidor (padrão: 3000)
- `A_HOST` - Endereço gRPC do Módulo A 
  (padrão: localhost:50051)
- `B_HOST` - Endereço gRPC do Módulo B 
  (padrão: localhost:50052)
- `MODULO_A_URL` - URL REST do Módulo A 
  (padrão: http://localhost:8001)
- `MODULO_B_URL` - URL REST do Módulo B 
  (padrão: http://localhost:8002)

## Estrutura de Arquivos

```
modulo-p/
├── src/
│   ├── app.js           # Servidor Express principal
│   ├── grpcClient.js    # Cliente gRPC para A e B
│   └── restClient.js    # Cliente REST para A e B
├── package.json         # Dependências Node.js
└── README.md            # Este arquivo
```


## Resposta de Exemplo

```json
{
  "id": 1,
  "nome": "Notebook Dell",
  "categoria": "eletrônicos",
  "preco": 3500.50,
  "disponivel": true,
  "nota": 4.5,
  "comentario": "Excelente produto!",
  "prazo_entrega": 5
}
```
