# Plan S-002

Propuesto por: OpenCode · deepseek-v4.1-flash · modo Plan
Revisado y aprobado por: JavEstrada09 · 06-11-2026

Spec: `specs/S-002-datos-sinteticos/spec.md`
Issue: #6
Estado: aprobado; Entrega 2 implementada, pendiente de verificación

## Enfoque

Ampliar la base creada por S-001 sin reemplazar sus modelos ni sus
migraciones iniciales. Se añadirán los modelos de docentes, asignaciones
docente-curso, temas y notas, y se extenderá el comando compartido
`rebuild_synthetic_data` para generar el conjunto completo de datos
sintéticos de forma reproducible e idempotente.

D-008 quedó confirmada: la nota es un entero de 0 a 100, existe una
sola nota por estudiante y tema, y corregirla reemplaza la anterior
sin conservar historial. El rol se determina por el perfil, según D-009.

## Archivos que se crean o modifican

- `academics/models.py`: modelos `TeacherProfile`, `TeachingAssignment`,
  `Topic` y `Grade`.
- `academics/migrations/0002_*.py`: migración posterior a `0001_initial`.
- `academics/management/commands/rebuild_synthetic_data.py`: manifiesto
  completo, generación de docentes, temas, notas y validaciones.
- `academics/tests.py`: pruebas de los nuevos modelos, restricciones,
  datos generados, perfiles e idempotencia.
- `README.md`: cantidades de datos, cuentas demo, comando de
  reconstrucción y umbral de tema débil.
- `docs/plan.md`: estado de S-002.
- `docs/registro-ia.md`: entrada de S-002.
- `specs/S-002-datos-sinteticos/verificacion.md`: se crea únicamente
  durante la fase de verificación.

## Cambios al modelo de datos

### `TeacherProfile`

- `user`: `OneToOneField` con `settings.AUTH_USER_MODEL`,
  `on_delete=CASCADE`, `related_name="teacher_profile"`.
- Sin campos adicionales: el nombre y las credenciales se obtienen
  del usuario de Django.
- Un usuario no puede tener más de un perfil docente.

### `TeachingAssignment`

- `teacher`: `ForeignKey` a `TeacherProfile`,
  `related_name="teaching_assignments"`.
- `course`: `ForeignKey` a `Course`,
  `related_name="teaching_assignments"`.
- Restricción única por pareja docente-curso.

### `Topic`

- `course`: `ForeignKey` a `Course`, `related_name="topics"`,
  `on_delete=CASCADE`.
- `name`: `CharField(max_length=150)`.
- Restricción única por curso y nombre.

### `Grade`

- `student`: `ForeignKey` a `StudentProfile`,
  `related_name="grades"`, `on_delete=CASCADE`.
- `topic`: `ForeignKey` a `Topic`,
  `related_name="grades"`, `on_delete=CASCADE`.
- `value`: `PositiveSmallIntegerField` con validadores de 0 a 100 y
  restricción de base de datos equivalente.
- Restricción única por estudiante y tema.
- La corrección reemplaza el valor existente, sin historial (D-008).

### Relaciones existentes

- Se conservan `User`, `StudentProfile`, `Course` y `Enrollment`
  creados por S-001.
- No se modifica `accounts.User`; el rol se deriva del perfil (D-009).
- No se modifican destructivamente las migraciones de S-001.

## Datos sintéticos y manifiesto

### Docentes

- `docente_01`: imparte Programación Comercial y Desarrollo Web.
- `docente_02`: imparte Bases de Datos Aplicadas.
- `docente_03`: imparte Redes de Computadoras.

### Cursos y temas

- `PROG-COM` — Programación Comercial, con los seis temas del enunciado.
- `BD-APL` — Bases de Datos Aplicadas:
  modelo relacional, consultas SQL, normalización, transacciones,
  índices y rendimiento, copias de seguridad y recuperación.
