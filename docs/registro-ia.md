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

## S-003 · 09-11-2026 · Asistencia a la verificación independiente

Herramienta y modelo: OpenCode · `openai/gpt-6.1-sol`.
Fases en que se usó: pruebas, diagnóstico local y documentación.

Instrucción clave:
Ayudar a ramosdeleon555 a registrar su verificación real de CA-1 a CA-8
del commit `9f8c6e2`, sin atribuir pruebas ni aprobaciones inexistentes.
El usuario confirmó haber revisado ese commit y haber probado manualmente
los casos especiales; aportó dos capturas del estado inicial.

Trabajo realizado por el agente:
- Inspeccionó migraciones y base local: un estudiante, un curso y ningún
  tema ni nota. Reconstruyó el conjunto sintético con la configuración
  local existente, sin mostrar secretos ni instalar dependencias.
- Ejecutó sobre `9f8c6e2` la suite de `accounts`, `academics` y `tutor`:
  80 pruebas OK, en 53.632 segundos. CA-1 a CA-8 están cubiertos por
  métodos explícitos de `StudentProfileViewTests` que pasaron.
- Ejecutó `check`, `makemigrations --check --dry-run` y `pip check`, sin
  problemas; `migrate` indicó que no había migraciones pendientes.
- Comprobó autenticación y HTML del perfil mediante el cliente de Django
  con tres cuentas de la base reconstruida. Esto no fue una revisión
  visual humana del navegador. Un primer comando auxiliar falló por
  comillas antes de ejecutar Django; el comando corregido pasó.
- Creó `s-003-verificacion` desde el main remoto actualizado `45ee80e`.
  Comparó los directorios de aplicación con `9f8c6e2`, sin diferencias.
- Documentó resultados, procedencia de la evidencia y capturas originales.
  No presentó la captura del curso sin temas como prueba de promedios ni
  como escenario de temas existentes sin notas.

Decisiones de documentación:
- La declaración de pruebas manuales pertenece al usuario; las ejecuciones
  automatizadas pertenecen al agente. No se inventaron valores ni capturas
  de las modificaciones manuales.
- Se conservó S-003 en verificación, pendiente de confirmación humana del
  registro y revisión del PR documental, conforme a AGENTS §12.

Costo o cuota consumida: no hubo llamadas reales a Gemini; las pruebas
simularon el proveedor. El consumo de OpenCode no se cuantificó.

## S-003 · 09-11-2026 · Evidencia complementaria posterior al PR #41

Herramienta y modelo: OpenCode · `openai/gpt-6.1-sol`.
Fases en que se usó: pruebas automatizadas de navegador y documentación.

Instrucción clave:
Corregir los pendientes de evidencia señalados tras fusionar el PR #41,
ejecutar los casos y tomar las capturas faltantes, sin hacerse pasar por
el verificador humano ni aprobar la spec en su nombre.

Trabajo realizado:
- Se creó `s-003-evidencia-complementaria` desde `7b2a79b`, main después
  del PR #41. No se modificó el código de la aplicación.
- Se ejecutaron las tres pruebas existentes de CA-4, CA-6 y CA-8:
  3 OK en 2.043 segundos. Se guardó su salida real en
  `specs/S-003-perfil-academico/evidencia/ca4-ca6-ca8.txt`.
- Se preparó una base SQLite temporal con cinco perfiles sintéticos y
  un servidor Django de loopback, sin alterar la base demo.
- Se utilizó Chrome headless con CDP y el WebSocket integrado de Node.js.
  Python estándar y dos scripts temporales fuera del repositorio
  coordinaron los escenarios; no se instalaron dependencias.
- Se generaron diez capturas reales de página completa para CA-1 a CA-8,
  con aserciones sobre el DOM y CSS local cargado. CA-7 usa dos sesiones
  diferentes y CA-8 captura la recarga antes/después de cambiar 65 a 95,
  con promedios 71.67 y 81.67. Las sesiones se inyectaron desde
  `Client.force_login`; no se presenta esto como prueba del login.
- Se cerraron los procesos temporales y se descartaron base y perfil de
  navegador al terminar. No se versionaron claves, cookies ni bases.
- Se documentó que los merges previos precedieron a la confirmación
  formal; esta evidencia posterior no corrige retroactivamente el proceso.

