```python
from datetime import datetime, timedelta
from typing import Tuple, List, Dict, Any

def crear_pedido(
    estudiante: Dict[str, Any], 
    productos: List[Dict[str, Any]], 
    fecha_hora: datetime
) -> Tuple[bool, str]:
    """
    Crea un pedido para el sistema de pedidos anticipados de CafeFET.
    
    Valida las reglas de negocio antes de procesar el pedido:
    - Horario válido (lunes a sábado, 7:00-18:00).
    - Cantidad de productos entre 1 y 5.
    - Saldo suficiente en el carné sin quedar negativo.
    - Productos no agotados.
    
    Si todo es válido, descuenta el saldo y calcula la hora límite de recogida.
    
    Args:
        estudiante (dict): Diccionario con al menos las claves 'nombre' y 'saldo'.
        productos (list): Lista de diccionarios con claves 'nombre', 'precio' y 'agotado'.
        fecha_hora (datetime): Fecha y hora en la que se realiza el pedido.
        
    Returns:
        tuple: (bool, str) donde bool indica si el pedido fue creado exitosamente 
               y str es el motivo ("OK" o una explicación de rechazo).
    """
    
    # Validar día de la semana (lunes=0 a sábado=5)
    if fecha_hora.weekday() < 1 or fecha_hora.weekday() > 5:
        return False, "El pedido solo se acepta de lunes a sábado."
    
    # Validar hora (7:00 a 18:00 en punto)
    if fecha_hora.hour < 7 or fecha_hora.hour > 18:
        return False, "El horario de pedidos es de 7:00 a 18:00."
    
    # Validar cantidad de productos (mínimo 1, máximo 5)
    if not productos or len(productos) < 1:
        return False, "Se requiere al menos un producto en el pedido."
    
    if len(productos) > 5:
        return False, "El pedido no puede contener más de 5 productos."
    
    # Validar saldo y disponibilidad de productos
    total_precio = 0
    productos_seleccionados = []
    
    for producto in productos:
        if producto.get("agotado", False):
            return False, f"El producto '{producto['nombre']}' está agotado."
        
        precio = producto.get("precio", 0)
        total_precio += precio
        productos_seleccionados.append(producto)
    
    # Validar saldo del estudiante (nunca negativo)
    saldo_actual = estudiante.get("saldo", 0)
    if saldo_actual < total_precio:
        return False, f"Saldo insuficiente. Necesitas {total_precio}€, tienes {saldo_actual}€."
    
    # Si todo es válido, procesar el pedido
    estudiante["saldo"] -= total_precio
    
    hora_limite_recogida = fecha_hora + timedelta(minutes=30)

