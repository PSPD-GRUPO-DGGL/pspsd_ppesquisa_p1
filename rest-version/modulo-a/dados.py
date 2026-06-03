"""Base de dados do Módulo A (versão REST) — espelha a versão gRPC.

Mantida igual à de modulo-a/dados.py para garantir equivalência funcional
e comparação justa de desempenho (gRPC x REST).
"""

PRODUTOS = [
    {"id": 1, "nome": "Notebook Ultra", "categoria": "Eletrônicos", "preco": 3500.00, "disponivel": True},
    {"id": 2, "nome": "Mouse Gamer", "categoria": "Eletrônicos", "preco": 150.00, "disponivel": True},
    {"id": 3, "nome": "Cadeira Ergonômica", "categoria": "Móveis", "preco": 980.50, "disponivel": False},
    {"id": 4, "nome": "Monitor 27\"", "categoria": "Eletrônicos", "preco": 1200.00, "disponivel": True},
    {"id": 5, "nome": "Mesa de Escritório", "categoria": "Móveis", "preco": 640.00, "disponivel": True},
    {"id": 6, "nome": "Teclado Mecânico", "categoria": "Eletrônicos", "preco": 320.00, "disponivel": True},
    {"id": 7, "nome": "Luminária LED", "categoria": "Decoração", "preco": 89.90, "disponivel": True},
]

_POR_ID = {p["id"]: p for p in PRODUTOS}


def buscar_por_id(produto_id: int):
    return _POR_ID.get(produto_id)


def listar(categoria: str = "", limite: int = 0):
    itens = PRODUTOS
    if categoria:
        itens = [p for p in itens if p["categoria"].lower() == categoria.lower()]
    if limite and limite > 0:
        itens = itens[:limite]
    return itens
