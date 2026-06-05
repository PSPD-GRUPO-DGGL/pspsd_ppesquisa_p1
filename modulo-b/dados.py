"""Base de dados em memória do Módulo B (avaliações e prazo de entrega dos produtos).

Os ids de produto correspondem aos do Módulo A para que o Módulo P possa
combinar as respostas de A e B numa única visão ao cliente.
"""

AVALIACOES = [
    {"id_produto": 1, "nota": 4.7, "comentario": "Excelente desempenho e bateria duradoura.", "prazo_entrega": 5},
    {"id_produto": 2, "nota": 4.5, "comentario": "Responsivo e confortável para longas sessões.", "prazo_entrega": 3},
    {"id_produto": 3, "nota": 3.8, "comentario": "Boa qualidade, mas montagem demorada.", "prazo_entrega": 10},
    {"id_produto": 4, "nota": 4.6, "comentario": "Imagem nítida e cores precisas.", "prazo_entrega": 7},
    {"id_produto": 5, "nota": 4.2, "comentario": "Resistente e bem acabada.", "prazo_entrega": 12},
    {"id_produto": 6, "nota": 4.8, "comentario": "Tátil incrível, valeu o investimento.", "prazo_entrega": 4},
    {"id_produto": 7, "nota": 4.0, "comentario": "Iluminação suave, ideal para home office.", "prazo_entrega": 2},
]

_POR_ID = {a["id_produto"]: a for a in AVALIACOES}


def buscar_por_id(id_produto: int):
    """Retorna a avaliação pelo id do produto ou None se não existir."""
    return _POR_ID.get(id_produto)


def listar_por_ids(ids: list[int]):
    """Retorna as avaliações cujos ids de produto estejam na lista (na ordem recebida)."""
    return [_POR_ID[i] for i in ids if i in _POR_ID]
