"""Parte B · Evaluar prompts como código: clasificar mensajes del chat de CafeFET con dos versiones del prompt.

    uv run evalua.py
    uv run evalua.py --modelo qwen3.5:0.8b
"""
import argparse
import re
from comun import preguntar

CATEGORIAS = "PEDIDO|CANCELACION|RECLAMO|CONSULTA"

CASOS = [
    ("Me separan dos empanadas y un tinto para las 10?", "PEDIDO"),
    ("Cancelen mi pedido de las 12, ya no voy a ir.", "CANCELACION"),
    ("Me descontaron el saldo dos veces por el mismo almuerzo.", "RECLAMO"),
    ("¿Hasta qué hora reciben pedidos los sábados?", "CONSULTA"),
    ("Pedí 3 buñuelos y me entregaron 2.", "RECLAMO"),
    ("Quiero pedir un capuchino y un pandebono para las 3.", "PEDIDO"),
    # Ambiguos
    ("¿Me pueden guardar un jugo de mora para las 11?", "PEDIDO"),                       # suena a pregunta, pero es un pedido
    ("No alcancé a recoger mi pedido, ¿me van a devolver la plata?", "CONSULTA"),        # suena a reclamo, pero no hay falla
    ("¿Por qué me rechazan el pedido si tengo saldo?", "RECLAMO"),                       # es pregunta, pero algo funciona mal
    ("Ya no quiero el sándwich, mejor cámbienmelo por una arepa.", "CANCELACION"),       # cambia un pedido existente
]

V1 = """Clasifica el mensaje de un estudiante al chat de CafeFET en UNA categoría: PEDIDO, CANCELACION, RECLAMO o CONSULTA.
Responde solo con la categoría.
Mensaje: "{mensaje}\""""

V2 = """Clasifica el mensaje de un estudiante al chat de pedidos de CafeFET (cafetería de la universidad) en UNA categoría.
- PEDIDO: quiere pedir productos nuevos, aunque lo escriba como pregunta.
- CANCELACION: quiere cancelar o cambiar un pedido que ya hizo.
- RECLAMO: algo salió mal o el sistema funciona mal (cobros, productos que faltan, rechazos sin razón), aunque lo escriba como pregunta.
- CONSULTA: pregunta sobre reglas, horarios o saldo, sin que nada haya fallado.

Ejemplos:
"¿Me guardan un tinto para las 9?" -> PEDIDO
"Cambien mi chocolate por un café" -> CANCELACION
"¿Por qué me cobraron de más?" -> RECLAMO
"Si no recojo mi pedido, ¿qué pasa con mi saldo?" -> CONSULTA

Responde solo con PEDIDO, CANCELACION, RECLAMO o CONSULTA.
Mensaje: "{mensaje}\""""


def clasificar(plantilla, mensaje, modelo):
    r = preguntar(plantilla.format(mensaje=mensaje), modelo=modelo, num_predict=10)
    m = re.search(CATEGORIAS, r.message.content.upper().replace("CANCELACIÓN", "CANCELACION"))
    return m.group(0) if m else r.message.content.strip()


ap = argparse.ArgumentParser()
ap.add_argument("--modelo", default="qwen3.5:4b")
a = ap.parse_args()

print(f"Modelo: {a.modelo}\n")
for nombre, plantilla in [("v1", V1), ("v2", V2)]:
    ok = 0
    for mensaje, esperado in CASOS:
        obtenido = clasificar(plantilla, mensaje, a.modelo)
        if obtenido == esperado:
            ok += 1
        else:
            print(f"  [{nombre}] falló: «{mensaje}» -> {obtenido} (esperado {esperado})")
    print(f"{nombre}: {ok}/{len(CASOS)}\n")
