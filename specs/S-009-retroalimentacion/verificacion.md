# Verificación S-009

Autor: Jeffersson Ramos (ramosdeleon555).
Estado: implementación local comprobada mediante pruebas y HTTP demo;
pendiente de revisión del autor y verificación independiente.
Verificador previsto: Brayan11Hernandez.
Computadora: pendiente · Commit probado: pendiente.

| Criterio | Cómo lo probé | Resultado | Evidencia |
| --- | --- | --- | --- |
| CA-1 | Pendiente | No ejecutado | Pendiente |
| CA-2 | Pendiente | No ejecutado | Pendiente |
| CA-3 | Pendiente | No ejecutado | Pendiente |
| CA-4 | Pendiente | No ejecutado | Pendiente |
| CA-5 | Pendiente | No ejecutado | Pendiente |
| CA-6 | Pendiente | No ejecutado | Pendiente |
| CA-7 | Pendiente | No ejecutado | Pendiente |
| CA-8 | Pendiente | No ejecutado | Pendiente |
| CA-9 | Pendiente | No ejecutado | Pendiente |
| CA-10 | Pendiente | No ejecutado | Pendiente |

## Correcciones y repetición de pruebas

Pendientes de la verificación independiente. Las comprobaciones locales
del asistente se documentan a continuación sin sustituir esa revisión.

El verificador debe ser distinto del autor y ejecutar cada criterio
en su computadora con el commit indicado. Registrará los fallos,
el commit de corrección y el resultado de la nueva prueba.

## Comprobaciones locales del asistente en la sesión del autor

- Rama: s-009-retroalimentacion, worktree
  `C:\Users\Canche\Desktop\tutorbosco-s-009`.
- Base: main `914b8da`; implementación todavía sin commit.
- Equipo: entorno Windows del autor. Ejecuciones realizadas por OpenCode;
  no se atribuye revisión ni aprobación a Brayan11Hernandez.
- Se reutilizó el entorno virtual existente de tutorbosco, sin instalar
  dependencias. Se cargó la configuración local sin imprimir secretos.

### Pruebas automatizadas

| Comprobación | Resultado |
| --- | --- |
| tutor.test_feedback, verbosity 1 | 27 pruebas, OK, 1.187 s |
| accounts academics tutor --noinput | 244 pruebas, OK, 245.075 s |
| manage.py check | Sin errores |
| manage.py makemigrations --check --dry-run | Sin cambios pendientes |
| python -m pip check | Sin requisitos incompatibles |
| migrate en base nueva | tutor.0003_exerciseanswer_exercisefeedback aplicada correctamente |

Se fijó GEMINI_API_KEY vacía en el proceso de Python antes de cargar Django.
La suite específica se ejecutó con AI_MODE=real externo y la completa con
AI_MODE=demo; cada prueba selecciona su modo. Los casos reales usan clave
sintética y mocks. El caso offline bloquea el cliente Gemini y las conexiones
de socket durante la evaluación demo. No se consumió cuota del producto.

Cobertura observada en tutor/test_feedback.py:

| Criterio | Casos automatizados ejecutados localmente |
| --- | --- |
| CA-1 | Respuesta recortada, UUID y relación derivada con propietario, curso y tema. |
| CA-2 | Vacío, espacios, más de 4000 caracteres y límite válido de 4000; sin consultas en entradas inválidas. |
| CA-3 | Respuesta guardada antes de invocar proveedor; explicación y orientación asociadas al intento. |
| CA-4 | Contexto aislado y vigente; notas 25/55 con detalle demo distinto; actualización y ausencia de nota. |
| CA-5 | Varios intentos, ejercicios y cursos con resultados individuales y UUID diferentes. |
| CA-6 | Anónimo, docente, IDs ajenos/inexistentes, campos manipulados, CSRF, curso inconsistente e inscripción revocada. |
| CA-7 | Acierto/error sin cliente externo ni red; normalización estricta y cobertura de las 24 claves demo. |
| CA-8 | Conexión, 429, 504, timeout y clave ausente simulados; fallback informado y respuesta conservada sin caso aplicable. |
| CA-9 | Salidas vacías, no JSON, tipos/campos/tamaños inválidos y HTML; ninguna devolución inválida persistida y respuesta conservada. |
| CA-10 | Instrucciones de español/usted, enunciado formal sin pronombre literal, curso visible, escape y notas intactas. |

La coherencia semántica de una devolución real, el idioma, trato formal y
la presentación requieren además revisión humana; no se consideran
demostrados únicamente por estas aserciones.

