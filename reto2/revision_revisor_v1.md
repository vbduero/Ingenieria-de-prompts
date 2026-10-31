CAMBIOS REQUERIDOS

**Hallazgos:**
- **Línea 3:** Regla violada (Máximo 5 productos). El código permite hasta 6 (`len(productos) > 6`), lo cual es incorrecto.
- **Línea 4:** Regla violada (Saldo negativo). La lógica `saldo - sum(...) < -1000` solo rechaza si el saldo queda menor a -1000, permitiendo saldos negativos intermedios que son prohibidos. Debe ser `saldo - sum(...) < 0`.
- **Línea 5:** Regla violada (Horario). La condición `7 <= hora <= 18` es correcta para el horario de atención, pero la función no valida si los productos están agotados ni devuelve un mensaje claro en caso de error.
- **Legibilidad:** El uso de `est.saldo` sin contexto y la falta de mensajes informativos dificultan el mantenimiento.

**Corrección sugerida:**
```python
def crear_pedido(est, productos, hora):
    if len(productos) > 5: return False # Regla: Max 5 productos
    total = sum(p.precio for p in productos)
    if est.saldo - total < 0: return False # Regla: Saldo no negativo
    
    if not (7 <= hora <= 18): return False # Regla: Horario 7-18
    
    # Agregar validación de stock agotado aquí si aplica
    return True
```

