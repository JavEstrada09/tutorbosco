# Verificación S-001 — Esqueleto funcional

Autor que realizó la comprobación local: JavEstrada09.
Computadora del autor: Windows, Python 3.12.10.
Estado del código probado: cambios sin commit sobre `ff4c8f0`.
Verificador independiente asignado: douglas-yasser.

Este documento separa la comprobación local del autor de la verificación
independiente. Los resultados de Douglas no se registrarán hasta que ejecute
los siete criterios en su computadora sobre un commit identificado.

## Comprobación local del autor

Fecha: 08-11-2026.

| Criterio | Cómo se comprobó | Resultado local | Evidencia |
| --- | --- | --- | --- |
| CA-1 | Pruebas de autenticación y recorrido HTTP aislado con la cuenta creada por `rebuild_synthetic_data`. | Cumple localmente. | Inicio de sesión HTTP redirigió a la pantalla protegida; la suite completa pasó. |
| CA-2 | Pruebas con contraseña incorrecta, usuario inexistente y protección CSRF. | Cumple localmente. | Ambos errores conservan a la persona sin autenticar y muestran el mismo mensaje seguro. |
| CA-3 | Pruebas de cuenta autenticada, dato propio, perfil, inscripción, cuenta administrativa y acceso anónimo. | Cumple localmente. | La suite comprueba aislamiento y el recorrido aislado mostró la carrera sintética esperada. |
| CA-4 | Antecedente real del autor con dos respuestas en la interfaz; no se realizó otra consulta en Entrega 4. | Comprobado previamente por el autor; pendiente de Douglas. | `docs/registro-ia.md`: respuesta sobre variables y cálculo correcto de Q75 con `gemini-3.8-flash`. |
| CA-5 | Recorrido HTTP con `AI_MODE=demo`, clave vacía y bloqueos simulados de red y constructor Gemini. | Cumple localmente. | Se mostró la respuesta grabada identificada como demo; ambos mocks quedaron sin llamadas. |
| CA-6 | Pruebas simuladas de configuración ausente o inválida, conexión, `429`, `504` y respuesta inválida. | Cumple localmente. | Mensajes en español sin detalles internos, límite total de 60 segundos, un solo intento y continuación demo sin Gemini. |
| CA-7 | Entorno virtual temporal nuevo, instalación de `requirements.txt`, base SQLite aislada, migraciones, datos, suite y recorrido demo. | Cumple localmente. | 48 pruebas superadas y recorrido aislado completo sin red ni Gemini. |

## Comandos y resultados del autor

Los valores de `DJANGO_SECRET_KEY` y `DEMO_STUDENT_PASSWORD` se generaron
solo en memoria y no se mostraron ni registraron. La clave de Gemini permaneció
vacía durante el recorrido demo.

| Comando o paso | Resultado real |
| --- | --- |
| `py -3.12 -m venv <directorio-temporal>` | Correcto; Python 3.12.10. |
| `<python-temporal> -m pip install -r requirements.txt` | Correcto; se instalaron únicamente las versiones fijadas. |
| `<python-temporal> manage.py migrate --noinput` | Correcto; se aplicaron todas las migraciones en la base aislada. |
| `<python-temporal> manage.py rebuild_synthetic_data` | Correcto; datos mínimos reconstruidos. |
| `<python-temporal> manage.py check` | Sin problemas. |
| `<python-temporal> manage.py test accounts academics tutor` | 48 pruebas superadas en 40.918 s. |
| `<python-temporal> manage.py makemigrations --check --dry-run` | No se detectaron cambios. |
| `<python-temporal> -m pip check` | No se detectaron dependencias incompatibles. |
| Recorrido HTTP demo con cliente Django y CSRF activo | Acceso, carrera y respuesta grabada correctos; sin llamadas a Gemini ni a red. |

La suite se repitió en el entorno habitual después de corregir la política:
49 pruebas superadas en 16.570 s. `check`,
`makemigrations --check --dry-run` y `pip check` finalizaron
correctamente.

## Correcciones durante la comprobación

