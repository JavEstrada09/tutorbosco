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
| CA-6 | Pruebas simuladas de configuración ausente o inválida, conexión, `429`, `504` y respuesta inválida. | Cumple localmente. | Mensajes en español sin detalles internos, límite total de 15 segundos, un solo intento y continuación demo sin Gemini. |
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
solo intento con límite total de 15 segundos. Una prueba de regresión confirma
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
Computadora: pendiente de registrar.
Commit probado: pendiente de crear y registrar.

| Criterio | Resultado de Douglas | Evidencia |
| --- | --- | --- |
| CA-1 | Pendiente. | Pendiente. |
| CA-2 | Pendiente. | Pendiente. |
| CA-3 | Pendiente. | Pendiente. |
| CA-4 | Pendiente. | Pendiente. |
| CA-5 | Pendiente. | Pendiente. |
| CA-6 | Pendiente. | Pendiente. |
| CA-7 | Pendiente. | Pendiente. |

S-001 no está terminada. Faltan el commit de Entrega 4, la prueba de Douglas
en su computadora, la evidencia independiente, la revisión del PR y la fusión.
