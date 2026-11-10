# Registro de uso de inteligencia artificial

Registrar una entrada por spec.
No incluir claves, contraseñas ni datos reales de estudiantes.

Este archivo registra las herramientas y los modelos usados para
desarrollar el proyecto. El modelo predeterminado del producto es Gemini
3.5 Flash-Lite (`gemini-3.5-flash-lite`), documentado en docs/adr/ADR-001-stack.md.

Formato de cada entrada (plantilla 9.7 del enunciado):

```
## S-NNN · [fecha]
Herramienta y modelo:
Fases en que se usó: spec / plan / implementación / pruebas / depuración
Instrucción clave (resumen, no la conversación completa):
Qué se aceptó sin cambios:
Qué se corrigió o descartó, y por qué:
Costo o cuota consumida (si aplica):
```

## S-000 · 27-10-2026 · Preparación documental

Herramienta y modelo: ChatGPT · GPT-6.1 Sol.
Usado por: JavEstrada09.

Fases en que se usó: organización, propuesta de stack
y redacción de documentación.

Instrucción clave:
Analizar el enunciado y preparar el repositorio de TutoBosco
siguiendo las plantillas y el método de trabajo obligatorio.

Qué se aceptó sin cambios (como borrador revisado en PR #1):
- AGENTS.md.
- Variables de .env.example.
- Plantilla de pull requests.
- ADR del stack.

Qué se corrigió o descartó, y por qué:
- Se adaptó la inicialización a un repositorio creado vacío,
  con README y .gitignore preparados localmente.
- La propuesta inicial de 15 specs se sustituyó por la lista
  de 10 specs proporcionada por el equipo.
- Se dividió RF-05 entre S-007, generación de ejercicios,
  y S-009, respuestas y retroalimentación (PR #2), para que
  cada integrante tenga dos specs obligatorias asignadas.
- RF-07, plan de estudio, se mantuvo como requisito deseable
  fuera del alcance obligatorio.

Costo o cuota consumida: ninguna llamada a la API de IA
del producto.

## S-007 · 05-11-2026 · Borrador de especificación

Herramienta y modelo: OpenCode · GPT-6.1 Sol (openai/gpt-6.1-sol).

Fases en que se usó: spec y preparación de la estructura documental.
No se elaboró el plan técnico ni se implementó la funcionalidad.

Instrucción clave:
Preparar S-007 siguiendo docs/plan.md y docs/guia-trabajo.md,
crear la estructura propuesta e indicar los pasos humanos pendientes.

Qué se aceptó sin cambios:
- El usuario autorizó crear la estructura documental propuesta y
  preparar el borrador con el alcance presentado en la conversación.
- El contenido final de los archivos queda pendiente de revisión;
  no se registra aprobación de la spec ni del plan técnico.

Qué se corrigió o descartó, y por qué:
- Se dejó el plan técnico pendiente hasta la fusión de la spec,
  para respetar el orden obligatorio del repositorio.
- Se dejaron los resultados y la evidencia de verificación pendientes,
  porque todavía no existe implementación de S-007.

Costo o cuota consumida: ninguna llamada a la API de IA del producto.
El costo de la herramienta de desarrollo no está disponible en la sesión.

## S-000 · 27-10-2026 · Ajustes de estructura

Herramienta y modelo: Claude Code · Claude Opus 5.5.
Usado por: AlexDLG1.

Fases en que se usó: revisión de la estructura del repositorio
contra el enunciado y redacción de documentación.

Instrucción clave:
Revisar el repositorio con las plantillas 9.1 a 9.9 del enunciado
e identificar lo que falta antes de empezar a codificar.

Qué se aceptó sin cambios: pendiente de la revisión del PR.

Propuesto por el agente:
- CLAUDE.md con la referencia @AGENTS.md (N5).
- Plantillas en specs/_plantilla/ a partir de 9.3, 9.4 y 9.5.
- Estado aceptado del ADR-001.
- Este registro con el formato de 9.7.
- Decisiones D-002 a D-007 como propuestas.
- Calendario propuesto en docs/plan.md.

Qué se corrigió o descartó, y por qué: pendiente de la revisión del PR.

Costo o cuota consumida: ninguna llamada a la API de IA
del producto.


## S-009 · 05-11-2026 · Borrador de especificación

Herramienta y modelo: OpenCode · GPT-6.1 Sol (openai/gpt-6.1-sol).
Usado por: Jeffersson Ramos (ramosdeleon555).

Fases en que se usó: spec y preparación de la estructura documental.
No se elaboró el plan técnico ni se implementó la funcionalidad.

Instrucción clave:
Preparar S-009 siguiendo el plan y la guía, con Jeffersson Ramos
(ramosdeleon555) como autor, y utilizar git worktree para trabajar
simultáneamente en S-007 y S-009.

Qué se aceptó sin cambios:
- Jeffersson confirmó la estructura y el alcance documental
  propuestos y autorizó utilizar un worktree independiente.
- El contenido final queda pendiente de revisión en PR; no se
  registra aprobación técnica ni verificación de funcionalidad.

Qué se corrigió o descartó, y por qué:
- Se explicitó el nombre del autor junto a su usuario de GitHub,
  conforme a la aclaración del usuario.
- Se dejó el plan técnico pendiente hasta fusionar la spec,
  para respetar el proceso obligatorio del repositorio.
- Se dejaron resultados y evidencia pendientes, porque no existe
  implementación de S-009.

Costo o cuota consumida: ninguna llamada a la API de IA del producto.
El costo de la herramienta de desarrollo no está disponible en la sesión.

## S-005 · 05-11-2026

Herramienta y modelo: Claude (app de Claude) · Claude Sonnet 5.5.
Usado por: AlexDLG1.

Fases en que se usó: spec.

Instrucción clave:
Redactar la spec del registro y corrección de notas (RF-03 parcial)
con criterios Dado/Cuando/Entonces, incluyendo el rechazo en el
servidor de notas que el docente no puede registrar.

Qué se aceptó sin cambios: La estructura de la spec y los 8 criterios de aceptación.

Qué se corrigió o descartó, y por qué: Ninguna corrección; leí la spec completa y la contrasté con el enunciado (RF-03), AGENTS.md y la spec de S-002 antes de aceptarla.

Costo o cuota consumida: ninguna llamada a la API de IA
del producto.

## S-001 · 05-11-2026

Herramienta y modelo: ChatGPT · GPT-6.1 Sol.
Usado por: JavEstrada09.

Fases en que se usó: spec.

Instrucción clave:
Redactar la especificación del esqueleto funcional siguiendo
AGENTS.md, el plan del equipo y la plantilla del repositorio,
sin implementar código.

Qué se aceptó sin cambios:
El borrador con el problema, comportamiento esperado,
siete criterios de aceptación, exclusiones y restricciones.

Qué se corrigió o descartó, y por qué:
No se registraron correcciones de contenido a la spec. La especificación
fue fusionada en `main` mediante PR #24; esto no registra todavía una
verificación de implementación.

Costo o cuota consumida:
No se realizaron llamadas a la API de IA del producto.
El consumo de esta conversación no se cuantificó.

## S-001 · 06-11-2026

Herramienta y modelo: OpenCode · GPT-5.6 Sol.
Usado por: JavEstrada09.

Fases en que se usó: plan y actualización documental.

Instrucción clave:
Revisar y completar el plan técnico de S-001 sin implementar código,
conservar el modelo coordinado para S-002, registrar la decisión de roles
y actualizar los estados documentales después de la fusión de la spec
en PR #24.

Qué se aceptó sin cambios:
- Los siete criterios de aceptación de la spec.
- La separación entre proveedor Gemini y proveedor demo local.
- El manejo explícito de configuración, conexión, cuota y respuesta
  inválida.
- Las pruebas automatizadas y la futura verificación independiente de
  Douglas.
- Cuatro entregas revisables dentro de `s-001-esqueleto`.

Qué se corrigió o descartó, y por qué:
- Se conservó `StudentProfile` con `user`, `student_id`, `career` y
  `semester`; S-001 solo mostrará `career`.
- Se asignó la creación de `User` a `accounts/0001_initial.py` y la de
  `StudentProfile`, `Course` y `Enrollment` a
  `academics/0001_initial.py`, según la coordinación previa con S-002.
- Se mantuvieron `Course.code` único y una sola inscripción por pareja
  estudiante-curso.
- La decisión de roles dejó de posponerse a S-002: JavEstrada09 la aprobó
  antes de la implementación de S-001 con roles mediante perfiles y sin
  imponer exclusividad.
- Durante la integración de `main`, esa decisión se renumeró de D-008 a
  D-010 porque D-008 y D-009 ya estaban ocupadas. No cambió el acuerdo
  histórico ni se registró una aprobación adicional.
- La resolución conservó las entradas documentales de ambas ramas y
  eliminó los marcadores de conflicto y una secuencia de control de
  terminal que provenía de `main`.
- Se separaron las responsabilidades entre S-001 y S-002 de las
  entregas internas de S-001 para evitar tratarlas como specs nuevas.
- Se restauró `rebuild_synthetic_data` como comando mínimo que S-001
  crea y S-002 amplía.
- La revisión del diff restauró `AI_MODE=real` o `AI_MODE=demo`,
  `AI_MODEL`, `GEMINI_API_KEY` y `DEMO_STUDENT_PASSWORD`; el código
  `PROG-COM`; la ejecución idempotente; y la protección de registros
  ajenos.
- También restauró los controles CSRF, las comprobaciones de perfil e
  inscripción, la ausencia de permisos académicos por `is_staff`, las
  dependencias aprobadas y los PR secuenciales de cada entrega.

Costo o cuota consumida:
No se realizaron llamadas a la API de IA del producto.
El consumo de esta conversación de OpenCode no se cuantificó.

## S-001 · 06-11-2026 · Implementación de Entrega 1

Herramienta y modelo: OpenCode · GPT-5.6 Sol.
Usado por: JavEstrada09.

Fases en que se usó: implementación, pruebas y revisión técnica.

Instrucción clave:
Implementar únicamente la base ejecutable, los modelos y los datos
sintéticos mínimos de la Entrega 1 conforme a la spec y el plan aprobados,
sin avanzar las pantallas ni los proveedores del tutor.

Qué se aceptó sin cambios:
- La separación en las aplicaciones `accounts`, `academics` y `tutor`.
- `accounts.User` basado en `AbstractUser` y los tres modelos académicos
  acordados.
- El comando `rebuild_synthetic_data`, sus identificadores exactos y la
  contraseña obtenida desde `DEMO_STUDENT_PASSWORD`.
- Django 5.2 LTS y `python-dotenv` como dependencias necesarias para esta
  entrega. `google-genai` no se instaló porque aún no se integra Gemini.

Qué se corrigió o descartó, y por qué:
- Django dividió inicialmente la migración académica en dos archivos. Se
  consolidó en `academics/0001_initial.py` con dependencia del usuario,
  como exige el plan, y se comprobó que no quedan migraciones pendientes.
- La revisión técnica detectó que un perfil con el usuario manifiesto y
  otro carné podía sobrescribirse. El comando ahora aborta la transacción
  ante colisiones por usuario o carné, y las pruebas comprueban que los
  registros ajenos permanecen intactos.
- Una revisión posterior detectó que `update_or_create` modificaba la
  cuenta `estudiante_demo` antes de comprobar su pertenencia al
  manifiesto. Todas las colisiones se validan ahora antes de escribir. El
  comando también rechaza cuentas sin el perfil exacto o con privilegios
  `is_staff` o `is_superuser`, conservando contraseña, nombre y permisos.
- Se añadieron pruebas para una cuenta sin perfil y para cada privilegio,
  y se completó la preparación segura de `.env` y el inicio local en el
  README.

Resultado registrado por el autor:
- `manage.py check`: sin problemas.
- Pruebas de `accounts` y `academics`: 12 pruebas superadas.
- No se declaran cumplidos los criterios de aceptación completos de S-001.
- La verificación independiente de Douglas sigue pendiente.

Costo o cuota consumida:
No se realizaron llamadas a Gemini ni a la API de IA del producto.
El consumo de esta conversación de OpenCode no se cuantificó.

## S-001 · 06-11-2026 · Implementación de Entrega 2

Herramienta y modelo: OpenCode · GPT-5.6 Sol.
Usado por: JavEstrada09.

Fases en que se usó: implementación, pruebas y documentación.

Instrucción clave:
Implementar únicamente el acceso del estudiante, la pantalla protegida
de carrera y el cierre de sesión de la Entrega 2, conservando la Entrega
1 y sin crear formularios del tutor ni integrar Gemini.

Qué se aceptó sin cambios:
- Autenticación mediante `LoginView`, `LogoutView` y
  `AuthenticationForm` de Django.
- Perfil obtenido exclusivamente desde `request.user` y autorización
  condicionada por la inscripción en `PROG-COM`.
- Protección CSRF activa y cierre de sesión disponible solo mediante POST.
- Mensaje genérico para credenciales incorrectas o cuentas inactivas.

Qué se corrigió o descartó, y por qué:
- No se aceptan identificadores enviados por el navegador para elegir el
  perfil; las pruebas intentan seleccionar otro carné y confirman que se
  mantiene la carrera de la cuenta autenticada.
- Se conservó la validación segura de redirecciones de `LoginView` y se
  añadió una prueba que rechaza un destino externo en `next`.
- No se modificaron modelos, migraciones ni el comando de datos.

Resultado registrado por el autor:
- `manage.py check`: sin problemas.
- Pruebas de `accounts` y `academics`: 23 pruebas superadas.
- `makemigrations --check --dry-run`: no detectó cambios.
- `/acceso/` y el CSS local respondieron HTTP 200; `/` respondió 302 hacia
  `/acceso/?next=/` para una visita anónima.
- La verificación independiente de Douglas sigue pendiente.
- S-001 no se considera terminada.

Costo o cuota consumida:
No se realizaron llamadas a Gemini ni a la API de IA del producto.
El consumo de esta conversación de OpenCode no se cuantificó.

## S-001 · 07-11-2026 · Implementación de Entrega 3

Herramienta y modelo: OpenCode · GPT-5.6 Sol.
Usado por: JavEstrada09.

Fases en que se usó: implementación, pruebas, depuración y documentación.

Instrucción clave:
Implementar el formulario protegido del tutor, el contrato común, el modo
demo sin red y el proveedor real con `google-genai`, sin hacer commit ni
usar una clave cuando no estuviera configurada.

Qué se aceptó sin cambios:
- La selección pública mediante `AI_MODE=demo` o `AI_MODE=real`.
- El contexto limitado a pregunta, carrera y curso.
- La importación diferida del SDK para no inicializar Gemini en modo demo.
- La pregunta y respuesta grabadas para Programación Comercial.

Qué se corrigió o descartó, y por qué:
- Se fijó `google-genai==3.0.0` después de comprobar su instalación con
  Python 3.12 y ejecutar `pip check`.
- Se agregó validación de texto no vacío, extensión, curso, trato de usted
  e indicadores básicos de español antes de mostrar una respuesta.
- Las 44 pruebas automatizadas simulan Gemini. La prueba del constructor
  también usa un mock y no realiza una solicitud de red.
- CA-4 se comprobó después mediante consultas reales separadas, registradas
  en la siguiente entrada.
- El cambio automático al modo demo ante fallos del proveedor permanece
  para la Entrega 4 aprobada.

Resultado registrado por el autor:
- `manage.py check`: sin problemas.
- Pruebas de `accounts`, `academics` y `tutor`: 44 pruebas superadas.
- `makemigrations --check --dry-run`: no detectó cambios.
- `pip check`: no detectó dependencias incompatibles.
- La verificación independiente de Douglas sigue pendiente.

Costo o cuota consumida:
Las 44 pruebas automatizadas no realizaron llamadas reales a Gemini porque
usaron simulaciones. Las consultas reales se registran por separado.

## S-001 · 08-11-2026 · Comprobación real de Entrega 3

Herramienta y modelo: Google Gemini API · Gemini 3.8 Flash
(`gemini-3.8-flash`).
Usado por: JavEstrada09.

Fases en que se usó: pruebas de aceptación y diagnóstico.

Instrucción clave:
Comprobar CA-4 desde la interfaz con consultas de Programación Comercial y
realizar, por separado, una consulta directa de diagnóstico, sin registrar
la clave ni habilitar facturación de pago.

Qué se aceptó sin cambios:
- `gemini-3.8-flash` respondió dos consultas reales desde la interfaz: una
  sobre variables y otra que calculó correctamente Q75.
- La consulta de Q75 tardó aproximadamente tres minutos.
- Una consulta directa de diagnóstico, separada de CA-4, también respondió
  correctamente.

Qué se corrigió o descartó, y por qué:
- En intentos reales se observaron `429 RESOURCE_EXHAUSTED` y
  `504 DEADLINE_EXCEEDED`.
- El 504 se conserva como caso pendiente para el manejo completo de errores
  de la Entrega 4.
- Estos resultados no se confunden con las 44 pruebas automatizadas, que
  simulan Gemini y usan un mock en la prueba del constructor.
- La verificación independiente de Douglas sigue pendiente.

Costo o cuota consumida:
Se utilizó el nivel gratuito. El total de solicitudes y los tokens consumidos
no están confirmados. El gasto monetario registrado es USD 0.00; este valor
no significa que el consumo de solicitudes o tokens haya sido cero.

## S-001 · 08-11-2026 · Implementación de Entrega 4

Herramienta y modelo: OpenCode · GPT-5.6 Sol.
Usado por: JavEstrada09.

Fases en que se usó: implementación, pruebas, depuración y documentación.

Instrucción clave:
Limitar la espera y los reintentos de Gemini, manejar configuración, conexión,
cuota, tiempo de espera y salida inválida, permitir continuar en modo demo y
preparar la verificación de los siete criterios sin atribuir resultados a
Douglas.

Qué se aceptó sin cambios:
- Mensajes seguros y diferenciados para conexión, `429` y `504`.
- Continuación explícita con la pregunta grabada y sin inicializar Gemini.
- Verificación local de CA-7 con entorno virtual nuevo y base aislada.

Qué se corrigió o descartó, y por qué:
- La revisión humana corrigió la política inicial de dos intentos de 15
  segundos. El SDK reintentaba `429` de forma predeterminada y podía registrar
  la excepción completa antes del segundo intento. La política final usa un
  solo intento y un límite total de 60 segundos, por lo que `429` ofrece el
  modo demo inmediatamente y no entra al registro de reintentos.
- El primer comando del recorrido aislado fue dividido incorrectamente por
  PowerShell debido a sus comillas internas. Se pasó el código como un único
  argumento y el recorrido terminó correctamente; no fue un fallo del producto.
- El `504` real observado anteriormente no se repitió contra Gemini. Se simuló
  como exige el plan para verificar el manejo sin consumir cuota.
- CA-4 no se repitió porque ya tiene evidencia real del autor y esta entrega
  no necesitaba otra solicitud. Esa evidencia no sustituye a Douglas.

Resultado registrado por el autor:
- `manage.py check`: sin problemas.
- Suite completa después de corregir la política: 49 pruebas superadas en el
  entorno habitual.
- Instalación limpia previa: 48 pruebas, que eran todas las disponibles al
  ejecutar esa comprobación, superadas en el entorno virtual temporal nuevo.
- `makemigrations --check --dry-run`: no detectó cambios.
- `pip check`: no detectó dependencias incompatibles.
- Recorrido demo aislado: acceso, carrera y respuesta grabada correctos; sin
  invocar Gemini ni la red.
- La verificación independiente de Douglas quedó pendiente en esa fecha; se
  completó el 09-11-2026 en la entrada siguiente.

Costo o cuota consumida:
No se realizaron llamadas reales a Gemini durante la Entrega 4. Las pruebas
usaron simulaciones y el recorrido aislado bloqueó Gemini y la salida de red.
El consumo de esta conversación de OpenCode no se cuantificó.

## S-001 · 09-11-2026 · Verificación independiente

Herramienta y modelo: Google Gemini API · Gemini 3.8 Flash (`gemini-3.8-flash`)
y Gemini 3.5 Flash-Lite (`gemini-3.5-flash-lite`).
Usado por: douglas-yasser.

Fases en que se usó: pruebas de aceptación de la verificación independiente.

Instrucción clave:
Verificar los siete criterios de S-001 sobre el commit `eb01cc7` en un
worktree aislado, registrar la evidencia y comprobar CA-4 con una consulta
real desde la interfaz sin mostrar la clave.

Qué se aceptó sin cambios:
- CA-1 a CA-6 cumplen según el registro de `specs/S-001-esqueleto/verificacion.md`.
- La respuesta real de `gemini-3.5-flash-lite` se mostró en la interfaz en
  4.12 s, en español, con trato de usted y mención de Programación Comercial.
- El recorrido demo funcionó sin red y sin inicializar Gemini.
- Se mantiene el límite vigente de 60 segundos y un solo intento de `eb01cc7`.
- La instalación limpia y el recorrido demo se repitieron con Python 3.12.10:
  50 pruebas superadas en 91.695 s y recorrido completo con `runserver`.

Qué se corrigió o descartó, y por qué:
- Con `gemini-3.8-flash` se realizaron tres intentos reales que fallaron:
  uno agotó el plazo de 60 segundos (62.464 s), otro devolvió el error
  genérico del proveedor (4.676 s) y un diagnóstico directo confirmó
  `504 DEADLINE_EXCEEDED`.
- Se repitió CA-4 con el modelo documentado `gemini-3.5-flash-lite`: la
  llamada al servicio respondió en 4.531 s y la interfaz mostró la respuesta
  real en 4.12 s.
- La ejecución inicial con Python 3.13.14 se conserva como evidencia
  adicional; la comprobación principal se repitió con Python 3.12.10.
- El `.env` local se alineó a `AI_MODEL=gemini-3.5-flash-lite`.

Costo o cuota consumida:
Se utilizó el nivel gratuito. Se realizaron cinco solicitudes reales: tres
con `gemini-3.8-flash` (todas fallidas) y dos con `gemini-3.5-flash-lite`
(ambas correctas). El total de tokens no está confirmado. El gasto monetario
registrado es USD 0.00; este valor no significa que el consumo de solicitudes
o tokens haya sido cero.

## S-003 · 05-11-2026

Herramienta y modelo: Claude (app de Claude) · Claude Sonnet 5.5.
Usado por: AlexDLG1.

Fases en que se usó: spec.

Instrucción clave:
Redactar la spec del perfil académico (RF-02) con criterios
Dado/Cuando/Entonces, a partir del enunciado, de docs/plan.md
y de las decisiones D-003, D-004 y D-007.

Qué se aceptó sin cambios: La estructura de la spec y los 8 criterios de aceptación.

Qué se corrigió o descartó, y por qué: Ninguna corrección; leí la spec completa y la contrasté con D-003, D-004 y D-007 antes de aceptarla.

Costo o cuota consumida: ninguna llamada a la API de IA
del producto.

## S-002 · 06-11-2026 · Plan, modelos y datos sintéticos

Herramienta y modelo: OpenCode · deepseek-v4.1-flash.
Usado por: douglas-yasser.

Fases en que se usó: plan, implementación y pruebas.

Instrucción clave:
Ampliar el modelo académico de S-001 con docentes, asignaciones,
temas y notas, y extender `rebuild_synthetic_data` con el conjunto
completo de datos sintéticos.

Qué se aceptó sin cambios:
- El plan aprobado en el PR #33.
- El acuerdo de modelos con S-001 y las decisiones D-003, D-004,
  D-007, D-008 y D-009.
- La división de la implementación en dos incrementos revisables.

Qué se corrigió o descartó, y por qué:
- Se reemplazaron las pruebas que esperaban únicamente los datos
  mínimos de S-001 por pruebas del conjunto completo.
- Se usó MD5 solo en las pruebas de reconstrucción para reducir el
  costo de generar 33 cuentas; la aplicación mantiene los hashers
  de Django.
- Se corrigió el borrado accidental de notas de estudiantes ajenos al
  reconstruir los temas del conjunto sintético; se agregó una prueba
  de regresión.
- Se limitó la limpieza de la reconstrucción a las inscripciones, notas
  y asignaciones que genera el manifiesto para cada cuenta, conservando
  los registros agregados fuera de ese conjunto; se agregaron dos
  pruebas de regresión.
- No se modificó `accounts.User` ni las migraciones de S-001.

Resultado registrado por el autor:
- `manage.py check`: sin problemas.
- Pruebas de `accounts` y `academics`: 34 superadas.
- `makemigrations --check --dry-run`: sin cambios.
- La verificación independiente de JavEstrada09 sigue pendiente.

Costo o cuota consumida:
No se realizaron llamadas a Gemini ni a la API de IA del producto.
El consumo de esta conversación de OpenCode no se cuantificó.

## S-003 · 09-11-2026 · Plan e implementación

Herramienta y modelo: Claude Code · Claude Opus 5.5 (`claude-opus-5-5`).
Usado por: AlexDLG1.

Fases en que se usó: plan, implementación y pruebas.

Instrucción clave:
Proponer el plan de S-003 en modo de solo lectura, con una función única de
promedio reutilizable por S-007 y una vista `/perfil/` separada de
`student_home`. Después, implementar las tareas una por una, mostrando el diff
y deteniéndose antes de cada commit, sin hacer push.

Qué se aceptó sin cambios:
- El enfoque del plan: `academics/services.py` con `calculate_average` y
  `get_course_summaries`, y la vista `student_profile` solo para estudiantes.
- El uso de `|unlocalize` para mostrar `71.67` como dice la spec, aunque
  `LANGUAGE_CODE` sea `es`.
- La cobertura de CA-4 y CA-6 mediante pruebas automatizadas, porque los
  datos sintéticos no tienen notas parciales ni estudiantes sin cursos.
- El aviso para un curso sin temas, que el plan no incluía. El agente lo
  señaló antes del commit y AlexDLG1 autorizó el commit sin pedir cambios.

Qué se corrigió o descartó, y por qué:
- AlexDLG1 agregó la tarea 0, para documentar el plan aprobado en un commit
  propio junto con el cambio de estado de la spec y de `docs/plan.md`.
- AlexDLG1 pidió aclarar que D-004 no fija el modo de redondeo y que
  `ROUND_HALF_UP` es una decisión del plan.
- AlexDLG1 corrigió la línea del registro de cambios de la spec para indicar
  que la spec se fusionó en el PR #21.
- AlexDLG1 fijó la forma de trabajo: revisar cada diff, ejecutar las pruebas
  y revisar en el navegador antes de autorizar cada commit.
- El agente estimó el PR en 300 a 350 líneas; el resultado supera la
  referencia de 400 líneas, principalmente por las pruebas.

Resultado registrado por el autor:
- Suite de `accounts`, `academics` y `tutor`: 80 pruebas superadas.
- `manage.py check`: sin problemas.
- `makemigrations --check --dry-run`: no detectó cambios.
- `pip check`: no detectó dependencias incompatibles.
- Revisión en el navegador de `/perfil/`: `estudiante_demo` con promedio
  78.00, `estudiante_01` con dos cursos y promedio 77.50, y `estudiante_02`
  con `Sin nota` y `Sin notas`. El enlace desde `student_home` funciona.
- La verificación independiente de ramosdeleon555 sigue pendiente.

Costo o cuota consumida:
No se realizaron llamadas a Gemini ni a la API de IA del producto.
El consumo de esta conversación de Claude Code no se cuantificó.