El primer intento de automatizar el recorrido aislado aplicó correctamente
las migraciones, reconstruyó los datos y superó `check`, pero PowerShell
dividió el código de `manage.py shell` por sus comillas internas. Se corrigió
el comando pasando el código como un único argumento. La repetición completó
el recorrido; no se modificó el producto por este error de ejecución.

La revisión posterior corrigió la política inicial de dos intentos de 15
segundos. El SDK incluía `429` entre sus estados reintentables y podía registrar
la excepción completa antes del segundo intento. La política corregida usa un
solo intento con límite total de 60 segundos. Una prueba de regresión confirma
una sola llamada, ausencia de registro propio y continuidad mediante modo demo.

## Evidencia actualizada de la Entrega 4

- **CA-4.** JavEstrada09 comprobó en el navegador que Gemini 3.5 Flash-Lite
  (`gemini-3.5-flash-lite`) respondió en modo real en el puerto 8001. El tutor
  explicó en español y con trato de usted un descuento de Q10 sobre Q100 y
  calculó correctamente un total de Q90.
- **CA-6.** Después de un fallo del proveedor, la interfaz ofreció continuar
  en modo demo y mostró la respuesta grabada con su etiqueta. La política
  vigente cancela la consulta al vencer el plazo total de 60 segundos y
  permite un único intento.
- **Suite actualizada.** En Windows pasaron 50 pruebas de `accounts`,
  `academics` y `tutor` en 28.321 segundos.

Estos resultados corresponden a la comprobación local del autor.

## Verificación independiente de Douglas

Verificador: douglas-yasser.
Computadora: Douglas, Windows 11 (NT 10.0.22631), Python 3.12.10 y 3.13.14.
Commit probado: `eb01cc7`.
Fecha: 09-11-2026.

La comprobación se ejecutó en un worktree aislado sobre una base SQLite nueva.
La instalación limpia y el recorrido demo se repitieron con Python 3.12.10,
la versión exigida por el README. La ejecución inicial con Python 3.13.14 se
conserva como evidencia adicional. Los valores de `DJANGO_SECRET_KEY`,
`DEMO_STUDENT_PASSWORD` y `GEMINI_API_KEY` se cargaron en memoria y no se
mostraron ni se versionaron.

| Criterio | Cómo lo probé | Resultado | Evidencia |
| --- | --- | --- | --- |
| CA-1 | `runserver` en 127.0.0.1:8011 con base SQLite aislada, cliente HTTP con CSRF y la cuenta `estudiante_demo`. | Cumple. | El POST a `/acceso/` respondió 302 a `/`; la pantalla mostró la carrera `Ingeniería en Sistemas` y el curso `Programación Comercial`. |
| CA-2 | Intentos con contraseña incorrecta y usuario inexistente; POST de acceso sin token CSRF. | Cumple. | Ambos casos devolvieron 200 sin sesión y el mismo mensaje `Las credenciales ingresadas no son válidas.`; el POST sin token respondió 403. |
| CA-3 | Segundo estudiante sintético con carrera distinta e inscripción en `PROG-COM`; acceso anónimo a `/`. | Cumple. | El segundo estudiante vio únicamente `Carrera Ajena Verificación`; el acceso anónimo redirigió a `/acceso/?next=/`. |
| CA-4 | `runserver` en 127.0.0.1:8012 con `AI_MODE=real`, `AI_MODEL=gemini-3.5-flash-lite` y la clave local, sin mostrarla; POST de la pregunta demo con CSRF. | Cumple. | Respuesta real mostrada como `Respuesta del tutor real` en 4.12 s, en español, con trato de usted y mención de `Programación Comercial`; sin alertas. |
| CA-5 | Cliente HTTP aislado de Django con `AI_MODE=demo`, `GEMINI_API_KEY` vacía y bloqueo de `socket.connect` y del constructor Gemini; recorrido demo adicional con `runserver`. | Cumple. | La pantalla mostró `Modo demo`, `Respuesta grabada del modo demo` y el texto grabado con trato de usted; los bloqueos no se activaron. |
| CA-6 | Cliente HTTP aislado con `AI_MODE=real` y clave vacía; después, POST de `continue_in_demo=1` con la red bloqueada. | Cumple. | Mensaje seguro `El tutor real no está configurado. Puede continuar en modo demo.`, sin traza ni detalles técnicos; la continuación mostró la respuesta grabada. |
| CA-7 | Entorno virtual nuevo con Python 3.12.10, instalación de `requirements.txt`, base SQLite temporal, `migrate`, `rebuild_synthetic_data`, `check`, suite, `makemigrations --check --dry-run`, `pip check` y recorrido demo con `runserver`. | Cumple. | Instalación y migraciones correctas; 50 pruebas superadas en 91.695 s con Python 3.12.10; sin cambios de migración; `pip check` limpio; recorrido demo completo. La ejecución con Python 3.13.14 se conserva como evidencia adicional. |

