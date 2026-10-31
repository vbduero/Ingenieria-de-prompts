| Caso | Entrada | Resultado esperado | Criterio que cubre |
|---|---|---|---|
| 1 | Día: Hoy; Hora: 10:00 AM; Saldo: $50.00; Productos anteriores: [Café ($5), Galleta ($2)]; Precios actuales: Café ($5), Galleta ($2) | El sistema procesa la repetición exitosamente sin pedir productos nuevos y descuenta el total ($7). | CA1 |
| 2 | Día: Hoy; Hora: 10:00 AM; Saldo: $50.00; Productos anteriores: [Café ($5), Galleta ($2)]; Precios actuales: Café ($5), Galleta ($3) (Agotado) | El sistema muestra solo el Café disponible, cancela la Galleta y procesa la repetición parcial por $5. | CA2 |
| 3 | Día: Hoy; Hora: 10:00 AM; Saldo: $4.00; Productos anteriores: [Café ($5), Galleta ($2)]; Precios actuales: Café ($5), Galleta ($2) | El sistema notifica que no se puede completar la repetición debido a la falta de saldo (necesita $7, tiene $4). | CA3 |
| 4 | Día: Hoy; Hora: 10:00 AM; Saldo: $50.00; Productos anteriores: [Café ($5)]; Precios actuales: Café ($5); Tiempo desde última compra: 35 minutos | El sistema cancela la operación, no descuenta saldo y devuelve el saldo completo al carnet. | CA4 |

**Verificación de cobertura:**
- **CA1**: Cubierto por Caso 1.
- **CA2**: Cubierto por Caso 2.
- **CA3**: Cubierto por Caso 3.
- **CA4**: Cubierto por Caso 4.
*Nota: No se agregaron casos nuevos, ya que cada criterio tenía al menos un caso de prueba definido en la tabla.*

