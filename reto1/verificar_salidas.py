"""Ejecuta las funciones generadas por el modelo (salida_nuevo.md y salida_variante.md)
con casos concretos de CafeFET para comprobar qué reglas cumplen.

Uso (desde reto1/, con el entorno del repo de clase):
    uv run --project <ruta>/fet-diplomadoIA-prompting-p2 python verificar_salidas.py salida_nuevo.md salida_variante.md
"""
import re, sys
from datetime import datetime
def cargar(f):
    code = re.search(r"```python\n(.*?)(```|\Z)", open(f, encoding="utf-8").read(), re.S).group(1)
    ns = {}; exec(code, ns); return ns["crear_pedido"]
P = lambda precio=2000, agotado=False: {"nombre": "x", "precio": precio, "agotado": agotado}
casos = [
    ("Válido: martes 10:00, 2 productos, saldo 10000", datetime(2026,10,27,10,0), [P(),P()], 10000),
    ("Lunes 10:00 (válido)",                datetime(2026,10,26,10,0), [P()], 10000),
    ("Domingo 10:00 (inválido)",            datetime(2026,10,25,10,0), [P()], 10000),
    ("18:00 en punto (válido)",             datetime(2026,10,27,18,0), [P()], 10000),
    ("18:45 (inválido)",                    datetime(2026,10,27,18,45), [P()], 10000),
    ("6 productos (inválido)",              datetime(2026,10,27,10,0), [P()]*6, 100000),
    ("0 productos (inválido)",              datetime(2026,10,27,10,0), [], 10000),
    ("Saldo exacto 4000, total 4000 (válido)", datetime(2026,10,27,10,0), [P(),P()], 4000),
    ("Saldo 3000, total 4000 (inválido)",   datetime(2026,10,27,10,0), [P(),P()], 3000),
    ("Producto agotado (inválido)",         datetime(2026,10,27,10,0), [P(),P(agotado=True)], 10000),
]
for f in sys.argv[1:]:
    fn = cargar(f); print(f"\n== {f}")
    for nombre, fh, prods, saldo in casos:
        est = {"nombre": "Ana", "saldo": saldo}
        print(f"  {nombre:42} -> {fn(est, prods, fh)}  saldo final={est['saldo']}")
