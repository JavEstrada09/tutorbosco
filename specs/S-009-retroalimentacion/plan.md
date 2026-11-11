# Plan S-009 — Respuestas y retroalimentación

Autor: Jeffersson Ramos (ramosdeleon555).
Estado: plan actualizado aprobado por Jeffersson en la conversación actual;
implementación entregada en el PR #60 sobre 360da36; corrección pedagógica
en curso, pendiente de revisión humana y cierre de verificación independiente.
Propuesto por: OpenCode · openai/gpt-6.1-sol · análisis de solo lectura.
Revisión de la propuesta anterior: usuario de esa sesión, 2026-11-09, mediante
«entonces hazlo, adelante», después de presentar contrato, flujo,
persistencia, estructura y pruebas. No equivale a revisión de PR ni
verificación independiente. La autorización actual para resguardar,
actualizar la rama y ajustar documentos no aprueba automáticamente los
detalles técnicos actualizados que se presentan a continuación. Tras presentar
el resumen actualizado, el autor confirmó «si, autorizo», aprobando el plan
y la estructura para comenzar la implementación.

## Enfoque

Registrar cada respuesta a un ejercicio propio antes de consultar al
proveedor compartido. Recuperar el contexto académico vigente, validar
la devolución y asociarla a esa respuesta concreta. Conservar la respuesta
ante fallos y permitir el recorrido demo mediante casos locales explícitos.

## Base y condiciones de inicio

- Worktree: `C:\Users\Canche\Desktop\tutorbosco-s-009`.
- Rama: `s-009-retroalimentacion`; base actualizada a main `914b8da`.
- La propuesta anterior se preparó sobre la base documental `58881f0`.
  Se conservó mediante stash autorizado antes del avance rápido a main.
- S-007 ya está integrada mediante el PR #56. Existe PracticeExercise con
  UUID, student, course, topic, statement, mode, demo_key y created_at.
- La spec de S-009 está incorporada a main y se mantiene aprobada. El
  código de S-009 comienza después de aprobar estos ajustes al plan.
- No crear una implementación paralela de S-007 o S-006 para suplir sus
  dependencias. Cualquier cambio sustancial del contrato requiere revisión.

## Contrato acordado con S-007

El usuario indicó que ambas specs le corresponden y aprobó la propuesta
compartida en esta conversación el 2026-11-09. Este acuerdo no representa
aprobación del verificador Brayan11Hernandez.

S-007 proporciona `PracticeExercise` con UUID estable, estudiante propietario,
curso, tema, enunciado, procedencia, clave demo opcional y fecha. S-009
reutiliza esos campos existentes; comprueba la consistencia entre course
y topic.course y no crea otro modelo ni modifica el contrato de ejercicios.

S-009 recibe el identificador del ejercicio y el contenido de la respuesta.
El servidor recupera propietario, curso, tema, enunciado y contexto desde
la base; nunca confía en esas relaciones si las envía el navegador.

Los ejercicios demo conservan una clave estable de tutor/demo_exercises.py. S-009
vincula sus respuestas y devoluciones grabadas con esa clave. Las claves
concretas ya existen, por ejemplo git-merge-v1 y prompts-v1, sin depender de
IDs locales de base de datos. Los ejercicios reales no se evaluarán con
casos demo de otro enunciado aunque compartan tema.

## Archivos que se crean o modifican

