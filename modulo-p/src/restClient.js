import axios from "axios";

const MODULO_A_URL = 
  process.env.MODULO_A_URL || "http://localhost:8001";
const MODULO_B_URL = 
  process.env.MODULO_B_URL || "http://localhost:8002";

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
