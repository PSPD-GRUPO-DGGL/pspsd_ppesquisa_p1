"""Cliente de demonstração: exercita os 4 tipos de comunicação gRPC."""
import os
import sys

import grpc

import demo_pb2
import demo_pb2_grpc


def gerar_mensagens():
    """Generator usado nos modos client/bidirecional streaming."""
    for palavra in ["alpha", "beta", "gama"]:
        yield demo_pb2.Echo(texto=palavra, n=len(palavra))


def main() -> int:
    addr = os.getenv("DEMO_ADDR", "localhost:50090")
    with grpc.insecure_channel(addr) as channel:
        stub = demo_pb2_grpc.DemoServiceStub(channel)

        print("== 1) UNARY ==")
        r = stub.Unary(demo_pb2.Echo(texto="ola", n=1))
        print(f"  resposta: {r.texto}")

        print("\n== 2) SERVER STREAMING ==")
        for msg in stub.ServerStream(demo_pb2.Echo(texto="item", n=3)):
            print(f"  recebido: {msg.texto}")

        print("\n== 3) CLIENT STREAMING ==")
        resumo = stub.ClientStream(gerar_mensagens())
        print(f"  total={resumo.total} | concat='{resumo.concat}'")

        print("\n== 4) BIDIRECTIONAL STREAMING ==")
        for msg in stub.BidiStream(gerar_mensagens()):
            print(f"  recebido: {msg.texto}")

    print("\nOK: demonstração dos 4 tipos de comunicação concluída.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