| Archivo | Cambio y motivo técnico |
| --- | --- |
| `tutor/models.py` | Añadir respuesta y retroalimentación sobre el ejercicio existente, evitando relaciones redundantes. |
| `tutor/migrations/0003_*.py` | Crear respuestas y devoluciones, dependiendo de 0002_practiceexercise. |
| `tutor/forms.py` | Validar contenido sin espacios vacíos y limitar tamaño. |
| `tutor/feedback.py` | Orquestar guardado, contexto vigente, proveedor, validación y alternativa demo. |
| `tutor/demo_feedback.py` | Casos explícitos por clave de ejercicio, respuesta y nivel de apoyo. |
| `tutor/feedback_providers.py` | Especializar GeminiTutorProvider mediante instructions y reutilizar transporte, configuración, 60 segundos y un intento. |
| `tutor/views.py` | Enviar respuestas y consultar resultados con permisos en cada petición. |
| `tutor/urls.py` | Rutas de respuesta y consulta individual. |
| `config/urls.py` | Incluir las nuevas rutas de tutor sin mover las rutas existentes de otras specs. |
| `tutor/test_feedback.py` | Verificar criterios, permisos, fallos y separación entre intentos sin aumentar tutor/tests.py. |
| `templates/tutor/practice.html` | Enlazar cada ejercicio propio con su formulario de respuesta. |
| `templates/tutor/exercise_answer.html` | Mostrar formulario, intentos y devolución del resultado seleccionado. |
| `README.md` | Documentar el recorrido y los casos demo disponibles. |
| `specs/S-009-retroalimentacion/plan.md` | Conservar decisiones, aprobación y ajustes reales. |
| `docs/registro-ia.md` | Declarar el uso real de IA de desarrollo. |
| `docs/plan.md` | Actualizar el estado real de S-009 al comenzar la implementación. |
| `specs/S-009-retroalimentacion/verificacion.md` | Registrar resultados locales identificados como tales, dejando pendiente la matriz independiente. |

docs/gasto.md solo se actualizará si se autoriza y realiza una llamada real;
no se inventará consumo de Gemini ni se cambiará .env para ejecutar pruebas.

## Cambios al modelo de datos

### ExerciseAnswer

- `id`: UUID generado por el servidor.
- `exercise`: relación con `PracticeExercise` y borrado en cascada.
- `content`: texto validado entre 1 y 4 000 caracteres después de quitar
  espacios de los extremos.
- `created_at`: fecha del intento.

El propietario se obtiene mediante `exercise.student`; el curso y tema
mediante `exercise.course` y `exercise.topic`. No se aceptan relaciones independientes
que permitan asignar la respuesta a otro estudiante.

### ExerciseFeedback

- `answer`: relación uno a uno con `ExerciseAnswer`, con borrado en cascada.
- `text`: explicación validada, máximo de 10 000 caracteres.
- `source`: valor restringido a `real` o `demo`.
- `created_at`: fecha de creación.

Cada nuevo envío válido crea un intento independiente; no sobrescribe
respuestas ni devoluciones anteriores. La ausencia de devolución no se
presenta como evaluación. La primera entrega no incorpora un reintento
automático de consultas fallidas: el estudiante puede enviar otro intento.

Usar related_name explícitos para consultar exercise.answers y answer.feedback.
Crear un índice sobre (exercise, created_at) para ordenar los intentos por
ejercicio. Restringir source a real/demo mediante choices y CheckConstraint.

Guardar la respuesta antes de llamar al proveedor y fuera de una
transacción que pudiera revertirla por un error externo. Persistir la
retroalimentación solamente después de validarla. No modificar `Grade`.

## Flujo, permisos y validación

1. Exigir sesión y rol estudiante; rechazar docentes. Resolver el ejercicio
   filtrando por propietario e inscripción vigente antes de registrar datos.
2. GET muestra el formulario o resultado, sin escribir ni llamar a IA.
3. POST mantiene CSRF y valida contenido. Un envío vacío o excesivo no
   registra respuesta ni consulta al proveedor.
4. Guardar el intento válido. Preparar el contexto con perfil y notas
   vigentes únicamente del propietario en el curso del ejercicio.
5. Consultar la integración compartida con ejercicio, respuesta y contexto.
   Reutilizar modelo configurable y límites vigentes; no fijar un modelo
   distinto por esta spec ni crear un segundo cliente de Gemini.
