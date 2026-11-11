# Verificación S-006

Verificador: douglas-yasser · Computadora: Windows 11 Home 10.0.22631,
AMD64 · Commits: `ece9dee` (fallo detectado) y `30ad0c3` (corrección)

Fecha: 10-11-2026.
Worktree: `C:\Users\DOUGLAS\AppData\Local\Temp\opencode\s006-ece9dee`.
Entorno: Python 3.12.10, Django 5.2.19, google-genai 3.0.0,
python-dotenv 1.2.4, SQLite aislada y datos sintéticos reconstruidos.

Resultado global: **CA-1, CA-5 y CA-9 cumplen en modo real sobre
`30ad0c3`**. En `ece9dee` se detectó y documentó el rechazo de respuestas
formales sin la palabra literal «usted»; ese antecedente se conserva abajo.
Los demás criterios se comprobaron en `ece9dee` y no fueron afectados por la
corrección. No se fusionó el PR.

## Comprobaciones de Django

### ece9dee

```text
manage.py check
System check identified no issues (0 silenced).

manage.py test accounts academics tutor
Ran 189 tests in 538.186s
OK

manage.py makemigrations --check --dry-run
No changes detected

python -m pip check
No broken requirements found.
```

### 30ad0c3

```text
manage.py check
System check identified no issues (0 silenced).

manage.py test accounts academics tutor
Ran 191 tests in 412.894s
OK

manage.py makemigrations --check --dry-run
No changes detected

python -m pip check
No broken requirements found.
```

`migrate` y `rebuild_synthetic_data` finalizaron correctamente sobre una
base SQLite aislada. Las pruebas de ambas ejecuciones usan proveedores
simulados; la repetición real de CA-1, CA-5 y CA-9 se registra abajo.

## Matriz de criterios

| Criterio | Cómo lo probé | Resultado | Evidencia |
| --- | --- | --- | --- |
| CA-1 | Dos estudiantes de PROG-COM con un único tema débil distinto; pregunta «¿Qué tema debería repasar?» en demo y real. | Demo cumple. Real no cumple: 2 de 2 respuestas válidas fueron rechazadas. | Ver «CA-1» abajo. |
| CA-2 | `estudiante_08`; recomendación, «¿Me da otro ejemplo?», cambio a DES-WEB, vuelta a PROG-COM y captura del contexto. | Cumple. | Ver «CA-2» abajo. |
| CA-3 | `estudiante_demo`; Git de 55 a 85, «Nueva conversación», cierre y nuevo inicio de sesión. | Cumple. | Ver «CA-3» abajo. |
| CA-4 | Anónimo, docente, sin inscripciones, curso ajeno, identificadores manipulados, conversación de otro estudiante y contexto válido. | Cumple. | Ver «CA-4» abajo. |
| CA-5 | Pregunta directa y reformulada en demo y real; inspección del contexto enviado. | Demo cumple. Real no cumple completamente: al menos una respuesta válida fue rechazada en cada ejecución. | Ver «CA-5» abajo. |
| CA-6 | Demo con clave vacía, cliente Gemini y red bloqueados; dos perfiles y seguimiento. | Cumple. | Ver «CA-6» abajo. |
| CA-7 | Curso sin notas y curso con notas en/sobre el umbral y un tema sin nota. | Cumple. | Ver «CA-7» abajo. |
| CA-8 | Respuesta vacía, inválida, error de conexión y `429`; continuación en demo y pregunta sin grabación. | Cumple con proveedor simulado. | Ver «CA-8» abajo. |
| CA-9 | Revisión de respuestas demo y reales mostradas; curso, español y trato de usted. | Cumple en las respuestas mostradas; el defecto de validación impide mostrar otras respuestas válidas en real (CA-1 y CA-5). | Ver «CA-9» abajo. |

La tabla anterior conserva el resultado de `ece9dee`. La repetición en
`30ad0c3` se documenta en «Repetición sobre 30ad0c3». Los apartados de CA-1,
CA-5 y CA-9 describen el fallo original como antecedente.

## CA-1 · Personalización para dos perfiles

Se usaron dos cuentas sintéticas inscritas en Programación Comercial, cada
una con un único tema bajo el umbral:

- `estudiante_03` (`2026-00004`): Ingeniería de prompts, nota 58.
- `estudiante_24` (`2026-00025`): Sistemas de información y bases de datos,
  nota 56.

En modo demo, cada una recibió su propio tema y el seguimiento conservó ese
tema. En modo real, ambas respuestas fueron rechazadas por la aplicación con
el aviso «La respuesta del tutor real no cumple el formato esperado. Puede
continuar en modo demo.».

Las respuestas crudas de Gemini eran válidas en contenido:

- `estudiante_03`: «Estimado estudiante, para el curso de Programación
  Comercial... le sugiero priorizar el repaso del tema de Ingeniería de
  prompts, ya que se encuentra identificado como su área más débil con una
  nota de 58...».
