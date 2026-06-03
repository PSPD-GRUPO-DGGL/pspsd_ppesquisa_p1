"""Cliente de teste do Módulo A.

Exercita os dois tipos de comunicação do ProdutoService:
  - BuscarProduto  (unary)
  - ListarProdutos (server streaming)

Uso:
    python client_test.py
Variáveis de ambiente:
    GRPC_A_ADDR (padrão localhost:50051)
"""
import os
import sys

import grpc

import produto_pb2
import produto_pb2_grpc


def main() -> int:
    addr = os.getenv("GRPC_A_ADDR", "localhost:50051")
    with grpc.insecure_channel(addr) as channel:
        stub = produto_pb2_grpc.ProdutoServiceStub(channel)

        print("== Unary: BuscarProduto(id=1) ==")
        resp = stub.BuscarProduto(produto_pb2.ProdutoRequest(id=1))
        print(f"  -> {resp.nome} | {resp.categoria} | R$ {resp.preco:.2f} | disp={resp.disponivel}")

        print("\n== Unary: BuscarProduto(id=999) deve dar NOT_FOUND ==")
        try:
            stub.BuscarProduto(produto_pb2.ProdutoRequest(id=999))
        except grpc.RpcError as e:
            print(f"  -> {e.code().name}: {e.details()}")

        print("\n== Server streaming: ListarProdutos(categoria='Eletrônicos') ==")
        pedido = produto_pb2.ListarProdutosRequest(categoria="Eletrônicos", limite=0)
        for item in stub.ListarProdutos(pedido):
            print(f"  -> #{item.id} {item.nome} (R$ {item.preco:.2f})")

    print("\nOK: testes do Módulo A concluídos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