## Comandos y resultados de Douglas

| Comando o paso | Resultado real |
| --- | --- |
| `python3.12 -m venv <directorio-temporal>` | Correcto; Python 3.12.10. |
| `-m pip install -r requirements.txt` en el entorno nuevo | Correcto; se instalaron las versiones fijadas. |
| `manage.py migrate --noinput` sobre base temporal | Correcto; se aplicaron todas las migraciones. |
| `manage.py rebuild_synthetic_data` | Correcto; datos mínimos reconstruidos. |
| `manage.py check` | Sin problemas. |
| `manage.py test accounts academics tutor` | 50 pruebas superadas en 91.695 s con Python 3.12.10 y en 79.036 s con Python 3.13.14. |
| `manage.py makemigrations --check --dry-run` | No se detectaron cambios. |
| `-m pip check` en ambos entornos | No se detectaron dependencias incompatibles. |
| Recorrido demo con `runserver` y cliente HTTP con CSRF | Acceso, carrera, curso y respuesta grabada correctos; sin llamadas a Gemini ni a red. |
| Recorrido real con `runserver` y `gemini-3.5-flash-lite` | Respuesta real en 4.12 s, sin alertas y con el curso identificado. |

## Hallazgos y repeticiones de Douglas

- **CA-4 con `gemini-3.8-flash`.** El `.env` local tenía `AI_MODEL=gemini-3.8-flash`.
  Dos consultas reales fallaron: una agotó el plazo total de 60 segundos en
  62.464 s con `TutorUnavailableError` y otra devolvió el error genérico del
  proveedor en 4.676 s. Un diagnóstico directo confirmó `504 DEADLINE_EXCEEDED`.
  La repetición con el modelo documentado `gemini-3.5-flash-lite` respondió
  correctamente en 4.531 s desde el servicio y en 4.12 s desde la interfaz.
  El `.env` local se alineó a `AI_MODEL=gemini-3.5-flash-lite` después de esta
  comprobación.
- **CA-7 con Python 3.12.10.** Se repitió la instalación limpia y el recorrido
  demo con la versión exigida por el README: 50 pruebas superadas en 91.695 s
  y recorrido demo completo con `runserver`. La ejecución con Python 3.13.14
  queda como evidencia adicional.
- **Preparación de CA-3.** El primer intento creó el segundo estudiante sin
  inscripción y la aplicación respondió 403. Se corrigió el dato de prueba
  inscribiéndolo en `PROG-COM`; no fue un defecto del producto.

La verificación independiente de los siete criterios quedó completa sobre
`eb01cc7`, con la instalación limpia en Python 3.12.10 y la evidencia adicional
de Python 3.13.14. El PR final #38 se fusionó a `main` en `febd35c` y cerró
el issue #4.

## Comprobación técnica de `main`

El 09-11-2026, Codex ejecutó `febd35c` en un entorno Linux aislado con
Python 3.12.14 y una base SQLite nueva. Las migraciones y la reconstrucción
se completaron. `check`, `makemigrations --check --dry-run` y `pip check`
terminaron sin incidencias. Pasaron las 55 pruebas de `accounts`, `academics`
y `tutor`. Un cliente HTTP de Django confirmó el inicio de sesión con CSRF,
la carrera del estudiante y la respuesta grabada con la red y Gemini
bloqueados.
