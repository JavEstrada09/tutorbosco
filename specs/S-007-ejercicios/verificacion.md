# Verificación S-007

Estado: suites repetidas sin fallos en la corrección del autor y capturas
obtenidas sobre el nuevo commit; decisión de aprobación pendiente.
Verificador: Brayan Hernández / Brayan11Hernandez.
Computadora: Windows · Python 3.12.10 · Microsoft Edge 157.0.4341.42.
Commits probados: `a6bd399ea1f33394b526c131e6cfba94e9e71e62` (reporte
original con fallos) y `8a7a72c7a4ea95097d45ab270ae64b7a6fff8375`
(repetición correcta de las suites y capturas).

| Criterio | Cómo lo probé | Resultado | Evidencia |
| --- | --- | --- | --- |
| CA-1 | Caso aislado con 45, 59, 60 y 85; umbral 60. | Cumple en la comprobación independiente. | `evidencia/brayan-resultados.md` y `evidencia/brayan-pruebas.txt` |
| CA-2 | Caso aislado con 60, 69 y 70; umbral efectivo 70. | Cumple en la comprobación independiente. | `evidencia/brayan-resultados.md` y `evidencia/brayan-pruebas.txt` |
| CA-3 | Dos temas sin nota y temas bajo el umbral. | Cumple; las notas ausentes no se trataron como cero. | `evidencia/brayan-resultados.md` y `evidencia/brayan-pruebas.txt` |
| CA-4 | Proveedor simulado instrumentado y recorrido demo real en Edge. | Cumple automática y visualmente en modo demo; Gemini real independiente fue omitido. | `evidencia/brayan-resultados.md`, `evidencia/brayan-http.txt` y `evidencia/capturas/ca-4-practica-demo.png` |
| CA-5 | Sin temas débiles y sin notas, con proveedores instrumentados. | Cumple; avisos distintos, sin botón y cero llamadas. | `evidencia/brayan-resultados.md`, `evidencia/brayan-http.txt` y `evidencia/capturas/ca-5-*.png` |
| CA-6 | Práctica antes y después de corregir 45/80 a 60/40. | Cumple; cambió la selección nueva y se conservó el UUID histórico. | `evidencia/brayan-resultados.md`, `evidencia/brayan-http.txt` y `evidencia/capturas/ca-6-*.png` |
| CA-7 | Anónimo, docente, curso y UUID ajenos, campo manipulado, CSRF y contexto. | Cumple automática y visualmente; los rechazos no revelaron datos. | `evidencia/brayan-resultados.md`, `evidencia/brayan-pruebas.txt` y `evidencia/capturas/ca-7-*.png` |
| CA-8 | Dos perfiles, demo sin clave y cliente Gemini instrumentado. | Cumple; ejercicios distintos, cero cliente Gemini y recursos locales. | `evidencia/brayan-resultados.md`, `evidencia/brayan-http.txt` y `evidencia/capturas/ca-8-*.png` |
| CA-9 | Conexión y 429 simulados; salidas inválidas y catálogo ausente. | Cumple en casos independientes; no se provocaron fallos reales. | `evidencia/brayan-resultados.md` y `evidencia/brayan-pruebas.txt` |
| CA-10 | UUID, relaciones, español formal, escape y notas antes/después. | Cumple automática y visualmente. | `evidencia/brayan-resultados.md`, `evidencia/brayan-http.txt` y `evidencia/capturas/ca-10-uuid-y-usted.png` |

## Verificación independiente de Brayan · 2026-11-10

Brayan Hernández, usuario GitHub `Brayan11Hernandez`, ejecutó la verificación
en su computadora Windows sobre el commit exacto entregado. Se utilizó Python
3.12.10, el entorno virtual existente y una base SQLite aislada en el
directorio temporal local. La base se creó desde cero, recibió todas las
migraciones y se reconstruyó únicamente con datos sintéticos.

La configuración del recorrido usó `AI_MODE=demo`, modelo efectivo
`gemini-3.5-flash-lite` y clave Gemini vacía. Las contraseñas demo se generaron
y guardaron localmente sin mostrarlas. No se instalaron paquetes, navegadores
ni herramientas adicionales.

### Pruebas automatizadas solicitadas

- `manage.py check`: OK, sin problemas.
- `manage.py test tutor.test_exercises --verbosity 2`: **falló**; 19 pruebas,
  2 fallos y 14 errores en 0.265 segundos.
