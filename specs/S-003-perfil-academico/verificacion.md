# Verificación S-003 — Perfil académico

Verificador: ramosdeleon555, según la asignación de la spec y la
declaración del usuario de esta sesión.
Computadora: equipo local de Canche, Windows 10, Python 3.12.10,
Django 5.2.19, SQLite.
Commit probado en la ejecución inicial: `9f8c6e25320f865af1dc7795817ba5f526e244bd`.
Commit probado en la evidencia complementaria:
`7b2a79b6c2f7e80c3348b76b8d51c8f66c223118` (main después del PR #41).
Fecha de ejecución y registro: 2026-11-09.

Estado: controles automatizados satisfactorios y revisión manual
declarada por el usuario; registro confirmado por el verificador en la
sección final (10-11-2026). El agente no aprueba la spec en nombre del
verificador.

## Cronología y corrección del proceso

- El PR #40 fusionó la implementación y cerró el issue #7 antes de que
  existiera el registro de verificación completo. Esto incumplió el orden
  de AGENTS §4 y §12; documentarlo después no vuelve retroactiva la revisión.
- El PR #41 incorporó el primer registro, todavía pendiente de confirmación
  explícita de ramosdeleon555. Fusionarlo no resolvió esa confirmación.
- Esta corrección agrega evidencia ejecutada después de ambos merges.
  No reescribe las fechas originales ni representa aprobación del agente.
- La verificación formal corresponde a Ramos y la revisión de este cambio
  documental corresponde a otro integrante. Si cambia el verificador,
  el equipo debe registrar formalmente la reasignación antes del cierre.

## Alcance y procedencia de la evidencia inicial

- El usuario confirmó haber revisado el sistema en `9f8c6e2` y haber
  comprobado manualmente los casos especiales CA-4, CA-6 y CA-8. No
  proporcionó valores concretos ni capturas de esos cambios; no se
  inventan procedimientos ni resultados numéricos de esa revisión.
- OpenCode ejecutó los comandos y comprobaciones automatizadas descritos
  aquí en esa computadora. Estos resultados no se presentan como una
  nueva revisión visual realizada por una persona.
- Las dos capturas aportadas corresponden al estado inicial de la base,
  no al conjunto sintético completo. Su alcance se detalla más abajo.
- La rama documental `s-003-verificacion` parte de `45ee80e` (main,
  merge del PR #40). La suite se ejecutó antes de cambiar de rama, sobre
  `9f8c6e2`. La comparación de `accounts`, `academics`, `tutor`,
  `templates` y `config` entre ambos commits no mostró diferencias.

## Preparación y comandos ejecutados

La inspección inicial encontró las migraciones académicas aplicadas, pero
solo un estudiante, un curso, una inscripción, cero temas y cero notas.
Por eso el perfil mostraba un curso sin temas, sin poder demostrar los
promedios del conjunto completo.

Las variables de configuración y contraseñas demo estaban disponibles
localmente; no se incluyeron sus valores en comandos, capturas ni archivos.

```powershell
& ".\.venv\Scripts\python.exe" manage.py test accounts academics tutor --verbosity 2
& ".\.venv\Scripts\python.exe" manage.py check
& ".\.venv\Scripts\python.exe" manage.py makemigrations --check --dry-run
& ".\.venv\Scripts\python.exe" -m pip check
& ".\.venv\Scripts\python.exe" manage.py migrate
& ".\.venv\Scripts\python.exe" manage.py rebuild_synthetic_data
```

La suite usó una base SQLite en memoria, separada de la base local.
Los escenarios temporales de notas e inscripciones de las pruebas no
modificaron los datos de demostración. Gemini se simuló en la suite;
no se hicieron llamadas reales al proveedor de IA.

## Resultados por criterio

Los nombres abreviados de la última columna pertenecen a
`academics.tests.StudentProfileViewTests`. Todos los métodos indicados
se ejecutaron con resultado `ok` dentro de la suite de 80 pruebas.

| Criterio | Cómo se comprobó en esta ejecución | Resultado | Evidencia |
| --- | --- | --- | --- |
| CA-1 | La prueba creó un estudiante con nombre, carné, carrera y semestre conocidos; comprobó esos datos en el HTML del usuario autenticado. Además se consultaron la base y `/perfil/` con las cuentas demo reconstruidas. | Cumple en prueba automatizada. La captura inicial respalda solo la visualización de datos personales. | `test_ca1_shows_personal_data_of_authenticated_student`; comprobación local descrita abajo; [perfil inicial](img/estado-inicial-perfil.png). |
| CA-2 | Estudiante inscrito en dos cursos, con un tercero ajeno; el HTML mostró solo los dos asignados. En el conjunto reconstruido se comprobaron las dos inscripciones de `estudiante_01`. | Cumple en prueba automatizada. | `test_ca2_shows_only_enrolled_courses`; consulta local: `BD-APL` y `PROG-COM`. |
| CA-3 | Con notas 80, 65 y 70, se comprobaron cada nota y el promedio `71.67` en HTML. El conjunto demo se comprobó aparte y mostró `78.00`. | Cumple en prueba automatizada con los valores exactos de la spec. | `test_ca3_shows_each_grade_and_course_average`; `CalculateAverageTests.test_simple_average_is_rounded_to_two_decimals`. |
| CA-4 | Se crearon notas 80 y 60 y se dejó un tema sin nota; se comprobó una celda `Sin nota` y promedio `70.00`. | Cumple en prueba automatizada. El usuario también declaró comprobación manual, sin captura específica. | `test_ca4_topic_without_grade_is_shown_and_excluded`; `CalculateAverageTests.test_topics_without_grade_are_excluded`. |
| CA-5 | Un curso con tres temas y sin notas mostró tres celdas `Sin nota` y promedio `Sin notas`. En la base reconstruida se comprobó el mismo estado para `estudiante_02`. | Cumple en prueba automatizada. | `test_ca5_course_without_grades_shows_sin_notas`; comprobación local descrita abajo. |
| CA-6 | Estudiante sin inscripciones: respuesta 200, datos personales y aviso `Aún no tiene cursos asignados.`. | Cumple en prueba automatizada. El usuario también declaró comprobación manual, sin captura específica. | `test_ca6_student_without_courses_sees_data_and_notice`. |
| CA-7 | Dos estudiantes con cursos, datos y notas distintos vieron solo sus perfiles, incluso enviando el carné ajeno en `student_id`. También se autenticaron tres cuentas locales por separado y se comprobó el parámetro manipulado para demo. | Cumple en prueba automatizada. | `test_ca7_each_student_sees_only_own_profile`; comprobación local descrita abajo. |
| CA-8 | Se consultó el perfil con promedio `71.67`, se cambió una nota de 65 a 95 en la base de prueba y se repitió GET; aparecieron 95 y `81.67`, sin la nota anterior. | Cumple en prueba automatizada. El usuario también declaró comprobación manual, sin captura específica. | `test_ca8_reload_shows_updated_grade_and_average`. |

## Evidencia textual de ejecución

Resumen transcrito de la salida real de la suite, no una ejecución manual
del navegador ni un archivo de log bruto:

```text
Creating test database for alias 'default'
('file:memorydb_default?mode=memory&cache=shared')...
Found 80 test(s).
Ran 80 tests in 53.632s
OK
Destroying test database for alias 'default'...
```

Resultados de los otros controles:

```text
manage.py check:
  System check identified no issues (0 silenced).
manage.py makemigrations --check --dry-run:
  No changes detected
python -m pip check:
  No broken requirements found.
manage.py migrate:
  No migrations to apply.
manage.py rebuild_synthetic_data:
  Datos sintéticos completos reconstruidos.
```

### Comprobación adicional de la base local reconstruida

Se utilizó el cliente de pruebas de Django contra la base local, con
autenticación mediante las contraseñas configuradas y peticiones GET a
`/perfil/`. Se ajustó `ALLOWED_HOSTS` solo durante esa comprobación para
admitir `testserver`. Las tres sesiones creadas se cerraron al terminar.
No se modificó la configuración del proyecto ni se abrió un navegador.

Recuentos verificados: 30 estudiantes, 3 docentes, 4 cursos, 24 temas,
342 notas y 59 inscripciones.

| Cuenta | Datos consultados en la base y resultado comprobado en HTML |
| --- | --- |
| `estudiante_demo` | Estudiante Demo, `2026-00001`, Ingeniería en Sistemas, semestre 1; `PROG-COM`, notas 55, 58, 90, 92, 88, 85; promedio `78.00`; GET 200. |
| `estudiante_01` | Estudiante 01, `2026-00002`, Ingeniería en Sistemas, semestre 1; inscripciones `BD-APL` y `PROG-COM`, notas 70, 73, 76, 79, 82, 85 en cada curso; promedio `77.50`; GET 200. |
| `estudiante_02` | Estudiante 02, `2026-00003`, Administración de Empresas, semestre 2; `DES-WEB` y `PROG-COM` sin notas; HTML con `Sin nota` y `Sin notas`; GET 200. |

Para demo, GET `/perfil/?student_id=2026-00002` siguió mostrando
`2026-00001` y no mostró el carné ajeno. Las aserciones de estado HTTP,
carné propio, promedios, inscripciones y ausencia de notas pasaron.

## Capturas proporcionadas por el verificador

- [Estado inicial: pantalla de inicio](img/estado-inicial-inicio.png),
  original `Captura 1.png`: muestra el enlace al perfil desde el inicio.
- [Estado inicial: perfil](img/estado-inicial-perfil.png), original
  `Captura 2.png`: muestra los datos de Estudiante Demo y un curso sin
  temas registrados. Respalda parcialmente CA-1; no demuestra CA-3 ni
  CA-5 ni sustituye evidencia de los escenarios especiales.

Las imágenes iniciales se conservaron sin alterar. En el registro del
PR #41 no existían capturas de CA-2 a CA-8; su evidencia era la suite y
la declaración manual del usuario. Las capturas nuevas de la sección
siguiente corresponden a escenarios aislados, no a una repetición humana
de aquellas pruebas ni al estado inicial de la base demo.

## Evidencia complementaria posterior al PR #41

Fecha: 2026-11-09, hora local registrada en el archivo de ejecución.
Ejecutor: OpenCode, a solicitud del usuario. Commit: `7b2a79b`.
La comparación de `accounts`, `academics`, `tutor`, `config` y `templates`
contra `9f8c6e2` no mostró diferencias de aplicación.

Se ejecutaron de nuevo los tres métodos de `StudentProfileViewTests`
correspondientes a CA-4, CA-6 y CA-8: **3 pruebas OK en 2.043 segundos**.
La salida real completa está en [evidencia/ca4-ca6-ca8.txt](evidencia/ca4-ca6-ca8.txt).
No se presenta esta ejecución como una segunda ejecución de las 80 pruebas.

Después se levantó Django en una dirección de loopback con una base SQLite
temporal migrada y datos sintéticos creados únicamente para los escenarios.
Chrome headless accedió a la aplicación real y capturó la página completa
a 1440 píxeles de ancho, con el CSS local cargado. No son imágenes
reconstruidas a partir de HTML ni capturas editadas. Se comprobaron el DOM,
los cursos, las celdas y los datos esperados antes de cada captura.

Las sesiones se generaron con `Client.force_login` y se suministraron al
navegador solo durante la ejecución, sin versionar cookies ni claves.
Esta evidencia comprueba el perfil autenticado; no vuelve a probar el
formulario de login. Las dos cuentas de CA-7 utilizaron sesiones separadas
en el mismo navegador, sustituyendo la cookie entre consultas.

### Escenarios y capturas

| Criterio | Datos, acción y observación en Chrome | Resultado | Evidencia |
| --- | --- | --- | --- |
| CA-1 | `Perfil principal Sintético`, carné `2026-30001`, carrera `Carrera de prueba 1`, semestre 2; los datos creados en la base temporal aparecen en el perfil. | Cumple en escenario automatizado de navegador. | [Datos](img/ca1-datos.png). |
| CA-2 | El mismo estudiante tiene `S003-BD` y `S003-PROG`; se creó también `S003-RED` sin inscribirlo. Solo se muestran los dos cursos asignados. | Cumple en escenario automatizado de navegador. | [Cursos](img/ca2-cursos.png); cursos observados en el log. |
| CA-3 | Variables 80, Condicionales 65 y Ciclos 70 en `S003-PROG`; promedio visible `71.67`. | Cumple con los valores exactos de la spec. | [Promedio](img/ca3-promedio.png). |
| CA-4 | `Perfil parcial Sintético`, carné `2026-30002`: Variables 80, Condicionales 60 y Ciclos sin registro de nota; se ven `Sin nota` y promedio `70.00`. | Cumple en prueba dirigida y navegador automatizado. | [Tema sin nota](img/ca4-sin-nota.png); log del método CA-4. |
| CA-5 | `Perfil sin notas Sintético`, carné `2026-30003`, inscrito con tres temas existentes y ninguna nota; aparecen tres `Sin nota` y promedio `Sin notas`. | Cumple en escenario automatizado de navegador. | [Curso sin notas](img/ca5-sin-notas.png). |
| CA-6 | `Perfil sin cursos Sintético`, carné `2026-30004`, sin inscripciones; conserva sus datos, no muestra tarjetas de cursos y aparece `Aún no tiene cursos asignados.`. | Cumple en prueba dirigida y navegador automatizado. | [Sin cursos](img/ca6-sin-cursos.png); log del método CA-6. |
| CA-7 | Perfiles `2026-30001` y `2026-30005`, con carreras y cursos distintos. Cada sesión consulta `/perfil/?student_id=` con el carné de la otra; el DOM conserva el propietario y no muestra los datos ajenos. | Cumple en escenario automatizado de navegador. | [Primer perfil](img/ca7-primer-perfil.png), [segundo perfil](img/ca7-segundo-perfil.png); aserciones del DOM registradas. |
| CA-8 | En `2026-30001` se captura 65 y `71.67`, se actualiza una fila de nota a 95 mediante ORM y se recarga la misma pestaña con caché ignorada. Se muestran 95 y `81.67`, sin las celdas 65 ni `71.67`. | Cumple en prueba dirigida y recarga real de navegador automatizado. | [Antes](img/ca8-antes.png), [después](img/ca8-despues.png); actualización y DOM registrados en el log. |

### Aislamiento, reproducción y alcance

- Los perfiles con carnés `2026-30001` a `2026-30005` pertenecen al montaje
  temporal, no al manifiesto de `rebuild_synthetic_data` ni a la base demo.
- Se utilizó automatización temporal con Python estándar y CDP mediante
  Node.js y Chrome existentes. No se instalaron dependencias ni se
  modificaron modelos, vistas, plantillas o pruebas del producto.
- El log contiene la salida de Django y los valores DOM observados en las
  diez capturas, sin secretos. Las comprobaciones no registraron llamadas
  externas de la página ni errores de sus recursos requeridos; se excluyó
  el icono opcional `favicon.ico` del control de errores de recursos.
- Se detuvieron el servidor y navegador creados para esta ejecución y se
  descartaron la base y el perfil temporales. La base demo no se modificó.
- Para reproducir las pruebas dirigidas, ejecutar desde el commit indicado:

```powershell
& ".\.venv\Scripts\python.exe" manage.py test academics.tests.StudentProfileViewTests.test_ca4_topic_without_grade_is_shown_and_excluded academics.tests.StudentProfileViewTests.test_ca6_student_without_courses_sees_data_and_notice academics.tests.StudentProfileViewTests.test_ca8_reload_shows_updated_grade_and_average --verbosity 2
```

Para reproducir visualmente los escenarios, preparar los datos de la tabla
en una base aislada y abrir `/perfil/` con el propietario correspondiente.
La ejecución de Chrome y la comparación de DOM son pruebas automatizadas
del agente, no evidencia de que Ramos haya inspeccionado personalmente las
capturas. Su confirmación explícita está en la sección final.

## Correcciones y repetición de pruebas

- Se corrigió la preparación local de datos, no el código de S-003:
  `rebuild_synthetic_data` reemplazó el conjunto mínimo por el manifiesto
  completo. Después se comprobaron las cuentas mediante el cliente Django.
- No se detectaron fallos en las 80 pruebas ni en los otros controles.
- Un primer intento del comando auxiliar de comprobación HTTP falló por
  comillas en PowerShell (`SyntaxError`), antes de ejecutar Django. Se
  corrigió el comando y la comprobación posterior pasó; no fue un fallo
  de la aplicación ni requirió cambios al repositorio.
- En la ejecución inicial del agente no se realizaron cambios manuales a
  notas o inscripciones de la base demo. CA-4, CA-6 y CA-8 se ejecutaron
  en la base de prueba descartada al terminar. En la ejecución complementaria
  se modificó una nota únicamente en la base temporal para capturar CA-8.

## Confirmación del verificador

ramosdeleon555 · 10-11-2026: revisé este registro y la evidencia de los
PR #41 y #42. Representan las pruebas de CA-1 a CA-8 realizadas en mi
computadora, incluidas las comprobaciones automatizadas que OpenCode
ejecutó a mi solicitud y que se describen como tales en este documento.
Confirmo la verificación de S-003.