Qué requiere revisión humana:
Ramos debe revisar el registro y confirmar explícitamente su aceptación;
otro integrante revisa el PR documental. No se registra esa confirmación
ni una aprobación humana inexistente. S-003 continúa en verificación.

Costo o cuota consumida: sin llamadas a Gemini ni uso pagado del producto.
El consumo de la herramienta de desarrollo no se cuantificó.

## S-005 · 09-11-2026 y 10-11-2026 · Plan e implementación

Herramienta y modelo: Claude Code · Claude Opus 5.5 (`claude-opus-5-5`),
para el plan y la implementación. Claude (chat) · Claude Opus 5.5, como
apoyo de AlexDLG1 para revisar el plan.
Usado por: AlexDLG1.

Fases en que se usó: plan, implementación, pruebas y documentación.

Instrucción clave:
Proponer el plan de S-005 en modo de solo lectura, con las reglas de guardado
en `academics/services.py`, validación en el servidor, `update_or_create` para
corregir y una ruta mínima del docente coordinada con S-004 y S-010. Después,
implementar las tareas una por una, mostrando el diff y deteniéndose antes de
cada commit, sin hacer push.

Revisión del plan:
AlexDLG1 se apoyó en Claude (chat, Claude Opus 5.5) para revisar el plan que
propuso Claude Code. Las decisiones y las correcciones las tomó AlexDLG1; las
que dependían de S-004 y S-010 las confirmó antes con Brayan11Hernandez.

Qué se aceptó sin cambios:
- El enfoque del plan: `get_taught_course`, `record_grade` y
  `get_course_grade_sheet` en `academics/services.py`, y una sola pantalla en
  `/docente/cursos/<código>/notas/`.
- El formulario solo valida el formato; la pertenencia del estudiante y del
  tema al curso la decide el servicio (CA-8).
- La misma respuesta 403 para un curso ajeno, un curso inexistente y una
  cuenta sin perfil docente.

Qué se corrigió o descartó, y por qué:
- AlexDLG1 fijó con Brayan11Hernandez los nombres de las rutas de S-004 y
  S-005, y que `get_taught_course` reciba `user` y devuelva `None` en los tres
  casos de rechazo. Por coherencia, `record_grade` también recibe `user`.
- AlexDLG1 movió `get_taught_course` al primer commit de servicios, porque la
  rama de S-004 parte de la de S-005, y descartó el rebase y el force push.
- AlexDLG1 decidió entregar un solo PR con `Closes #9`, sin dividirlo en
  entregas, y justificar su tamaño en la descripción del PR.
- AlexDLG1 confirmó que `estudiante_08` tiene 60 en "Git y GitHub avanzado"
  para CA-2 y que el enlace a la planilla lo agrega S-004.
- El agente propuso rechazar en `record_grade` a un usuario no autenticado sin
  consultar la base; AlexDLG1 lo aprobó con su prueba.
- La primera versión de esa prueba contó tres `SAVEPOINT` de la transacción.
  La comprobación se movió fuera de `transaction.atomic`.
- Dos pruebas de vista fallaron por errores de las pruebas, no de la vista:
  `assertRedirects` consumía el mensaje de confirmación, y cambiar la
  contraseña invalidaba la sesión de CA-5. Se corrigieron ambas.
- Al documentar el README se comprobó que `rebuild_synthetic_data` no borra
  las notas registradas a estudiantes sin notas en el manifiesto, como
  `estudiante_02`. Se documentó; el comando no se modificó porque pertenece
  a S-002.

Resultado registrado por el autor:
- Suite de `accounts`, `academics` y `tutor`: 120 pruebas superadas.
- `manage.py check`: sin problemas.
- `makemigrations --check --dry-run`: no detectó cambios.
- `pip check`: no detectó dependencias incompatibles.
- Revisión en el navegador con `docente_01`: CA-1 (85 a `estudiante_02`),
  CA-2 (`estudiante_08` de 60 a 75), CA-3 (`-5`, `101` y vacío con errores en
  español), CA-4 (`estudiante_02` ve 85 y 85.00 en `/perfil/`), CA-6 (DES-WEB
  sin `estudiante_demo` ni `estudiante_01`) y CA-8 (`BD-APL` responde 403).
  CA-5 y CA-7 quedaron cubiertos por las pruebas automatizadas.