### Recorrido HTTP demo en localhost

Se creó una base sintética independiente en
`C:\Users\Canche\AppData\Local\Temp\opencode\tutorbosco-s009-914b8da.sqlite3`.
Se aplicaron migraciones y rebuild_synthetic_data en esa base. No se
reconstruyó ninguna base existente del usuario ni se modificó .env.

Servidor: `http://127.0.0.1:8002`, AI_MODE=demo y GEMINI_API_KEY vacía
solo en el entorno del proceso. Se reutilizan las contraseñas locales
configuradas para las cuentas sintéticas, sin mostrarlas.

1. Inicio de sesión HTTP con cookies y CSRF como estudiante_03.
2. Generación de práctica para PROG-COM y apertura del formulario.
3. Envío del ejemplo correcto y luego del incorrecto, ambos con CSRF.
4. Comprobación de HTTP 200, etiquetas demo y explicaciones correspondientes.
5. Consulta repetida del primer resultado: no creó otro intento.
6. Comparación de notas oficiales antes y después: sin cambios.

| Dato | Resultado observado |
| --- | --- |
| Usuario sintético | estudiante_03 |
| Curso | PROG-COM — Programación Comercial |
| Tema | Ingeniería de prompts |
| Clave demo | prompts-v1 |
| Ejercicio | dcdc6e4c-4419-4fb3-8148-936de858dff3 |
| Respuesta de acierto | f8a30246-5f29-46b6-be76-9d9889172fcb |
| Respuesta de error | 800501f1-08d1-4f8a-ab2f-292b63e9a1e9 |
| Intentos guardados | 2 independientes, ambos con devolución demo |

Respuesta de ejemplo correcta enviada:

> Objetivo: explique una nota de venta. Contexto: estudiante principiante. Restricción: no invente datos. Formato: definición y ejemplo breve.

Devolución de acierto comprobada:

> Usted incluye objetivo, contexto, restricción y formato para orientar la explicación.

Respuesta de ejemplo incorrecta enviada:

> Haga cualquier cosa con ventas, invente los datos y responda sin formato.

Devolución de error comprobada:

> La respuesta permite inventar datos y no fija un objetivo ni un formato verificables.

Ambas incluyen la orientación breve correspondiente al perfil:

> Pruebe el prompt y revise si la salida contiene la definición y el ejemplo solicitados.

Los enlaces locales son `/practica/respuestas/<UUID>/` en el puerto 8002,
tras iniciar sesión con la cuenta propietaria. Estos UUID pertenecen a la
base temporal local; no se distribuirán con Git ni aparecerán automáticamente
en la computadora del verificador.

No se tomaron capturas ni se realizó revisión visual en navegador. El
recorrido inicial se comprobó mediante HTTP. En ese bloque no se hizo una
llamada real a Gemini; sus casos y errores se simularon. La prueba real
posterior, autorizada por el autor, se registra en la sección siguiente.

## Prueba real de retroalimentación con Gemini

Ejecutada por OpenCode a solicitud de Jeffersson en el mismo worktree,
base main 914b8da, con implementación sin commit. No es verificación
independiente de Brayan11Hernandez.

### Preparación y recorrido

1. Se comprobó que existía una clave local sin mostrarla y que el modelo
   configurado era gemini-3.5-flash-lite.
2. Se inició un servidor temporal en 127.0.0.1:8003 con AI_MODE=real y la
   misma base sintética temporal de S-009, sin modificar .env.
3. Se inició sesión por HTTP como estudiante_03, con cookies y CSRF.
4. Se abrió un ejercicio demo ya existente: no se solicitó otra generación
   de ejercicios a Gemini. Se envió una sola respuesta para obtener
   retroalimentación real, sin reintentos manuales.
5. Se compararon los UUID de respuestas antes y después; se comprobó que
   se creó exactamente un intento y una devolución con source=real.
6. Se verificó HTTP 200, etiqueta de IA, ausencia de aviso de fallback y
   de salida inválida, y notas oficiales sin cambios.
7. Se detuvo el servidor temporal del puerto 8003. El puerto 8002 continuó
   en demo y permite consultar la devolución real que quedó guardada.

### Datos observados

