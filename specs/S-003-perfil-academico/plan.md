# Plan S-003

Propuesto por: Claude Code · claude-opus-5-5 · modo Plan
Revisado y aprobado por: AlexDLG1 · 09-11-2026

## Enfoque

Se agrega la vista `student_profile` en `/perfil/`, separada de
`student_home`. Exige sesión y un `StudentProfile` y no depende de ningún
curso en particular. Los datos académicos los arma un servicio nuevo,
`academics/services.py`, que contiene la única función de promedio del
proyecto (D-004, AGENTS §9). S-007, S-008 y el tutor podrán reutilizarla.
La plantilla solo muestra el resultado y no hace cálculos. No hay IA, modo
demo ni cambios al modelo.

## Archivos que se crean o modifican

Se crean:
- `academics/services.py`: cálculo del promedio y armado del resumen
  académico.
- `templates/academics/student_profile.html`: pantalla del perfil.

Se modifican:
- `academics/views.py`: agrega la vista `student_profile`.
  `student_home` no cambia.
- `academics/urls.py`: agrega `path("perfil/", student_profile, name="student_profile")`.
- `templates/academics/student_home.html`: agrega el enlace
  "Ver su perfil académico".
- `static/css/tutobosco.css`: estilos de la tabla de temas y del aviso
  de estado vacío (unas 30 líneas).
- `academics/tests.py`: pruebas del servicio y de la vista.
- `README.md`: URL `/perfil/` y alcance actualizado.
- `docs/registro-ia.md`: uso de IA en S-003 (este plan).
- `specs/S-003-perfil-academico/verificacion.md`: lo completa el verificador.

No se tocan: `accounts/`, `tutor/`, los modelos, las migraciones, el
comando de datos sintéticos, ni el alcance de S-004, S-005 y S-010.

## Cambios al modelo de datos

Ninguno. Se usan `StudentProfile`, `Enrollment`, `Course`, `Topic` y `Grade`
tal como los dejó S-002. `makemigrations --check` no debe detectar cambios.

## Diseño del servicio (`academics/services.py`)

- `calculate_average(values) -> Decimal | None`
  - Recibe notas enteras o `None`. Descarta los `None` (D-003).
  - Si no queda ninguna nota, devuelve `None`.
  - Si no, devuelve el promedio simple como `Decimal`, redondeado a dos
    decimales (D-004).
  - D-004 no dice qué modo de redondeo usar. Este plan elige
    `ROUND_HALF_UP`. Con `round()` sobre `float` se aplicaría el redondeo
    bancario, y 70.125 daría 70.12 en lugar de 70.13.
  - Es la única función de promedio del proyecto.
- Dataclasses inmutables:
  - `TopicGrade(topic, value: int | None)`.
  - `CourseSummary(course, topics: tuple[TopicGrade, ...], average: Decimal | None)`.
- `get_course_summaries(student_profile) -> list[CourseSummary]`
  - Usa tres consultas y ninguna N+1:
    1. inscripciones del estudiante, con `select_related("course")`;
    2. temas de esos cursos;
    3. notas del estudiante en esos temas, en un diccionario `topic_id → value`.
  - Ordena los cursos por nombre y los temas por `pk`, que es el orden del
    manifiesto.
  - Consulta la base en cada llamada, sin caché, para que CA-8 se cumpla.
  - Solo recibe el perfil del usuario autenticado. Nunca recibe un
    identificador que venga de la petición.
- S-007 podrá obtener los temas débiles con el filtro
  `value is not None and value < WEAK_TOPIC_THRESHOLD` sobre los mismos
  `TopicGrade`. Ese filtro no se implementa aquí.

## Diseño de la vista y la plantilla

- `student_profile(request)`:
  - Lleva `@login_required`; sin sesión, redirige a `login?next=/perfil/`.
  - Obtiene `StudentProfile` con `filter(user=request.user).first()`.
  - Sin perfil de estudiante (cuenta sin perfil, docente o personal
    técnico), responde 403 con `access_denied.html`, que ya existe.
  - Ignora cualquier parámetro de la URL. Siempre usa `request.user`.
  - Pasa al contexto:
    - nombre: `user.get_full_name()`, o el nombre de usuario si está vacío;
    - `student_id`, `career`, `semester`;
    - `course_summaries`.
  - Solo atiende GET.
- `student_profile.html`:
  - Extiende `base.html`. Título: "Su perfil académico".
  - Tarjeta de datos con Nombre, Carné, Carrera y Semestre.
  - Un `panel` por curso con el título `Código – Nombre` y una tabla
    Tema | Nota. El pie de la tabla muestra "Promedio del curso".
  - Nota `None` → "Sin nota". Promedio `None` → "Sin notas".
  - Los números se muestran con `{% load l10n %}` y `|unlocalize`, así salen
    `71.67` y `70.00` como dice la spec y como se escriben en Guatemala.
  - Sin cursos: aviso "Aún no tiene cursos asignados." dentro de un panel.
  - Botón "Cerrar sesión" (POST con CSRF), igual que en las demás pantallas.
  - Todos los textos en español y de usted.

## Tareas en orden

0. `S-003: documenta el plan aprobado`. En este commit:
   - se copia este plan a `specs/S-003-perfil-academico/plan.md`;
   - en `spec.md`, el Estado pasa de "borrador" a "aprobada" y se agrega
     una línea al registro de cambios;
   - en la tabla de `docs/plan.md`, S-003 pasa de "Por especificar" a
     "En implementación".
