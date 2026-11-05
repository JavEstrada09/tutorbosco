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
No se han registrado correcciones de contenido al borrador.
La revisión de douglas-yasser está pendiente.

Costo o cuota consumida:
No se realizaron llamadas a la API de IA del producto.
El consumo de esta conversación no se cuantificó.

]633;E;echo;65469bf1-3e3d-44cc-bb99-92783a4d9c7d]633;C
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