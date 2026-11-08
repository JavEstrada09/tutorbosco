# Registro de uso de inteligencia artificial

Registrar una entrada por spec.
No incluir claves, contraseñas ni datos reales de estudiantes.

Este archivo registra las herramientas y los modelos usados para
desarrollar el proyecto. El modelo del producto es Gemini 3.8 Flash
(`gemini-3.8-flash`) y se documenta en docs/adr/ADR-001-stack.md.

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
