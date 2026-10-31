
## Qué hicimos

Es el único reto con Python. Copiamos y adaptamos a CafeFET los dos scripts del repositorio de la clase (`reporte_json.py` y `evalua.py`). También copiamos `comun.py`, que es la función que habla con Ollama.

| Parte | Script | Salida | Qué hace |
|---|---|---|---|
| A | `reporte_json.py` | `salida_reporte_json.txt` | Convierte mensajes de pedido por chat en datos (JSON) que Pydantic valida |
| B | `evalua.py` | `salida_evalua_4b.txt`<br>`salida_evalua_0.8b.txt` | Compara dos versiones de un prompt de clasificación con 10 casos etiquetados a mano |

Cómo se ejecuta (desde esta carpeta, con el entorno del repositorio de la clase):
```bash
uv run --project ../../Diplomado/fet-diplomadoIA-prompting-p2 python reporte_json.py
uv run --project ../../Diplomado/fet-diplomadoIA-prompting-p2 python evalua.py
uv run --project ../../Diplomado/fet-diplomadoIA-prompting-p2 python evalua.py --modelo qwen3.5:0.8b
```
(Si los scripts se copian a la carpeta `scripts/` del repositorio, basta con `uv run reporte_json.py`).

## Parte A · Del texto libre a datos (JSON validado)

La clase de Pydantic `Pedido` tiene 5 campos:

| Campo | Tipo | Valores |
|---|---|---|
| `accion` | `Literal` | `nuevo`, `modificar`, `cancelar` |
| `productos` | lista de `Producto` | cada uno con `nombre` y `cantidad` |
| `hora_recogida` | texto o `null` | HH:MM |
| `para_llevar` | sí/no o `null` | |
| `observaciones` | texto o `null` | |

Le pasamos el esquema a Ollama (`format=Pedido.model_json_schema()`), así que el modelo **solo puede** responder con un JSON que tenga esa forma. Después Pydantic lo revisa (`model_validate_json`).

Resultados con `qwen3.5:4b`:

| # | Mensaje | Lo que extrajo | ¿Bien? |
|---|---|---|---|
| 1 | «Hola, para las 10:30 quiero 2 empanadas y un tinto, porfa.» | nuevo · 2 empanadas, 1 tinto · 10:30 | ✅ |
| 2 | «Me separan un jugo de mora sin azúcar y 3 pandebonos para llevar? Paso a las 12 y media.» | nuevo · 1 jugo de mora sin azúcar, 3 pandebono · 12:30 · para llevar | ⚠️ «sin azúcar» quedó en el nombre y no en observaciones |
| 3 | «Ya no quiero el pedido de las 3 de la tarde, cancélenlo por favor.» | cancelar · sin productos · hora null | ✅ (pero perdimos «el de las 3», que sirve para saber cuál pedido cancelar) |
| 4 | «Cambien el capuchino de mi pedido por un chocolate caliente… Lo recojo a las 4.» | modificar · 1 chocolate caliente · 16:00 | ⚠️ Supuso que «las 4» es de la tarde, y no dejó registrado que se quita el capuchino |
| 5 | **Incompleto:** «Quiero lo mismo de siempre.» | nuevo · **sin productos** · todo null | ⚠️ JSON válido, pero es un pedido vacío |
| 6 | **Ambiguo:** «Un almuerzo y unos buñuelos para más tarde.» | nuevo · 1 almuerzo, 1 buñuelos · hora null · obs «para más tarde» | ⚠️ «unos buñuelos» quedó como 1 |

Los 6 JSON pasaron la validación de Pydantic. Ninguno salió con formato malo.

**¿Qué hace el modelo cuando falta un dato?**
- **Casi siempre pone `null`, como le pedimos:** no se inventó horas en los mensajes 3, 5 y 6, ni puso `para_llevar` donde no lo decía. Que el esquema permita `null` y el prompt diga «no inventes» funcionó.
- En el mensaje 6 hizo algo inteligente: como «más tarde» no es una hora, la dejó en `null` y guardó el texto en observaciones.
- **Pero completa con supuestos cuando el dato está «a medias»:** «las 4» → 16:00, «unos buñuelos» → 1 (porque le dijimos «si no dice cantidad, 1»). No son inventos locos, pero son decisiones que tomó el modelo sin avisar.
- **Lo más importante: un JSON válido no es un pedido válido.** «Quiero lo mismo de siempre» salió como un pedido nuevo sin productos, y Pydantic lo aceptó, porque una lista vacía cumple el esquema. Pydantic revisa la **forma**, no el **sentido**. Para eso hay que agregar reglas en el código (por ejemplo, que un pedido nuevo tenga entre 1 y 5 productos, como dicen las reglas de CafeFET) o un campo para que el modelo diga «me falta información».




"Yo creo que lo más inteligente sería conectar ese «lo mismo de siempre» con el requisito del reto 3: que el sistema busque automáticamente su última compra en la base de datos y la cargue."




## Parte B · Evaluación A/B de prompts

Clasificamos mensajes del chat de CafeFET en 4 categorías: **PEDIDO, CANCELACION, RECLAMO, CONSULTA**. Etiquetamos 10 casos a mano: 6 claros y **4 ambiguos**:

