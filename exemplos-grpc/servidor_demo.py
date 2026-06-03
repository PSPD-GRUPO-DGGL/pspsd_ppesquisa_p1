"""Servidor de demonstração dos 4 tipos de comunicação gRPC.

Implementa o DemoService de demo.proto. Apenas didático (não faz parte do
backend P/A/B), serve de evidência para o relatório (Danilo Carvalho Antunes).
"""
import os
from concurrent import futures

import grpc

import demo_pb2
import demo_pb2_grpc


class DemoService(demo_pb2_grpc.DemoServiceServicer):
    # 1) Unary -------------------------------------------------------------
    def Unary(self, request, context):
        return demo_pb2.Echo(texto=f"recebi: {request.texto}", n=request.n)

    # 2) Server streaming --------------------------------------------------
    def ServerStream(self, request, context):
        for i in range(1, request.n + 1):
            yield demo_pb2.Echo(texto=f"{request.texto} #{i}", n=i)

    # 3) Client streaming --------------------------------------------------
    def ClientStream(self, request_iterator, context):
        textos = []
        for msg in request_iterator:
            textos.append(msg.texto)
        return demo_pb2.Resumo(total=len(textos), concat=" | ".join(textos))

    # 4) Bidirectional streaming ------------------------------------------
    def BidiStream(self, request_iterator, context):
        for msg in request_iterator:
            yield demo_pb2.Echo(texto=f"eco[{msg.texto}]", n=msg.n)


def serve():
    port = os.getenv("DEMO_PORT", "50090")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    demo_pb2_grpc.add_DemoServiceServicer_to_server(DemoService(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"[Demo] DemoService ouvindo em 0.0.0.0:{port}", flush=True)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
