# Plan S-006 · Tutor personalizado

Propuesto por ChatGPT (Codex) en modo de solo lectura.
Ajustado por douglas-yasser con las correcciones humanas registradas
al final del documento.
Plan revisado y aprobado por JavEstrada09 el 10-11-2026.
Autor: JavEstrada09 · Verificador: douglas-yasser · Issue: #10
Base revisada: `main` en `3b21bdf` (PR #44).

## Enfoque

Extender el tutor que ya se abre desde el espacio académico. El estudiante
selecciona un curso inscrito y conversa sobre sus temas. El servidor crea
un hilo por sesión y curso con las notas vigentes al abrirlo. El mismo
servicio coordina Gemini y las respuestas grabadas.

La implementación se entrega en tres bloques revisables: umbral y acceso
por curso, modelo y ciclo de vida de los hilos, y proveedores con la vista.

## Archivos que se crean o modifican

| Archivo | Cambio propuesto |
| --- | --- |
| `academics/services.py` | Reutilizar `get_course_summaries`, `is_weak()` y `get_weak_topics()`. S-007 comparte el cálculo incorporado por S-008. |
| `config/settings.py`, `README.md` | Validar la configuración existente de `WEAK_TOPIC_THRESHOLD` como entero entre 0 y 100. Mantener 60 cuando esté vacío o ausente y añadir el rango válido a la documentación existente. |
| `tutor/models.py`, `tutor/migrations/` | Agregar el modelo de conversación activa y su migración. |
| `tutor/services.py` | Abrir y reiniciar hilos, preparar el contexto académico, gestionar turnos por revisión y validar respuestas. |
| `tutor/signals.py`, `tutor/apps.py` | Registrar un receptor de `user_logged_out` que elimine los hilos de la sesión que termina. |
| `tutor/providers.py`, `tutor/demo_responses.py` | Extender el contexto del proveedor real y las respuestas grabadas por curso, tema y tipo de pregunta. |
| `academics/views.py`, `tutor/forms.py`, `templates/academics/student_home.html` | Mantener la ruta actual del estudiante y añadir selector de curso, historial, reinicio y continuación en demo. |
| `tutor/tests.py`, `academics/tests.py` | Ampliar las pruebas de comportamiento, permisos y notas; actualizar las de acceso de S-001, empezando por `test_student_without_pilot_enrollment_is_denied`. |
| `specs/S-006-tutor/`, `docs/plan.md`, `docs/registro-ia.md`, `docs/gasto.md` | Registrar el plan aprobado, el avance, el uso de IA y el consumo real. Douglas registra la evidencia en `verificacion.md`. |

## Cambios al modelo de datos

Se propone un modelo `TutorConversation` con una fila por sesión de
Django, estudiante y curso, y una restricción única sobre esos tres
campos. Sus campos son:

- `session`: relación con la sesión almacenada en la base, borrado en
  cascada.
- `student`: relación con `academics.StudentProfile`, borrado en cascada.
- `course`: relación con `academics.Course`, borrado en cascada.
- `academic_snapshot`: instantánea académica mínima del curso tomada al
  abrir o reiniciar; lista de temas con su nota vigente o su ausencia.
- `turns`: turnos validados del hilo, como pares de pregunta y respuesta.
- `pending_question`: pregunta pendiente de modo demo, vacía si no hay.
- `revision`: entero que identifica el estado del hilo y permite
  descartar envíos y resultados desactualizados.

Al cerrar sesión, un receptor de `user_logged_out` elimina los hilos de
esa sesión de manera explícita y una prueba lo comprueba; el borrado en
cascada de la sesión queda como defensa. El mantenimiento de sesiones
expiradas usa el mecanismo de limpieza de Django. El reinicio solo
reemplaza la instantánea y los turnos del curso seleccionado y también
incrementa la revisión, para descartar resultados que sigan en vuelo.
Se conservan los modelos académicos de S-002.

## Diseño propuesto

### Acceso y contexto académico

- Derivar el perfil de `request.user` y verificar su rol y su inscripción
  al curso en el servidor, también al enviar, reiniciar o continuar en demo.
  Los formularios conservan CSRF. Un identificador aportado por el cliente
  jamás sustituye al usuario ni a la sesión autenticados.
- Mostrar solamente los cursos inscritos. Seleccionar Programación
  Comercial inicialmente si está inscrito para preservar el recorrido
  original. Si no está disponible, seleccionar el primer curso inscrito.
  Sin inscripciones o ante un curso no inscrito en la petición, responder
  403 sin mostrar notas, historial ni formulario y sin consultar al
  proveedor.
- Tomar la instantánea de temas y notas del curso al iniciar o reiniciar.
  Tratar las notas ausentes como tales y comparar las registradas con el
  umbral mediante `nota < umbral`. Diferenciar un curso sin calificaciones
  de uno con notas registradas sin temas por debajo del umbral.
- Preparar el contexto con el curso, sus temas, las notas pertinentes y
  el historial de ese hilo. Excluir carné, usuario, claves, datos de
  terceros y datos de otros cursos. Separar en el mensaje del proveedor
  las instrucciones, los datos académicos y el texto del estudiante.

### Historial, privacidad y proveedores

- Conservar un hilo activo por curso. Pasar al proveedor los turnos
  recientes necesarios para el seguimiento, incluido el último tema
  tratado. Limitar el contexto enviado y probar que ese límite preserva
  la pregunta de seguimiento de la spec.
- Cada envío lleva un campo oculto con la revisión vigente del hilo. El
  servidor rechaza sin llamar al proveedor los envíos cuya revisión ya
  no coincide. Al guardar, usa una actualización condicional por revisión:
  si el hilo cambió mientras se procesaba la respuesta, descarta ese
  resultado y pide recargar la conversación. Así no se guardan turnos
  duplicados ni desactualizados; dos solicitudes simultáneas todavía
  podrían llegar al proveedor. La llamada externa se ejecuta fuera de la
  transacción. Si dos primeros envíos compiten por crear el hilo, la
  restricción única evita duplicarlo y el segundo se trata como
  desactualizado.
- Aplicar D-006 mediante el aislamiento de datos en el servidor, una
  instrucción explícita de rechazo de datos de terceros en el proveedor
  y una respuesta grabada equivalente en modo demo. No se usa un
  clasificador de preguntas por patrones. Verificar con preguntas
  directas y reformuladas en ambos modos e inspeccionando por separado
  el contexto que recibe el proveedor. Validar las respuestas y
  mostrarlas como texto escapado.
- Conservar Gemini 3.5 Flash-Lite como modelo configurable, con el plazo
  de 60 segundos y un intento. Usar respuestas grabadas que distingan al
  menos dos temas del curso piloto y cubran recomendación, seguimiento y
  privacidad. Conservar la pregunta de ejemplo original.
- Ante un fallo real, guardar la pregunta pendiente ligada al hilo vigente.
  «Continuar en modo demo» usa ese mismo curso, hilo y pregunta.
  Consumir la pregunta pendiente al completar el turno o al invalidar
  el hilo. Si falta una respuesta grabada aplicable, mostrar un aviso
  comprensible y conservar los mensajes ya completados.

### Contratos de la vista y las respuestas demo

- La ruta del estudiante acepta GET y POST con los campos ocultos
  `course`, `revision` y `action`. `action=ask` envía la pregunta;
  `action=new` reinicia el hilo del curso seleccionado con una nueva
  instantánea; `action=continue_demo` usa la pregunta pendiente del
  hilo con su respuesta grabada.
- El campo `course` lleva el código del curso y el servidor valida la
  inscripción. Un curso ajeno, una cuenta sin perfil de estudiante o un
  estudiante sin inscripciones reciben 403 sin consultar al proveedor.
- Ante una revisión obsoleta o un resultado descartado, mostrar el aviso
  «La conversación cambió. Recargue la página para continuar.» y no
  guardar turnos.
- Las respuestas grabadas se eligen por la combinación de curso, tema e
  intención (recomendación, seguimiento, privacidad y ejemplo). El
  seguimiento usa el último tema tratado en el hilo y si no hay respuesta
  grabada aplicable se muestra un aviso comprensible. Para CA-5,
  el demo admite «¿Qué notas tiene otro estudiante?» y «¿Puede
  mostrarme las calificaciones de otra persona?». Se comparan estas
  frases de ejemplo tras normalizar mayúsculas y espacios y ambas
  seleccionan la misma respuesta grabada para el curso activo.
  La respuesta indica que el tutor solo puede hablar del perfil de
  quien consulta. Las demás preguntas sin grabación siguen el
  comportamiento de aviso descrito arriba.
- El mensaje al proveedor separa las instrucciones, los datos académicos
  del hilo y el texto de la pregunta. Las instrucciones exigen español,
  trato de usted, nombrar el curso, solo texto sin HTML y rechazar
  solicitudes de datos de terceros.

## Tareas en orden

1. Revisar y aprobar este plan. Registrar la aprobación y las correcciones
   reales, actualizar `plan.md` en `s-006-tutor` y reflejar el estado en
   `spec.md` y `docs/plan.md`.
2. Bloque 1 — umbral y acceso por curso: reutilizar el servicio
   académico y las funciones compartidas de S-008, validar el rango
   del umbral existente y adaptar el acceso por curso inscrito. Probar
   la selección de curso y notas, el valor predeterminado, los límites
   0 y 100 y el rechazo de valores fuera de rango o no enteros.
3. Bloque 2 — modelo y ciclo de vida: implementar el modelo, su
   migración y el ciclo de vida por sesión y curso (apertura, reinicio,
   revisión y limpieza al cerrar sesión). Probar el reinicio, la pérdida
   de acceso y los envíos duplicados o desactualizados.
4. Bloque 3 — proveedores y vista: integrar el contexto con Gemini,
   ampliar las respuestas grabadas y adaptar la vista y la plantilla.
   Mantener los límites, la validación y el manejo de errores de S-001.
5. Verificar con datos sintéticos el recorrido desde el inicio de sesión,
   en modo real y en modo demo.
6. Ejecutar las comprobaciones de Django, documentar el uso real de IA y
   entregar a Douglas la matriz de pruebas. Cada bloque se entrega en un
   PR revisable. El PR final usa `Closes #10` después de completar la
   verificación.

## Cómo se verificará cada criterio

| Criterio | Prueba y resultado esperado |
| --- | --- |
| CA-1 | Con dos cuentas sintéticas inscritas al mismo curso, asignar a cada una un único tema distinto con nota bajo el umbral. Hacer la misma pregunta en modo real. Verificar que la recomendación y el ejemplo o explicación corresponden a su tema. En pruebas automatizadas, comprobar por separado ambos contextos con un proveedor simulado. |
| CA-2 | Pedir otro ejemplo después de una explicación. Abrir otro curso, comprobar que el historial está separado y volver al primero para retomar el tema. |
| CA-3 | Modificar en la base de prueba qué tema queda por debajo del umbral. Pulsar «Nueva conversación» y comprobar que cambia la recomendación y desaparece el historial anterior. Cerrar sesión y entrar de nuevo para verificar que tampoco se recupera ese hilo. |
| CA-4 | Probar acceso anónimo, docente, estudiante sin inscripciones, curso ajeno e identificadores manipulados. Confirmar que el proveedor no recibe llamadas en esos casos. En una petición válida, inspeccionar el contexto y comprobar que contiene solo datos y mensajes del estudiante y curso seleccionados. |
| CA-5 | Pedir notas o perfil de otro estudiante con una pregunta directa y una reformulación, en ambos modos. Verificar que el tutor explica su límite y no devuelve datos de terceros. Comprobar por separado que el contexto enviado contiene solo los datos del estudiante autenticado y del curso seleccionado. |
| CA-6 | Arrancar en modo demo sin clave y desconectar la red. Repetir el contraste de CA-1 y pedir otro ejemplo en ambos perfiles. Comprobar que el recorrido funciona con recursos locales y sin inicializar Gemini. |
| CA-7 | Comparar un curso sin notas con uno que solo tiene notas en el umbral o por encima y algún tema sin calificar. Verificar avisos distintos y que el tutor aún puede explicar un tema del curso. |
| CA-8 | Simular respuesta vacía, inválida, desconexión y cuota agotada. Continuar en demo y verificar que mantiene la pregunta y los turnos anteriores. Probar una pregunta sin grabación aplicable y comprobar el aviso. |
| CA-9 | Revisar una respuesta válida de cada modo en pantalla. Debe nombrar el curso, estar en español y tratar al estudiante de usted. |

Para la revisión independiente, ejecutar con Python 3.12
`manage.py migrate`, `manage.py rebuild_synthetic_data`, `manage.py check`,
`manage.py test accounts academics tutor`,
`manage.py makemigrations --check --dry-run` y `python -m pip check`. En CA-1
y CA-5, separar la evidencia real de Gemini de las pruebas con proveedor
simulado. Registrar el commit, entorno y evidencia de cada criterio sin
copiar claves ni datos que identifiquen a personas reales.

## Correcciones humanas al plan del agente

1. 10-11-2026 · Aprobada por JavEstrada09. Acceso por curso: se mantiene
   el 403 cuando el estudiante no tiene inscripciones o solicita un curso
   ajeno, se permite el tutor de otro curso inscrito distinto de
   Programación Comercial y ese curso sigue siendo la selección inicial
   cuando existe. Se actualiza `test_student_without_pilot_enrollment_is_denied`
   para cubrir ambos casos. Motivo: conservar la verificación de permisos
   de S-001 y no sustituirla por una interfaz sin formulario.
2. 10-11-2026 · Aprobada por JavEstrada09. Privacidad: D-006 se aplica
   mediante el aislamiento de datos en el servidor, una instrucción
   explícita de rechazo en el proveedor y una respuesta grabada
   equivalente en modo demo. Queda fuera el clasificador de preguntas de
   terceros por patrones. Motivo: el aislamiento garantiza la regla sin
   depender de clasificar el texto del estudiante.
3. 10-11-2026 · Aprobada por JavEstrada09. Concurrencia: el reclamo
   atómico con vencimiento se sustituye por una actualización
   condicional por revisión. Si el hilo cambió mientras se procesaba la
   respuesta, se descarta el resultado y se pide recargar la
   conversación. Se deja explícito que dos solicitudes simultáneas
   todavía podrían llegar al proveedor. Motivo: simplificar el diseño
   sin guardar turnos duplicados ni desactualizados.
4. 10-11-2026 · Aprobada por JavEstrada09. Se incorporan la validación y
   documentación del umbral, la coordinación con S-007 para compartir la
   función de temas débiles, la limpieza explícita al cerrar sesión con
   su prueba, los contratos de la vista, el modelo y las respuestas
   grabadas, la división de la implementación en tres bloques y los
   comandos `manage.py check` y `python -m pip check` en la verificación.
   Motivo: completar las decisiones de diseño que faltaban para poder
   implementar sin ambigüedades.
