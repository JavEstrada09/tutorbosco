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

Las Entregas 1, 2 y 3 de S-001 incorporan la base ejecutable de Django,
el modelo académico mínimo, datos sintéticos, inicio de sesión, la pantalla
protegida del estudiante y el formulario del tutor con proveedores demo y
Gemini.

El recorrido demo está comprobado sin clave ni cliente Gemini. JavEstrada09
también comprobó CA-4 localmente con `gemini-3.8-flash`. La verificación
independiente de Douglas y el manejo completo de errores de la Entrega 4
siguen pendientes; S-001 todavía no está terminada.

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
- `AI_MODE=demo`: usa la respuesta grabada sin red ni clave de Gemini.
- `AI_MODEL=gemini-3.8-flash`: identificador configurable previsto para
  la comprobación real.
- `GEMINI_API_KEY`: se deja vacío en modo demo. En modo real contiene la
  clave local y nunca debe mostrarse, registrarse ni versionarse.
- `DJANGO_DEBUG=true`: habilita ayudas de desarrollo local.
- `DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1`: limita los nombres locales
  aceptados por Django.

`.env` está excluido de Git. No guarde contraseñas ni claves en README,
código, registros o commits. El modo demo no importa ni inicializa el
cliente Gemini al responder.

## Base y datos mínimos

```powershell
& ".\.venv\Scripts\python.exe" manage.py migrate
& ".\.venv\Scripts\python.exe" manage.py rebuild_synthetic_data
```

`rebuild_synthetic_data` puede repetirse sin duplicar datos. Administra
solo su manifiesto sintético, que incluye:

- Usuario: `estudiante_demo`.
- Carné: `2026-00001`.
- Curso: `PROG-COM`, Programación Comercial.

El comando exige `DEMO_STUDENT_PASSWORD`, guarda su hash mediante Django
y no borra registros ajenos.

## Comprobaciones de las Entregas 1, 2 y 3

```powershell
& ".\.venv\Scripts\python.exe" manage.py check
& ".\.venv\Scripts\python.exe" manage.py test accounts academics tutor
& ".\.venv\Scripts\python.exe" manage.py makemigrations --check --dry-run
& ".\.venv\Scripts\python.exe" -m pip check
```

Las 44 pruebas automatizadas cubren modelos, autenticación, autorización,
aislamiento, CSRF, formulario, selección de proveedor, salida validada y
ausencia de inicialización de Gemini en modo demo. Estas pruebas simulan
Gemini, incluida la prueba del constructor mediante un mock, por lo que no
consumen cuota ni sustituyen las consultas reales. Tampoco verifican todavía
los siete criterios completos de S-001.

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

## Comprobación real de CA-4

JavEstrada09 comprobó localmente la disponibilidad de
`gemini-3.8-flash` en el nivel gratuito. La interfaz recibió dos respuestas
reales: una sobre variables y otra que calculó correctamente Q75. La
consulta de Q75 tardó aproximadamente tres minutos.

De forma separada se realizó una consulta directa de diagnóstico que
respondió correctamente. En otros intentos reales se observaron los errores
`429 RESOURCE_EXHAUSTED` y `504 DEADLINE_EXCEEDED`. El 504 se conserva como
caso pendiente para el manejo completo de errores de la Entrega 4.

Esta comprobación corresponde al autor y no reemplaza la verificación
independiente pendiente de Douglas. El total de solicitudes y los tokens
utilizados no están confirmados. No se registraron claves ni datos sensibles.

## Versiones comprobadas

- Python 3.12.10.
- Django 5.2.19.
- google-genai 3.0.0.
- python-dotenv 1.2.4.
