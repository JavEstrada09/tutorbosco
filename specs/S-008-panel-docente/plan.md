# Plan S-008

Propuesto por: OpenCode · deepseek-v4.1-flash · modo Plan
Revisado y aprobado por: douglas-yasser · 10-11-2026

## Enfoque

Tres vistas de solo lectura para el docente: inicio con sus cursos, panel
del curso con lista de estudiantes (promedio y temas débiles, ordenable
por promedio) y desglose por tema con el conteo de estudiantes que lo
tienen débil, y detalle por estudiante. Se reutiliza `calculate_average()`
de S-003 y se centraliza el cálculo de temas débiles en
`academics/services.py` para que S-007 lo reutilice. Sin cambios de modelo
ni de migraciones. No usa IA.

## Archivos que se crean o modifican

### Archivos nuevos

- `templates/academics/teacher_panel.html`: cursos del docente.
- `templates/academics/teacher_course_panel.html`: estudiantes del curso
  con promedio y temas débiles, orden por promedio y desglose por tema.
- `templates/academics/teacher_student_detail.html`: detalle del estudiante.

### Archivos existentes que se modificarán parcialmente

- `config/settings.py`: `WEAK_TOPIC_THRESHOLD` (D-002) y
  `LOGIN_REDIRECT_URL = "role_home"`.
- `academics/services.py`: `is_weak()`, `get_weak_topics()`,
  `get_taught_courses()`, `get_course_panel()`, `get_student_panel_row()`
  y los dataclasses del panel. No se reemplazan las funciones existentes.
- `academics/views.py`: `role_home`, `teacher_panel`,
  `teacher_course_panel`, `teacher_student_detail`.
- `academics/urls.py`: rutas del panel bajo `/docente/panel/`.
- `academics/tests.py`: pruebas de servicios y de los criterios CA-1 a CA-5.
- `accounts/tests.py`: ajuste de dos aserciones del redirect posterior al
  login (ahora `role_home`); sin cambios de comportamiento de S-001.
- `README.md`, `docs/plan.md`, `docs/registro-ia.md`,
  `specs/S-008-panel-docente/spec.md`: documentación y registro de cambios.

## Cambios al modelo de datos

Ninguno. S-002 ya provee `TeacherProfile`, `TeachingAssignment`,
`Enrollment`, `Topic` y `Grade`.

## Decisiones técnicas

- Tema débil: nota estrictamente menor que `WEAK_TOPIC_THRESHOLD`
  (D-002), configurable por entorno, default 60. Un tema sin nota nunca
  es débil (D-003).
- Promedio: `calculate_average()` única de S-003 (D-004).
- Permiso en servidor: toda vista del panel exige `TeacherProfile` y, para
  un curso, que exista `TeachingAssignment` del docente; cualquier caso
  contrario responde HTTP 403 con `academics/access_denied.html` (CA-5).
- `role_home` redirige a `student_home` si el usuario tiene
  `StudentProfile` y a `teacher_panel` si solo tiene `TeacherProfile`;
  sin perfil responde 403. La prioridad del perfil estudiantil conserva
  el comportamiento de S-001.
- Orden por promedio mediante `?orden=promedio-asc|promedio-desc`; los
  estudiantes sin notas quedan al final en ambos sentidos.
- Rutas bajo `/docente/panel/` con `course_code`, sin tocar el espacio
  `/docente/cursos/` acordado por S-004.

## Tareas en orden

1. Sincronizar `main` local.
2. `config/settings.py`: umbral y redirect por rol.
3. `academics/services.py`: umbral de temas débiles y servicios del panel.
4. `academics/views.py` y `academics/urls.py`: vistas, permisos y rutas.
5. Plantillas del panel reutilizando estilos existentes.
6. Pruebas de servicios y de los criterios.
7. Documentación y registro de IA.

## Cómo se verificará cada criterio

CA-1 → abrir el panel de un curso con datos sintéticos y comparar la
lista, los promedios y los temas débiles contra la base de datos.
CA-2 → pulsar el orden por promedio en ambos sentidos y comprobar que el
orden cambia según el promedio calculado.
CA-3 → abrir el detalle de un estudiante y comprobar promedio y temas
débiles.
CA-4 → revisar el desglose por tema y comprobar el conteo de estudiantes
con el tema débil.
CA-5 → pedir la URL de un curso no asignado al docente y con una cuenta
sin perfil docente y confirmar la respuesta 403.

## Correcciones humanas al plan del agente

1. El redirect posterior al login se mantiene en S-008 pese a la nota del
   plan de S-004 que lo reservaba para S-010; se acordó con el equipo en
   el issue #8 y S-010 podrá endurecerlo después.
2. Las rutas se cambian de identificadores numéricos a `course_code` bajo
   el espacio `/docente/panel/`, para no pisar las rutas de S-004.
