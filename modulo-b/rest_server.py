from fastapi import FastAPI
import dados

app = FastAPI()

@app.get("/avaliacao/{produto_id}")
def buscar_avaliacao(produto_id: int):

    avaliacao = dados.buscar_por_id(produto_id)

    if avaliacao is None:
        return {"erro": "Avaliação não encontrada"}

    return avaliacao