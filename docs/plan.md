# Plan de trabajo — TutoBosco

## Estado

Plan inicial con las 10 specs seleccionadas.

El reparto comienza con:
- JavEstrada09: S-001, esqueleto funcional.
- douglas-yasser: S-002, modelo y datos sintéticos.

Las asignaciones se revisarán con el equipo en el PR
de preparación documental.

Entrega final: 11 de noviembre de 2026.

## Organización

- Cada spec tiene un autor y un verificador distinto.
- El autor lleva la funcionalidad desde su especificación
  hasta el PR final.
- El verificador ejecuta los criterios en su computadora
  y registra resultados y evidencia.
- Cada integrante debe completar al menos dos specs como autor
  y dos como verificador de otros integrantes.
- Cada spec tendrá un issue de GitHub.
- Los números de issues se añadirán después de crearlos.
- S-000 corresponde a la preparación documental y no cuenta
  como una funcionalidad para las contribuciones mínimas.

Este documento organiza el trabajo del equipo.
El plan técnico de cada spec se guarda en:
specs/S-NNN-nombre/plan.md.

## Lista de specs

| Spec | Nombre | Requisito | Autor | Verificador | Issue | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | Esqueleto: login, dato de perfil, respuesta IA y modo demo | RF-01, RF-02 y RF-04 parciales; RNF-04 y RNF-06 parciales | JavEstrada09 | douglas-yasser | Pendiente | Por especificar |
| S-002 | Modelo de datos y script de datos sintéticos | RNF-01; soporte de RF-02 y RF-03 | douglas-yasser | JavEstrada09 | Pendiente | Por especificar |
| S-003 | Perfil académico | RF-02 | AlexDLG1 | ramosdeleon555 | Pendiente | Por especificar |
| S-004 | Gestión académica del docente: temas y asignación | RF-03 parcial | Brayan11Hernandez | AlexDLG1 | Pendiente | Por especificar |
| S-005 | Registro y corrección de notas | RF-03 parcial | AlexDLG1 | ramosdeleon555 | Pendiente | Por especificar |
| S-006 | Tutor personalizado: contexto académico e historial | RF-04; RNF-05 | JavEstrada09 | douglas-yasser | Pendiente | Por especificar |
| S-007 | Identificación de temas débiles y generación de ejercicios | RF-05 parcial; RNF-04 | ramosdeleon555 | Brayan11Hernandez | Pendiente | Por especificar |
| S-008 | Panel del docente | RF-06 | douglas-yasser | JavEstrada09 | Pendiente | Por especificar |
| S-009 | Respuestas a ejercicios y retroalimentación personalizada | RF-05 parcial; RNF-04 | ramosdeleon555 | Brayan11Hernandez | Pendiente | Por especificar |
| S-010 | Control de acceso, seguridad e interfaz en español | RF-01; RNF-07 | Brayan11Hernandez | AlexDLG1 | Pendiente | Por especificar |

## Distribución por integrante

| Integrante | Autor de | Verificador de |
| --- | --- | --- |
| JavEstrada09 | S-001 y S-006 | S-002 y S-008 |
| douglas-yasser | S-002 y S-008 | S-001 y S-006 |
| AlexDLG1 | S-003 y S-005 | S-004 y S-010 |
| Brayan11Hernandez | S-004 y S-010 | S-007 y S-009 |
| ramosdeleon555 | S-007 y S-009 | S-003 y S-005 |

## Alcance de S-007 y S-009

### S-007 — Temas débiles y generación de ejercicios

Autor: ramosdeleon555.
Verificador: Brayan11Hernandez.

Responsabilidades:
- Permitir solicitar práctica de un curso del estudiante.
- Identificar temas con nota menor al umbral configurable.
- Generar ejercicios únicamente de esos temas mediante IA.
- Mostrar un aviso cuando no existan temas débiles.
- Permitir generar la práctica mediante respuestas grabadas
  cuando esté activo el modo demo.

La recepción de respuestas y su retroalimentación
corresponden a S-009.

### S-009 — Respuestas y retroalimentación

Autor: ramosdeleon555.
Verificador: Brayan11Hernandez.

Responsabilidades:
- Permitir responder los ejercicios generados en S-007.
- Relacionar cada respuesta con su ejercicio y estudiante.
- Obtener retroalimentación de IA sobre las respuestas.
- Mostrar la retroalimentación en español y con trato de usted.
- Permitir completar este recorrido sin red en modo demo.

Dependencia: S-007.

Ambas specs deben acordar cómo se identifican y representan
los ejercicios y las respuestas antes de implementar.
Cada spec tendrá sus propios criterios de aceptación,
plan, verificación e issue.

## Arranque: S-001 y S-002