6. Solicitar JSON con assessment (aciertos o aspectos por mejorar) y
   guidance (orientación concreta). Analizarlo una sola vez dentro de un
   bloque de validación; exigir objeto, ambos textos no vacíos de hasta
   4 000 caracteres cada uno y un tamaño total de salida de hasta 12 000.
   Guardar ambos apartados como texto legible de hasta 10 000 caracteres.
   Rechazar HTML activo, tipos incorrectos y campos requeridos ausentes;
   ignorar metadatos extra que no se usen. Exigir español y trato formal
   en las instrucciones, sin imponer «usted» ni listas de palabras obligatorias.
   Complementar con revisión humana de CA-3 y CA-10 y casos «Defina»/«Revise».
   Evaluar solo requisitos explícitos del enunciado; reconocer los cumplidos
   y separar ampliaciones opcionales de errores. La nota orienta el apoyo,
   no demuestra por sí sola que una respuesta sea incorrecta.
7. Identificar el curso en la presentación a partir del ejercicio.
8. Revalidar permisos e inscripción antes de persistir o mostrar la devolución
   si cambiaron durante la llamada. Conservar el intento ya registrado.
9. Redirigir al resultado de ese UUID de respuesta para que actualizar
   la página no repita la consulta ni cree otro intento.

En toda consulta de resultados, volver a comprobar propietario e
inscripción vigente. Para IDs ajenos o inexistentes, responder sin revelar
su contenido. Rechazar campos extra de propietario, curso o tema en el POST.
Mostrar respuesta y devolución con escape automático de Django, sin
`safe`, interpretación de HTML ni ejecución de código.

## Modo demo y fallos

- En demo no construir el cliente externo ni exigir clave o red.
- Preparar casos para las 24 claves existentes de S-007: por clave, una
  respuesta correcta conocida y una incorrecta conocida, con devolución
  específica para cada una. Mostrar los ejemplos aplicables en la pantalla
  para que el recorrido grabado sea reproducible sin adivinar frases.
- Seleccionar un caso mediante la clave exacta del ejercicio y la respuesta
  conocida, normalizando solo mayúsculas y espacios. No usar coincidencias
  parciales que puedan convertir respuestas distintas en un mismo acierto.
- Incluir casos correctos e incorrectos con devoluciones específicas y
  variantes de apoyo para perfiles académicos distintos en un mismo tema.
- Para el apoyo, usar la nota vigente de ese tema recuperada mediante
  get_course_summaries: explicación paso a paso si es menor de 40 o no hay
  nota, y explicación breve a partir de 40. Este corte solo selecciona
  detalle pedagógico de grabaciones; no redefine temas débiles ni notas.
  Probar dos estudiantes del mismo tema con notas 25 y 55 y la misma
  respuesta conocida, para demostrar distinto apoyo sin mezclar perfiles.
- Ejemplo concreto para git-merge-v1:
  - Acierto: «Integro main en mi rama con git merge, resuelvo los conflictos,
    ejecuto las pruebas y después publico los cambios.»
  - Error: «Sobrescribo main y elimino el historial para evitar los conflictos.»
  - Explicar respectivamente la conservación del historial o el riesgo de
    pérdida, y orientar hacia revisión de conflictos y pruebas. No usar una
    devolución genérica compartida con SQL, redes u otros temas.
- Validar clave, curso, tema y enunciado contra el catálogo de S-007 antes
  de elegir grabaciones. Si falta la clave, se alteró el enunciado o no
  coincide exactamente la respuesta normalizada, conservar el intento e
  informar que no hay devolución aplicable. No inventar un acierto o error.
- Si una respuesta o ejercicio no tiene un caso aplicable, informar que
  no se pudo obtener devolución grabada, conservando el intento.
- Ante conexión fallida, tiempo agotado o cuota, intentar la alternativa
  demo aplicable e informar el cambio. No sustituir un ejercicio real por
  otro grabado para inventar una evaluación.
- Una respuesta del proveedor vacía o inválida no se guarda como
  retroalimentación. Mostrar un aviso y conservar la respuesta del alumno.

## Tareas en orden

1. Actualización de base realizada: main 914b8da y contrato PracticeExercise
   revisados; conservar el borrador previo y registrar esta adaptación.
