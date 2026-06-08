import axios from "axios";

// Aceita os nomes usados pelo docker-compose/k8s (URL_REST_A/B) e
// tambem MODULO_A_URL/MODULO_B_URL, com fallback para execucao local.
const MODULO_A_URL =
  process.env.URL_REST_A ||
  process.env.MODULO_A_URL ||
  "http://localhost:8001";
const MODULO_B_URL =
  process.env.URL_REST_B ||
  process.env.MODULO_B_URL ||
  "http://localhost:8002";

export async function buscarProdutoCompletoRest(
  produtoId
) {
  const produtoResponse = await axios.get(
    `${MODULO_A_URL}/produto/${produtoId}`
  );

  const avaliacaoResponse = await axios.get(
    `${MODULO_B_URL}/avaliacao/${produtoId}`
  );

  return {
    ...produtoResponse.data,
    ...avaliacaoResponse.data,
  };
}
