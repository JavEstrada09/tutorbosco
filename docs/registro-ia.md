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
conservar el modelo coordinado para S-002, registrar D-008 y actualizar
los estados documentales después de la fusión de la spec en PR #24.

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
- D-008 dejó de posponerse a S-002: JavEstrada09 la aprobó antes de la
  implementación de S-001 con roles mediante perfiles y sin imponer
  exclusividad.
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
