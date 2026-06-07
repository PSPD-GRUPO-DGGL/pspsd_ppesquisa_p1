from fastapi import FastAPI
import dados

app = FastAPI()

@app.get("/produto/{produto_id}")
def buscar_produto(produto_id: int):

    produto = dados.buscar_por_id(produto_id)

    if produto is None:
        return {"erro": "Produto não encontrado"}

    return produto