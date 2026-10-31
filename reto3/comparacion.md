
## Qué hicimos

Partimos del requisito nuevo de CafeFET: «Que el estudiante pueda repetir su último pedido con un solo clic». Lo pasamos por una cadena de tres prompts, donde la salida de uno es la entrada del siguiente (todo con `qwen-demo`):

| Paso | Prompt | Salida | Qué hace |
|---   |---     |---     |---       |     
| 1    | `prompt1.txt` | `salida1.md` | Few-shot: convierte el requisito en historia de usuario. Le dimos dos ejemplos propios de CafeFET (ver saldo y agotados) |
| 2    | `prompt2.txt` | `salida2.md` | Formato fijo: la historia va dentro de `<historia>` y pedimos de 3 a 5 criterios Dado / Cuando / Entonces con las reglas del caso |
| 3    | `prompt3.txt` | `salida3.md` | Tabla de casos de prueba + auto-verificación («revisa que cada criterio tenga al menos un caso…») |

Después revisamos la cadena, encontramos el paso donde apareció el primer error, corregimos ese prompt y volvimos a ejecutar desde ahí:

| Paso | Prompt | Salida |
|---|---|---|
| 2 corregido | `prompt2_corregido.txt` | `salida2_corregida.md` |
| 3 (otra vez, la misma instrucción) | `prompt3_corregido.txt` | `salida3_corregida.md` |

## Paso 1 · Historia de usuario: salió bien

> Como estudiante, quiero poder repetir mi último pedido con un solo clic, para agilizar la realización de mis compras y ahorrar tiempo.

Copió el formato de los ejemplos (una línea, «Como…, quiero…, para…») y no agregó nada raro. Los ejemplos funcionaron: no tuvimos que explicarle el formato.


"La historia de usuario me parece bastante buena porque es clara, corta y sigue la estructura típica. Lo único que le añadiría para que quede perfecta es especificar si al repetir el pedido te carga los mismos productos en el carrito o si los paga de una vez."


## Paso 2 · Criterios de aceptación: aquí apareció el primer error

Pedimos los criterios «usando las reglas de negocio del caso» y el modelo hizo exactamente eso, pero **se olvidó de la historia**. Los 5 criterios son las 5 reglas de CafeFET copiadas una por una (agotados, máximo 5, saldo, horario, 30 minutos) para un pedido normal. **Ninguno habla de repetir el último pedido.**

Otros problemas:
- El CA4 se contradice: «Dado que estoy **dentro** del horario… Cuando intento pedir **fuera** de este periodo…».
- Pedimos cada criterio en tres líneas y los escribió en una sola.

Creo que pasó porque las reglas ocupaban casi todo el prompt y la historia era una sola línea al final. El modelo le hizo más caso a la lista larga que a la historia.

## Paso 3 · Tabla de casos (cadena original): heredó el error y agregó otros

Como los criterios no hablaban de repetir pedidos, **la tabla tampoco**: probó un sistema de pedidos normal, no la funcionalidad nueva. Además:
- CP1 tiene datos sin sentido: «Agotados: 50%, Disponibles: 30%».
- CP3 se contradice: «se descuenta el saldo hasta llegar a 0, pero no se permite pagar si el saldo es insuficiente». O sea, inventó un pago parcial.
- Usó euros (€).
- La auto-verificación dijo «todos los criterios tienen al menos un caso», y era cierto. El problema es que **los criterios estaban mal desde antes**: la auto-verificación solo revisa lo que le pasamos, no se da cuenta si lo que le pasamos ya venía mal.



Sí, me lo esperaba totalmente. En una cadena de prompts, cada paso construye sobre lo que entregó el anterior; si la entrada del paso 3 ya venía mal desde el paso 2, era imposible que la IA adivinara por arte de magia lo que debía probar.


## Nota de corrección · Qué paso corregimos y por qué

**Corregimos el prompt 2**, porque fue el primer paso con error. El paso 1 estaba bien, y los errores del paso 3 venían arrastrados del paso 2. Si hubiéramos corregido el paso 3, igual habría probado la funcionalidad equivocada.

Cambios en `prompt2_corregido.txt`:
1. **Pusimos la historia primero** y las reglas después.
2. Agregamos: «Todos los criterios deben tratar sobre la acción de la historia: repetir el último pedido. No escribas criterios sobre hacer un pedido normal.»
3. Le pedimos un criterio para el caso exitoso y otros para cuando una regla impide repetir el pedido (con dos ejemplos: saldo que ya no alcanza y producto que ahora está agotado).
4. Le dijimos que esas reglas «son las únicas que existen; no inventes otras».

El prompt 3 no lo tocamos (misma instrucción); solo cambió lo que va dentro de `<criterios>`.

### Resultado después de corregir

Paso 2 corregido: **los 4 criterios ahora son sobre repetir el pedido** (repetición exitosa, producto agotado, saldo insuficiente, 30 minutos). Mucho mejor, pero no perfecto:
- **CA2 inventó una regla:** si un producto está agotado, quita ese producto y sigue con el resto. Las reglas solo dicen que los agotados no se pueden pedir; no dicen si se cancela todo o se hace un pedido parcial. Esa decisión la debería tomar el equipo, no el modelo.
- **CA4 entendió mal la regla de los 30 minutos.** La regla es sobre recoger el pedido; el modelo la aplicó a «el tiempo desde la última compra», como si no se pudiera repetir un pedido de hace más de 30 minutos. Eso no tiene sentido.
- No hay criterio para repetir el pedido un domingo o fuera del horario.
- Siguió escribiendo cada criterio en una línea en vez de tres.

Paso 3 corregido: la tabla ahora sí prueba la funcionalidad nueva, con datos más concretos (café $5, galleta $2, saldo $50 o $4). Pero:
- Puso «Día: Hoy» en todos los casos, así que no prueba el horario aunque pedimos día y hora concretos.
- El caso 4 se contradice: «no descuenta saldo y devuelve el saldo completo».
- Los precios no parecen de una cafetería en Colombia.
- La auto-verificación otra vez dijo que todo estaba cubierto. Es cierto para los 4 criterios, pero no detectó que falta la regla del horario ni la del máximo de 5 productos.


"El error más grave es que el CA2 haya inventado la regla del «pedido parcial con agotados», porque cambiar la lógica del negocio sin consultar puede confundir a los clientes y generar cobros raros. Para solucionarlo, volvería a corregir el paso 2."


## Conclusiones

1. **Dividir en pasos ayudó a encontrar el error.** Como cada salida quedó guardada, pudimos ver que el paso 1 estaba bien y que el problema empezó en el paso 2. Con un solo prompt gigante no sabríamos dónde se dañó.
2. **Un error en un paso se arrastra a todos los siguientes.** La tabla del paso 3 salió bien hecha, pero probando lo que no era.
3. **Los ejemplos (few-shot) controlan muy bien el formato:** la historia salió perfecta. La instrucción «escribe en tres líneas» la ignoró las dos veces.
4. **La auto-verificación es limitada:** solo revisa lo que tiene enfrente. No sabe si los criterios estaban bien ni si falta alguna regla.
5. **Aunque le digas «no inventes reglas», el modelo llena los huecos:** cuando la regla no dice qué hacer (pedido parcial con agotados), decide por su cuenta.