- `manage.py test accounts academics tutor --noinput`: **falló**; 215
  pruebas, los mismos 2 fallos y 14 errores, sin fallos adicionales, en
  110.798 segundos.
- `manage.py makemigrations --check --dry-run`: OK, sin cambios.
- `python -m pip check`: OK, sin dependencias incompatibles.

No hubo timeout. La repetición dirigida de
`test_valid_real_response_and_private_context_ca4_ca7`, incluso iniciando el
proceso con `AI_MODE=real`, produjo el mismo error porque el proveedor Gemini
simulado no fue invocado.

### Causa reproducida y corrección solicitada

`PracticeTests` aplica `override_settings(AI_MODE="demo")` a toda la clase.
Los métodos que intentan probar modo real no consiguen sustituir ese modo en
la ejecución entregada. Además, varios de esos métodos parchean
`GeminiExerciseProvider.generate` sin configurar una clave sintética; el
constructor valida la clave antes de llegar al método parcheado y activa la
alternativa demo.

Esto afecta las pruebas que respaldan CA-4, CA-7, CA-9, el rechazo de lotes
mixtos y el cambio de notas durante una generación. La afirmación del autor
de que las 19 y 215 pruebas finalizaron correctamente no es reproducible en
`a6bd399`.

Jeffersson debe aislar correctamente `AI_MODE="real"` en esos casos y
proporcionar una `GEMINI_API_KEY` sintética cuando el constructor real forma
parte del camino probado. Después debe entregar un nuevo commit. Brayan
repetirá la suite específica y la completa; si cambia código de aplicación,
también repetirá los criterios afectados.

### Casos independientes y recorrido visual

El auxiliar reproducible `evidencia/brayan-casos.py` ejecutó los diez
criterios sobre la base aislada: 10 PASS y 0 FAIL. Separó ejercicios nuevos
de históricos, usó un proceso con umbral 70, instrumentó llamadas y ausencia
de llamadas, simuló conexión y cuota, comprobó atomicidad, permisos, CSRF,
contexto privado, recursos locales, UUID, relaciones, escape y notas intactas.
No realizó llamadas externas.

Brayan recorrió la interfaz real en Microsoft Edge y confirmó expresamente:

- práctica demo con curso, tema, enunciado y etiqueta demo;
- avisos distintos para ausencia de temas débiles y ausencia de notas;
- cambio de temas débiles tras corregir notas, con UUID histórico conservado;
- acceso docente rechazado sin revelar datos;
- ejercicios distintos para perfiles distintos;
- español, trato formal de usted y UUID visible.

No se conservaron capturas en esa ejecución sobre `a6bd399`. El primer
intento de guardar CA-4 no creó un archivo en la ruta acordada y Brayan
decidió continuar sin evidencia gráfica. Las capturas se obtuvieron después,
sobre el commit corregido, y se documentan en la sección siguiente.
La prueba real independiente de Gemini fue omitida por decisión de Brayan; no
hubo solicitud, tokens ni costo que atribuir a esta verificación.

Brayan confirmó que estos resultados deben documentarse y que se solicite la
corrección al autor. **El PR no está aprobado.** La confirmación de resultados
no sustituye la repetición exitosa de las suites en el nuevo commit.

Ejecuté cada criterio antes de aprobar: la repetición de las suites y las
capturas quedaron completadas en el commit corregido; la aprobación sigue
pendiente de la decisión de Brayan11Hernandez.

Evidencia independiente:

- `evidencia/brayan-entorno.txt`
- `evidencia/brayan-pruebas.txt`
- `evidencia/brayan-http.txt`
- `evidencia/brayan-resultados.md`
- `evidencia/brayan-casos.py`
- `evidencia/brayan-capturas.txt`
- `evidencia/capturas/`

## Repetición sobre la corrección del autor · 2026-11-10

Commit: `8a7a72c7a4ea95097d45ab270ae64b7a6fff8375`, rama `s-007-ejercicios`,
mensaje «S-007: aísla modo y clave de Gemini en las pruebas». Se comprobó con
`git rev-parse HEAD` que no existían commits posteriores.

