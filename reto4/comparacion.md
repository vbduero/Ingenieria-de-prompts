
## Qué hicimos

El reto tiene dos partes:

| Parte | Técnica | Modelo | Archivos |
|---|---|---|---|
| A | Cadena de pensamiento: preguntar en una línea vs. pedir que evalúe paso a paso | `phi-demo` (sin `--think=false`, porque no razona solo) | `cot_sin.txt` → `salida_cot_sin.md`<br>`cot_con.txt` → `salida_cot_con.md` |
| B | La instrucción que se olvida: regla de formato como mensaje del chat vs. en `/set system`, con `num_ctx 512` | `qwen-demo --think=false` (y `phi-demo` como control, ver abajo) | `chat_contexto.txt` (las líneas que escribimos)<br>`salida_chat_qwen.md`, `salida_chat_phi.md`<br>`medir_contexto.py` → `medicion_contexto.txt` |

Comandos de la parte A:
```bash
ollama run phi-demo < cot_sin.txt > salida_cot_sin.md
ollama run phi-demo < cot_con.txt > salida_cot_con.md
```

## Parte A · Cadena de pensamiento

Usamos la misma función con errores de los retos anteriores (`crear_pedido`) y un caso inválido que rompe **las 4 reglas a la vez**: un domingo a las 10:00, 6 productos, uno agotado, saldo de $3.000 y un total de $3.800 (el saldo quedaría en -800). La función lo acepta.

Los dos prompts tienen las reglas en `<reglas>` y el código en `<codigo>`. Lo único que cambia es la pregunta:
- **Sin pasos:** «¿Por qué la función dejó pasar el pedido? Responde en una línea.»
- **Con pasos:** «Evalúa la función paso a paso con estos datos (len = 6, saldo = 3000, suma = 3800, hora = 10, domingo, un agotado). Para cada if escribe la condición, su valor y si retorna. Después compara con cada regla y escribe la corrección.»

Los 4 errores que tiene la función (los sabíamos de antemano):
1. `> 6` deja pasar 6 productos (el máximo es 5).
2. `< -1000` deja que el saldo quede negativo.
3. No revisa el día (acepta domingos).
4. No revisa los productos agotados.

| | Sin pasos | Con pasos |
|---|---|---|
| 6 productos (`> 6`) | ❌ | ❌ (y en la corrección dejó `> 6`) |
| Saldo negativo (`< -1000`) | ❌ | ❌ (y en la corrección dejó `-1000`) |
| No revisa el día | ❌ | ✅ |
| No revisa agotados | ✅ | ❌ |
| **Errores encontrados** | **1 de 4** | **1 de 4** |
| Tiempo | ~6 s | ~20 s |

Lo que vi:
- **Pedir los pasos no le sirvió para encontrar más errores.** Las dos versiones encontraron uno, solo que distinto.
- **El «paso a paso» fue de mentira.** No evaluó los `if` de la función: puso los datos como si fueran condiciones («`len(productos) = 6` → True», «`est.saldo = 3000` → True»). Nunca calculó `6 > 6` (False) ni `3000 - 3800 = -800 < -1000` (False), y justo ahí estaban los dos errores. Copió la forma de un razonamiento, pero sin hacer las cuentas.
- **Se inventó un `if` que no existe.** Escribió un paso 5, «día = domingo → la función retorna False», cuando la función no revisa el día. Además eso contradice el enunciado, que dice que la función **aceptó** el pedido.
- **La corrección arregla una sola cosa y deja lo demás igual.** Agregó la revisión del día (con los días en inglés, `'Monday'`…), pero dejó `> 6` y `-1000` tal cual y no revisó los agotados. Encima, dice que «ahora revisa correctamente las reglas».
- Dijo que el error estaba en la línea 4, pero el horario se revisa en la última línea (`return 7 <= hora <= 18`).

**Comparación con la práctica 9 de la guía:** allá la cadena de pensamiento sí funcionó, porque la función tenía un solo `if` con un solo número (`3 > 3`). Aquí hay 3 condiciones, 2 reglas que no se revisan y 6 datos. Creo que para un modelo pequeño (phi4-mini, 3.8B) es demasiado: le pedimos los pasos y escribió algo con cara de pasos, pero sin evaluarlos de verdad. Pedir el razonamiento ayuda cuando el modelo de verdad hace las cuentas; si solo repite los datos, no gana nada y se demora más del triple.

Una idea para mejorarlo (no la probamos): escribirle nosotros los `if` uno por uno («`if len(productos) > 6`: con len = 6, ¿es True o False?»), para que no tenga que adivinar qué evaluar.



"Sinceramente sí me sorprendió un poco al principio, porque uno siempre asume que obligar a la IA a desglosar las cosas hará que sea más lista, pero vi que si el modelo es pequeño solo simula que piensa sin hacer las cuentas reales."



## Parte B · La instrucción que se olvida

La regla de formato de nuestro caso: **«empieza SIEMPRE tu respuesta con "CafeFET responde:"»**. Las dos preguntas largas (al menos 400 palabras):
1. Cómo funciona el pago de un pedido con el saldo del carné y por qué el saldo nunca puede quedar negativo.
2. Qué pasa cuando un estudiante no recoge su pedido en 30 minutos.