2. Obtener aprobación del autor a estos detalles actualizados antes de código.
3. Incorporar modelos y migración dependiente del ejercicio existente.
4. Añadir formulario, guardado del intento y permisos de envío/consulta.
5. Preparar catálogo demo y servicio de retroalimentación.
6. Extender el proveedor compartido y validar su salida.
7. Incorporar presentación, navegación y redirección tras envío.
8. Ejecutar pruebas de aceptación y controles de Django.
9. Recorrer manualmente los casos de acierto, error, perfiles distintos,
   ausencia de caso demo y conservación de respuesta ante fallos.
10. Documentar uso, asistencia de IA y resultados reales. Solicitar la
    verificación independiente antes de declarar terminada la spec.

## Cómo se verificará cada criterio

| Criterio | Verificación prevista |
| --- | --- |
| CA-1 | Enviar respuesta propia y comprobar contenido, UUID y relaciones derivadas con estudiante, curso y tema. |
| CA-2 | Vacío y espacios: error de formulario, sin registro ni llamada externa. Probar también el límite de contenido. |
| CA-3 | Simular devolución estructurada; comprobar explicación ligada al enunciado y respuesta, con orientación concreta. |
| CA-4 | Dos perfiles en el mismo tema: contexto vigente y aislado, con variantes demo de apoyo distintas. |
| CA-5 | Crear varios ejercicios e intentos; consultar cada UUID y verificar que no intercambia resultados. |
| CA-6 | Anónimo, docente, ID ajeno/inexistente y pérdida de inscripción; sin escrituras ni llamadas. Manipular propietario y forzar comprobación CSRF. |
| CA-7 | Sin clave y cliente que falle si se construye: casos correctos e incorrectos muestran devoluciones locales pertinentes. Recorrido manual sin red. |
| CA-8 | Simular conexión, espera y cuota: caso aplicable usa demo con aviso; caso ausente conserva la respuesta sin inventar evaluación. |
| CA-9 | Salida vacía, tipo o estructura inválidos: no hay devolución persistida y sí respuesta conservada. |
| CA-10 | Revisar idioma, usted y curso; comprobar escape de contenido activo y que las notas oficiales no cambian. |

En tutor/test_feedback.py, cada prueba declara AI_MODE explícitamente y los
casos de proveedor real usan una clave sintética y mocks, incluyendo el
constructor/transporte cuando corresponda. Repetir la suite con clave externa
vacía para no depender de secretos del equipo ni producir llamadas reales.
Incluir aislamiento de ejercicio/respuesta ajenos, pérdida de inscripción
durante la consulta y rechazo de propietario manipulado. La vista usará
solo content y csrfmiddlewaretoken; campos de relación extra se rechazan.

Rutas propuestas:

- GET/POST `/practica/ejercicios/<uuid:exercise_id>/responder/`.
- GET `/practica/respuestas/<uuid:answer_id>/`.

Se conservará el ejercicio histórico aunque su tema haya dejado de ser
débil: S-009 valida propiedad e inscripción, sin volver a generar práctica
ni impedir consultar una respuesta por una corrección posterior de notas.

Después de integrar la base ejecutable, ejecutar con su configuración local:

```powershell
& ".\.venv\Scripts\python.exe" manage.py check
& ".\.venv\Scripts\python.exe" manage.py test tutor.test_feedback
& ".\.venv\Scripts\python.exe" manage.py test accounts academics tutor
& ".\.venv\Scripts\python.exe" manage.py makemigrations --check --dry-run
& ".\.venv\Scripts\python.exe" -m pip check
```

Estos comandos son controles previstos, no pruebas ejecutadas en este
worktree. No instalar dependencias sin preguntar. Las pruebas automatizadas
simulan IA; no equivalen a una respuesta real ni consumen cuota del producto.

## Correcciones humanas al plan del agente

- 2026-11-09: el usuario aclaró que S-007 y S-009 le corresponden y autorizó
  continuar tras presentar la propuesta técnica compartida.
- No indicó correcciones específicas a modelos, límites o archivos.
- El verificador previsto sigue siendo Brayan11Hernandez; no se registra
  aprobación suya ni ejecución independiente de criterios.
