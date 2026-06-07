from fastapi import FastAPI
from fastapi.responses import JSONResponse
from rest_client import buscar_produto_completo_rest

from grpc_client import buscar_produto_completo

app = FastAPI(
    title="Modulo P - API Gateway",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "modulo": "P",
        "status": "ativo"
    }


@app.get("/produto/{produto_id}")
def produto(produto_id: int):

    try:
        resultado = buscar_produto_completo(
            produto_id
        )

        return JSONResponse(
            status_code=200,
            content=resultado
        )

    except Exception as e:

        return JSONResponse(
            status_code=500,
            content={
                "erro": str(e)
            }
        )

@app.get("/rest/produto/{produto_id}")
def produto_rest(produto_id: int):

    return buscar_produto_completo_rest(
        produto_id
    )