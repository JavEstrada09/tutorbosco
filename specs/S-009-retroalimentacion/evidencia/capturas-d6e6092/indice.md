# Capturas reales de d6e6092

Fecha: 2026-11-11. Edge headless mediante CDP, ancho de 1440 píxeles.
Commit: `d6e6092e2fd243b1cfb45de15c7cc0d027af9331`.
Modo demo, clave vacía, base sintética nueva. Automatización: OpenCode.

| Archivo | CA | Escenario | Esperado | Observado |
| --- | --- | --- | --- | --- |
| [01-ejercicio-propio.png](01-ejercicio-propio.png) | 1/10 | Estudiante 03, ejercicio propio | Curso, tema, enunciado y formulario | Programación Comercial / Ingeniería de prompts; formulario disponible. |
| [02-respuesta-vacia.png](02-respuesta-vacia.png) | 2 | Envío de espacios | Validación sin intento | Mensaje visible; ausencia de registro cubierta además por prueba y consultas. |
| [03-demo-acierto.png](03-demo-acierto.png) | 3/7 | Respuesta con cuatro componentes | Acierto y orientación pertinente | Reconoce objetivo, contexto, restricción y formato; propone probar la salida. |
| [04-demo-error.png](04-demo-error.png) | 3/7 | Respuesta que permite inventar datos | Corrección distinta del acierto | Señala datos inventados y falta de objetivo/formato. |
| [05-perfil-apoyo-detallado.png](05-perfil-apoyo-detallado.png) | 4 | Estudiante 15, nota preparada 25 | Apoyo detallado | «Construya cuatro líneas» y contraste de cuatro condiciones. |
| [06-perfil-apoyo-breve-historial.png](06-perfil-apoyo-breve-historial.png) | 4/5 | Estudiante 03, nota preparada 55; consulta del primer intento | Apoyo breve e intentos separados | «Pruebe el prompt»; dos UUID en historial, devolución del acierto. |
| [07-acceso-rechazado.png](07-acceso-rechazado.png) | 6 | Docente solicita ejercicio del estudiante | Rechazo sin datos del ejercicio | 403 «Acceso denegado». |
| [08-sin-devolucion-aplicable.png](08-sin-devolucion-aplicable.png) | 8 parcial | Respuesta fuera del catálogo | Conservar respuesta sin inventar evaluación | Aviso de ausencia de caso y respuesta registrada. Fallos de red/cuota cubiertos por simulación. |
| [09-contenido-escapado.png](09-contenido-escapado.png) | 10 | Respuesta con etiqueta script | HTML literal, curso y trato formal | Etiqueta visible como texto; comprobación DOM sin scripts en línea. |

Las notas de los perfiles proceden de la preparación de la base, no de un
valor visible en estas pantallas. Las capturas complementan las pruebas;
no acreditan por sí solas ausencia de llamadas, escrituras o cambios de notas.
Consulte `../brayan-d6e6092-resultados.md` y `../brayan-d6e6092-pruebas.txt`.
