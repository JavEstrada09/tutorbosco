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

Las Entregas 1 y 2 de S-001 incorporan la base ejecutable de Django, el
modelo académico mínimo, datos sintéticos mínimos, inicio de sesión y la
pantalla protegida que muestra la carrera del estudiante.

Los proveedores del tutor, el modo demo y la integración con Gemini
siguen pendientes de las entregas posteriores. S-001 no está terminada.

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
- `DJANGO_DEBUG=true`: habilita ayudas de desarrollo local.
- `DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1`: limita los nombres locales
  aceptados por Django.

`.env` está excluido de Git. No guarde contraseñas ni claves en README,
código, registros o commits. La Entrega 2 no necesita `GEMINI_API_KEY`
ni realiza llamadas a Gemini.

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

## Comprobaciones de las Entregas 1 y 2

```powershell
& ".\.venv\Scripts\python.exe" manage.py check
& ".\.venv\Scripts\python.exe" manage.py test accounts academics
& ".\.venv\Scripts\python.exe" manage.py makemigrations --check --dry-run
```

Estas pruebas cubren los modelos, sus restricciones, el hash de la
contraseña, la reconstrucción idempotente, autenticación, autorización,
aislamiento entre estudiantes, CSRF y cierre de sesión mediante POST.
No verifican todavía los siete criterios completos de S-001.

## Inicio del servidor

```powershell
& ".\.venv\Scripts\python.exe" manage.py runserver
```

Abra `http://127.0.0.1:8000/acceso/`. Use el usuario sintético
`estudiante_demo` y la contraseña definida localmente en
`DEMO_STUDENT_PASSWORD`. Después del acceso verá únicamente la carrera
asociada a esa cuenta y podrá cerrar sesión mediante el formulario.

La pantalla del tutor y sus formularios todavía no están implementados.

## Versiones comprobadas

- Python 3.12.10.
- Django 5.2.19.
- python-dotenv 1.2.4.
