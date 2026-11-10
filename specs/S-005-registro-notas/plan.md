# Plan S-005

Propuesto por: Claude Code · claude-opus-5-5 · modo Plan
Revisado y aprobado por: AlexDLG1 · 09-11-2026

## Contexto

Hoy ningún docente puede registrar notas en la plataforma: no existe
ninguna pantalla de docente. S-005 (issue #9, spec en main desde
`1b623d7`) pide registrar y corregir la nota entera de 0 a 100 de cada
estudiante inscrito en cada tema de un curso que el docente imparte
(D-008). El guardado debe rechazar en el servidor los datos que el
docente no puede calificar (CA-8). La rama `s-005-registro-notas` salió
de `s-003-perfil-academico` porque CA-4 se comprueba con `/perfil/`. El
PR #40 (S-003) ya está fusionado y la rama ya tiene `main` integrado.

## Enfoque

Una sola pantalla nueva, `/docente/cursos/<código>/notas/`. Muestra la
planilla del curso (estudiantes inscritos × temas del curso) y un
formulario con Estudiante, Tema y Nota. La regla de guardado vive en
`academics/services.py` (`record_grade`). Esa función comprueba
TeachingAssignment, Enrollment, que el tema sea del curso y el rango, y
guarda con `update_or_create`. La vista resuelve el curso con
`get_taught_course`, que se comparte con S-004, entrega los datos al
servicio y muestra el resultado. No se construyen la lista de cursos,
la gestión de temas ni la de estudiantes (S-004), ni la redirección por
rol (S-010). No hay IA ni modo demo.

## Coordinación con S-004 y S-010

Brayan11Hernandez, autor de S-004 y S-010, confirmó lo siguiente:

1. **Rutas bajo `/docente/`:**
   - S-004: `/docente/cursos/` (`name="teacher_courses"`),
     `/docente/cursos/<str:course_code>/temas/` y
     `/docente/cursos/<str:course_code>/estudiantes/`.
   - S-005: `/docente/cursos/<str:course_code>/notas/`
     (`name="teacher_course_grades"`).
2. **Función compartida:** `get_taught_course(user, course_code) -> Course | None`
   en `academics/services.py`. Devuelve `None` si la cuenta no tiene
   `TeacherProfile`, si no imparte el curso o si el curso no existe.
   Las vistas de ambas specs responden 403 con `access_denied.html`
   cuando recibe `None`.
3. **Orden de entrega:** `get_taught_course` va en el primer commit de
   servicios de S-005 (tarea 1). Brayan creará su rama desde
   `s-005-registro-notas`, así que no necesita que la función llegue
   antes a main. Por lo mismo, esa rama no se reescribe: no se hace
   rebase ni force push. El push de la tarea 1 solo se hace cuando
   AlexDLG1 lo indique.
4. **Llegada del docente:** S-010 redirige al docente a `/docente/cursos/`
   después del login. S-005 no toca `LOGIN_REDIRECT_URL` ni `base.html`.
   Mientras S-010 no esté en main, se entra a la planilla con
   `/acceso/?next=/docente/cursos/PROG-COM/notas/`.
5. **Enlace a la planilla:** Brayan agrega el enlace a
   `teacher_course_grades` desde su pantalla de cursos (S-004). S-005 no
   lo agrega.

## Archivos que se crean o modifican

Se crean:
- `academics/forms.py`: `GradeForm`. Solo valida el formato: campos
  obligatorios, número entero y rango, con mensajes en español.
- `templates/academics/teacher_course_grades.html`: planilla y formulario.

Se modifican:
- `academics/services.py`: `get_taught_course`, constantes de rango,
  `record_grade`, `GradeRegistrationError` y la planilla del curso.
- `academics/views.py`: vista `teacher_course_grades`.
- `academics/urls.py`: agrega
  `path("docente/cursos/<str:course_code>/notas/", teacher_course_grades, name="teacher_course_grades")`.
- `static/css/tutobosco.css`: contenedor con desplazamiento horizontal
  para la planilla y aviso de confirmación (unas 25 líneas).
- `academics/tests.py`: pruebas del servicio y de la vista.
- `README.md`: URL de la pantalla, cuenta `docente_01`,
  `DEMO_TEACHER_PASSWORD` y alcance actualizado.
- `docs/registro-ia.md`: uso de IA en S-005 (este plan).
- `specs/S-005-registro-notas/plan.md`, `spec.md` y `docs/plan.md`: tarea 0.
- `specs/S-005-registro-notas/verificacion.md`: lo completa ramosdeleon555.

No se tocan: `base.html`, `accounts/`, `tutor/`, `config/settings.py`,
los modelos, las migraciones ni `rebuild_synthetic_data`.

## Cambios al modelo de datos