- La verificación independiente de ramosdeleon555 sigue pendiente.

Costo o cuota consumida:
No se realizaron llamadas a Gemini ni a la API de IA del producto.
El consumo de las conversaciones de Claude Code y Claude no se cuantificó.

## S-004 · 09-11-2026 · Especificación y planificación

Herramienta y modelo: ChatGPT (OpenAI) · GPT-6.
Usado por: Brayan11Hernandez.

Fases en que se usó: spec, plan, implementación, pruebas y depuración.

Instrucción clave:
Analizar los requisitos de S-004 y preparar la especificación
y el plan técnico para gestionar cursos, temas académicos y
asignaciones de estudiantes en TutoBosco.

Respetar AGENTS.md, docs/plan.md y las decisiones del equipo.
Conservar las funcionalidades de S-003 y S-005, reutilizar
get_taught_course() y evitar reemplazar archivos compartidos.

Qué se aceptó sin cambios:
- La estructura general de la especificación S-004.
- Los ocho criterios de aceptación Dado/Cuando/Entonces.
- La propuesta de utilizar los modelos académicos existentes.
- La organización de las pantallas de cursos, temas y estudiantes.
- La estrategia de realizar modificaciones pequeñas y verificables.

Qué se corrigió o descartó, y por qué:
- Se aclaró la diferencia entre usuarios no autenticados
  y usuarios autenticados sin permisos.
- Se confirmó que los permisos deben verificarse en el servidor
  mediante get_taught_course().
- Se mantuvo la separación de responsabilidades entre S-004,
  S-005 y S-010 para evitar conflictos entre implementaciones.
- Se descartó reemplazar archivos completos que ya contienen
  código de otros integrantes.
- Se estableció que verificacion.md será completado por
  AlexDLG1 y no por el autor de S-004.

Revisión humana:
El autor revisó y aprobó el plan técnico, documentando los
ajustes de seguridad y las responsabilidades de integración.
La implementación y las pruebas funcionales están pendientes.


Actualizacion de implementacion y pruebas (10-11-2026):

- Herramienta utilizada: ChatGPT (OpenAI), modelo GPT-6.
- Se desarrollaron las pantallas de cursos, temas y estudiantes.
- Se implementaron formularios, vistas y rutas de S-004.
- Se agregaron pruebas de listado, validaciones y operaciones.
- Se ejecutaron 96 pruebas generales correctamente.
- Se corrigieron importaciones duplicadas y cambios innecesarios
  de formato para conservar el codigo de otros integrantes.
- Las pruebas de vistas utilizaron autorizacion simulada.
- Queda pendiente verificar los permisos reales mediante
  get_taught_course cuando S-005 se integre en main.
Costo o cuota consumida:
No se realizaron llamadas directas a la API de IA desde
TutoBosco para esta actividad.
El consumo de la conversación en ChatGPT no se cuantificó.

## S-008 · 10-11-2026 · Plan e implementación

Herramienta y modelo: OpenCode · deepseek-v4.1-flash.
Usado por: douglas-yasser.

Fases en que se usó: plan / implementación / pruebas.

Instrucción clave (resumen, no la conversación completa):
Proponer el plan de S-008 en modo solo lectura, incorporar las
correcciones humanas acordadas en el issue #8 e implementar el panel
del docente con pruebas de los criterios CA-1 a CA-5.

Qué se aceptó sin cambios:
- La propuesta de plan.md revisada y aprobada por douglas-yasser.

Qué se corrigió o descartó, y por qué:
- El redirect posterior al login se mantuvo en S-008 frente a la nota
  del plan de S-004 que lo reservaba a S-010; decisión humana del
  autor registrada en el issue #8.
- Las rutas cambiaron de identificadores numéricos a course_code
  bajo /docente/panel/ para no pisar las rutas acordadas de S-004.

Costo o cuota consumida (si aplica): sin llamadas a Gemini ni uso
pagado del producto. El consumo de la herramienta de desarrollo no se
cuantificó.

## S-005 · 10-11-2026 · Verificación independiente asistida