- En la sesión actual el autor recordó trabajar en la rama S-009 y
  autorizó resguardar los dos documentos locales, incorporar main y
  adaptar esta propuesta a PracticeExercise y a los componentes disponibles.
  Esa primera autorización fue documental. Posteriormente aprobó el plan
  actualizado, incluidos modelos, catálogo, límites, archivos y pruebas,
  mediante «si, autorizo» después del resumen de la propuesta.

## Entregas revisables

1. Plan actualizado y contrato confirmado, sin código funcional.
2. Modelos, migración y permisos/formulario, con pruebas pertinentes.
3. Catálogo demo y servicio/proveedores con validación y pruebas de fallos.
4. Vistas, rutas, navegación y pruebas HTTP.
5. Documentación, recorrido local y evidencia para la revisión independiente.

Dividir los bloques en PRs de tamaño revisable cercano a 400 líneas
(excluyendo datos/migraciones generadas), según el diff real. La referencia
al issue es #13; el PR final usará Closes #13 tras completar la verificación.
No se crearán commits ni PRs sin solicitud del autor.

### Desviación de tamaño y propuesta de excepción

La entrega real agrupó los cinco bloques en el PR #60, en vez de separarlos
como estaba previsto. Esto es una desviación del plan, aunque haya varios
commits. El 11-11-2026 Jeffersson autorizó documentar la corrección y una
justificación de excepción; no se atribuye aceptación de esa excepción a Brayan.

Se propone conservar el PR para mantener trazabilidad con la verificación de
360da36 y evitar reescribir la rama compartida. La revisión puede seguir los
bloques anteriores y sus commits: modelos/permisos, servicio/proveedor,
catálogo de datos demo, interfaz, pruebas y documentación. No equivale a
cumplir el tamaño previsto: Brayan debe aceptar expresamente esta excepción
o solicitar entregas separadas antes de aprobar.

## Ejecución y evidencia

Se conservaron el borrador y su registro; se actualizó la rama desde main
y se adaptó esta propuesta al contrato implementado. Se resolvió el conflicto
de restauración en registro-ia.md conservando el historial de main y la
entrada local de S-009. El stash de resguardo permanece disponible.
Tras aprobar el autor la propuesta actualizada, se implementaron los modelos,
la migración 0003, catálogo demo, proveedores, servicio, formularios y pantallas.
Se ejecutaron 27 pruebas específicas y 244 de regresión, ambas suites OK con
clave externa vacía, además de check, revisión de migraciones y pip check.
El recorrido HTTP demo en el puerto 8002 comprobó acierto/error e intentos
separados en una base sintética temporal. No se consultó Gemini real.
Los resultados locales se registran en verificacion.md, sin completar la
matriz independiente en nombre de Brayan. La lectura y ejecución del autor y
la verificación ajena siguen pendientes de cierre. Posteriormente se crearon
los commits de entrega hasta 360da36 y se abrió el PR #60.

### Corrección autorizada tras el informe de Brayan · 11-11-2026

Jeffersson Daniel Ramos trasladó el informe de Brayan Hernández y aprobó
la estructura y el ajuste pedagógico mediante «si, apruebo. adelante con todo».
Se refuerzan las instrucciones del proveedor sin cambiar el contrato, modelos,
spec ni transporte. Se amplía la prueba existente de transporte para comprobar
que esas reglas llegan al cliente Gemini. Una simulación no acredita la calidad
de una futura devolución real: CA-3 y CA-10 requieren revisión humana posterior.
Las capturas, evidencia original, costo y lectura final del autor siguen
pendientes de confirmación; no se registra aprobación de Brayan.

La corrección pasó 27 pruebas específicas y 244 de regresión con Python
3.12.10 y Gemini simulado; check, migraciones pendientes y pip check también
correctos. Comandos, duraciones y alcance en verificacion.md. Estos resultados
corresponden a cambios locales sobre 360da36, sin commit de corrección todavía.