Ninguno. `Grade` ya tiene `UniqueConstraint(student, topic)` y
`CheckConstraint` de 0 a 100. `TeachingAssignment`, `Enrollment` y
`Topic.course` ya expresan las tres pertenencias que exige CA-8.
`makemigrations --check --dry-run` no debe detectar cambios.

## Diseño del servicio (`academics/services.py`)

- `get_taught_course(user, course_code) -> Course | None`:
  `Course.objects.filter(code=course_code, teaching_assignments__teacher__user=user).first()`.
  Una sola consulta cubre los tres casos de `None`: sin `TeacherProfile`,
  curso ajeno y curso inexistente. Para un usuario anónimo devuelve
  `None` sin consultar.
- `GRADE_MIN_VALUE = 0` y `GRADE_MAX_VALUE = 100` (D-008). Las usan el
  formulario y el servicio.
- `class GradeRegistrationError(Exception)`: lleva el mensaje en español
  para la persona usuaria.
- `record_grade(*, user, course, student_pk, topic_pk, value) -> tuple[Grade, bool]`,
  dentro de `transaction.atomic`. Recibe `user` por la misma razón que
  `get_taught_course`. Las comprobaciones van en este orden y cada fallo
  lanza `GradeRegistrationError` sin escribir nada:
  1. El docente imparte el curso
     (`TeachingAssignment.objects.filter(teacher__user=user, course=course)`):
     "Usted no imparte este curso. La nota no se guardó."
  2. El tema es del curso (`Topic.objects.filter(pk=topic_pk, course=course)`):
     "El tema no pertenece a este curso. La nota no se guardó."
  3. El estudiante está inscrito (`Enrollment.objects.filter(student_id=student_pk, course=course)`):
     "El estudiante no está asignado a este curso. La nota no se guardó."
  4. `value` es un `int` (no `bool`) dentro del rango:
     "La nota debe ser un número entero entre 0 y 100."
  5. `Grade.objects.update_or_create(student=..., topic=..., defaults={"value": value})`.
     Corregir reemplaza la nota anterior y la restricción única garantiza
     un solo registro (D-008, CA-2).

  El curso nunca sale del formulario: llega desde la URL ya resuelta y el
  servicio vuelve a comprobar la asignación. Que el formulario también
  valide el rango es solo para la experiencia de uso. La regla que manda
  es la del servicio.
- Dataclasses inmutables:
  - `StudentGradeRow(student: StudentProfile, grades: tuple[int | None, ...])`,
    en el mismo orden que `topics`.
  - `GradeSheet(course, topics: tuple[Topic, ...], rows: tuple[StudentGradeRow, ...])`.
- `get_course_grade_sheet(course) -> GradeSheet`: hace tres consultas y
  ninguna N+1.
  1. Inscripciones del curso con `select_related("student__user")`,
     ordenadas por carné.
  2. Temas del curso ordenados por `pk`, igual que en S-003.
  3. Notas de esos temas en un diccionario `(student_id, topic_id) → value`.

  Solo aparecen los inscritos (CA-6) y los temas del curso (CA-7).

## Diseño de la vista y la plantilla

- `teacher_course_grades(request, course_code)`:
  - Lleva `@login_required` y `@require_http_methods(["GET", "POST"])`.
  - Obtiene `course = get_taught_course(request.user, course_code)`. Si es
    `None`, responde 403 con `access_denied.html`. La respuesta es la
    misma para los tres casos, como se acordó con S-004 y S-010.
  - Arma la planilla con `get_course_grade_sheet(course)`. `GradeForm`
    recibe la planilla para llenar las opciones de Estudiante (carné y
    nombre) y Tema. Las opciones son solo para mostrar; la pertenencia la
    decide el servicio.
  - Si el formulario es válido, llama a `record_grade(user=request.user, ...)`.
    Si guarda, `messages.success("Se guardó la nota 85 de <nombre> en <tema>.")`
    (o "Se actualizó…" al corregir) y redirige a la misma URL con el
    patrón PRG.
  - Si el formulario es inválido o hay `GradeRegistrationError`, vuelve
    a mostrar la planilla con los errores y conserva lo escrito. Responde
    con estado 400.
- `teacher_course_grades.html`: extiende `base.html` y reutiliza `panel`,
  `grade-table`, `field`, `form-control`, `alert`, `field-error` y
  `button`.
  - Encabezado: "Notas del curso" y `Código – Nombre`.
  - Mensajes de `django.contrib.messages` con `role="status"`. Los
    errores del servicio van en `.alert` con `role="alert"`.
  - Formulario POST con `{% csrf_token %}` y `novalidate`, para que el
    servidor muestre los errores de CA-3. La nota usa
    `type="number" min="0" max="100" step="1"`. Texto de ayuda: "Si el
    estudiante ya tiene nota en ese tema, la nueva nota reemplaza la
    anterior."
  - Planilla con una fila por estudiante (carné y nombre) y una columna
    por tema. Muestra "Sin nota" si falta (D-003), dentro de un contenedor
    con desplazamiento horizontal.
  - Estados vacíos: "Este curso aún no tiene estudiantes asignados." y
    "Este curso aún no tiene temas registrados." En ambos casos el
    formulario no se muestra.
  - Botón "Cerrar sesión", igual que en las demás pantallas. Textos en
    español y de usted.