Herramienta y modelo: OpenCode · GPT-6.1 Sol (`openai/gpt-6.1-sol`).
Usado por: ramosdeleon555, según la confirmación del usuario de la sesión.

Fases en que se usó: pruebas y documentación de la verificación.

Instrucción clave:
Verificar el commit `1c26d94` del PR #45 en la misma rama, registrar solo
resultados comprobados, obtener capturas reales del navegador, restaurar
los datos y avisar al autor ante cualquier fallo sin corregir su código.

Qué se aceptó sin cambios:
- El usuario confirmó la estructura y el plan de verificación de S-005 y
  autorizó los dos auxiliares temporales fuera del repositorio.
- Suite completa: 150 pruebas OK. Recorrido de CA-1 a CA-8 en Chrome
  automatizado, con formularios reales de acceso, cierre de sesión y notas.
- Registro de consultas de persistencia, nota única, promedio y aislamiento;
  capturas reales en `specs/S-005-registro-notas/img/`.
- Limpieza posterior comprobada: `estudiante_02` sin notas y `estudiante_08`
  nuevamente con 60 en Git y GitHub avanzado de PROG-COM.

Qué se corrigió o descartó, y por qué:
- La suite se repitió después de una interrupción por el tiempo máximo del
  comando. Solo se declara aprobada la ejecución completa de 150 pruebas.
- Se reutilizó el servidor local identificado del repositorio porque el
  puerto 8000 ya estaba ocupado. Se desactivó la caché de Chrome en lugar
  de declarar una pulsación manual de Ctrl+F5.
- Se repitió la captura del 403 sin el aviso de guardar contraseña de Chrome.
- Los POST no autorizados de CA-8 se atribuyen a la suite; no se presentan
  como formularios manipulados manualmente ni se atribuye al usuario un
  recorrido manual realizado por el agente.
- No se modificó el código de la aplicación ni se instalaron paquetes.

Costo o cuota consumida: sin llamadas a Gemini ni a la API de IA del
producto. El consumo de la herramienta de desarrollo no está disponible.

## S-006 · 10-11-2026 · Plan y primer bloque

ChatGPT (Codex) ayudó a proponer y ajustar el plan técnico aprobado por
JavEstrada09 y a preparar el acceso al tutor por curso inscrito y la
validación del umbral. Se incorporaron las observaciones de
douglas-yasser sobre el 403, la privacidad en modo demo y las revisiones
de conversación. Se reutilizó el cálculo de temas débiles de S-008.

Se usaron respuestas locales y dobles de prueba para comprobar este
bloque, sin llamadas a Gemini. La revisión del cambio por el autor y
la verificación independiente de la funcionalidad quedan pendientes.

## S-004 · 10-11-2026 · Continuación de implementación

Herramienta y modelo: OpenCode · `openai/gpt-5.6-sol`.
Usado por: Brayan11Hernandez.

Fases en que se usó: revisión de la implementación, ajustes de interfaz,
pruebas automatizadas y documentación.

Instrucción clave:
Continuar la parte de Brayan correspondiente a S-004 siguiendo el plan
aprobado y los lineamientos del repositorio.

Trabajo realizado:
- Se comparó la implementación existente con los ocho criterios de
  aceptación y el plan aprobado.
- Se corrigió la edición inválida de temas para conservar el valor enviado
  y mostrar el error junto al campo correspondiente.
- Se agregó el mensaje específico para nombres de tema obligatorios.
- Se ampliaron las pruebas para comprobar aislamiento entre cursos,
  confirmaciones visibles, datos actualizados, prevención de duplicados y
  conservación de datos ante una edición inválida.
- Se documentaron en README las tres pantallas de gestión académica.
- Se ejecutaron 17 pruebas específicas de S-004 y las 129 pruebas de
  `accounts`, `academics` y `tutor`; todas finalizaron correctamente.

Pendiente:
- Las pruebas de vistas todavía simulan `get_taught_course()`. La
  autorización real de CA-7 se probará después de que la implementación de
  S-005 se fusione en `main`, conforme al plan aprobado de S-004.
- AlexDLG1 debe realizar la verificación independiente; no se registra aquí
  ninguna aprobación ni evidencia en su nombre.

