# Plan S-001 — Esqueleto funcional

Propuesto por: OpenCode · GPT-5.6 Sol · modo Plan.
Revisado y aprobado por: JavEstrada09 · 06-11-2026.
Estado: aprobado; Entrega 2 en implementación.
Spec de referencia: fusionada en `main` mediante PR #24.

## Enfoque

Construir un recorrido vertical mínimo en Django que conecte
autenticación, un dato académico propio y dos proveedores del tutor:
Gemini en modo real y respuestas locales en modo demo.

La estructura inicial separará autenticación (`accounts`), datos
académicos (`academics`) e integración del tutor (`tutor`). S-001
creará solo el modelo y los datos necesarios para sus siete criterios.
S-002 ampliará esa base sin volver a crear sus modelos iniciales.

Este plan no implementa el acceso completo por roles ni el perfil
académico completo. Las comprobaciones del esqueleto se realizarán
en el servidor y no dependerán de ocultar elementos de la interfaz.

## Decisiones y dependencias previas

- ADR-001 define Python 3.12, Django 5.2 LTS, SQLite, plantillas
  renderizadas en el servidor, Gemini y un proveedor demo local.
- D-007 define el formato de carné, las carreras sintéticas y el
  intervalo válido de semestre.
- D-010 está aprobada antes de la implementación de S-001: la cuenta
  se representa con `accounts.User` y cada rol mediante su perfil.
- Los perfiles no serán mutuamente excluyentes. Una misma cuenta
  podrá tener más de un perfil cuando futuras specs lo necesiten.
- La existencia de un perfil no sustituirá las comprobaciones de
  permisos sobre cursos y estudiantes que correspondan a cada spec.
- La aprobación de este plan incluye Django 5.2 LTS, `google-genai` y
  `python-dotenv`. Sus versiones compatibles se verificarán y fijarán
  durante la implementación, sin solicitar una autorización redundante.
- La disponibilidad real de `gemini-3.8-flash` y su cuota se comprobarán
  durante la implementación. No se habilitará facturación de pago sin
  aprobación del equipo.

## Responsabilidades de S-001 y S-002

### S-001 — Esqueleto funcional

- Crear el proyecto Django y las aplicaciones iniciales.
- Crear `accounts.User` en `accounts/0001_initial.py`.
- Crear `StudentProfile`, `Course` y `Enrollment` en
  `academics/0001_initial.py`.
- Crear el comando mínimo `python manage.py rebuild_synthetic_data`.
- Permitir el inicio de sesión de un estudiante sintético.
- Mostrar únicamente su carrera desde `StudentProfile.career`.
- Integrar el proveedor Gemini y el proveedor demo.
- Manejar configuración ausente, conexión, cuota y respuesta inválida.
- Probar y documentar el recorrido correspondiente a los siete
  criterios de S-001.

### S-002 — Modelo y datos sintéticos

- Ampliar el modelo académico creado por S-001 para incorporar las
  entidades adicionales de docentes, temas y notas.
- Ampliar `rebuild_synthetic_data` para generar los volúmenes y perfiles
  variados exigidos por S-002 y reconstruirlos de forma reproducible.
- Reutilizar `User`, `StudentProfile`, `Course` y `Enrollment`; no
  sustituir sus migraciones iniciales ni crear modelos duplicados.

Esta división corresponde al alcance entre specs. Las entregas
revisables descritas más adelante son etapas internas de S-001.

## Archivos que se crearán o modificarán al implementar

### Proyecto y configuración

- `manage.py`: entrada de los comandos de Django.
- `config/settings.py`: aplicaciones, base SQLite, plantillas,
  archivos estáticos, `AUTH_USER_MODEL` y configuración del tutor.
- `config/urls.py`: rutas de acceso, cierre de sesión y esqueleto.
- `config/asgi.py` y `config/wsgi.py`: entradas estándar de Django.
- `.env.example`: nombres de variables con valores vacíos.
- `.gitignore`: exclusión de `.env`, SQLite y entornos virtuales.
- `requirements.txt`: versiones exactas verificadas de Django 5.2 LTS,
  `google-genai` y `python-dotenv`, incluidas en la aprobación del plan.

