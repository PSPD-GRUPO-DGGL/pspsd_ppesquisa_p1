import requests


def buscar_produto_completo_rest(produto_id: int):

    produto = requests.get(
        f"http://localhost:8001/produto/{produto_id}"
    ).json()

    avaliacao = requests.get(
        f"http://localhost:8002/avaliacao/{produto_id}"
    ).json()

    return {
        **produto,
        **avaliacao
    }