Costo o cuota consumida: no hubo llamadas a Gemini ni uso pagado del
producto. El consumo de la herramienta de desarrollo no se cuantificó.

## S-007 · 10-11-2026 · Implementación local de práctica

Herramienta y modelo: OpenCode · `openai/gpt-6.1-sol`.
Usado por: ramosdeleon555, autor de S-007 y S-009.

- Se propuso el plan en modo de solo lectura. El autor confirmó el contrato
  PracticeExercise con S-009, la rama s-007-ejercicios y aprobó el plan completo.
- Se integró main conservando el historial; la integración y el desarrollo
  quedaron sin commit a la espera de revisión del autor.
- El asistente implementó persistencia UUID, catálogo demo por curso/tema,
  proveedores reutilizando el transporte Gemini, validación de lotes,
  autorización, pantalla y pruebas. No instaló dependencias.
- Las 19 pruebas específicas y las 215 de regresión pasaron. También
  pasaron check, makemigrations --check --dry-run y pip check.
- La migración se aplicó localmente y el recorrido HTTP con estudiante_03
  creó un ejercicio demo y lo consultó por UUID desde localhost.
- El autor debe leer y ejecutar los cambios antes de solicitar commits.
  Brayan11Hernandez tiene pendiente la verificación independiente de CA-1 a CA-10.
  No se presenta S-007 como terminada ni se atribuye aprobación al verificador.

Costo del producto durante el bloque inicial de implementación y pruebas:
USD 0.00; ninguna llamada real a Gemini en ese bloque. El proveedor real y
el error 429 se simularon. El consumo de la herramienta de desarrollo no
se cuantificó. La prueba real posterior se registra en la entrada siguiente.

## S-007 · 10-11-2026 · Prueba real con Gemini y evidencia detallada

Herramienta y modelo de desarrollo: OpenCode · `openai/gpt-6.1-sol`.
Usado por: ramosdeleon555. Modelo del producto: `gemini-3.5-flash-lite`.

El autor informó que probó el modo demo y solicitó una prueba real con la
clave ya configurada. El asistente inició temporalmente el servidor en el
puerto 8001 con `AI_MODE=real`, sin modificar `.env` ni mostrar secretos.
Realizó acceso HTTP como estudiante_03 y un POST de práctica con CSRF.

- Curso: PROG-COM, Programación Comercial; tema: Ingeniería de prompts.
- Nota comprobada: 58; umbral: 60. El tema cumple la comparación estricta.
- Resultado: HTTP 200 en 6,12 segundos, un ejercicio persistido con modo
  `real`, sin clave demo ni aviso de alternativa grabada.
- UUID: `04ee22d6-a90a-485a-ae8e-0d227530cb94`.
- Persistido a las 19:44 del 10-11-2026, Guatemala
  (`2026-11-11T01:44:04.025239+00:00`).

Enunciado completo recuperado del ejercicio persistido:

> Diseñe un prompt estructurado utilizando la técnica de pocos ejemplos (few-shot prompting) para que un modelo de lenguaje extraiga correctamente los datos fiscales de una factura en formato de texto libre y los devuelva en un formato JSON estandarizado para su posterior registro contable.

El asistente comprobó el texto en español, trato formal y correspondencia
con el tema débil, así como los datos persistidos y la etiqueta de IA en
el HTML. No conservó la respuesta HTTP cruda del proveedor ni realizó una
revisión visual en navegador. Después detuvo el servidor temporal;
el puerto 8000 continuó en demo con el ejercicio real disponible.

El autor solicitó incluir la respuesta completa y mayores detalles en la
evidencia; revisó la propuesta y autorizó actualizar verificacion.md,
registro-ia.md y gasto.md. El recorrido y sus límites se documentan en
`specs/S-007-ejercicios/verificacion.md`. La verificación independiente
de Brayan11Hernandez y el cierre de S-007 permanecen pendientes.

Consumo: una solicitud real a Gemini. Tokens y costo monetario pendientes
de confirmar con el proveedor; no se afirma costo cero para esta llamada.
No se habilitó facturación ni se modificó su configuración durante la prueba.

## S-007 · Corrección de aislamiento de pruebas tras el reporte de Brayan