### Aplicación `accounts`

- `accounts/models.py`: modelo `User` basado en la autenticación
  estándar de Django, sin un campo exclusivo de rol.
- `accounts/migrations/0001_initial.py`: creación de `User`.
- `accounts/tests.py`: pruebas de autenticación y mensajes de error.

### Aplicación `academics`

- `academics/models.py`: `StudentProfile`, `Course` y `Enrollment`.
- `academics/migrations/0001_initial.py`: creación de los tres modelos
  y dependencia de la migración inicial de `accounts`.
- `academics/views.py`: pantalla protegida del esqueleto y consulta
  del perfil perteneciente al usuario autenticado.
- `academics/urls.py`: ruta de la pantalla protegida.
- `academics/management/commands/rebuild_synthetic_data.py`: datos
  mínimos de S-001 que S-002 ampliará.
- `academics/tests.py`: pruebas del dato propio, permisos, restricciones
  del modelo y comando de datos.

### Aplicación `tutor`

- `tutor/forms.py`: validación de la pregunta enviada por el estudiante.
- `tutor/providers.py`: contrato de proveedor, proveedor Gemini,
  proveedor demo y errores controlados.
- `tutor/services.py`: selección del proveedor, preparación del contexto
  mínimo, validación de la respuesta y cambio seguro al modo demo.
- `tutor/demo_responses.py`: respuestas grabadas disponibles sin red.
- `tutor/tests.py`: pruebas de selección, salida, fallos y ausencia de
  llamadas externas en modo demo.

### Interfaz, documentación y verificación

- `templates/base.html`: estructura común y recursos locales.
- `templates/registration/login.html`: formulario de acceso en español.
- `templates/academics/student_home.html`: carrera, formulario del tutor,
  respuesta, modo activo y errores comprensibles.
- `static/vendor/bootstrap/`: archivos locales autorizados de Bootstrap.
- `static/css/tutobosco.css`: ajustes visuales propios.
- `README.md`: instalación, configuración, migraciones,
  `rebuild_synthetic_data`, ejecución y pruebas con comandos realmente
  comprobados, sin incluir contraseñas.
- `AGENTS.md`: comandos reales, solo después de comprobarlos.
- `docs/registro-ia.md`: uso real de IA durante cada fase.
- `docs/gasto.md`: consumo real de Gemini, aunque sea cero.
- `specs/S-001-esqueleto/verificacion.md`: resultados y evidencia de
  Douglas después de ejecutar los criterios en su computadora.

Los archivos estándar `__init__.py` y `apps.py` de cada paquete se
incluirán donde Django los requiera, sin añadir lógica de negocio.

## Cambios al modelo de datos

### `accounts.User`

- Extenderá el usuario estándar de Django para conservar sus mecanismos
  de autenticación, sesiones y hash de contraseñas.
- No tendrá un campo que obligue a escoger un único rol.
- Se configurará `AUTH_USER_MODEL` antes de crear las migraciones.
- Los roles se obtendrán mediante perfiles relacionados, según D-010.

### `academics.StudentProfile`

Conservará los cuatro campos acordados:

- `user`: relación uno a uno con `accounts.User`.
- `student_id`: carné sintético único con el formato de D-007.
- `career`: carrera académica sintética.
- `semester`: entero entre 1 y 10.

S-001 consultará el perfil correspondiente a la cuenta autenticada,
pero mostrará únicamente `career`. El carné y el semestre quedarán
disponibles para specs posteriores.

### `academics.Course`

- `code`: código obligatorio y único del curso.
- `name`: nombre mostrado del curso.

El dato mínimo incluirá el curso Programación Comercial con el código
exacto `PROG-COM`.

### `academics.Enrollment`

- `student`: relación con `StudentProfile`.
- `course`: relación con `Course`.
- Restricción única por pareja estudiante-curso para impedir que una
  misma inscripción se repita.

`academics/0001_initial.py` dependerá de `accounts/0001_initial.py`
porque `StudentProfile.user` referencia al modelo `User`.

## Datos mínimos y comando compartido

S-001 introducirá el comando:

