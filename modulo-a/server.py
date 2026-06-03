"""Módulo A — Servidor gRPC (dados básicos de produtos).

Implementa o ProdutoService definido em proto/produto.proto:
  - BuscarProduto  -> unary call        (1 request  -> 1 response)
  - ListarProdutos -> server streaming  (1 request  -> N responses)

Execução:
    python server.py            # escuta em 0.0.0.0:50051
Variáveis de ambiente:
    GRPC_A_PORT (padrão 50051)
"""
import os
import time
from concurrent import futures

import grpc

import produto_pb2
import produto_pb2_grpc
import dados


class ProdutoService(produto_pb2_grpc.ProdutoServiceServicer):
    """Implementação dos RPCs do Módulo A."""

    def BuscarProduto(self, request, context):
        """Unary: retorna um único produto pelo id."""
        produto = dados.buscar_por_id(request.id)
        if produto is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Produto com id={request.id} não encontrado")
            return produto_pb2.ProdutoResponse()
        return _to_response(produto)

    def ListarProdutos(self, request, context):
        """Server streaming: emite os produtos um a um."""
        itens = dados.listar(categoria=request.categoria, limite=request.limite)
        for produto in itens:
            # pequeno atraso para evidenciar o streaming durante demos/testes
            time.sleep(0.05)
            yield _to_response(produto)


def _to_response(produto: dict) -> "produto_pb2.ProdutoResponse":
    return produto_pb2.ProdutoResponse(
        id=produto["id"],
        nome=produto["nome"],
        categoria=produto["categoria"],
        preco=produto["preco"],
        disponivel=produto["disponivel"],
    )


def serve():
    port = os.getenv("GRPC_A_PORT", "50051")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    produto_pb2_grpc.add_ProdutoServiceServicer_to_server(ProdutoService(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"[Modulo A] ProdutoService gRPC ouvindo em 0.0.0.0:{port}", flush=True)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
