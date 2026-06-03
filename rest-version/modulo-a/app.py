"""Módulo A — Versão REST/JSON (equivalente à versão gRPC).

Usa apenas a biblioteca padrão do Python (http.server) para evitar dependências.
Endpoints:
  GET /produto/<id>                     -> dados básicos de um produto
  GET /produtos?categoria=&limite=      -> lista de produtos
  GET /health                           -> verificação de saúde

Execução:
    python app.py
Variáveis de ambiente:
    REST_A_PORT (padrão 8001)
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
            return self._send(200, {"status": "ok", "modulo": "A", "tipo": "rest"})

        if len(partes) == 2 and partes[0] == "produto":
            try:
                pid = int(partes[1])
            except ValueError:
                return self._send(400, {"erro": "id inválido"})
            produto = dados.buscar_por_id(pid)
            if produto is None:
                return self._send(404, {"erro": f"Produto com id={pid} não encontrado"})
            return self._send(200, produto)

        if len(partes) == 1 and partes[0] == "produtos":
            q = parse_qs(url.query)
            categoria = q.get("categoria", [""])[0]
            limite = int(q.get("limite", ["0"])[0] or 0)
            time.sleep(0.05 * max(len(dados.listar(categoria, limite)), 0))
            return self._send(200, dados.listar(categoria, limite))

        return self._send(404, {"erro": "rota não encontrada"})

    def log_message(self, *args):
        pass  # silencia o log padrão por requisição


def main():
    port = int(os.getenv("REST_A_PORT", "8001"))
    httpd = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"[Modulo A] REST ouvindo em 0.0.0.0:{port}", flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
