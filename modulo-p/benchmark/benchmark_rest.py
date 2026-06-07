import requests
import time

URL = "http://localhost:8000/rest/produto/1"
N = 100

inicio = time.perf_counter()

for _ in range(N):
    r = requests.get(URL)
    assert r.status_code == 200

fim = time.perf_counter()

tempo_total = fim - inicio

print("\n=== REST ===")
print(f"Requisições: {N}")
print(f"Tempo total: {tempo_total:.4f}s")
print(f"Tempo médio: {(tempo_total/N)*1000:.2f} ms")
print(f"RPS: {N/tempo_total:.2f}")