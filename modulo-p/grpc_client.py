import grpc

import produto_pb2
import produto_pb2_grpc

import avaliacao_pb2
import avaliacao_pb2_grpc


A_HOST = "localhost:50051"
B_HOST = "localhost:50052"


def buscar_produto_completo(produto_id: int):

    # Serviço A
    canal_a = grpc.insecure_channel(A_HOST)

    stub_a = produto_pb2_grpc.ProdutoServiceStub(
        canal_a
    )

    produto = stub_a.BuscarProduto(
        produto_pb2.ProdutoRequest(
            id=produto_id
        )
    )

    # Serviço B
    canal_b = grpc.insecure_channel(B_HOST)

    stub_b = avaliacao_pb2_grpc.AvaliacaoServiceStub(
        canal_b
    )

    avaliacao = stub_b.BuscarAvaliacao(
        avaliacao_pb2.AvaliacaoRequest(
            id_produto=produto_id
        )
    )

    return {
        "id": produto.id,
        "nome": produto.nome,
        "categoria": produto.categoria,
        "preco": produto.preco,
        "disponivel": produto.disponivel,
        "nota": avaliacao.nota,
        "comentario": avaliacao.comentario,
        "prazo_entrega": avaliacao.prazo_entrega,
    }