Herramienta y modelo: OpenCode · `openai/gpt-6.1-sol`.
Usado por: Jeffersson Ramos (`ramosdeleon555`), autor de S-007.
Base de la corrección: `a6bd399`, rama `s-007-ejercicios`.

El autor trasladó el reporte de Brayan: 2 fallos y 14 errores en la suite
entregada. Solicitó corregir la selección de modo y la configuración de
Gemini de las pruebas, ejecutar ambas suites y entregar un nuevo commit.
Confirmó la estructura de tres archivos antes de modificarlos.

Diagnóstico y cambio:

- Se reprodujeron exactamente 2 fallos y 14 errores con GEMINI_API_KEY
  vacía en el proceso de Python. Las pruebas anteriores habían pasado en
  el equipo del autor con una clave local disponible: eso ocultó la dependencia.
- Parchear GeminiExerciseProvider.generate no evita que se ejecute antes
  su constructor. Sin clave, este lanza un error de configuración y el
  servicio utiliza demo; los mocks del proveedor real no reciben la llamada.
- Se eliminó AI_MODE del override común de PracticeTests y se declaró
  explícitamente demo o real en cada prueba, según corresponda.
- Se centralizó una clave sintética en la configuración común de pruebas.
  No es una credencial del proveedor y las llamadas reales siguen simuladas.
- No se relajaron aserciones ni se cambió el servicio de producción.

Comprobaciones ejecutadas por el asistente en el entorno Windows del autor:

| Ejecución | Configuración externa | Resultado |
| --- | --- | --- |
| tutor.test_exercises, verbosity 2 | GEMINI_API_KEY vacía; AI_MODE=real | 19 pruebas, OK, 0.881 s |
| accounts academics tutor --noinput | GEMINI_API_KEY vacía; AI_MODE=demo | 215 pruebas, OK, 350.511 s |

Comandos utilizados para excluir la clave local antes de cargar Django:

```powershell
& ".\.venv\Scripts\python.exe" -c "import os, runpy, sys; os.environ['GEMINI_API_KEY'] = ''; os.environ['AI_MODE'] = 'real'; sys.argv = ['manage.py', 'test', 'tutor.test_exercises', '--verbosity', '2', '--noinput']; runpy.run_path('manage.py', run_name='__main__')"
& ".\.venv\Scripts\python.exe" -c "import os, runpy, sys; os.environ['GEMINI_API_KEY'] = ''; os.environ['AI_MODE'] = 'demo'; sys.argv = ['manage.py', 'test', 'accounts', 'academics', 'tutor', '--noinput']; runpy.run_path('manage.py', run_name='__main__')"
```

Se usa Python para fijar el valor vacío porque PowerShell 5.1 puede eliminar
una variable al asignarle una cadena vacía, permitiendo que dotenv vuelva a
cargar el valor local. No se modificó .env ni se mostraron secretos.

Estos resultados son del autor asistido; no son la repetición independiente
de Brayan. No se modificaron verificacion.md ni los archivos de evidencia
del verificador. Brayan debe repetir ambas suites sobre el nuevo commit.

Consumo del producto en esta corrección: ninguna llamada real a Gemini;
sin consumo de cuota ni costo del servicio. No se instalaron dependencias.
El consumo de la herramienta de desarrollo no se cuantificó.

## S-007 · Corrección de enunciados formales tras la revisión del PR #56

Herramienta y modelo: OpenCode · `openai/gpt-6.1-sol`.
Usado por: Jeffersson Ramos (`ramosdeleon555`), autor de S-007.
Base de la corrección: `8a7a72c`, rama `s-007-ejercicios`.

El autor trasladó una revisión de código que encontró una heurística de
trato formal demasiado restrictiva. Un enunciado válido podía rechazarse
por no incluir palabras de una lista literal. El autor aprobó la propuesta
de cambios en exercise_services.py, test_exercises.py, plan.md y este registro.

Reproducción antes de corregir:

- Se añadieron dos pruebas de regresión: una con dos enunciados formales
  y otra con un lote completo de seis ejercicios.
- «Defina las etapas del ciclo de integración de una rama.» fue rechazado.
- El enunciado real documentado, sustituyendo «para su posterior registro
  contable» por «para posterior registro contable», también fue rechazado.