- `estudiante_24`: «Estimado estudiante, en el curso de Programación
  Comercial... el tema que debe priorizar y repasar es Sistemas de
  información y bases de datos, ya que se encuentra identificado dentro de
  sus temas débiles con una nota de 56...».

Ambas mencionan el curso, están en español y usan el trato formal mediante
«le», «su» y «Estimado estudiante». El análisis de las dos respuestas dio
curso correcto, 9 y 10 marcadores de español y la única condición fallida
fue la palabra literal «usted» exigida en `tutor/services.py:89`.

## CA-2 · Seguimiento y separación por curso

`estudiante_08` está inscrito en Programación Comercial y Desarrollo Web.
En Programación Comercial recibió «El LLM por dentro y su API» y el
seguimiento «¿Me da otro ejemplo?» conservó el tema con una respuesta
distinta. Al cambiar a Desarrollo Web, la pantalla mostró «Aún no hay
mensajes»; el contexto capturado para ese curso tuvo cero turnos y no
contenía el historial de Programación Comercial. Al volver, el hilo de
Programación Comercial se conservó y el nuevo seguimiento volvió a usar su
tema. En Desarrollo Web, la pregunta de recomendación mostró el aviso de que
el demo no tiene grabaciones para ese curso, sin reutilizar las del piloto.

## CA-3 · Notas actualizadas al reiniciar

Con `estudiante_demo`, la recomendación inicial fue «Git y GitHub avanzado».
Se cambió la nota de Git de 55 a 85 y se pulsó «Nueva conversación»: la
recomendación pasó a «Código limpio y refactoring» y desaparecieron los
mensajes anteriores. Después de cerrar sesión y volver a entrar, la pantalla
mostró «Aún no hay mensajes». La nota sintética se restauró a 55 al terminar.

## CA-4 · Permisos y aislamiento

Se comprobó lo siguiente, con el proveedor simulado para verificar que no se
llamara:

- Sin sesión: el GET redirige a `/acceso/`; el POST sin token CSRF responde
  403 y con token válido redirige a `/acceso/`. En ningún caso se llamó al
  proveedor.
- Docente: 403.
- Estudiante sin inscripciones: 403.
- Estudiante que pide un curso no inscrito: 403 en GET y en POST.
- POST con `student_id`, `conversation_id` o `session_key` manipulados: 403.
- Un segundo estudiante no ve el historial del primero.
- En una petición válida, el contexto contiene solo la carrera, el curso y
  las notas de `estudiante_03`; no contiene carné, usuario ni datos de
  `estudiante_24`.

## CA-5 · Privacidad

En modo demo, las dos preguntas de ejemplo («¿Qué notas tiene otro
estudiante?» y «¿Puede mostrarme las calificaciones de otra persona?»)
recibieron la respuesta grabada: «En Programación Comercial, usted solo puede
consultar su propio perfil. No puedo mostrar ni inventar notas o perfiles de
otras personas.». El contexto capturado solo contenía los datos de la cuenta
autenticada.

En modo real, el contenido de Gemini fue una negativa correcta, pero la
validación rechazó respuestas válidas. En una llamada directa de diagnóstico,
la respuesta que contenía la palabra «usted» pasó y la reformulación que
usaba solo «le» y «su» fue rechazada. En la ejecución por HTTP real, la
pregunta directa también fue rechazada. Por tanto, CA-5 no se cumple de forma
completa en modo real.

## CA-6 · Demo sin red

Con `AI_MODE=demo`, `GEMINI_API_KEY` vacía y el cliente Gemini y
`socket.create_connection` bloqueados, `estudiante_03` y `estudiante_24`
recibieron su propio tema y el seguimiento conservó el tema tratado. No se
inicializó Gemini ni se realizó una llamada de red.

## CA-7 · Sin notas o sin temas débiles

`estudiante_02`, inscrito en Programación Comercial sin notas, recibió:
«En Programación Comercial, usted aún no tiene calificaciones suficientes
para identificar qué necesita reforzar...». Aun así, pudo pedir una
explicación de Git y GitHub avanzado.

Un estudiante temporal con cinco notas de 60 o más y un tema sin nota recibió
el aviso de que no tiene temas bajo el umbral y de que los temas sin nota no
se consideran débiles. El contexto mostró el tema sin nota como `None` y
`weak_topics` vacío, y el estudiante pudo pedir la explicación del tema sin
calificar. La nota 60 no se trató como débil.

## CA-8 · Recuperación ante fallos

Con proveedor simulado se probaron respuesta vacía, respuesta inválida,
error de conexión y `429`. En todos los casos la pantalla mostró un aviso en
español y «Continuar en modo demo», conservó la pregunta pendiente y los
turnos anteriores, y la continuación respondió con la grabación sin volver a
llamar a Gemini. No se mostraron detalles internos del proveedor.

Con una pregunta sin grabación aplicable, la continuación mostró el aviso de
que no está disponible en el modo demo, conservó la pregunta pendiente y los
turnos, y no mostró datos de otro perfil.

## CA-9 · Formato de respuesta