```text
python manage.py rebuild_synthetic_data
```

### Manifiesto de identificadores exactos

Los nombres e identificadores públicos acordados son:

- Modelo de cuenta: `accounts.User`.
- Perfil del estudiante: `academics.StudentProfile`.
- Curso: `academics.Course` con `code=PROG-COM`.
- Inscripción: `academics.Enrollment`, única por estudiante y curso.
- Comando: `python manage.py rebuild_synthetic_data`.
- Configuración de modo: `AI_MODE`, con valores `real` o `demo`.
- Configuración de modelo: `AI_MODEL`.
- Clave del proveedor: `GEMINI_API_KEY`.
- Contraseña local del estudiante demo: `DEMO_STUDENT_PASSWORD`.

Los identificadores sintéticos estables de la cuenta y del perfil se
declararán juntos en el manifiesto versionado del comando, no se
obtendrán de registros preexistentes ni de datos reales.

El comando tendrá ejecución idempotente: repetirlo producirá el mismo
estado mínimo sin duplicar registros. Creará o actualizará únicamente
los registros cuyos identificadores exactos pertenezcan a su manifiesto:

- Una cuenta sintética de estudiante. Leerá su contraseña desde
  `DEMO_STUDENT_PASSWORD` y la guardará solo mediante el hash de Django.
- Su `StudentProfile` con carné, carrera y semestre válidos.
- El curso Programación Comercial con `code=PROG-COM`.
- La inscripción del estudiante en ese curso.

Si falta `DEMO_STUDENT_PASSWORD`, el comando terminará con un error
comprensible sin crear una contraseña predeterminada. La contraseña no
se guardará en README, código, registros, salida del comando ni commits.
La base SQLite tampoco se versionará.

S-002 ampliará este mismo comando para reconstruir el conjunto completo
de estudiantes, docentes, cursos, temas y notas. Tanto S-001 como S-002
limitarán las actualizaciones y eliminaciones a identificadores incluidos
en el manifiesto. No modificarán ni borrarán registros ajenos, aunque el
comando se ejecute varias veces sobre una base que contenga otros datos.

## Configuración pública acordada

La interfaz de configuración conservará exactamente estas variables:

- `AI_MODE=real` selecciona el proveedor real.
- `AI_MODE=demo` selecciona el proveedor local sin red.
- `AI_MODEL` contiene el identificador configurable del modelo; el valor
  previsto por ADR-001 es `gemini-3.8-flash`.
- `GEMINI_API_KEY` contiene la clave usada solo por el backend.
- `DEMO_STUDENT_PASSWORD` proporciona la contraseña al comando de datos.

El proveedor real puede llamarse Gemini dentro del código, pero no se
usará `gemini` como valor público de `AI_MODE`. Cambiar estos nombres o
valores requerirá una decisión documental previa.

`.env.example` conservará únicamente los nombres con valores vacíos. La
configuración local se cargará con `python-dotenv` y no se versionará.

## Seguridad y autorización del recorrido

- `CsrfViewMiddleware` permanecerá activo en la configuración de Django.
- Todos los formularios con método POST incluirán `{% csrf_token %}`.
- Ninguna vista utilizará `csrf_exempt`.
- Las pruebas de formularios POST usarán
  `Client(enforce_csrf_checks=True)` y comprobarán rechazo sin token y
  aceptación con token válido.
- La vista comprobará en el servidor que la cuenta autenticada tiene su
  `StudentProfile` y una `Enrollment` para el curso `PROG-COM` antes de
  mostrar datos académicos o permitir preguntas al tutor.
- `is_staff` solo habilita funciones administrativas de Django; no
  concede acceso académico, perfil de estudiante ni inscripción.
- Las contraseñas se establecerán mediante los mecanismos de hash de
  Django y nunca se compararán, registrarán ni almacenarán en texto plano.

## Proveedores del tutor

`tutor.providers` expondrá un contrato común que reciba la pregunta y
el contexto permitido, y devuelva texto validado. La vista no llamará
directamente a Gemini.

### Proveedor Gemini

- Se ejecutará únicamente en el backend.
- Leerá la clave y el identificador del modelo desde variables de
  entorno; no incluirá secretos en código, registros ni respuestas.