- **Versión A:** `/set parameter num_ctx 512`, la regla como un mensaje del chat y luego las dos preguntas.
- **Versión B:** `/clear`, la regla en `/set system` y las mismas dos preguntas.

(Las líneas exactas están en `chat_contexto.txt`.)

### Con `qwen-demo`: no se olvidó nada (y no era lo que esperábamos)

| Versión | Dónde está la regla | Respuesta 1 | Respuesta 2 |
|---|---|---|---|
| A | Mensaje del chat | ✅ «CafeFET responde:» | ✅ «CafeFET responde:» |
| B | System prompt | ✅ «CafeFET responde:» | ✅ «CafeFET responde:» |

Según la guía, en la versión A la respuesta 2 ya no debía empezar con la frase. Pero las respuestas fueron largas (~490 palabras), así que no fue que la primera respuesta saliera corta y se quedara en la ventana.

Para saber qué pasó, medimos con la API de Ollama cuántos tokens leyó de verdad el modelo (`medir_contexto.py`, el mismo dato que muestra la práctica 14 con «tokens que el modelo realmente leyó»):

| Modelo | num_ctx | Tokens que el modelo realmente leyó (de ~1.550) |
|---|---|---|
| qwen-demo | 512 | **1565** ← leyó todo |
| qwen-demo | 8192 | 1565 |
| phi-demo | 512 | **16** ← solo el último mensaje |
| phi-demo | 8192 | 1547 |

Con el historial real de la versión A pasó lo mismo: antes de la pregunta 2, `qwen-demo` leyó **851 tokens** con `num_ctx 512`.

**Conclusión: en nuestra versión de Ollama (0.40.11), `qwen-demo` no recorta el historial aunque le pongamos `num_ctx 512`.** La regla nunca salió de la ventana, así que el modelo la siguió viendo y la cumplió. Tampoco fue deriva: la regla seguía ahí y la cumplió todas las veces. No pudimos probar el olvido con este modelo, y bajar a `num_ctx 384` (lo que sugiere la guía) tampoco cambia nada, porque igual lee todo.

### Con `phi-demo` (control): aquí sí se ve el olvido

Como `phi-demo` sí respeta el `num_ctx`, repetimos exactamente el mismo chat con ese modelo:

| Versión | Dónde está la regla | Respuesta 1 | Respuesta 2 |
|---|---|---|---|
| A | Mensaje del chat | ✅ «CafeFET responde: Al realizar un pedido…» | ❌ «CafeFET es una plataforma innovadora…» |
| B | System prompt | ✅ «CafeFET responde: Entender el proceso…» | ✅ «CafeFET responde: En CafeFET, si un estudiante…» |

Es justo lo que dice la práctica 14B.

### Por qué pasa (lo que entendí)

- El chat no tiene memoria: **en cada turno le reenvía al modelo toda la conversación** desde el principio.
- La ventana es de 512 tokens. La primera respuesta (~400 palabras) ya ocupa más que eso.
- En la pregunta 2, la conversación no cabe. Ollama **bota mensajes completos, empezando por el más viejo**: la regla, el «Entendido», la pregunta 1 y la respuesta 1. El modelo solo ve la pregunta 2 (por eso phi leyó 16 tokens). Ya no sabe que había una regla.
- Que también se bote la respuesta 1 es importante: si siguiera en la ventana, el modelo vería que empezó con «CafeFET responde:» y lo **imitaría**, aunque la regla ya no estuviera.
- **El system prompt nunca se bota.** Ollama siempre conserva el system prompt y el último mensaje. Por eso, en la versión B, la regla estuvo en las dos respuestas.

### Algo extra que noté

En las 8 respuestas los dos modelos **se inventaron cómo funciona CafeFET**: repartidores, multas, «criptografía de grado militar», puntos de reputación, impuestos… La regla real de los 30 minutos dice que el pedido se cancela y **se devuelve el saldo**, y los dos modelos dijeron que se le **cobra una multa** al estudiante, o sea, lo contrario. Es lo mismo del reto 1: si no le das las reglas, el modelo las inventa con mucha seguridad. Las dos respuestas 1 de `qwen-demo` además se cortaron a la mitad (el límite de 700 tokens del Modelfile).


## Conclusiones

1. **Pedir el razonamiento por escrito no siempre ayuda.** Con una función sencilla (práctica 9) sí sirve; con la nuestra, phi4-mini escribió pasos que parecían razonamiento, pero no evaluó nada, encontró los mismos errores (uno) y se demoró más.
2. **Hay que revisar el razonamiento, no solo la conclusión.** El paso a paso tenía un `if` inventado y una corrección incompleta que el modelo daba por buena.
3. **Lo que se dice en el chat se puede perder; lo que va en el system prompt se queda.** Cuando la conversación no cabe en la ventana, se botan los mensajes más viejos, y la regla del primer mensaje es la primera en irse.
4. **No hay que creer que el experimento funcionó o falló sin medir.** Con `qwen-demo` parecía que la regla resistía. En realidad el recorte nunca ocurrió, y eso solo lo supimos al contar los tokens.


