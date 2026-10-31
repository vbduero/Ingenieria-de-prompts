# Mide cuántos tokens lee de verdad cada modelo cuando el historial no cabe en num_ctx.
# Se envía una conversación de ~1.500 tokens (regla + respuesta larga + pregunta)
# y se mira prompt_eval_count en la respuesta de la API de Ollama.
# Uso: python3 medir_contexto.py
import json
import urllib.request

HISTORIAL = [
    {"role": "user", "content": "Regla: empieza SIEMPRE tu respuesta con «CafeFET responde:». ¿Entendido?"},
    {"role": "assistant", "content": "CafeFET responde: " + "pedido " * 1500},
    {"role": "user", "content": "¿Qué pasa si no recojo mi pedido en 30 minutos?"},
]


def tokens_leidos(modelo, num_ctx):
    cuerpo = json.dumps({
        "model": modelo,
        "messages": HISTORIAL,
        "think": False,
        "stream": False,
        "options": {"num_ctx": num_ctx, "num_predict": 1},
    }).encode()
    peticion = urllib.request.Request("http://localhost:11434/api/chat", cuerpo,
                                      {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(peticion))["prompt_eval_count"]


print("modelo     | num_ctx | tokens que el modelo realmente leyó")
for modelo in ("qwen-demo", "phi-demo"):
    for num_ctx in (512, 8192):
        print(f"{modelo:10} | {num_ctx:7} | {tokens_leidos(modelo, num_ctx)}")