- `DES-WEB` — Desarrollo Web:
  HTML semántico, CSS y diseño adaptable, JavaScript básico,
  formularios y validación, accesibilidad web, despliegue local.
- `REDES` — Redes de Computadoras:
  modelo OSI, direccionamiento IP, subredes, protocolos de transporte,
  seguridad básica de red, diagnóstico de conectividad.

### Estudiantes y notas

- 30 estudiantes en total, incluido `estudiante_demo`.
- Todos inscritos en Programación Comercial y distribuidos además
  entre los otros tres cursos.
- Perfiles deterministas y claramente distintos:
  - `estudiante_demo` con exactamente dos temas débiles;
  - un estudiante sin temas débiles;
  - un estudiante sin notas;
  - estudiantes con notas altas, medias y bajas.
- Las notas son enteros de 0 a 100 y solo se registran para temas
  de cursos en los que el estudiante está inscrito.
- Las contraseñas de estudiantes y docentes se guardan con el hash
  de Django y se toman de `DEMO_STUDENT_PASSWORD` y
  `DEMO_TEACHER_PASSWORD`.

### Comando `rebuild_synthetic_data`

- Conserva el nombre y amplía el comando existente.
- Usa un manifiesto cerrado de usuarios, carnés, códigos de curso y temas.
- Rechaza identificadores del manifiesto que pertenezcan a registros
  ajenos o con privilegios.
- Reconstruye únicamente los registros administrados por el manifiesto.
- Es idempotente: ejecutarlo dos veces deja las mismas cantidades y
  no duplica datos.
- Conserva usuarios y registros ajenos al conjunto sintético.
- No modifica migraciones ni requiere conexión a internet.
- No realiza llamadas a IA.

## Tareas en orden

1. Confirmar D-008 y dejarla registrada como decisión vigente.
2. Agregar los cuatro modelos y sus restricciones en `academics/models.py`.
3. Generar la migración `academics/0002_*` y comprobar que
   `0001_initial` no cambia.
4. Implementar el manifiesto completo de docentes, cursos y temas.
5. Extender `rebuild_synthetic_data` con docentes, temas, notas,
   distribución de inscripciones, contraseñas y controles de colisión.
6. Actualizar las pruebas de S-001 afectadas por los nuevos volúmenes.
7. Agregar pruebas de modelos, restricciones, distribución de datos,
   perfiles débiles, ausencia de notas e idempotencia.
8. Actualizar `README.md`, `docs/plan.md` y `docs/registro-ia.md`.
9. Ejecutar migraciones, reconstrucción, suite completa,
   `manage.py check` y `makemigrations --check`.
10. Publicar el PR de implementación con `Closes #6` solo después de
    la verificación independiente de JavEstrada09.

## Cómo se verificará cada criterio

- **CA-1:** ejecutar `rebuild_synthetic_data` sobre una base limpia y
  consultar la base: 30 estudiantes, 3 docentes, 4 cursos con 6 temas
  cada uno y los seis temas correctos de Programación Comercial.
- **CA-2:** consultar los perfiles generados y comprobar que existen
  estudiantes con dos temas débiles, sin temas débiles y sin notas,
  además de notas variadas entre cursos.
- **CA-3:** ejecutar la reconstrucción en otra computadora siguiendo
  únicamente el README y comparar cantidades y perfiles.
- **CA-4:** comprobar en la base las relaciones docente-curso,
  curso-tema, estudiante-curso y estudiante-tema.
- **CA-5:** ejecutar el comando dos veces, verificar que no duplica,
  que no altera migraciones y que conserva un usuario ajeno al
  conjunto sintético.

## Correcciones humanas al plan del agente

Aprobado en el PR #33 sin correcciones humanas registradas.

## Dependencias y riesgos

- D-008 está confirmada.
- S-001 continúa en implementación; S-002 no debe modificar sus
  migraciones ni sus modelos base.
- El manifiesto de cursos adicionales y temas queda sujeto a la
  revisión del plan.
