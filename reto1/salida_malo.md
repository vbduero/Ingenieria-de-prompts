Aquí tienes un ejemplo completo de cómo crear una función para gestionar pedidos en **JavaScript**. Este código incluye la lógica para validar los datos, calcular el total y registrar el pedido en una lista.

Puedes copiar y pegar este bloque directamente en tu navegador o proyecto.

```javascript
// Función principal para crear un pedido
function crearPedido(producto, cantidad, precioUnitario) {
  
  // 1. Validación de entrada (Input Validation)
  if (!producto || typeof producto !== 'string') {
    throw new Error("El nombre del producto debe ser una cadena de texto no vacía.");
  }
  
  if (cantidad <= 0 || !Number.isInteger(cantidad)) {
    throw new Error("La cantidad debe ser un número entero mayor a cero.");
  }
  
  if (precioUnitario < 0 || !Number.isFinite(precioUnitario)) {
    throw new Error("El precio unitario debe ser un número no negativo y finito.");
  }

  // 2. Cálculos
  const total = cantidad * precioUnitario;

  // 3. Estructura del objeto pedido
  const nuevoPedido = {
    id: Date.now(), // Genera un ID único basado en la fecha actual
    producto: producto,
    cantidad: cantidad,
    precioUnitario: precioUnitario,
    total: total,
    fechaCreacion: new Date().toLocaleString()
  };

  // 4. Simulación de almacenamiento (Aquí iría tu base de datos o API)
  // En este ejemplo, lo guardamos en un array global para demostración
  if (!window.pedidos) {
    window.pedidos = [];
  }
  
  window.pedidos.push(nuevoPedido);

  console.log(`✅ Pedido creado exitosamente: ${producto} (${cantidad} x $${precioUnitario})`);
  console.log(`   Total a pagar: $${total}`);
  console.log(`   ID del pedido: ${nuevoPedido.id}`);

  return nuevoPedido;
}

// --- Ejemplo de uso ---

// Crear un pedido de manzanas
const pedido1 = crearPedido("Manzanas Rojas", 5, 2.50);

// Crear otro pedido de leche
const pedido2 = crearPedido("Leche Entera", 3, 1.80);

// Verificar que se guardaron (simulando una base de datos)
console.log("\n--- Pedidos registrados en el sistema ---");
window.pedidos.forEach((p, index) => {
  console.log(`${index + 1}. ${p.producto} - Total: $${p.total}`);
});
```

### Características clave de esta función:

1.  **Validación estricta:** Evita errores comunes como cantidades negativas o productos vacíos lanzando excepciones claras (`throw new Error`).
2.  **Cálculo automático:** Calcula el total multiplicando cantidad por precio sin que tengas que hacerlo manualmente.
3.  **Generación de ID:** Asigna un identificador único basado en la hora actual (`Date.now()`), útil para rastrear pedidos.
4.  **