1. `S-003: centraliza el cálculo del promedio del curso`.
   `services.py` con `calculate_average` y sus pruebas unitarias.
2. `S-003: arma el resumen académico del estudiante`.
   `get_course_summaries` y sus pruebas, incluido el orden y la
   ausencia de N+1 con `assertNumQueries(3)`.
3. `S-003: muestra el perfil académico del estudiante`.
   Vista, URL, plantilla, CSS y pruebas de CA-1 a CA-8 y de acceso.
4. `S-003: enlaza el perfil desde el espacio del estudiante`.
   Enlace en `student_home.html`. Comprobar que las pruebas de S-001
   siguen pasando.
5. `S-003: documenta el perfil y el uso de IA`.
   README y `docs/registro-ia.md`.
6. Antes de cada commit, el agente se detiene y muestra el diff.
   AlexDLG1, como autor, lo revisa y ejecuta los comandos de AGENTS §11:
   `check`, `test accounts academics tutor`,
   `makemigrations --check --dry-run` y `pip check`. Además revisa
   `/perfil/` en el navegador con `estudiante_demo`, `estudiante_01`
   y `estudiante_02`.
7. Abrir el PR con la plantilla y `Closes #7`. ramosdeleon555 verifica
   y registra la evidencia en `verificacion.md`.

## Cómo se verificará cada criterio

Pruebas automatizadas: clase `StudentProfileViewTests` en
`academics/tests.py`. Usa estudiantes y cursos creados dentro de la prueba,
con tres temas por curso.

Verificación manual del verificador:
- Partir de `rebuild_synthetic_data` y abrir `/perfil/`.
- Para los casos que no existen en los datos sintéticos, hacer un cambio
  temporal con `manage.py shell -c "..."`.
- Volver a ejecutar `rebuild_synthetic_data` al terminar. El comando
  restaura las inscripciones y notas del manifiesto.

CA-1 → Prueba: el estudiante ve su nombre completo, carné, carrera y
  semestre tal como están en la base. Manual: `estudiante_demo` ve
  "Estudiante Demo", `2026-00001`, "Ingeniería en Sistemas" y semestre 1.
  Se compara con una consulta en el shell.
CA-2 → Prueba: un estudiante inscrito en A y B, con un curso C en el que
  no está inscrito, ve A y B y no ve C. Manual: `estudiante_01` ve
  `PROG-COM` y `BD-APL`, y no ve `DES-WEB` ni `REDES`.
CA-3 → Prueba: con notas 80, 65 y 70 se ve cada nota y "71.67". Prueba
  unitaria: `calculate_average([80, 65, 70]) == Decimal("71.67")`.
  Manual: con `estudiante_demo` en `PROG-COM` (55, 58, 90, 92, 88, 85)
  se ve 78.00, que se compara con el cálculo en el shell.
CA-4 → Solo prueba automatizada, porque no hay notas parciales en los datos
  sintéticos: notas 80 y 60 y un tema sin nota muestran "Sin nota" y
  "70.00". Prueba unitaria: `calculate_average([80, 60, None]) == Decimal("70.00")`.
  Opcional en manual: borrar una nota en el shell, revisar y reconstruir.
CA-5 → Prueba: un curso sin notas muestra "Sin nota" en todos sus temas y
  "Sin notas" en el promedio. Prueba unitaria: `calculate_average([None, None]) is None`
  y `calculate_average([]) is None`. Manual: `estudiante_02`, que no tiene
  notas, ve "Sin notas" en sus dos cursos.
CA-6 → Prueba: un estudiante sin inscripciones recibe 200, no 403, ve sus
  datos y el aviso "Aún no tiene cursos asignados.". Manual: borrar en el
  shell las inscripciones de `estudiante_03`, abrir `/perfil/` y reconstruir.
CA-7 → Prueba: dos estudiantes con datos y notas distintos. Cada uno ve los
  suyos y no los del otro, aunque se agregue `?student_id=<carné ajeno>`
  a la URL. Manual: `estudiante_demo` y `estudiante_01` en dos navegadores
  o en una ventana privada.
CA-8 → Prueba: después de un GET se cambia `Grade.value` en la base, el
  segundo GET muestra la nota nueva y el promedio recalculado. Manual:
  cambiar una nota de `estudiante_demo` en el shell, recargar y comprobar
  el nuevo promedio, luego reconstruir.

Pruebas de apoyo, fuera de los CA:
- Sin sesión, redirige al login.
- Cuenta sin perfil, docente o `is_staff` → 403 en español.
- El redondeo sigue `ROUND_HALF_UP`: 70.125 da 70.13.
- `get_course_summaries` usa tres consultas.
- Las pruebas de S-001 sobre `student_home` siguen pasando.

## Correcciones humanas al plan del agente

AlexDLG1 · 09-11-2026:

1. Se agregó la tarea 0. Primero se documenta el plan aprobado en un commit
   propio. En ese mismo commit, la spec pasa a "aprobada" con su línea en el
   registro de cambios, y `docs/plan.md` pasa S-003 a "En implementación".
2. Se aclaró que D-004 no fija el modo de redondeo y que `ROUND_HALF_UP`
   es una decisión de este plan.
