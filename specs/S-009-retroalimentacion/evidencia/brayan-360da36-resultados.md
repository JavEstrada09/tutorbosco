# Resultados independientes asistidos de S-009

Verificador: Brayan Hernández (`Brayan11Hernandez`).  
Ejecución técnica: OpenCode en la computadora del verificador.  
Commit: `360da36fc6010e1974f6d75c1bd7bca738d8db08`.  
Fecha: 2026-11-11.

Esta ejecución no registra aprobación humana de Brayan. Las capturas y su
confirmación final permanecen pendientes.

| CA | Resultado observado | Estado técnico |
| --- | --- | --- |
| CA-1 | POST válido: UUID propio y relaciones correctas con ejercicio, estudiante, curso y tema. | PASS |
| CA-2 | Vacío, espacios y 4001 no registraron; 4000 se aceptó; el proveedor instrumentado no recibió entradas inválidas. | PASS |
| CA-3 | Demo y Gemini distinguieron la respuesta y orientaron. Gemini exigió un nivel avanzado no solicitado. | PASS con observación pedagógica |
| CA-4 | Notas 25/55 produjeron apoyo detallado/breve; cambiar 25 a 55 afectó el siguiente intento; el mock confirmó contexto privado. | PASS |
| CA-5 | Intentos y cursos conservaron UUID y contenido propios; recargar creó 0 intentos. | PASS |
| CA-6 | Anónimo, docente, ajeno, inexistente, inscripción revocada, propietario extra y falta de CSRF fueron rechazados sin escrituras. | PASS |
| CA-7 | Clave vacía, cliente y sockets bloqueados, 24 casos demo y respuesta desconocida cubiertos; recursos locales. | PASS técnico |
| CA-8 | Conexión, timeout, 429 y 504 simulados; fallback o ausencia de devolución correctos. | PASS |
| CA-9 | Salidas vacías, JSON/estructura/tipos/tamaños/HTML inválidos no se guardaron; respuestas conservadas. | PASS |
| CA-10 | Escape, curso, español, trato formal y notas intactas comprobados técnicamente. | PASS técnico; revisión visual pendiente |

## Recorrido Demo

- Ejercicio: `464f6998-0a2b-484e-8d15-62a4876f86e8`.
- Acierto: `c77ecec0-79fe-4f31-98c5-4b32e02d2b62`.
- Error: `eaadfe88-7da6-4cb7-8ea4-e520cbcaf5a4`.
- Otro curso, REDES: `b48f598d-c0e6-4329-8061-b3dbb1c81fc4`.

Respuesta correcta:

> Objetivo: explique una nota de venta. Contexto: estudiante principiante. Restricción: no invente datos. Formato: definición y ejemplo breve.

Devolución demo de acierto:

> Usted incluye objetivo, contexto, restricción y formato para orientar la explicación. Pruebe el prompt y revise si la salida contiene la definición y el ejemplo solicitados.

Respuesta incorrecta:

> Haga cualquier cosa con ventas, invente los datos y responda sin formato.

Devolución demo de error:

> La respuesta permite inventar datos y no fija un objetivo ni un formato verificables. Pruebe el prompt y revise si la salida contiene la definición y el ejemplo solicitados.

## Perfiles Vigentes

- Nota 25, respuesta `30e961b6-df10-4070-aec5-c0536532d398`: orientación paso a paso.
- Nota 55, respuesta `23178db2-5659-4a76-9a3e-05a8b280e1c1`: orientación breve.
- Tras cambiar 25 a 55, respuesta `b9eb32a7-4758-42cb-9935-f1e3f9073f96`: orientación breve con el dato vigente.

## Gemini Real

Se autorizó y ejecutó una sola solicitud con `gemini-3.5-flash-lite`, sin
generar otra práctica ni hacer reintentos manuales.

| Dato | Observado |
| --- | --- |
| Duración HTTP | 11.215 s |
| Ejercicio | `464f6998-0a2b-484e-8d15-62a4876f86e8` |
| Respuesta | `bf28fdbf-0c61-43fd-8060-ca411b6b3198` |
| Curso y tema | Programación Comercial, Ingeniería de prompts |
| Nota vigente | 55 |
| Procedencia | `real` |
| Fallback | No |
| Notas oficiales | Sin cambios |

Respuesta enviada:

> Objetivo: explique una nota de venta. Contexto: estudiante principiante. Restricción: no invente datos. Formato: definición y ejemplo breve.

Retroalimentación completa:

> **Aciertos y aspectos por mejorar:**  
> Estimado/a estudiante, su respuesta aborda de manera correcta los componentes fundamentales solicitados en el enunciado: define un objetivo, establece un contexto, incluye una restricción clara y especifica el formato esperado para la redacción del prompt. Sin embargo, dado que su nota actual en el tema de «Ingeniería de prompts» es de 55 (indicando una debilidad en esta área según su historial académico), la respuesta actual resulta demasiado escueta y carece del nivel de detalle y precisión profesional que se espera en el ámbito de la programación comercial y contable. Un prompt efectivo para explicar una nota de venta a un principiante requiere mayor riqueza en la definición de roles, tono y estructura para garantizar que la inteligencia artificial o el lector obtengan la guía exacta que usted busca transmitir.  
> **Para continuar:**  
> Para fortalecer su dominio en ingeniería de prompts, le sugiero ampliar su respuesta estructurándola bajo metodologías avanzadas (por ejemplo, asignando un rol específico a la IA, detallando el tono pedagógico y desglosando el formato en secciones concretas como introducción, desglose de conceptos y caso práctico). Revise cómo redactar instrucciones más completas y específicas, y practique integrando un escenario contable más realista que le permita elevar su rendimiento en este tema crítico para el curso.

Conclusión pedagógica: identifica correctamente los cuatro componentes y da
acciones concretas, por lo que satisface el mínimo de CA-3. Sin embargo,
exige técnicas "avanzadas", precisión "profesional" y secciones que el
enunciado no pidió. Es una observación de calidad, no una aprobación basada
solo en que el JSON sea válido.

Tokens y costo no fueron informados. No se habilitó facturación.

## Pendientes Humanos

No se instalaron herramientas de navegador. Brayan debe tomar las nueve
capturas propuestas sin mostrar cookies ni contraseñas y confirmar idioma,
trato formal, presentación visual y la conclusión pedagógica antes de aprobar.

Los comandos entregados con `run_name='_main_'` no ejecutan pruebas y
devuelven código 0. La reproducción está en `brayan-pruebas.txt`; las suites
reales se ejecutaron con `run_name='__main__'`.
