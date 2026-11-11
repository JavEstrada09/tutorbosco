# TutoBosco

Plataforma web educativa con tutor de inteligencia artificial
personalizado según el perfil académico del estudiante.

Proyecto final de Programación Comercial — UMES.

## Equipo

- AlexDLG1
- douglas-yasser
- Brayan11Hernandez
- JavEstrada09
- ramosdeleon555

## Estado

Las Entregas 1, 2, 3 y la implementación local de la Entrega 4 de S-001
incorporan la base ejecutable de Django,
el modelo académico mínimo, datos sintéticos, inicio de sesión, la pantalla
protegida del estudiante y el formulario del tutor con proveedores demo y
Gemini. La consulta real tiene un límite total de 60 segundos y realiza un
solo intento. Esto evita que `429` y otros fallos activen reintentos que
prolonguen la espera o registren detalles internos del proveedor.

El recorrido demo está comprobado sin clave ni cliente Gemini. JavEstrada09
también comprobó CA-4 localmente con `gemini-3.8-flash`. Douglas completó la
verificación independiente de los siete criterios sobre `eb01cc7`, incluida
una instalación limpia con Python 3.12.10 y una respuesta real con
`gemini-3.5-flash-lite`; S-001 queda pendiente de la revisión y fusión del PR.

S-002 incorporó docentes, temas, notas y el conjunto completo de datos
sintéticos. La verificación independiente quedó registrada en
[verificacion.md](specs/S-002-datos-sinteticos/verificacion.md).

S-003 agrega el perfil académico del estudiante en `/perfil/`: datos
personales, cursos inscritos, nota por tema y promedio del curso. El promedio
se calcula en una sola función, `academics.services.calculate_average`. La
verificación independiente de ramosdeleon555 quedó registrada en
[verificacion.md](specs/S-003-perfil-academico/verificacion.md).

S-005 agrega la pantalla del docente para registrar y corregir notas en
`/docente/cursos/<código>/notas/`. La regla de guardado vive en
`academics.services.record_grade`, que comprueba en el servidor que el
docente imparta el curso, que el tema sea del curso, que el estudiante esté
inscrito y que la nota sea un entero de 0 a 100. La verificación
independiente de ramosdeleon555 quedó registrada en
[verificacion.md](specs/S-005-registro-notas/verificacion.md). La
gestión de temas y estudiantes de S-004 incluye el enlace a esta
pantalla.

## Requisitos

- Python 3.12.
- Git.
- SQLite, incluido con Python.

Las versiones exactas de Python y las dependencias comprobadas se
encuentran en `requirements.txt` y al final de esta sección.

## Instalación local en PowerShell

Desde la raíz del repositorio:

```powershell
py -3.12 -m venv .venv
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
```

El entorno `.venv` es local y está excluido de Git.

## Configuración local

Crear `.env` y generar `DJANGO_SECRET_KEY` sin mostrar su valor, solo si
el archivo todavía no existe:

```powershell
if (-not (Test-Path -LiteralPath ".env")) {
    Copy-Item -LiteralPath ".env.example" -Destination ".env"
    $secret = (& ".\.venv\Scripts\python.exe" -c `
        "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())").Trim()
    $content = Get-Content -LiteralPath ".env"
    $content = $content -replace '^DJANGO_SECRET_KEY=$', "DJANGO_SECRET_KEY=$secret"
    $content = $content -replace '^DJANGO_DEBUG=$', "DJANGO_DEBUG=true"
    $content = $content -replace '^DJANGO_ALLOWED_HOSTS=$', `
        "DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1"
    $utf8NoBom = [System.Text.UTF8Encoding]::new($false)
    [System.IO.File]::WriteAllLines(
        (Resolve-Path -LiteralPath ".env"), $content, $utf8NoBom
    )
    Remove-Variable secret, content, utf8NoBom
}
```

Si `.env` ya existe, el bloque no lo modifica. Revise localmente que
contenga:

- `DJANGO_SECRET_KEY`: valor aleatorio exclusivo de su instalación, sin
  imprimirlo ni compartirlo.
- `DEMO_STUDENT_PASSWORD`: contraseña fuerte para la cuenta sintética,
  escrita únicamente en `.env`.
- `DEMO_TEACHER_PASSWORD`: contraseña fuerte para las cuentas docentes
  sintéticas, escrita únicamente en `.env`.
- `AI_MODE=demo`: usa la respuesta grabada sin red ni clave de Gemini.
- `AI_MODEL=gemini-3.5-flash-lite` selecciona el modelo aprobado. Dejar
  `AI_MODEL` vacío usa el mismo valor. En instalaciones existentes,
  actualizar este valor si todavía indica Gemini 3.8 Flash.