- Enviará solo la carrera del estudiante autenticado, el nombre del
  curso y la pregunta. No enviará carné, contraseña ni datos de otros.
- Pedirá una respuesta en español, con trato de usted y mención de
  Programación Comercial.
- Rechazará respuestas vacías o con una estructura no utilizable.
- No ejecutará como código ningún contenido generado por el modelo.

### Proveedor demo

- Usará respuestas grabadas almacenadas en el repositorio.
- Funcionará sin conexión y sin clave de Gemini.
- No importará ni invocará el cliente externo al atender una pregunta.
- Identificará claramente el modo demo en la interfaz.
- Incluirá una respuesta para el caso mínimo de S-001; S-006, S-007 y
  S-009 ampliarán luego sus casos de conversación y práctica.

### Selección y errores

- `AI_MODE=real` seleccionará el proveedor Gemini y `AI_MODE=demo`
  seleccionará el proveedor local.
- El proveedor real leerá el modelo desde `AI_MODEL` y la clave desde
  `GEMINI_API_KEY`.
- Configuración ausente o inválida, fallo de conexión, cuota agotada y
  respuesta inválida se traducirán a errores propios de la aplicación.
- La interfaz mostrará un mensaje en español sin trazas, claves ni
  detalles internos del proveedor.
- Ante un fallo esperado de Gemini, el servicio permitirá continuar con
  una respuesta demo y dejará visible que se utilizó ese modo.
- Los errores inesperados se registrarán sin datos sensibles y se
  responderán de forma segura; no se ocultarán con un éxito falso.

## Entregas revisables dentro de S-001

Las entregas son puntos de revisión de una misma spec. No son nuevas
specs ni trasladan responsabilidades a S-002.

### Entrega 1 — Base ejecutable y modelo inicial

- Crear el proyecto y las tres aplicaciones.
- Configurar el usuario personalizado antes de migrar.
- Crear las migraciones iniciales en el orden acordado.
- Implementar `rebuild_synthetic_data` con su manifiesto y los datos
  mínimos protegidos.
- Probar modelos, restricciones, migraciones y repetición del comando.

### Entrega 2 — Autenticación y carrera del estudiante

- Implementar acceso y cierre de sesión con componentes de Django.
- Proteger la pantalla del esqueleto en el servidor.
- Comprobar el `StudentProfile` y la inscripción en `PROG-COM` de la
  cuenta autenticada, sin conceder acceso por `is_staff`.
- Mostrar solo `career` y mensajes de error en español.
- Probar credenciales válidas, inválidas, CSRF y aislamiento del dato
  propio con comprobaciones realizadas en el servidor.

### Entrega 3 — Tutor real y modo demo

- Implementar el contrato común y el proveedor demo.
- Verificar y fijar las versiones de las dependencias ya aprobadas.
- Integrar Gemini desde el backend y confirmar el modelo disponible.
- Validar entradas, contexto y salida.
- Probar el modo demo sin red y la integración real controlada.

### Entrega 4 — Errores, reproducibilidad y cierre técnico

- Completar el manejo de configuración, conexión, cuota y salida inválida.
- Incorporar recursos visuales locales y estados comprensibles.
- Documentar solo los comandos ejecutados correctamente.
- Ejecutar toda la suite y revisar los siete criterios como autor.
- Preparar `verificacion.md` para la ejecución independiente de Douglas.

## Secuencia en `s-001-esqueleto`

La implementación reutilizará la rama `s-001-esqueleto`. No se creará
otra rama para cada entrega.

Cada entrega se presentará mediante un PR secuencial desde
`s-001-esqueleto`. Antes de abrir el siguiente, el PR anterior deberá
estar revisado, probado y fusionado; después se actualizará la misma rama
desde `main` sin reescribir el historial compartido.

Los PR de las entregas 1, 2 y 3 usarán `Ref #4` para mantener abierto el
issue. Cada uno incluirá sus comandos y resultados de pruebas. Solo se
fusionarán si `main` queda ejecutable y el recorrido disponible hasta esa
entrega continúa funcionando.