Computadora: la misma de la verificación independiente, Windows, Python
3.12.10, entorno virtual existente y base SQLite aislada en el directorio
temporal. No se instalaron dependencias ni se modificó código de la
aplicación. Los cambios locales de esta verificación se conservaron: el
`pull --ff-only` fue fast-forward y no tocó `verificacion.md` ni `evidencia/`.

### Revisión del cambio

`git diff a6bd399..8a7a72c` modifica únicamente `tutor/test_exercises.py`,
`specs/S-007-ejercicios/plan.md` y `docs/registro-ia.md`: 87 líneas agregadas
y 4 eliminadas. No hay cambios en vistas, servicios, proveedores, modelos ni
plantillas. El override común de `PracticeTests` deja de imponer `AI_MODE` y
cada prueba declara demo o real; la configuración común usa una clave
sintética para construir el proveedor simulado. La lógica de producción es la
misma que se recorrió en `a6bd399`.

### Suites repetidas sin clave real

La clave vacía se fija dentro de Python antes de cargar Django para que dotenv
no recupere el valor local:

| Ejecución | Configuración externa | Resultado |
| --- | --- | --- |
| `test tutor.test_exercises --verbosity 2` | `GEMINI_API_KEY` vacía; `AI_MODE=real` | 19 pruebas, OK, 0.359 s |
| `test accounts academics tutor --noinput` | `GEMINI_API_KEY` vacía; `AI_MODE=demo` | 215 pruebas, OK, 113.664 s |

Los 2 fallos y 14 errores de `a6bd399` desaparecieron. No hubo timeout, no se
consultó Gemini y no se consumió cuota.

### Capturas del recorrido visual

Se repitió el recorrido en el navegador sobre `8a7a72c`, con servidor real en
`127.0.0.1:8012`, `AI_MODE=demo`, clave vacía y la base aislada. Navegador
Microsoft Edge 157.0.4341.42 en modo headless, controlado por el protocolo
DevTools; el inicio de sesión se hizo en el formulario real `/acceso/` con las
cuentas sintéticas. El único host contactado fue `127.0.0.1:8012`: no hubo
peticiones externas ni recursos de Internet.

| Archivo | Criterio | Escenario |
| --- | --- | --- |
| `capturas/ca-4-practica-demo.png` | CA-4 | `estudiante_demo` genera práctica demo; cada ejercicio muestra curso, tema, enunciado, etiqueta de modo y UUID |
| `capturas/ca-5-sin-temas-debiles.png` | CA-5 | `estudiante_01`, todas sus notas iguales o superiores a 60: aviso y sin botón |
| `capturas/ca-5-sin-notas.png` | CA-5 | `estudiante_02`, sin calificaciones: aviso distinto y sin botón |
| `capturas/ca-6-antes.png` | CA-6 | `estudiante_demo` con Git y GitHub 55 y Código limpio 58 |
| `capturas/ca-6-docente-corrige.png` | CA-6 | `docente_01` actualiza Git y GitHub a 65 desde la pantalla de notas |
| `capturas/ca-6-antes-de-regenerar.png` | CA-6 | la lista de temas débiles ya solo muestra Código limpio |
| `capturas/ca-6-despues.png` | CA-6 | la práctica nueva excluye Git y GitHub y conserva el ejercicio histórico |
| `capturas/ca-7-docente-rechazado.png` | CA-7 | `docente_01` en `/practica/PROG-COM/`: 403 |
| `capturas/ca-7-curso-ajeno.png` | CA-7 | `estudiante_demo` en `/practica/BD-APL/`: 403 |
| `capturas/ca-7-uuid-ajeno.png` | CA-7 | `estudiante_03` pide el UUID de `estudiante_demo`: 403 |
| `capturas/ca-8-perfil-a.png` | CA-8 | `estudiante_03`: Ingeniería de prompts |
| `capturas/ca-8-perfil-b.png` | CA-8 | `estudiante_07`: Git y GitHub y El LLM por dentro |
| `capturas/ca-10-uuid-y-usted.png` | CA-10 | detalle del ejercicio propio con UUID estable y trato de usted |

`evidencia/brayan-capturas.txt` registra fecha, commit, configuración, hosts,
códigos HTTP, tamaño y SHA-256 de cada PNG.

Para CA-6, `docente_01` cambió la nota de Git y GitHub avanzado de 55 a 65
mediante la pantalla de notas (S-005) y, al terminar, la restauró a 55. La
restauración se comprobó en la base aislada, que volvió a mostrar dos temas
débiles. No se alteró ninguna base ajena.