- `GEMINI_API_KEY`: se deja vacío en modo demo. En modo real contiene la
  clave local y nunca debe mostrarse, registrarse ni versionarse.
- `WEAK_TOPIC_THRESHOLD`: umbral de tema débil; vacío usa 60. Un tema es
  débil cuando su nota es estrictamente menor que este valor. Si lo configura,
  use un entero entre 0 y 100.
- `DJANGO_DEBUG=true`: habilita ayudas de desarrollo local.
- `DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1`: limita los nombres locales
  aceptados por Django.

`.env` está excluido de Git. No guarde contraseñas ni claves en README,
código, registros o commits. El modo demo no importa ni inicializa el
cliente Gemini al responder.

## Base y datos sintéticos

```powershell
& ".\.venv\Scripts\python.exe" manage.py migrate
& ".\.venv\Scripts\python.exe" manage.py rebuild_synthetic_data
```

`rebuild_synthetic_data` exige `DEMO_STUDENT_PASSWORD` y
`DEMO_TEACHER_PASSWORD`, guarda sus hashes mediante Django, puede
repetirse sin duplicar datos y no borra registros ajenos al manifiesto.

Genera:

- 30 estudiantes: `estudiante_demo` y `estudiante_01` a `estudiante_29`.
- 3 docentes: `docente_01` a `docente_03`.
- 4 cursos con 6 temas cada uno: `PROG-COM`, `BD-APL`, `DES-WEB` y
  `REDES`.
- Notas enteras de 0 a 100 con perfiles distintos, incluidos estudiantes
  con dos temas débiles, sin temas débiles y sin notas.

Todos los estudiantes están inscritos en Programación Comercial y se
distribuyen además entre los otros tres cursos. Las cuentas docentes usan
la contraseña local definida en `DEMO_TEACHER_PASSWORD`.

Un tema se considera débil cuando su nota es estrictamente menor que
`WEAK_TOPIC_THRESHOLD`, configurable en `.env` (60 por defecto).

## Comprobaciones locales

```powershell
& ".\.venv\Scripts\python.exe" manage.py check
& ".\.venv\Scripts\python.exe" manage.py test accounts academics tutor
& ".\.venv\Scripts\python.exe" manage.py makemigrations --check --dry-run
& ".\.venv\Scripts\python.exe" -m pip check
```

Las pruebas automatizadas cubren los modelos y sus restricciones, los
límites de las notas, el hash de las contraseñas, la reconstrucción
idempotente y los perfiles sintéticos. También comprueban autenticación,
autorización, aislamiento entre estudiantes, CSRF, cierre de sesión mediante
POST, el formulario del tutor, la selección de proveedor, la salida validada
y la ausencia de inicialización de Gemini en modo demo.

Para el perfil académico, las pruebas cubren el cálculo central del promedio
con redondeo a dos decimales, los temas sin nota, los cursos sin notas, el
estudiante sin cursos, el aislamiento entre estudiantes y la nota actualizada
al recargar.

Para el registro de notas, las pruebas cubren el guardado de una nota nueva,
la corrección que reemplaza la anterior sin duplicarla, los valores fuera de
rango o no enteros, la nota visible en el perfil del estudiante y después de
volver a iniciar sesión, y que la planilla solo muestre estudiantes inscritos
y temas del curso. También comprueban el rechazo en el servidor de un
estudiante no inscrito, un tema de otro curso y un curso que el docente no
imparte, el acceso de estudiantes y cuentas sin perfil docente, y CSRF.

Las pruebas simulan Gemini, incluida la prueba del constructor mediante un
mock. Cubren configuración inválida, conexión fallida, cuota agotada (`429`),
tiempo de espera (`504`) y respuesta inválida, sin consumir cuota. La
verificación independiente registra por separado las consultas reales.

La regresión de `429` comprueba que Gemini recibe un solo intento, que se
ofrece continuar en modo demo y que el detalle interno del proveedor no se
registra. Como no se conservan reintentos, el límite de 60 segundos cubre la
consulta completa.

## Inicio del servidor

```powershell
& ".\.venv\Scripts\python.exe" manage.py runserver
```

Abra `http://127.0.0.1:8000/acceso/`. Use el usuario sintético
`estudiante_demo` y la contraseña definida localmente en
`DEMO_STUDENT_PASSWORD`. Después del acceso verá su carrera y el formulario
del tutor. Con `AI_MODE=demo`, envíe la pregunta visible en la pantalla:

```text
¿Qué es una variable y para qué se usa?
```

La respuesta grabada debe mencionar Programación Comercial y dirigirse a
usted. Este recorrido funciona sin Internet y con `GEMINI_API_KEY` vacío.

