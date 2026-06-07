import express from "express";
import { 
  buscarProdutoCompleto 
} from "./grpcClient.js";
import { 
  buscarProdutoCompletoRest 
} from "./restClient.js";

const app = express();

const PORT = process.env.PORT || 3000;

app.get("/", (req, res) => {
  res.json({
    modulo: "P",
    status: "ativo",
  });
});

app.get("/produto/:produto_id", async (req, res) => {
  try {
    const produtoId = parseInt(req.params.produto_id);
    const resultado = await buscarProdutoCompleto(
      produtoId
    );

    res.status(200).json(resultado);
  } catch (error) {
    res.status(500).json({
      erro: error.message,
    });
  }
});

app.get("/rest/produto/:produto_id", async (req, res) => {
  try {
    const produtoId = parseInt(req.params.produto_id);
    const resultado = await buscarProdutoCompletoRest(
      produtoId
    );

    res.status(200).json(resultado);
  } catch (error) {
    res.status(500).json({
      erro: error.message,
    });
  }
});

app.listen(PORT, () => {
  console.log(
    `Modulo P - API Gateway ouvindo na porta ${PORT}`
  );
});