### Limitaciones de esta repetición

- Las capturas de CA-4 y CA-8 corresponden al modo demo; la consulta real a
  Gemini sigue omitida por decisión del verificador.
- Las tres capturas de CA-7 muestran la misma pantalla de acceso denegado,
  porque la aplicación responde igual en los tres casos; el registro
  distingue cada solicitud por su URL y su código 403.
- Las capturas se tomaron sobre `8a7a72c`. El recorrido visual anterior,
  documentado arriba sin capturas, se ejecutó sobre `a6bd399`.

## Correcciones y repetición de pruebas

- Commit con fallo: `a6bd399ea1f33394b526c131e6cfba94e9e71e62`.
- Corrección del autor: `8a7a72c7a4ea95097d45ab270ae64b7a6fff8375`
  «S-007: aísla modo y clave de Gemini en las pruebas».
- Repetición de las suites: 19 y 215 pruebas, OK, sin fallos ni errores.
- Capturas: 13 archivos en `evidencia/capturas/`, tomados sobre `8a7a72c`.
- Decisión de aprobación: pendiente de Brayan11Hernandez.

## Comprobaciones locales de implementación · 2026-11-10

Ejecutadas por el asistente OpenCode en la sesión del autor, Windows,
workspace `C:\Users\Canche\Desktop\tutorbosco`, rama s-007-ejercicios.
Cambios sin commit, sobre main `47a7977`; no se atribuye un commit probado
ni una verificación independiente a Brayan11Hernandez.

- `manage.py test tutor.test_exercises --verbosity 1`: 19 pruebas,
  OK, 0.673 segundos. CA-1 a CA-10 se cubren mediante casos automatizados;
  español, trato de usted y presentación requieren además revisión humana.
- `manage.py test accounts academics tutor --noinput`: 215 pruebas,
  OK, 254.688 segundos. La primera ejecución fue interrumpida por el límite
  de 120 segundos de la herramienta; la repetición con mayor tiempo terminó.
- `manage.py check`: sin errores.
- `manage.py makemigrations --check --dry-run`: sin cambios pendientes.
- `python -m pip check`: sin requisitos incompatibles.
- `manage.py migrate`: tutor.0002_practiceexercise aplicada correctamente.
- Recorrido HTTP real en `127.0.0.1:8000`, con cookies y CSRF: inicio de
  sesión de estudiante_03, GET de práctica, POST de generación demo y
  consulta individual por UUID. HTTP 200; se creó un ejercicio propio
  grabado y se comprobó la etiqueta del modo demo. No se imprimieron
  contraseñas ni claves. Se conserva ese ejercicio sintético en la base local.

En esta primera comprobación, las pruebas de proveedor real simularon
las respuestas y el error 429, sin consultar Gemini ni consumir cuota.
La llamada real posterior se detalla a continuación.
El recorrido se comprobó mediante HTTP, sin revisión visual en navegador.

## Prueba real con Gemini · 2026-11-10

Ejecutada por OpenCode en la sesión del autor, a solicitud de este.
Equipo y rama: mismo workspace Windows y s-007-ejercicios de la comprobación
local anterior. Cambios todavía sin commit; no constituye verificación
independiente ni aprobación de Brayan11Hernandez.

### Preparación y recorrido

1. Se comprobó la presencia de una clave local sin mostrarla y el modelo
   configurado `gemini-3.5-flash-lite`.
2. Se inició un servidor temporal en `127.0.0.1:8001` con `AI_MODE=real`
   únicamente en su entorno de proceso. No se modificó `.env`.
3. Se inició sesión mediante HTTP como `estudiante_03`, usando cookies y
   la contraseña local sin imprimirla. Se consultó la pantalla de práctica.
4. Se envió una sola solicitud de generación mediante POST con token CSRF
   a `/practica/PROG-COM/`. Se compararon los UUID anteriores y posteriores
   para identificar el ejercicio nuevo.
5. Se comprobó la respuesta HTTP, el aviso y la etiqueta de procedencia,
   y se consultó el registro persistido para recuperar el enunciado completo,
   propietario, curso, tema, fecha y modo.
6. Se detuvo el servidor temporal. El servidor habitual en el puerto 8000
   continuó disponible, en modo demo y con el ejercicio real guardado.

