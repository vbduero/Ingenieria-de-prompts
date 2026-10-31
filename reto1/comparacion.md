
## Qué hicimos

Probamos tres prompts con el mismo modelo (qwen-demo, siempre con la misma configuración para que la comparación sea justa):

1. El prompt malo del caso: «Haz una función para crear pedidos.»
2. Un prompt nuevo con los 5 bloques (qué quiero, para quién, contexto, formato y restricciones) y las reglas de CafeFET dentro de `<reglas>`.
3. El mismo prompt nuevo, pero sin el bloque de restricciones.

Después probamos las funciones que salieron con 10 casos (un domingo, las 18:00, 6 productos, sin saldo, un producto agotado, etc.) para ver cuáles funcionaban bien.

## Prompt malo

Como no le dijimos nada, el modelo se lo inventó todo:

- Lo hizo en JavaScript y no en Python.
- Un pedido era un solo producto con una cantidad, no varios productos.
- Nadie pagaba nada: solo calculaba el total.
- Guardaba los pedidos en una variable global del navegador.
- No revisaba horario, ni máximo de productos, ni agotados.
- Los ejemplos eran manzanas y leche, en dólares.
- Ni siquiera terminó: la respuesta se cortó a la mitad porque gastó el espacio en explicaciones.

O sea, no es que el código esté mal; es que resolvió otro problema. No cumplió ninguna regla porque no tenía cómo saberlas.

"La verdad no me sorprendió del todo porque sin pistas el modelo improvisa, pero lo más raro fue que inventara ejemplos con manzanas y leche cobrados en dólares, ¡nada que ver con una cafetería de verdad!"

## Prompt nuevo

Mejoró mucho: pasó de 0 a 8 casos correctos de 10.

Lo que ahora sí hace bien:
- Está en Python, con el nombre y los datos que pedimos.
- Devuelve si el pedido se aceptó y el motivo.
- Revisa el máximo de 5 productos, que no quede saldo negativo y que no haya productos agotados.
- Descuenta el saldo.
- No usó base de datos ni cosas raras, y fue corto.

Lo que todavía falla:
- **Acepta pedidos el domingo.** En el comentario escribió «lunes a sábado», pero en el código nunca revisa el día. Lo copió y se le olvidó hacerlo.
- **No deja pedir a las 18:00 en punto**, aunque se lo dijimos clarito en las reglas.
- Trata los productos como diccionarios y no como objetos, aunque le dijimos que tenían atributos.
- Calcula la hora límite de recogida pero no la guarda en ningún lado, así que no sirve de nada.

Me parece que las reglas fáciles (un número, un sí/no) sí las cumple, y las que tienen dos condiciones a la vez (día y hora) o un límite exacto (las 18:00) se le pierden. Para arreglarlo se podrían poner ejemplos («domingo → no», «sábado 18:00 → sí») o pedirle que revise cada regla antes de responder.


"Para mí, el fallo más grave es que acepte pedidos los domingos y falle con la hora límite, porque eso significa que el código le va a rechazar compras a clientes que sí deberían poder comprar, o peor, aceptarles pedidos cuando la cafetería está cerrada."

## Variante sin restricciones

Solo quitamos la línea de restricciones y empeoró: 5 de 10.

- Como ya no tenía el límite de 40 líneas, escribió mucho más (explicaciones largas, mensajes de error largos) y **se quedó sin espacio antes de terminar**. La función nunca dice que el pedido se aceptó, pero igual le quita la plata al estudiante.
- Esta vez sí revisó el día, pero mal: **no deja pedir los lunes**.
- Deja pedir hasta las 18:59.
- Puso los precios en euros.
- No usó base de datos: eso ya lo había entendido con el resto del prompt.

Lo curioso es que solo cambiamos un bloque y cambiaron cosas que no tenían nada que ver (el día, la moneda). Con un modelo pequeño, cualquier cambio en el prompt cambia toda la respuesta. Las restricciones no son un detalle: sin el límite de tamaño, la respuesta salió incompleta.


"No me imaginé que quitar una sola línea de restricciones fuera a descontrolar tanto al modelo, al punto de cambiar la moneda a euros o bloquear los lunes sin ningún motivo. Me dejó clarísimo que cada instrucción cuenta."

## Conclusiones

1. Lo que más ayudó fue darle las reglas del negocio. Sin ellas el modelo adivina.
2. Poner las reglas dentro de `<reglas>` le sirvió para tenerlas separadas de la instrucción (hasta las puso como comentarios en el código).
3. Que una regla esté escrita no quiere decir que la cumpla. Hay que probar el código que genera.
4. El bloque de restricciones también sirve para que la respuesta no sea tan larga y no se corte.