| Caso ambiguo | Etiqueta | Por qué es difícil |
|---|---|---|
| «¿Me pueden guardar un jugo de mora para las 11?» | PEDIDO | Es una pregunta, pero en realidad está pidiendo |
| «No alcancé a recoger mi pedido, ¿me van a devolver la plata?» | CONSULTA | Suena a queja, pero nada falló: la regla dice que se devuelve el saldo |
| «¿Por qué me rechazan el pedido si tengo saldo?» | RECLAMO | Es una pregunta, pero algo funciona mal |
| «Ya no quiero el sándwich, mejor cámbienmelo por una arepa.» | CANCELACION | Menciona un producto nuevo, pero está cambiando un pedido que ya hizo |

- **v1 (zero-shot):** solo la lista de categorías.
- **v2:** una definición de cada categoría (con «aunque lo escriba como pregunta») y 4 ejemplos.

### Resultados

| | qwen3.5:4b | qwen3.5:0.8b |
|---|---|---|
| v1 | 8/10 | 4/10 |
| v2 | **9/10** | **7/10** |

| Caso | 4b v1 | 4b v2 | 0.8b v1 | 0.8b v2 |
|---|---|---|---|---|
| Me descontaron el saldo dos veces | ✅ | ✅ | ❌ PEDIDO | ✅ |
| ¿Hasta qué hora reciben pedidos los sábados? | ✅ | ✅ | ❌ PEDIDO | ✅ |
| Pedí 3 buñuelos y me entregaron 2 | ✅ | ✅ | ❌ PEDIDO | ❌ PEDIDO |
| *(ambiguo)* No alcancé a recoger mi pedido, ¿me devuelven la plata? | ❌ RECLAMO | ❌ RECLAMO | ❌ PEDIDO | ❌ RECLAMO |
| *(ambiguo)* ¿Por qué me rechazan el pedido si tengo saldo? | ✅ | ✅ | ❌ PEDIDO | ✅ |
| *(ambiguo)* Cámbienmelo por una arepa | ❌ PEDIDO | ✅ | ❌ PEDIDO | ❌ RECLAMO |
| Los otros 4 casos | ✅ | ✅ | ✅ | ✅ |

### Qué vimos

- **La v2 mejoró en los dos modelos**, y mucho más en el pequeño (de 4 a 7). El modelo grande ya sabía casi todo; al pequeño, las definiciones y los ejemplos le dieron lo que no sabía.
- **El 0.8b con v1 respondía PEDIDO a casi todo.** Creo que se dejaba llevar por la palabra «pedido», que sale en muchos mensajes, o porque es la primera categoría de la lista. Con las definiciones dejó de hacerlo.
- **Casos que fallan en v1 y no en v2:**
  - En el 4b: «cámbienmelo por una arepa». Sin la definición, el modelo vio «arepa» y pensó que era un pedido nuevo; la v2 dice que cambiar un pedido es CANCELACION.
  - En el 0.8b: «me descontaron dos veces», «¿hasta qué hora…?» y «¿por qué me rechazan…?».
- **Un caso falló en todas las versiones:** «No alcancé a recoger mi pedido, ¿me van a devolver la plata?». Todos dijeron RECLAMO (o PEDIDO). Siendo honestos, **nuestra etiqueta es discutible**: el estudiante puede estar preocupado o molesto, y una persona también podría decir que es un reclamo. Cuando ni nosotros estamos seguros, no es justo exigirle al modelo que acierte. Para arreglarlo habría que dejar más clara la definición («si no hubo error del sistema, es CONSULTA») o aceptar que ese caso es ambiguo.
- **Ojo con hacer trampa sin querer:** los ejemplos de la v2 se parecen bastante a algunos casos de prueba (por ejemplo, «Cambien mi chocolate por un café» y «cámbienmelo por una arepa»). Eso puede inflar un poco el resultado de la v2. Lo correcto es que los ejemplos del prompt y los casos de prueba sean distintos, como en el machine learning, donde no se evalúa con los mismos datos con los que se entrena.
- **Con 10 casos, un acierto cambia el resultado en 10 puntos.** Sirve para comparar, pero para decidir en serio harían falta más casos.



**[ ¿cuál etiqueta le pondría yo a «no alcancé a recoger mi pedido…»?]**

A esa frase le pondría etiqueta de CONSULTA, porque el estudiante solo está preguntando una regla que ya existe (si le devuelven la plata), no está alegando que el sistema falló. Y sobre el modelo pequeño, para mí sí vale la pena usar el de 0.8b.




## Conclusiones

1. **El JSON Schema garantiza la forma, no el contenido.** Los 6 mensajes salieron con un JSON válido, pero uno era un pedido vacío. Las reglas del negocio hay que revisarlas aparte.
2. **Cuando falta un dato, el modelo usa `null` si se lo permitimos**, pero cuando el dato está a medias («las 4», «unos») completa con supuestos sin avisar.
3. **Las definiciones y los ejemplos ayudan más cuanto más pequeño es el modelo:** 4b pasó de 8 a 9 y 0.8b de 4 a 7.
4. **Medir con casos de prueba es mejor que opinar.** Sin el script habríamos dicho «la v2 se ve mejor»; con el script sabemos cuánto mejor, en qué casos y con qué modelo.