### Datos y resultados

| Dato | Resultado observado |
| --- | --- |
| Fecha local | 10-11-2026, 19:44, Guatemala (UTC−06:00) |
| Fecha de persistencia UTC | `2026-11-11T01:44:04.025239+00:00` |
| Modelo configurado para la llamada | `gemini-3.5-flash-lite` |
| Usuario sintético | `estudiante_03` |
| Curso | `PROG-COM` — Programación Comercial |
| Tema débil permitido | Ingeniería de prompts |
| Nota consultada al comprobar el ejercicio | 58 |
| Umbral configurado | 60; el tema cumple `58 < 60` |
| Duración HTTP de la generación y redirección | 6,12 segundos |
| Respuesta HTTP final | 200 |
| Ejercicios nuevos persistidos | 1 |
| Procedencia persistida | `real` |
| `demo_key` | Vacío |
| Aviso de alternativa demo | No apareció |
| Aviso de práctica inválida | No apareció |
| Etiqueta en el HTML recibido | Ejercicio generado por IA |
| UUID | `04ee22d6-a90a-485a-ae8e-0d227530cb94` |

### Respuesta completa de Gemini: enunciado validado y guardado

> Diseñe un prompt estructurado utilizando la técnica de pocos ejemplos (few-shot prompting) para que un modelo de lenguaje extraiga correctamente los datos fiscales de una factura en formato de texto libre y los devuelva en un formato JSON estandarizado para su posterior registro contable.

Esta es la respuesta a la solicitud de generar práctica: un ejercicio para
que lo resuelva el estudiante. Su solución y posterior retroalimentación
corresponden a S-009. El texto se recuperó del registro persistido; no se
conservó la respuesta HTTP original ni el JSON crudo del proveedor.

Consulta local, tras iniciar sesión con la misma cuenta:
`http://127.0.0.1:8000/practica/PROG-COM/?exercise=04ee22d6-a90a-485a-ae8e-0d227530cb94`.
El UUID identifica un registro de esta base local; otra instalación no lo
contendrá automáticamente y deberá generar sus propios ejercicios.

### Alcance de la evidencia

- La llamada real produjo un enunciado válido y pertinente al tema débil
  del curso seleccionado, aportando evidencia local para CA-4.
- El texto está en español y usa trato formal («Diseñe»); se comprobó
  UUID, propietario, curso y tema, aportando evidencia local para CA-10.
- La persistencia y la etiqueta `real`, sin aviso de fallback y sin
  `demo_key`, distinguen este resultado de la generación grabada.
- El autor informó previamente que probó el modo demo y que le pareció
  correcto; no se atribuye a ese comentario la verificación de cada criterio.
- El recorrido real se comprobó mediante HTTP; no se adjunta captura ni se
  declara revisión visual de esta llamada en navegador.
- Se realizó una solicitud real. Tokens y costo monetario no recuperados:
  pendientes de confirmar con los registros del proveedor (véase docs/gasto.md).
- No se provocaron fallos reales de cuota ni conexión en esta llamada.
  Esos casos se cubrieron mediante simulaciones automatizadas.
- Una generación exitosa no prueba los diez criterios completos; la matriz
  de verificación independiente permanece pendiente.

### Guía para la verificación independiente

1. Registrar equipo y commit recibido; aplicar migraciones en su instalación.
2. Ejecutar las pruebas y recorrer la pantalla con estudiantes distintos.
3. Para CA-1 a CA-3, preparar notas sintéticas 45/59/60/85 y un tema sin
   nota; repetir con umbral 70 y notas 60/69/70.
4. Para CA-4/CA-5/CA-6, generar, comprobar curso/tema, probar estados sin
   notas y sin temas débiles, corregir notas desde el docente y regenerar.
5. Para CA-7, comprobar rechazo de docente, curso ajeno, UUID ajeno,
   propietario manipulado y POST sin CSRF; revisar contexto con proveedor simulado.
6. Para CA-8/CA-9, ejecutar demo sin clave y sin red; revisar pruebas de
   cuota/conexión, salida inválida y catálogo ausente.
7. Para CA-10, revisar español/usted, UUID estable y propietario, escape de
   texto y que las notas oficiales no cambien.
8. Completar la matriz anterior con evidencia propia; no sustituirla por
   estos resultados locales del asistente.
