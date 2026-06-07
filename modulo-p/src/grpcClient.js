import grpc from "@grpc/grpc-js";
import protoLoader from "@grpc/proto-loader";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// CORREÇÃO: Lê as variáveis passadas pelo compose ou kubernetes
const A_HOST =
	process.env.URL_MODULO_A ||
	process.env.A_HOST ||
	"localhost:50051";

const B_HOST =
	process.env.URL_MODULO_B ||
	process.env.B_HOST ||
	"localhost:50052";

const PROTO_DIR = path.resolve(__dirname, "../../proto");

const produtoProtoPath = path.join(
	PROTO_DIR,
	"produto.proto"
);
const avaliacaoProtoPath = path.join(
	PROTO_DIR,
	"avaliacao.proto"
);

const produtoPackageDef = protoLoader.loadSync(
	produtoProtoPath,
	{
		keepCase: true,
		longs: String,
		enums: String,
		defaults: true,
		oneofs: true,
	}
);

const avaliacaoPackageDef = protoLoader.loadSync(
	avaliacaoProtoPath,
	{
		keepCase: true,
		longs: String,
		enums: String,
		defaults: true,
		oneofs: true,
	}
);

const produtoProto = grpc.loadPackageDefinition(
	produtoPackageDef
);
const avaliacaoProto = grpc.loadPackageDefinition(
	avaliacaoPackageDef
);

export function buscarProdutoCompleto(produtoId) {
	return new Promise((resolve, reject) => {
		const canalA = new produtoProto.produto.ProdutoService(
			A_HOST,
			grpc.credentials.createInsecure()
		);

		canalA.BuscarProduto(
			{ id: produtoId },
			(errProduto, produto) => {
				if (errProduto) {
					reject(errProduto);
					return;
				}

				const canalB = new avaliacaoProto.avaliacao
					.AvaliacaoService(
						B_HOST,
						grpc.credentials.createInsecure()
					);

				canalB.BuscarAvaliacao(
					{ id_produto: produtoId },
					(errAvaliacao, avaliacao) => {
						if (errAvaliacao) {
							reject(errAvaliacao);
							return;
						}

						const resultado = {
							id: produto.id,
							nome: produto.nome,
							categoria: produto.categoria,
							preco: produto.preco,
							disponivel: produto.disponivel,
							nota: avaliacao.nota,
							comentario: avaliacao.comentario,
							prazo_entrega: avaliacao.prazo_entrega,
						};

						resolve(resultado);
					}
				);
			}
		);
	});
}