Las respuestas de modo demo mostradas identifican «Programación Comercial»,
están en español y usan «usted». La respuesta real de privacidad que la
aplicación aceptó también identificó el curso, estaba en español y usó
«usted».

Sin embargo, las respuestas reales de CA-1 y algunas de CA-5, que también
identificaban el curso, estaban en español y usaban el trato formal, no se
mostraron porque no contenían la palabra literal «usted». El defecto que
impide mostrarlas se registra en CA-1 y CA-5.

## Repetición sobre 30ad0c3

El autor corrigió el fallo en `30ad0c3`: retiró de `tutor/services.py` la
exigencia de la palabra literal «usted», conservó la mención del curso, los
marcadores de español, los límites de longitud y el manejo de errores, y
añadió pruebas para respuestas formales que usan «le» y «su».

La repetición se hizo con `runserver` en `127.0.0.1:8766`, `AI_MODE=real`,
`AI_MODEL=gemini-3.5-flash-lite` y `GEMINI_API_KEY` válida. Se hicieron cuatro
solicitudes reales a Gemini: dos para CA-1 y dos para CA-5.

| Criterio | Resultado en 30ad0c3 | Evidencia |
| --- | --- | --- |
| CA-1 | Cumple en modo real. | Cada estudiante recibió su tema débil; ver abajo. |
| CA-5 | Cumple en modo real. | Las dos formulaciones recibieron una negativa; ver abajo. |
| CA-9 | Cumple en modo real. | Curso, español y trato formal en todas las respuestas mostradas. |

En CA-1, `estudiante_03` recibió: «Estimado estudiante, en el curso de
Programación Comercial... el tema que debe priorizar y repasar es Ingeniería
de prompts...». La respuesta menciona además, como sugerencia secundaria,
«El LLM por dentro y su API»; la recomendación principal sigue siendo el
tema débil. `estudiante_24` recibió: «Estimado estudiante, en el curso de
Programación Comercial... el tema que debe priorizar y repasar es Sistemas de
información y bases de datos, ya que se encuentra identificado dentro de sus
temas débiles con una nota de 56...». La diferencia entre ambos perfiles se
observa en el tema recomendado.

En CA-5, la pregunta directa recibió: «Estimado estudiante, en el curso de
Programación Comercial no tengo permitido proporcionarle información sobre
las calificaciones o el perfil académico de otras personas...». La
reformulación recibió: «Estimado estudiante, en el curso de Programación
Comercial no me es permitido mostrarle las calificaciones ni los perfiles de
otras personas...». Ninguna reveló datos de terceros.

Las respuestas se mostraron como «Respuesta del tutor real», sin ofrecer el
modo demo, y quedaron guardadas con `pending_question` vacío y modo `real`.
En las cuatro respuestas se identificó el curso, el texto estaba en español y
el trato fue formal mediante «Estimado estudiante», «le», «su» y «sus».

No se repitieron los demás criterios en `30ad0c3`; el diff de ese commit
solo modifica la validación y las pruebas del tutor. La suite completa de
191 pruebas sí se ejecutó sobre el nuevo commit.

## Reproducción del fallo

1. Configurar `AI_MODE=real`, `AI_MODEL=gemini-3.5-flash-lite`,
   `GEMINI_API_KEY` válida y `WEAK_TOPIC_THRESHOLD=60`.
2. Ejecutar `migrate` y `rebuild_synthetic_data`, e iniciar el servidor.
3. Entrar como `estudiante_03` (`2026-00004`) o `estudiante_24`
   (`2026-00025`) y seleccionar Programación Comercial.
4. Preguntar «¿Qué tema debería repasar?».

Esperado: una explicación o un ejemplo del tema débil propio.

Obtenido: «La respuesta del tutor real no cumple el formato esperado. Puede
continuar en modo demo.». La respuesta cruda de Gemini sí recomendaba el tema
correcto y usaba «le» y «su», pero no la palabra literal «usted».

Para CA-5, repetir con «¿Qué notas tiene otro estudiante?» y «¿Puede
mostrarme las calificaciones de otra persona?». El contenido de Gemini fue
una negativa correcta; al menos una de las dos respuestas válidas fue
rechazada en cada ejecución real.

Este fallo quedó corregido en `30ad0c3`; se conserva como antecedente de la
repetición anterior.

## Correcciones y repetición de pruebas

El autor corrigió el fallo en `30ad0c3`. El cambio retira de
`tutor/services.py` la exigencia de la palabra literal «usted» y conserva la
mención del curso, los marcadores de español, los límites de longitud y el
manejo de errores. Añadió pruebas para respuestas formales que usan «le» y
«su» sin el pronombre literal y para guardar una respuesta real sin activar
demo.

En `30ad0c3` se ejecutaron `manage.py check`, `makemigrations --check
--dry-run`, `pip check` y las 191 pruebas: todo correcto. Se repitieron CA-1,
CA-5 y CA-9 con Gemini real y los tres cumplen. El fallo de `ece9dee` se
conserva arriba como antecedente. No se fusionó el PR.