Desde esa pantalla, el enlace `Ver su perfil académico` abre
`http://127.0.0.1:8000/perfil/`. El perfil muestra nombre, carné, carrera,
semestre y, por cada curso inscrito, la nota de cada tema y el promedio del
curso. Un tema sin nota aparece como `Sin nota` y no entra al promedio; un
curso sin notas muestra `Sin notas`. Con los datos sintéticos,
`estudiante_demo` tiene promedio 78.00 en Programación Comercial y
`estudiante_02` no tiene notas.

Con un docente sintético, por ejemplo `docente_01` y la contraseña de
`DEMO_TEACHER_PASSWORD`, el acceso dirige a `http://127.0.0.1:8000/docente/panel/`.
El panel lista los cursos que imparte y, por curso, los estudiantes con su
promedio y sus temas débiles, ordenables por promedio, el detalle de cada
estudiante y el conteo de estudiantes con cada tema débil. Solo se muestran
los cursos asignados al docente; el resto responde 403.

La gestión académica de S-004 está disponible en
`http://127.0.0.1:8000/docente/cursos/`. Desde esa pantalla, el docente puede
consultar únicamente sus cursos, registrar o modificar sus temas y asignar
estudiantes existentes. Los formularios evitan temas e inscripciones
duplicados y muestran estados vacíos y errores comprensibles. Las rutas de un
curso ajeno o inexistente responden 403 mediante la autorización compartida
con S-005. Cada curso incluye también el enlace a su planilla de notas.

Si Gemini falla en modo real, la pantalla muestra un mensaje seguro y ofrece
`Continuar en modo demo`. Esa acción usa en el servidor la pregunta pendiente
del mismo hilo, muestra la etiqueta `Respuesta grabada del modo demo` y no
inicializa Gemini. Si no hay una grabación aplicable, muestra un aviso y
conserva los turnos completados.

### Registro de notas del docente

Abra `http://127.0.0.1:8000/acceso/?next=/docente/cursos/PROG-COM/notas/` y
use `docente_01` con la contraseña definida localmente en
`DEMO_TEACHER_PASSWORD`. Si inicia sesión desde `/acceso/` sin `next`, el
acceso lo lleva al panel del docente (`/docente/panel/`). La gestión académica
de `/docente/cursos/` enlaza la planilla de cada curso. `docente_01` imparte
`PROG-COM` y `DES-WEB`.

La pantalla muestra la planilla del curso, con una fila por estudiante
inscrito y una columna por tema; un tema sin nota aparece como `Sin nota`.
El formulario pide Estudiante, Tema y Nota. Si el estudiante ya tiene nota en
ese tema, la nueva la reemplaza. Un código de curso que el docente no imparte,
como `BD-APL` para `docente_01`, responde con acceso denegado.

Las notas registradas cambian los datos sintéticos. `rebuild_synthetic_data`
restablece las notas de los estudiantes que tienen notas en el manifiesto,
pero no borra las que se registren a estudiantes sin notas, como
`estudiante_02`. Esas notas deben eliminarse aparte si se quiere volver al
estado inicial.

## S-007 · Práctica de temas débiles (implementación local)

Después de actualizar, aplique `manage.py migrate`. Desde el inicio del
estudiante, use **Practicar sus temas débiles** o abra
`http://127.0.0.1:8000/practica/PROG-COM/`. Puede cambiar entre sus cursos
inscritos y pulsar **Generar nueva práctica**. Una nueva solicitud consulta
las notas vigentes, excluye notas ausentes y usa el umbral configurable.
Sin notas o sin temas débiles muestra avisos distintos sin consultar a IA.

Con `AI_MODE=demo` se usan ejercicios locales de los 24 temas sintéticos de
los cuatro cursos. Por ejemplo, `estudiante_03` tiene práctica disponible en
Programación Comercial con los datos locales usados en la comprobación.
La contraseña es la configurada en `DEMO_STUDENT_PASSWORD`.
No es necesario reconstruir los datos ni modificar notas para generar práctica.

En modo real se reutiliza Gemini con 60 segundos y un intento. Los errores
de conexión o cuota activan automáticamente ejercicios demo aplicables con
un aviso. Una respuesta inválida se rechaza; si no hay grabaciones aplicables
se informa sin sustituirlas por temas ajenos.

Cada ejercicio guarda UUID, propietario, curso, tema, enunciado y procedencia.
El enlace **Consultar este ejercicio** conserva su identificador, aunque
cambien las notas. La pantalla muestra hasta seis ejercicios recientes.
La generación usa POST con CSRF; recargar los resultados no genera ejercicios.
Responder y recibir retroalimentación corresponde a S-009.

Pruebas específicas: `manage.py test tutor.test_exercises`.
Esta implementación requiere revisión del autor y verificación independiente
de Brayan11Hernandez antes de declarar terminada S-007.