La entrega 4 se verificará con sus siete criterios antes de fusionarse.
Únicamente su PR final usará `Closes #4`, después de registrar la
verificación independiente y la evidencia real. No se crean ramas ni PR
durante esta corrección documental.

## Tareas en orden

1. Confirmar que la spec y este plan están en la base de la rama de
   implementación, sin reescribir historial compartido.
2. Verificar compatibilidad y fijar las versiones exactas de Django 5.2
   LTS, `google-genai` y `python-dotenv`, ya aprobadas en este plan.
3. Completar la Entrega 1, ejecutar sus pruebas y abrir su PR con
   `Ref #4`.
4. Revisar, probar y fusionar la Entrega 1 manteniendo `main` ejecutable.
5. Actualizar `s-001-esqueleto` desde `main`, completar la Entrega 2 y
   abrir su PR con `Ref #4` después de ejecutar sus pruebas.
6. Revisar, probar y fusionar la Entrega 2 manteniendo `main` ejecutable.
7. Actualizar la rama, completar la Entrega 3, comprobar el modelo Gemini,
   registrar cualquier consumo y abrir su PR con `Ref #4`.
8. Revisar, probar y fusionar la Entrega 3 manteniendo `main` ejecutable.
9. Actualizar la rama, completar la Entrega 4 y ejecutar la suite completa.
10. Leer y ejecutar cada cambio como autor antes de sus commits y PR.
11. Solicitar a Douglas la verificación de los siete criterios en su
    computadora y registrar únicamente sus resultados reales en
    `verificacion.md`.
12. Corregir los fallos encontrados y repetir los criterios afectados.
13. Actualizar los registros de IA y gasto con valores reales.
14. Abrir el PR final de la Entrega 4 con `Closes #4` únicamente cuando
    la verificación y la evidencia requeridas estén completas.

## Cómo se verificará cada criterio

### CA-1 — Inicio de sesión correcto

- Una prueba de cliente Django creará el usuario mediante el mecanismo
  estándar, iniciará sesión y comprobará la redirección a la pantalla.
- Se comprobará que la contraseña almacenada no coincide con el texto
  original y que el verificador de hash de Django la reconoce.
- El comando obtendrá la contraseña desde `DEMO_STUDENT_PASSWORD`; las
  pruebas comprobarán que no aparece en salidas ni registros.

### CA-2 — Inicio de sesión incorrecto

- Una prueba enviará contraseña incorrecta y otra un usuario inexistente.
- Ambas mantendrán a la persona sin autenticar y mostrarán el mismo
  mensaje general en español, sin revelar qué credencial falló.
- Las solicitudes POST se ejecutarán con
  `Client(enforce_csrf_checks=True)` para comprobar el rechazo sin token
  y el procesamiento con un `{% csrf_token %}` válido.

### CA-3 — Dato propio del perfil y acceso protegido

- Las pruebas crearán dos estudiantes con carreras distintas.
- Cada sesión verá únicamente su propia carrera si el servidor confirma
  tanto su `StudentProfile` como su inscripción en `PROG-COM`.
- Una cuenta sin perfil, sin inscripción o solo con `is_staff=True` no
  obtendrá acceso académico.
- Una solicitud anónima será redirigida al acceso y no incluirá datos
  académicos en la respuesta.
- La página no mostrará `student_id` ni `semester` en S-001.

### CA-4 — Respuesta real de IA

- Las pruebas automatizadas aislarán el cliente externo para comprobar
  contexto, validación y presentación sin gastar cuota en cada ejecución.
- La comprobación de aceptación realizará una llamada real desde el
  backend con `AI_MODE=real`, `AI_MODEL` y `GEMINI_API_KEY` configurados.
- La evidencia mostrará respuesta en español, trato de usted y curso,
  sin registrar la clave ni datos sensibles. Una respuesta demo no
  contará para este criterio.

### CA-5 — Respuesta grabada sin conexión

- Una prueba establecerá `AI_MODE=demo`, eliminará `GEMINI_API_KEY` y
  bloqueará o simulará como fallida cualquier salida de red.