## Tareas en orden

0. `S-005: documenta el plan aprobado`.
   - Copiar este plan a `specs/S-005-registro-notas/plan.md`.
   - En `spec.md`, el Estado pasa de "borrador" a "aprobada". Se agrega
     una línea al registro de cambios con la coordinación acordada con
     S-004 y S-010: rutas, `get_taught_course` y 403 ante un curso ajeno.
   - En `docs/plan.md`, S-005 pasa de "Por especificar" a "En implementación".
1. `S-005: resuelve el curso del docente y guarda la nota`.
   `get_taught_course`, constantes, `GradeRegistrationError`,
   `record_grade` y sus pruebas unitarias:
   - `get_taught_course`: curso propio, curso ajeno, curso inexistente,
     cuenta sin `TeacherProfile` y estudiante.
   - `record_grade`: CA-2, el rango de CA-3 y las tres ramas de CA-8.

   Es el commit del que Brayan parte su rama.
2. `S-005: arma la planilla de notas del curso`.
   `GradeSheet`, `get_course_grade_sheet` y pruebas (CA-6, CA-7, orden,
   "Sin nota" y `assertNumQueries(3)`).
3. `S-005: muestra y guarda notas desde la pantalla del docente`.
   `forms.py`, vista, URL, plantilla, CSS y pruebas de vista de CA-1 a
   CA-8 y de acceso.
4. `S-005: documenta la pantalla de notas y el uso de IA`.
   README y `docs/registro-ia.md`.
5. Antes de cada commit, el agente se detiene y muestra el diff. AlexDLG1
   lo revisa y ejecuta AGENTS §11: `check`, `test accounts academics tutor`,
   `makemigrations --check --dry-run` y `pip check`. También revisa la
   pantalla en el navegador con `docente_01`. No se hace push sin su
   indicación.
6. Un solo PR con la plantilla y `Closes #9`. Si `main` avanza, se
   integra con `git merge main`, sin rebase ni force push, porque la rama
   de S-004 parte de esta. ramosdeleon555 verifica CA-1 a CA-8 y
   registra la evidencia en `verificacion.md`.

## Tamaño estimado del PR

| Parte | Líneas aprox. |
| --- | --- |
| `services.py` (`get_taught_course`, `record_grade` y planilla) | 100 |
| `forms.py` | 40 |
| `views.py` y `urls.py` | 50 |
| `teacher_course_grades.html` | 90 |
| `tutobosco.css` | 25 |
| `tests.py` (servicio ~170, vista ~200) | 370 |
| Código y pruebas | **~675** |
| Documentación (plan, spec, README, registros) | ~240 |

Supera la referencia de unas 400 líneas de AGENTS §5. Aun así se entrega
en un solo PR, y la descripción del PR lo justifica así:
- La entrega final es el 11-11-2026 y cada PR necesita la aprobación del
  mismo verificador (ramosdeleon555). Dividirlo duplicaría esa espera.
- Brayan parte de esta rama, así que no hace falta adelantar
  `get_taught_course` a main.
- Más de la mitad son pruebas. Los commits de las tareas 1 a 4 se pueden
  revisar uno por uno: servicio, planilla, pantalla y documentación.

## Cómo se verificará cada criterio

Pruebas automatizadas: `TaughtCourseTests`, `RecordGradeTests` y
`CourseGradeSheetTests` (servicio) y `TeacherCourseGradesViewTests`
(vista) en `academics/tests.py`. Usan docentes, cursos, temas e
inscripciones creados dentro de cada prueba.

Verificación manual: partir de `rebuild_synthetic_data` y entrar con
`docente_01` (imparte PROG-COM y DES-WEB). Si S-010 ya está en main, se
llega a la planilla desde `/docente/cursos/`; si no, por
`/acceso/?next=/docente/cursos/PROG-COM/notas/`. Antes y después de cada
caso, consultar `Grade` en `manage.py shell -c "..."`. Al terminar,
volver a ejecutar `rebuild_synthetic_data`.

CA-1 → Prueba: POST con 85 para un inscrito sin nota da 302 y la
  confirmación. El GET muestra 85 y existe un `Grade` con valor 85.
  Manual: en PROG-COM, `estudiante_02` (sin notas), tema "Git y GitHub
  avanzado", nota 85. Se ve la confirmación y 85 en la planilla, y el
  shell muestra el registro.