## Comprobación real de CA-4 (S-001)

En la Entrega 4, JavEstrada09 probó `gemini-3.5-flash-lite` en modo real
desde TutorBosco. El tutor explicó en español, con trato de usted, cómo
restar el descuento de Q10 a Q100 y obtener Q90. La prueba usó un plazo
total de 60 segundos y un único intento. Douglas repitió CA-4 en modo real
con `gemini-3.5-flash-lite`: la interfaz mostró la respuesta en 4.12 s, con
trato de usted y mención de Programación Comercial. Con `gemini-3.8-flash`
la consulta falló con `504 DEADLINE_EXCEEDED`.

En las pruebas anteriores de la Entrega 3:

JavEstrada09 comprobó localmente la disponibilidad de
`gemini-3.8-flash` en el nivel gratuito. La interfaz recibió dos respuestas
reales: una sobre variables y otra que calculó correctamente Q75. La
consulta de Q75 tardó aproximadamente tres minutos.

De forma separada se realizó una consulta directa de diagnóstico que
respondió correctamente. En otros intentos reales se observaron los errores
`429 RESOURCE_EXHAUSTED` y `504 DEADLINE_EXCEEDED`. La Entrega 4 reproduce
ambos casos mediante pruebas simuladas para verificar sus mensajes sin
consumir cuota.

Esta comprobación corresponde al autor y no reemplaza la verificación
independiente pendiente de Douglas. El total de solicitudes y los tokens
utilizados no están confirmados. No se registraron claves ni datos sensibles.

## Comprobación local de CA-7

El 08-11-2026, JavEstrada09 repitió la instalación con Python 3.12.10 en un
entorno virtual temporal nuevo y una base SQLite aislada. La instalación de
`requirements.txt`, las migraciones, `rebuild_synthetic_data`, las 48 pruebas
disponibles en ese momento,
`check`, `makemigrations --check --dry-run` y `pip check` finalizaron
correctamente.

El recorrido HTTP aislado completó acceso, consulta de carrera y respuesta
grabada. Durante la pregunta demo se bloquearon mediante simulaciones tanto
la creación del cliente Gemini como la salida de red, y ninguna fue invocada.
Esta comprobación del autor no sustituye la ejecución independiente pendiente
de Douglas.

## Versiones comprobadas

- Python 3.12.10.
- Django 5.2.19.
- google-genai 3.0.0.
- python-dotenv 1.2.4.


### S-006 · Tutor personalizado

El servicio `conversation_context` prepara exclusivamente los temas y notas
capturados al abrir el hilo y sus cuatro últimos turnos. Para la llamada se
limita cada pregunta a 500 caracteres y cada respuesta previa a 2000; los
turnos completos permanecen en la base hasta reiniciar o cerrar sesión.
Gemini recibe las instrucciones separadas de los datos y de la pregunta.
Se mantienen el límite total de 60 segundos, un intento y la validación.

El proveedor demo admite «¿Qué tema debería repasar?», «¿Me da otro ejemplo?»,
«Explíqueme [nombre exacto del tema].», la pregunta original sobre variables
y los dos ejemplos de privacidad del plan. Hay explicaciones y ejemplos
adicionales grabados para los seis temas del piloto. Sin una grabación
aplicable, devuelve un aviso; no reutiliza respuestas del piloto en otro
curso. Se comparte el cálculo `is_weak` y se distinguen las notas ausentes.

La pantalla conserva un hilo por sesión y curso, muestra sus mensajes y
permite cambiar entre los cursos inscritos. «Nueva conversación» borra
los mensajes del curso seleccionado y consulta de nuevo sus notas. Cerrar
sesión elimina todos los hilos de esa sesión. Los formularios mantienen
CSRF e incluyen curso, revisión y acción; una revisión desactualizada se
rechaza antes de consultar al proveedor, y un resultado que llega después
de un reinicio se descarta.

Para probar el recorrido en demo, inicie sesión, pregunte qué tema debería
repasar y pida otro ejemplo. Cambie de curso y vuelva al primero para ver
su historial. Actualice una nota con la pantalla docente, vuelva al tutor
y pulse «Nueva conversación»: la recomendación usará la nota actualizada.
S-006 cuenta con verificación independiente de douglas-yasser para los nueve
criterios. La repetición de CA-1, CA-5 y CA-9 con Gemini real y las 191
pruebas pasaron sobre `30ad0c3`; el PR #53 integró la implementación y la
evidencia en `main`. El detalle, incluido el fallo inicial y su corrección,
está en `specs/S-006-tutor/verificacion.md`. El consumo real registrado
para S-006 fue de 14 solicitudes en el nivel gratuito, con costo USD 0.00;
los tokens no están confirmados (véase `docs/gasto.md`).
