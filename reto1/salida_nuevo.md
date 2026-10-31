```python
from datetime import datetime, timedelta
from typing import Tuple, List, Dict, Any

def crear_pedido(
    estudiante: Dict[str, Any], 
    productos: List[Dict[str, Any]], 
    fecha_hora: datetime
) -> Tuple[bool, str]:
    """
    Crea un pedido validando reglas de negocio y descuenta saldo.
    
    Args:
        estudiante: Diccionario con 'saldo' (float).
        productos: Lista de diccionarios con 'nombre', 'precio', 'agotado'.
        fecha_hora: datetime del pedido.
    
    Returns:
        Tuple[bool, str]: (True, "OK") si se crea; (False, motivo) si no.
    """
    # Validar rango horario (Lun-Sab 07:00-18:00)
    if not (7 <= fecha_hora.hour < 18):
        return False, "Horario inválido"
    
    # Validar cantidad de productos (1-5)
    if len(productos) == 0 or len(productos) > 5:
        return False, "Cantidad inválida"
    
    # Calcular total y verificar saldo
    total = sum(p['precio'] for p in productos if not p['agotado'])
    if estudiante['saldo'] < total:
        return False, "Saldo insuficiente"
    
    # Verificar disponibilidad de productos
    disponibles = [p for p in productos if not p['agotado']]
    if len(disponibles) != len(productos):
        return False, "Productos agotados"
    
    # Validar saldo final (nunca negativo)
    nuevo_saldo = estudiante['saldo'] - total
    if nuevo_saldo < 0:
        return False, "Saldo insuficiente"
    
    # Actualizar saldo y calcular hora límite
    estudiante['saldo'] = nuevo_saldo
    hora_limite = fecha_hora + timedelta(minutes=30)
    
    return True, "OK"
```

