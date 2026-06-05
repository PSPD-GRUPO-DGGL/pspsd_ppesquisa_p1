"""Cliente de teste do Módulo B.

Exercita os dois tipos de comunicação do AvaliacaoService:
  - BuscarAvaliacao  (unary)
  - ListarAvaliacoes (server streaming)

Uso:
    python client_test.py
Variáveis de ambiente:
    GRPC_B_ADDR (padrão localhost:50052)
"""
import os
import sys

import grpc

import avaliacao_pb2
import avaliacao_pb2_grpc


def main() -> int:
    addr = os.getenv("GRPC_B_ADDR", "localhost:50052")
    with grpc.insecure_channel(addr) as channel:
        stub = avaliacao_pb2_grpc.AvaliacaoServiceStub(channel)

        print("== Unary: BuscarAvaliacao(id_produto=1) ==")
        resp = stub.BuscarAvaliacao(avaliacao_pb2.AvaliacaoRequest(id_produto=1))
        print(f"  -> id={resp.id_produto} | nota={resp.nota} | prazo={resp.prazo_entrega}d | '{resp.comentario}'")

        print("\n== Unary: BuscarAvaliacao(id_produto=999) deve dar NOT_FOUND ==")
        try:
            stub.BuscarAvaliacao(avaliacao_pb2.AvaliacaoRequest(id_produto=999))
        except grpc.RpcError as e:
            print(f"  -> {e.code().name}: {e.details()}")

        print("\n== Server streaming: ListarAvaliacoes([1, 3, 6]) ==")
        pedido = avaliacao_pb2.ListarAvaliacoesRequest(ids_produto=[1, 3, 6])
        for item in stub.ListarAvaliacoes(pedido):
            print(f"  -> id={item.id_produto} | nota={item.nota:.1f} | prazo={item.prazo_entrega}d | '{item.comentario}'")

    print("\nOK: testes do Módulo B concluídos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