CA-2 → Prueba: con 60 existente, POST con 75. Se ve 75, no aparece 60 y
  `Grade.objects.filter(student, topic).count() == 1` con valor 75.
  También prueba unitaria de `record_grade` (`created is False`). Manual:
  `estudiante_08` tiene 60 en "Git y GitHub avanzado" (PROG-COM). Se
  corrige a 75 y se cuentan los registros en el shell.
CA-3 → Prueba: con 60 existente, POST con `-5`, `101`, vacío, `abc` y
  `85.5`. Cada uno da 400 y un mensaje en español, y la nota sigue en 60.
  Prueba unitaria: `record_grade` con `-1`, `101` y `True` lanza
  `GradeRegistrationError`. Manual: los mismos valores en el formulario;
  `novalidate` deja que responda el servidor.
CA-4 → Prueba: después de guardar con la vista del docente, `/perfil/`
  del estudiante muestra la nota nueva y el promedio recalculado. Manual:
  tras CA-1, `estudiante_02` abre `/perfil/` y ve 85 en ese tema y
  "85.00" en PROG-COM. Tras CA-2, `estudiante_08` ve 75 y su promedio
  recalculado, que se compara con el shell.
CA-5 → Prueba: guardar, `logout`, `login` de nuevo y el GET muestra la
  nota. Manual: cerrar sesión, volver a entrar (por `/docente/cursos/`
  o con `?next=`), abrir la planilla de PROG-COM y comprobar 85.
CA-6 → Prueba: un estudiante no inscrito no aparece en la planilla ni
  entre las opciones del formulario. Manual: en DES-WEB, `estudiante_01`
  (inscrito en PROG-COM y BD-APL) y `estudiante_demo` no aparecen.
CA-7 → Prueba: los temas de otro curso no aparecen en las columnas ni
  entre las opciones. Manual: en DES-WEB solo están sus seis temas, sin
  los de PROG-COM ni BD-APL.
CA-8 → Pruebas de vista con el número de notas y sus valores sin cambios
  y un mensaje en español:
  (a) POST en DES-WEB con el `pk` de un estudiante no inscrito: 400.
  (b) POST en PROG-COM con el `pk` de un tema de BD-APL: 400.
  (c) POST de `docente_01` a `/docente/cursos/BD-APL/notas/`: 403 en español.
  Pruebas unitarias de las tres ramas de `record_grade`, incluido un
  curso de otro docente pasado directamente al servicio.
  Manual: con las herramientas del navegador, cambiar el `value` de una
  opción de Estudiante o Tema por el `pk` ajeno que dé el shell, o cambiar
  el `action` del formulario a `/docente/cursos/BD-APL/notas/`. Enviar y
  comprobar el mensaje y que el shell no muestra cambios.

Pruebas de apoyo, fuera de los CA:
- Sin sesión, redirige al login con `next`.
- Estudiante, cuenta sin perfil o `is_staff` sin `TeacherProfile` → 403.
- Código de curso inexistente → 403, igual que un curso ajeno.
- POST sin token CSRF → 403 (`Client(enforce_csrf_checks=True)`).
- Curso sin estudiantes o sin temas muestra el estado vacío.
- `get_course_grade_sheet` usa tres consultas.
- Las pruebas de S-001 y S-003 siguen pasando.

## Correcciones humanas al plan del agente

AlexDLG1 · 09-11-2026, tras confirmarlo con Brayan11Hernandez:

1. Se fijaron los nombres de las rutas de S-004 y S-005 y el `name` de la
   planilla (`teacher_course_grades`).
2. `get_taught_course` recibe `user` en lugar de `TeacherProfile` y
   devuelve `None` en los tres casos de rechazo. Por coherencia,
   `record_grade` también recibe `user`.
3. `get_taught_course` pasa al primer commit de servicios (tarea 1),
   porque la rama de S-004 parte de la de S-005.
4. Se confirmó que S-010 redirige al docente a `/docente/cursos/` tras
   el login.
5. Se agregó la sección "Coordinación con S-004 y S-010". Brayan agrega
   el enlace a la planilla desde su pantalla de cursos.
6. Un solo PR con `Closes #9`, sin dividirlo en entregas. La entrega
   final es el 11-11-2026, cada PR necesita la aprobación del mismo
   verificador y la rama de S-004 parte de esta. Se conserva el orden de
   tareas para revisar por commits y el tamaño se justifica en el PR.
7. CA-2: AlexDLG1 confirmó que `estudiante_08` tiene 60 en "Git y GitHub
   avanzado" de PROG-COM. Se quitó el paso de confirmarlo en el shell.
