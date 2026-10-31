# Taller · Ingeniería de prompts y de contexto — Grupo 5

Diplomado en Ingeniería de Software con IA y Sistemas Agénticos · FET · Sesión 03

## Integrantes
- Valentina Bermeo Duero
- Sergio Andres Narvaez Cachaya
- Juan Esteban Cuchimba Perdomo

## Caso
**Caso 2 · CafeFET** — pedidos anticipados a la cafetería.

## Modelos y equipo
- Ollama 0.40.11
- Modelos: `qwen-demo` (qwen3.5:4b, temperatura 0, semilla 42), `phi-demo` (phi4-mini), `revisor-cafefet` (v1 y v2)
- Equipo: MacBook Air · Apple M1 (CPU y GPU integradas) · 8 GB de RAM · macOS

## Contenido
| Carpeta  | Reto                                                               |
|---       |---                                                                 |
| `reto1/` | Rescatar un prompt malo (fórmula base y delimitadores)             |
| `reto2/` | System prompt del revisor, Modelfile v1 y v2, ataques de inyección |
| `reto3/` | Del requisito a los casos de prueba (encadenamiento)               |
| `reto4/` | Cadena de pensamiento y manejo del contexto                        |
| `bonus/` | JSON validado y evaluación A/B (reto 5)                            |

## Reflexión del grupo

**¿Qué técnica tuvo más efecto en nuestro caso?** Darle al modelo las reglas de CafeFET. Sin ellas, el modelo no sabe nada de nuestra cafetería y se lo inventa todo: en el reto 1 hizo el código en otro lenguaje y sin revisar ninguna regla; en el reto 2, sin system prompt, no encontró ningún error, y con las reglas encontró 3 de 4; y en el reto 4 dijo que a quien no recoge su pedido le cobran una multa, cuando la regla dice que se le devuelve el saldo. El modelo no se queda callado cuando no sabe: inventa, y lo dice con mucha seguridad.

También aprendimos que tener la regla escrita no garantiza que el modelo la cumpla. En todos los retos se le olvidó revisar que no se pueden hacer pedidos el domingo. Y pedirle que «piense paso a paso» no siempre ayuda: a veces escribe algo que parece un razonamiento, pero no hizo las cuentas.

**¿Qué haríamos distinto si mañana le pidiéramos a una IA que programe algo de CafeFET?**
1. Le daríamos todas las reglas del negocio, separadas de la instrucción y explicadas con claridad, sin dar nada por obvio.
2. Pondríamos las reglas importantes en el system prompt y no en un mensaje del chat, porque en una conversación larga los primeros mensajes se pierden.
3. Dividiríamos el trabajo en pasos pequeños y revisaríamos cada resultado antes de seguir, porque un error en un paso se arrastra a todos los que vienen después.
4. Nunca confiaríamos en el código sin probarlo con casos concretos, sobre todo los límites (las 18:00, 5 productos, el domingo).

En resumen: la IA ayuda mucho, pero solo sabe lo que le contamos, y el desarrollador humano tiene que revisar lo que entrega.