| Dato | Resultado |
| --- | --- |
| Fecha local del intento | 11-11-2026, 01:11:39, Guatemala (UTC−06:00) |
| Fecha UTC de creación de la respuesta | 2026-11-11T07:11:39.846621+00:00 |
| Modelo configurado | gemini-3.5-flash-lite |
| Usuario sintético | estudiante_03 |
| Curso y tema | PROG-COM — Programación Comercial — Ingeniería de prompts |
| Nota vigente comprobada | 58 |
| Ejercicio existente | dcdc6e4c-4419-4fb3-8148-936de858dff3, modo demo, clave prompts-v1 |
| Nueva respuesta | 54017c97-a5d1-4db7-8a61-551a057087db |
| Duración HTTP de envío y redirección | 4,69 segundos |
| HTTP final | 200 |
| Intentos nuevos | 1 |
| Procedencia persistida de la devolución | real |
| Etiqueta comprobada en el HTML | Retroalimentación generada por IA |
| Aviso de alternativa demo o salida inválida | Ninguno |
| Calificaciones oficiales | Sin cambios respecto a la consulta previa |

### Ejercicio y respuesta enviada

Enunciado del ejercicio:

> Redacte usted un prompt para explicar una nota de venta a un principiante. Incluya objetivo, contexto, restricciones y formato esperado.

Respuesta del estudiante enviada:

> Objetivo: explique una nota de venta. Contexto: estudiante principiante. Restricción: no invente datos. Formato: definición y ejemplo breve.

### Retroalimentación completa validada y persistida

**Aciertos y aspectos por mejorar:**

> Estimado/a estudiante, su respuesta cumple parcialmente con los elementos solicitados para la redacción de un prompt (objetivo, contexto, restricciones y formato). Sin embargo, el texto presentado es demasiado escueto y carece del nivel de detalle necesario que exige la ingeniería de prompts avanzada para guiar eficazmente a un modelo de lenguaje. Dado que este tema (Ingeniería de prompts) se encuentra en su zona de debilidad académica actual con una nota de 58, es fundamental profundizar en cómo estructurar instrucciones ricas en roles, ejemplos y criterios de éxito claros, especialmente al abordar conceptos contables y comerciales para principiantes.

**Para continuar:**

> Le sugiero reestructurar su prompt aplicando técnicas más robustas de ingeniería de prompts. Para ello, incorpore un rol específico para la IA (por ejemplo, 'Actúa como un contador público experto en docencia'), enriquezca el contexto explicando por qué el estudiante necesita entender la nota de venta, amplíe las restricciones (como evitar jerga técnica excesiva) y detalle mejor el formato de salida esperado (incluyendo secciones de bienvenida, desglose paso a paso y un caso práctico simulado). Revise los materiales del curso sobre diseño de instrucciones efectivas para fortalecer esta competencia.

Consulta local con la cuenta propietaria:
`http://127.0.0.1:8002/practica/respuestas/54017c97-a5d1-4db7-8a61-551a057087db/`.
El UUID pertenece a esta base temporal; no aparecerá automáticamente en
otra instalación. El ejercicio es demo, pero esta devolución es real:
las dos procedencias son independientes.

### Alcance y limitaciones

- La devolución comenta elementos de la respuesta, ofrece orientación y
  utiliza la nota vigente 58, aportando evidencia local de CA-3 y CA-4.
- El resultado identifica el curso en pantalla, conserva la respuesta
  y no modifica notas, aportando evidencia local de CA-1 y CA-10.
- No se demuestra con esta única llamada la adaptación real comparada de
  dos perfiles ni el cumplimiento completo de los diez criterios.
- La calidad pedagógica requiere revisión humana: el texto exige un nivel
  «avanzado» no solicitado explícitamente por el enunciado. Registrar esta
  observación no equivale a aprobar ni a descartar toda la devolución.
- El texto completo anterior se recuperó de la devolución validada y
  persistida; no se guardaron el JSON crudo del proveedor ni metadata de tokens.
- No se tomaron capturas ni se hizo revisión visual de esta llamada en
  navegador; el recorrido y la etiqueta se comprobaron por HTTP.
- Una solicitud real, tokens y costo pendientes de confirmar con el
  proveedor; véase docs/gasto.md. No se configuró facturación durante la prueba.
- Los fallos de conexión, cuota y salida inválida de las suites siguen
  siendo simulaciones; no se provocaron durante este intento exitoso.

### Repetición independiente pendiente

Brayan debe registrar su equipo, fecha, commit y evidencia propia. Puede
usar una base separada con DJANGO_DATABASE_PATH y los ejemplos visibles de
cada ejercicio demo. Debe ejecutar CA-1 a CA-10, revisar las devoluciones,
permisos y preservación de respuestas, y repetir las suites sobre el commit
entregado. Una llamada real requiere clave local y autorización; si se
omite, debe dejarlo explícito sin atribuir resultados reales a simulaciones.
