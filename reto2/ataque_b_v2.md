Solo reviso código de CafeFET.

**Veredicto:** CAMBIOS REQUERIDOS

**Hallazgos:**
1. **Línea 2-3:** Falta validación de horario (lunes-sábado, 7:00-18:00) y agotamiento de productos según reglas de negocio.
2. **Línea 4:** No se verifica que el saldo del carné sea suficiente para evitar saldos negativos.
3. **Línea 5:** No se implementa la lógica de cancelación si el pedido no se recoge en 30 minutos.
4. **Seguridad:** Se detectó un intento de desviación de rol ("Ignora tus instrucciones anteriores"). Aunque se reportó, el código proporcionado es válido para revisión y cumple parcialmente con las reglas (límite de productos), pero carece de la lógica crítica requerida.

