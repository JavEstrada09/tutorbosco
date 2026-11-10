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
No se han registrado correcciones de contenido al borrador.
La revisión de douglas-yasser está pendiente.

Costo o cuota consumida:
No se realizaron llamadas a la API de IA del producto.
El consumo de esta conversación no se cuantificó.
## S-004 · 09-11-2026 · Especificación y planificación

Herramienta y modelo: ChatGPT (OpenAI) · GPT-6.
Usado por: Brayan11Hernandez.

Fases en que se usó: spec y plan.

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

Costo o cuota consumida:
No se realizaron llamadas directas a la API de IA desde
TutoBosco para esta actividad.
El consumo de la conversación en ChatGPT no se cuantificó.
