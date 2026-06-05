"""Módulo B — Versão REST/JSON (equivalente à versão gRPC).

Usa apenas a biblioteca padrão do Python (http.server) para evitar dependências.
Endpoints:
  GET /avaliacao/<id_produto>            -> avaliação de um produto
  GET /avaliacoes?ids=1,3,6             -> lista de avaliações por ids
  GET /health                            -> verificação de saúde

Execução:
    python app.py
Variáveis de ambiente:
    REST_B_PORT (padrão 8002)
"""
import json
import os
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

import dados


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, payload):
        corpo = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self):
        url = urlparse(self.path)
        partes = [p for p in url.path.split("/") if p]

        if url.path == "/health":
            return self._send(200, {"status": "ok", "modulo": "B", "tipo": "rest"})

        if len(partes) == 2 and partes[0] == "avaliacao":
            try:
                pid = int(partes[1])
            except ValueError:
                return self._send(400, {"erro": "id_produto inválido"})
            avaliacao = dados.buscar_por_id(pid)
            if avaliacao is None:
                return self._send(404, {"erro": f"Avaliação para id_produto={pid} não encontrada"})
            return self._send(200, avaliacao)

        if len(partes) == 1 and partes[0] == "avaliacoes":
            q = parse_qs(url.query)
            ids_raw = q.get("ids", [""])[0]
            try:
                ids = [int(x) for x in ids_raw.split(",") if x.strip()]
            except ValueError:
                return self._send(400, {"erro": "parâmetro 'ids' inválido"})
            # atraso proporcional ao tamanho da lista para paridade com o gRPC
            time.sleep(0.05 * len(ids))
            return self._send(200, dados.listar_por_ids(ids))

        return self._send(404, {"erro": "rota não encontrada"})

    def log_message(self, *args):
        pass  # silencia o log padrão por requisição


def main():
    port = int(os.getenv("REST_B_PORT", "8002"))
    httpd = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"[Modulo B] REST ouvindo em 0.0.0.0:{port}", flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
