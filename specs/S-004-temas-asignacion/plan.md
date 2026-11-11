# Plan S-004 — Gestión de temas y asignación

**Propuesto por:** ChatGPT (OpenAI) · GPT-6 · planificación en solo lectura
**Revisado y aprobado por:** Brayan11Hernandez
**Issue:** #8
**Verificador:** AlexDLG1

## Enfoque

Se implementarán tres pantallas para que el docente consulte sus cursos, administre temas académicos y asigne estudiantes.

Se reutilizarán los modelos existentes de Django y la función compartida `get_taught_course(user, course_code)` desarrollada en S-005.

Las operaciones verificarán los permisos desde el servidor. No se modificarán las funciones de registro de notas ni las funcionalidades del perfil académico.

## Archivos que se crean o modifican

### Archivos nuevos

- `academics/teacher_forms.py`: formularios para registrar o modificar temas y asignar estudiantes.
- `templates/academics/teacher_courses.html`: listado de cursos del docente.
- `templates/academics/teacher_course_topics.html`: consulta y administración de temas.
- `templates/academics/teacher_course_students.html`: estudiantes inscritos y formulario de asignación.

### Archivos existentes que se modificarán parcialmente

- `academics/views.py`: agregar las tres vistas de S-004.
- `academics/urls.py`: agregar las rutas y nombres acordados.
- `academics/tests.py`: agregar pruebas para los ocho criterios de aceptación.
- `static/css/tutobosco.css`: agregar únicamente estilos nuevos si son necesarios.
- `README.md`: documentar las pantallas del docente.
- `docs/registro-ia.md`: registrar el uso de ChatGPT, modelo GPT-6 y las correcciones humanas.
- `docs/plan.md`: actualizar el estado de S-004.
- `specs/S-004-temas-asignacion/spec.md`: documentar su aprobación mediante PR #27.

### Archivos que no se reemplazarán

- `academics/services.py`: reutilizar las funciones existentes sin sobrescribirlas.
- `academics/models.py`: conservar el modelo académico actual.
- `accounts/`: no modificar autenticación ni redirecciones.
- `tutor/`: no modificar funcionalidades de inteligencia artificial.
- `specs/S-004-temas-asignacion/verificacion.md`: será completado por AlexDLG1.

## Cambios al modelo de datos

Ninguno previsto.

Se utilizarán los modelos existentes:

- `Course`: información de cursos, identificados mediante `Course.code`.
- `Topic`: temas académicos asociados a cursos.
- `StudentProfile`: estudiantes registrados.
- `Enrollment`: inscripciones de estudiantes en cursos.
- `TeacherProfile`: docentes registrados.
- `TeachingAssignment`: cursos impartidos por cada docente.

Se respetarán las restricciones de unicidad existentes para temas e inscripciones.

No se crearán migraciones salvo que una revisión posterior del equipo determine que son indispensables.

## Rutas acordadas

| Ruta | Nombre |
|---|---|
| `/docente/cursos/` | `teacher_courses` |
| `/docente/cursos/<str:course_code>/temas/` | `teacher_course_topics` |
| `/docente/cursos/<str:course_code>/estudiantes/` | `teacher_course_students` |

Desde el listado de cursos se incluirá un enlace hacia `teacher_course_grades`, perteneciente a S-005, una vez que esa ruta esté integrada.

## Seguridad y permisos

La lista de cursos mostrará únicamente aquellos asociados al docente autenticado.

Las vistas de temas y estudiantes utilizarán `get_taught_course(request.user, course_code)`.

Si la función devuelve `None`, la vista responderá HTTP 403 mediante `academics/access_denied.html`.

Los usuarios que no hayan iniciado sesión serán dirigidos
al formulario de autenticación.

Los usuarios autenticados que no sean docentes, no impartan
el curso solicitado o indiquen un curso inexistente recibirán
una respuesta HTTP 403.

Las verificaciones de permisos se realizarán en el servidor,
sin depender de que los enlaces estén ocultos en la interfaz.

Los formularios usarán POST con protección CSRF. El curso se determinará mediante la URL y la autorización del servidor, no mediante un identificador editable del formulario.

Los datos inválidos deberán rechazarse sin registrar cambios.

## Tareas en orden

1. Documentar la aprobación de S-004, actualizar su estado y registrar el plan aprobado.
2. Preparar los formularios de temas y asignación de estudiantes.
3. Agregar la vista `teacher_courses` y su ruta.
4. Crear la plantilla con los cursos del docente y los enlaces de navegación.
5. Agregar la vista `teacher_course_topics` para consultar, registrar y modificar temas.
6. Crear la plantilla de gestión de temas con validación y mensajes en español.
7. Agregar la vista `teacher_course_students` para consultar y asignar estudiantes.
8. Crear la plantilla de estudiantes y prevenir asignaciones duplicadas.
9. Integrar el enlace hacia notas de S-005, sin modificar el módulo de notas.
10. Agregar pruebas de permisos, validación, integridad de datos y criterios de aceptación.
11. Ejecutar las pruebas del proyecto y revisar los cambios con `git diff`.
12. Documentar el uso de IA y actualizar README.
13. Preparar el Pull Request final con `Closes #8` y solicitar la revisión de AlexDLG1.

Cada modificación de archivos compartidos se realizará mediante bloques pequeños, conservando las funciones existentes.

## Cómo se verificará cada criterio

**CA-1 — Consulta de cursos**

Iniciar sesión con un docente y comprobar que únicamente se muestran los cursos que imparte.

**CA-2 — Consulta de temas**

Abrir los temas de un curso propio y comprobar que se muestran únicamente sus temas académicos.

**CA-3 — Registro de temas**

Registrar un tema válido y comprobar que queda asociado al curso seleccionado.

**CA-4 — Modificación de temas**

Modificar un tema existente y verificar que la información actualizada se conserva.

**CA-5 — Asignación de estudiantes**

Asignar un estudiante registrado a un curso y comprobar que aparece en la lista de inscritos.

**CA-6 — Prevención de duplicados**

Intentar asignar nuevamente al mismo estudiante y comprobar que no se crea una segunda inscripción.

**CA-7 — Restricción de acceso**

Intentar acceder a cursos ajenos, inexistentes o mediante una cuenta sin rol docente. Comprobar que se responde HTTP 403 y no se modifica información.

**CA-8 — Validación de datos**

Enviar formularios incompletos o inválidos y verificar que aparecen mensajes comprensibles sin guardar información incorrecta.

También se ejecutarán las pruebas existentes de `accounts`, `academics` y `tutor` para detectar regresiones.

## Integración con S-005

La función `get_taught_course()` y la ruta de notas pertenecen a S-005.

No se volverá a fusionar su rama mientras continúe recibiendo commits.

Una vez fusionada S-005 en `main`, S-004 integrará los cambios mediante `git merge main`, sin rebase ni force push, comprobando los conflictos y el resultado de las pruebas.

La redirección del docente después del inicio de sesión corresponde exclusivamente a S-010.

## Correcciones humanas al plan del agente

- Se aclaró la diferencia entre usuarios no autenticados
  y usuarios autenticados sin permisos.
- Se confirmó que la autorización de cursos debe realizarse
  desde el servidor mediante get_taught_course().
- Se mantiene la separación entre S-004, S-005 y S-010
  para evitar modificaciones ajenas a esta especificación.

Estado de revisión: Aprobado por el autor para iniciar la implementación de S-004.