- Un lote de seis enunciados formales fue rechazado sin persistir ejercicios.
- Ejecución de esas dos pruebas sobre el servicio anterior: tres errores
  InvalidTutorResponseError (dos subcasos y un lote), reproduciendo el bloqueo.

Corrección:

- Se retiró la exigencia de palabras literales, siguiendo la decisión de
  S-006 (`30ad0c3`). Se conserva el rechazo de tuteo explícito.
- Se mantienen las validaciones estructurales, de tamaño, HTML, duplicados
  y pertenencia de temas, así como la persistencia atómica del lote.
- La regresión comprueba que los enunciados formales se guardan con el
  propietario, curso, tema y procedencia correctos y que se guardan los
  seis ejercicios de un lote válido.
- Se sustituyó la expectativa de rechazar una frase inglesa por más casos
  de tuteo explícito. La lista retirada no era una detección fiable de idioma.
  La prueba de transporte comprueba ahora que las instrucciones enviadas
  exigen «en español con trato de usted»; CA-10 conserva revisión humana.

Resultados locales del asistente en Windows, sin clave real en el proceso:

| Ejecución | Configuración externa | Resultado |
| --- | --- | --- |
| tutor.test_exercises, verbosity 2 | GEMINI_API_KEY vacía; AI_MODE=real | 21 pruebas, OK, 0.715 s |
| accounts academics tutor --noinput | GEMINI_API_KEY vacía; AI_MODE=demo | 217 pruebas, OK, 236.405 s |
| manage.py check | Configuración local | Sin errores |
| manage.py makemigrations --check --dry-run | Configuración local | Sin cambios pendientes |

Se usaron los mismos comandos con Python/runpy registrados en la corrección
anterior para fijar la clave vacía antes de cargar Django y dotenv. Los
proveedores reales se simularon; no se modificó .env ni se instalaron paquetes.
Consumo del producto en esta corrección: ninguna llamada real a Gemini,
sin consumo de cuota ni costo del servicio. El consumo de desarrollo no se cuantificó.

No se alteró la evidencia de Brayan ni se declara aprobada la verificación.
Los resultados anteriores son comprobaciones del autor asistido. Brayan debe
repetir ambas suites sobre la entrega corregida antes de aprobar el PR.
No se modificó spec.md porque se corrige el cumplimiento de CA-4 y CA-10,
sin cambiar los requisitos.

## S-004 · 10-11-2026 · Integración final con S-005

Herramienta y modelo: OpenCode · `openai/gpt-5.6-sol`.
Usado por: Brayan11Hernandez.

Fases en que se usó: integración, pruebas de autorización y documentación.

Trabajo realizado:
- Se fusionó `main` después de la incorporación de S-005, sin fusionar
  directamente su rama.
- Las vistas de temas y estudiantes quedaron conectadas con la función
  compartida `get_taught_course()` y se habilitó el enlace a la planilla de
  notas desde el listado de cursos.
- Se eliminaron los mocks de autorización de S-004. Las pruebas ahora usan
  perfiles docentes, asignaciones y cursos reales de la base de pruebas.
- CA-7 cubre un docente ajeno, una cuenta estudiantil, un curso inexistente,
  POST no autorizados sin cambios, acceso anónimo y protección CSRF.
- Se ejecutaron 21 pruebas específicas de S-004 y las 173 pruebas de
  `accounts`, `academics` y `tutor`; todas finalizaron correctamente.
- `manage.py check`, `makemigrations --check --dry-run` y `pip check`
  finalizaron correctamente.

Pendiente:
- AlexDLG1 debe ejecutar CA-1 a CA-8 en su computadora y crear
  `specs/S-004-temas-asignacion/verificacion.md`. No se registra ninguna
  verificación ni aprobación en su nombre.
- S-004 no debe marcarse como terminada ni cerrar el issue #8 antes de que
  esa evidencia independiente sea revisada e integrada.

Costo o cuota consumida: no hubo llamadas a Gemini ni uso pagado del
producto. El consumo de la herramienta de desarrollo no se cuantificó.

## S-006 · 10-11-2026 · Segundo bloque