- Completará acceso, consulta de carrera y pregunta de demostración.
- Comprobará la respuesta grabada y la etiqueta visible de modo demo.
- La prueba fallará si intenta construir o llamar al cliente Gemini.

### CA-6 — Error del proveedor

- Pruebas separadas simularán configuración ausente, conexión fallida,
  cuota agotada y respuesta inválida.
- Comprobarán un mensaje seguro en español, ausencia de detalles
  sensibles y continuidad mediante el proveedor demo identificado.

### CA-7 — Ejecución local reproducible

- El autor probará los comandos documentados desde una preparación limpia.
- Douglas seguirá únicamente el README en su computadora, aplicará las
  migraciones, definirá localmente `DEMO_STUDENT_PASSWORD`, ejecutará
  `rebuild_synthetic_data`, iniciará el servidor y completará el recorrido
  demo sin red ni clave de Gemini.
- Se comprobará que SQLite, `.env` y secretos no estén versionados y que
  los recursos visuales requeridos sean locales.

## Pruebas y verificación

Las pruebas automatizadas cubrirán modelos, restricciones, comando de
datos, autenticación, aislamiento, proveedores, errores y vistas. No
harán llamadas reales de Gemini salvo en la ejecución controlada del
criterio CA-4.

Las pruebas POST utilizarán `Client(enforce_csrf_checks=True)`. También
comprobarán `CsrfViewMiddleware`, la presencia de `{% csrf_token %}`, la
ausencia de `csrf_exempt`, el perfil y la inscripción exigidos por el
servidor, y que `is_staff` no concede permisos académicos.

JavEstrada09 ejecutará y leerá los cambios antes de cada commit. Douglas
es el verificador asignado, pero este plan no le atribuye aprobación ni
pruebas todavía. Sus resultados, computadora, commit y evidencia se
registrarán solo después de que realice la verificación.

S-001 no se considerará terminada por aprobar este plan. Permanecerán
pendientes la implementación, la verificación ajena, la evidencia, el
PR final y la comprobación desde `main` en otra computadora.

## Correcciones humanas al plan del agente

Durante la revisión del 06-11-2026, JavEstrada09 solicitó y aprobó estas
correcciones reales:

- Conservar `accounts.User` como cuenta de autenticación.
- Conservar `StudentProfile` con `user`, `student_id`, `career` y
  `semester`, según la base coordinada con Douglas.
- Mostrar únicamente `career` en el recorrido de S-001.
- Crear `User` en `accounts/0001_initial.py` y los modelos académicos
  iniciales en `academics/0001_initial.py`.
- Mantener `Course.code` obligatorio y único, con `PROG-COM` para el
  curso piloto, y `Enrollment` único por estudiante y curso.
- Aprobar D-010 antes de implementar: roles mediante perfiles, sin
  imponer exclusividad entre ellos.
- Distinguir el alcance de S-001 y S-002 de las entregas revisables
  internas de S-001.
- Mantener el comando mínimo `rebuild_synthetic_data` para que S-002 lo
  amplíe, con ejecución idempotente y protección de registros ajenos.
- Mantener cuatro entregas secuenciales y revisables desde la rama
  `s-001-esqueleto`, sin crear ahora ramas ni PR.
- Conservar los siete criterios, ambos proveedores, el manejo de errores,
  las pruebas y la futura verificación independiente de Douglas.

La revisión posterior del diff corrigió desviaciones de redacción del
agente: restauró el nombre `rebuild_synthetic_data`; las variables
`AI_MODE`, `AI_MODEL`, `GEMINI_API_KEY` y `DEMO_STUDENT_PASSWORD`; los
controles CSRF y de autorización; las tres dependencias aprobadas; y los
PR secuenciales con `Ref #4` y `Closes #4`. Estas correcciones no agregan
decisiones ni aprobaciones atribuidas a Douglas.

Durante la integración de `main`, la decisión de roles se renumeró de
D-008 a D-010 porque los identificadores D-008 y D-009 ya estaban
ocupados. La renumeración no modifica el acuerdo aprobado.

La aprobación registrada corresponde a JavEstrada09. No se atribuye a
Douglas ninguna aprobación adicional ni una verificación todavía.