JavEstrada09 y douglas-yasser coordinarán primero
el modelo mínimo y los datos necesarios para el esqueleto.

### S-001 — Esqueleto funcional

Responsable: JavEstrada09.
Verificador: douglas-yasser.

Recorrido mínimo:
1. Iniciar sesión con un estudiante sintético.
2. Mostrar un dato de su perfil desde la base local.
3. Obtener una respuesta real del proveedor de IA.
4. Obtener una respuesta grabada al activar el modo demo.

El esqueleto utiliza únicamente los datos y componentes
necesarios para demostrar la integración.

No representa el cumplimiento completo de los requisitos
de acceso, perfil o tutor.

### S-002 — Modelo y datos sintéticos

Responsable: douglas-yasser.
Verificador: JavEstrada09.

Completar el modelo académico y el generador reproducible:
- Al menos 30 estudiantes.
- Al menos 3 docentes.
- Al menos 4 cursos.
- Al menos 6 temas por curso.
- Programación Comercial con los temas del enunciado.
- Notas variadas y perfiles claramente distintos.
- Reconstrucción de los datos con un comando documentado.

Coordinar los cambios con el modelo mínimo de S-001
para evitar estructuras duplicadas o migraciones incompatibles.

## Orden de trabajo

La numeración identifica las specs; no obliga a desarrollarlas
en orden numérico.

1. Completar la preparación documental.
2. Coordinar S-001 y S-002 para establecer el modelo mínimo.
3. Implementar y verificar el esqueleto de S-001.
4. Completar el modelo y los datos sintéticos de S-002.
5. Incorporar los controles de S-010 desde las primeras entregas.
6. Desarrollar S-003, S-004 y S-005 según sus dependencias.
7. Completar el tutor de S-006.
8. Implementar S-007 y después integrar S-009.
9. Completar S-008 cuando estén disponibles los datos académicos.
10. Verificar todos los requisitos obligatorios desde main.

Las actividades independientes pueden avanzar en paralelo
cuando sus specs estén fusionadas, sus planes aprobados
y sus dependencias disponibles.

El modo demo comienza en S-001 y se amplía con S-006,
S-007 y S-009 para demostrar RF-04 y RF-05 sin red.

## Trabajo en paralelo

Las specs podrán avanzar en paralelo cuando:
- Su especificación esté fusionada a main.
- Su plan haya sido revisado y aprobado.
- Sus dependencias estén disponibles.
- Los contratos de datos y las responsabilidades estén claros.

Coordinar modificaciones de modelos, migraciones y archivos comunes.

Si una persona trabaja en dos specs simultáneamente,
utilizar git worktree para mantener separados los cambios.

## Requisitos transversales

- RNF-02: secretos fuera del repositorio.
- RNF-03: presupuesto global de IA de USD 10 y registro del gasto.
- RNF-04: tutor y práctica demostrables sin red.
- RNF-05: contexto limitado al estudiante autenticado.
- RNF-06: ejecución local e instalación reproducible.
- RNF-07: español y trato de usted al estudiante.

Cada spec debe incluir las restricciones que le correspondan.

## Requisito deseable

RF-07, plan de estudio persistente, queda fuera
de las diez specs obligatorias de este plan.

Podrá incorporarse mediante una nueva spec cuando todos
los requisitos obligatorios estén completos y verificados.

Los cinco integrantes tienen asignadas dos specs obligatorias
como autores y dos como verificadores.

Las asignaciones cuentan para la contribución mínima
solo cuando las specs estén terminadas y exista evidencia.

## Proceso por spec

1. Crear el issue y registrar autor y verificador.
2. Redactar spec.md con criterios Dado/Cuando/Entonces.
3. Revisar y fusionar la spec mediante PR antes del código.
4. Solicitar al agente un plan en modo de solo lectura.
5. Revisar, corregir y aprobar plan.md.
6. Implementar en s-NNN-nombre con commits S-NNN:.
7. El autor lee y ejecuta cada cambio antes del commit.
8. El verificador prueba en otra computadora.
9. Registrar verificacion.md y evidencia.
10. Declarar el uso real de IA y resolver las desviaciones.
11. Aprobar y fusionar el PR final con Closes #N.
12. Comprobar main en otra computadora y actualizar el estado.

## Seguimiento

Estados:
- Por especificar.
- Spec en revisión.
- Spec aprobada.
- Plan en revisión.
- En implementación.
- En verificación.
- Terminada.

Usar Terminada únicamente cuando se cumpla el criterio
de terminado del enunciado y AGENTS.md.

Actualizar este documento al cambiar responsables,
issues, dependencias o estados.

## Disponibilidad

Horarios de desarrollo y revisión pendientes de confirmar.

Cada integrante comunicará cuándo puede desarrollar
y cuándo puede verificar el trabajo de otro compañero.