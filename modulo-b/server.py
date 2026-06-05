"""Módulo B — Servidor gRPC (avaliações e prazos de entrega dos produtos).

Implementa o AvaliacaoService definido em proto/avaliacao.proto:
  - BuscarAvaliacao  -> unary call        (1 request  -> 1 response)
  - ListarAvaliacoes -> server streaming  (1 request  -> N responses)

Execução:
    python server.py            # escuta em 0.0.0.0:50052
Variáveis de ambiente:
    GRPC_B_PORT (padrão 50052)
"""
import os
import time
from concurrent import futures

import grpc

import avaliacao_pb2
import avaliacao_pb2_grpc
import dados


class AvaliacaoService(avaliacao_pb2_grpc.AvaliacaoServiceServicer):
    """Implementação dos RPCs do Módulo B."""

    def BuscarAvaliacao(self, request, context):
        """Unary: retorna a avaliação de um único produto pelo id."""
        avaliacao = dados.buscar_por_id(request.id_produto)
        if avaliacao is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Avaliação para id_produto={request.id_produto} não encontrada")
            return avaliacao_pb2.AvaliacaoResponse()
        return _to_response(avaliacao)

    def ListarAvaliacoes(self, request, context):
        """Server streaming: emite as avaliações de uma lista de produtos."""
        itens = dados.listar_por_ids(list(request.ids_produto))
        for avaliacao in itens:
            # pequeno atraso para evidenciar o streaming durante demos/testes
            time.sleep(0.05)
            yield _to_response(avaliacao)


def _to_response(avaliacao: dict) -> "avaliacao_pb2.AvaliacaoResponse":
    return avaliacao_pb2.AvaliacaoResponse(
        id_produto=avaliacao["id_produto"],
        nota=avaliacao["nota"],
        comentario=avaliacao["comentario"],
        prazo_entrega=avaliacao["prazo_entrega"],
    )


def serve():
    port = os.getenv("GRPC_B_PORT", "50052")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    avaliacao_pb2_grpc.add_AvaliacaoServiceServicer_to_server(AvaliacaoService(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"[Modulo B] AvaliacaoService gRPC ouvindo em 0.0.0.0:{port}", flush=True)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
