"""Parte A · Del texto libre a datos: mensajes de pedido por chat de CafeFET → JSON validado con Pydantic.

    uv run reporte_json.py
"""
from typing import Literal, Optional
from pydantic import BaseModel, ValidationError
from comun import preguntar


class Producto(BaseModel):
    nombre: str
    cantidad: int


class Pedido(BaseModel):
    accion: Literal["nuevo", "modificar", "cancelar"]
    productos: list[Producto]
    hora_recogida: Optional[str]          # formato HH:MM; null si el mensaje no la dice
    para_llevar: Optional[bool]           # null si el mensaje no lo dice
    observaciones: Optional[str]


MENSAJES = [
    # Completos
    "Hola, para las 10:30 quiero 2 empanadas y un tinto, porfa.",
    "Me separan un jugo de mora sin azúcar y 3 pandebonos para llevar? Paso a las 12 y media.",
    "Ya no quiero el pedido de las 3 de la tarde, cancélenlo por favor.",
    "Cambien el capuchino de mi pedido por un chocolate caliente, lo demás igual. Lo recojo a las 4.",
    # Incompletos o ambiguos
    "Quiero lo mismo de siempre.",
    "Un almuerzo y unos buñuelos para más tarde.",
]

PROMPT = """Extrae los datos del mensaje de un estudiante que escribe al chat de pedidos de CafeFET (cafetería de la universidad).
- accion: "nuevo" si hace un pedido, "modificar" si cambia un pedido que ya hizo, "cancelar" si lo cancela.
- productos: cada producto con su cantidad (si no dice cantidad, 1).
- hora_recogida: en formato HH:MM de 24 horas.
- Si un dato no aparece en el mensaje, usa null. No inventes datos.

<mensaje>{mensaje}</mensaje>"""

for texto in MENSAJES:
    r = preguntar(PROMPT.format(mensaje=texto), formato=Pedido.model_json_schema())
    print(f"Mensaje: {texto}")
    try:
        p = Pedido.model_validate_json(r.message.content)   # falla si el JSON no cumple el esquema
        productos = ", ".join(f"{x.cantidad} x {x.nombre}" for x in p.productos) or "(ninguno)"
        print(f"  accion={p.accion} | productos=[{productos}] | hora={p.hora_recogida} "
              f"| para_llevar={p.para_llevar} | obs={p.observaciones}")
    except ValidationError as e:
        print(f"  JSON INVÁLIDO: {e.error_count()} error(es)\n  {r.message.content}")
    print()