ChatGPT (Codex) ayudó a implementar el modelo de conversación, su
migración, el control de revisiones y la limpieza al cerrar sesión.
Las pruebas usan SQLite y cuentas sintéticas. Este bloque se ejecutó
sin llamadas a Gemini. La revisión del autor y la verificación
independiente en la computadora de Douglas quedan pendientes.


## S-006 · 10-11-2026 · Bloque 3a: proveedores

ChatGPT (Codex) preparó el contexto mínimo del hilo, las instrucciones
separadas para Gemini y las grabaciones por curso, tema e intención.
Se reutiliza `is_weak` de S-008. Para mantener PRs revisables, el bloque 3
se entrega como proveedores (3a) e integración con la pantalla (3b), sin
cambiar las decisiones del plan aprobado ni declarar terminada S-006.

Las pruebas ejecutadas en Linux usan datos sintéticos, proveedor simulado
y red bloqueada para el demo. No se llamó a Gemini real ni se generó gasto
del producto. La lectura y ejecución por Jav en Windows y la verificación
independiente de Douglas quedan pendientes para este cambio.


## S-006 · 10-11-2026 · Bloque 3b: integración de la conversación

ChatGPT (Codex) ayudó a integrar la vista y la plantilla con el hilo del
curso, las revisiones, el historial, el reinicio y la continuación en
demo con la pregunta pendiente. Se sustituyó el formulario anterior de
continuación, que siempre usaba la pregunta de ejemplo, según el contrato
del plan aprobado. Las respuestas siguen mostrándose como texto escapado.

Se ejecutaron pruebas automatizadas en Linux con cuentas sintéticas y
Gemini simulado; no se hicieron llamadas reales ni hubo gasto del producto.
La lectura y ejecución del cambio por Jav en Windows y la aceptación
independiente de Douglas quedan pendientes. La matriz de los nueve
criterios está en `specs/S-006-tutor/plan.md`; su evidencia y el commit
probado deben registrarse en `verificacion.md` antes de fusionar.


## S-006 · 10-11-2026 · Corrección tras verificación independiente

Douglas reportó sobre `ece9dee` que Gemini recomendaba el tema correcto o
rechazaba solicitudes de terceros, pero la validación descartaba respuestas
formales que usaban «le» y «su» sin el pronombre literal «usted».
ChatGPT (Codex) ayudó a retirar esa condición y a añadir pruebas simuladas
de recomendación, privacidad y guardado en el historial sin activar demo.
Se conservan las instrucciones de trato formal, la mención del curso,
la comprobación de español, los límites de longitud y los errores esperados.

No se llamó a Gemini real durante esta corrección. No se modifican los
resultados ni el consumo registrados por Douglas en su worktree. Queda
pendiente la ejecución del autor en Windows y la repetición independiente
de CA-1, CA-5 y CA-9 en modo real sobre el nuevo commit antes de aprobar.


## S-006 · 10-11-2026 · Cierre documental

ChatGPT (Codex) ayudó a actualizar el estado de la spec, la tabla de
`docs/plan.md` y la nota del README a partir de la evidencia independiente
de douglas-yasser incorporada en el PR #53. Se mantuvieron sin cambios
`verificacion.md` y `docs/gasto.md`, incluidos los resultados originales,
la repetición sobre `30ad0c3` y el consumo de Gemini. Este cambio es solo
documental; no se ejecutaron nuevas consultas a Gemini ni pruebas de la
aplicación para el cierre. El PR documental queda pendiente de revisión.

## S-007 · 11-11-2026 · Cierre documental

Herramienta y modelo: OpenCode · `deepseek-v4.1-flash-free`.
Usado por: Jeffersson Ramos (`ramosdeleon555`), autor de S-007.

El asistente ayudó a actualizar el estado de la spec, la tabla de
`docs/plan.md` y la nota del README a partir de la verificación
independiente de Brayan11Hernandez y su aprobación del PR #56 sobre
`acf58d0`. Se mantuvieron sin cambios `verificacion.md` y `docs/gasto.md`,
incluidos los resultados originales, la repetición de CA-4, CA-9 y CA-10
sobre `acf58d0` (21 y 217 pruebas) y el consumo de Gemini. Este cambio es
solo documental; no se ejecutaron nuevas consultas a Gemini ni pruebas de
la aplicación para el cierre. El PR documental queda pendiente de revisión.
