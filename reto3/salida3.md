| Caso | Entrada | Resultado esperado | Criterio que cubre |
| :--- | :--- | :--- | :--- |
| CP1 | Usuario: Estudiante registrado; Acción: Ver productos (Agotados: 50%, Disponibles: 30%) | Se muestran solo los 30% disponibles; no se permite añadir los agotados. | CA1 |
| CP2 | Usuario: Realiza pedido anticipado; Acción: Añadir 6º producto al carrito | El sistema bloquea la finalización y muestra mensaje de límite máximo (5 productos). | CA2 |
| CP3 | Usuario: Saldo = 10€; Precio pedido = 12€; Acción: Proceder al pago | Se descuenta el saldo hasta llegar a 0€, pero no se permite pagar si el saldo es insuficiente. | CA3 |
| CP4 | Usuario: Intenta pedir a las 19:00 (Fuera horario); Fecha: Lunes | El sistema notifica que no se aceptan pedidos fuera del horario de atención. | CA4 |
| CP5 | Usuario: Realiza pedido anticipado; Tiempo transcurrido: 35 minutos sin recoger | El sistema cancela el pedido y devuelve el saldo completo al carné. | CA5 |

**Línea de verificación:** Todos los criterios (CA1 a CA5) tienen al menos un caso de prueba asociado.

