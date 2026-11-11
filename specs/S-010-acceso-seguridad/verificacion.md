# Verificación S-010 — Acceso, seguridad e interfaz por rol

Verificador: AlexDLG1 · Computadora: equipo de AlexDLG1, Windows, Python 3.12.10 · Commit: 3c3907a

## Procedencia de la evidencia

- La preparación y los controles automatizados los ejecuté yo en mi
  computadora, sobre `3c3907a` (rama local `verificacion-s010`).
- Las capturas de CA-1 a CA-8 las tomó Claude (Claude Opus 5.5)
  controlando el navegador integrado de la app de Claude en mi
  computadora, contra mi servidor local, con las cuentas
  `estudiante_demo` y `docente_01`. Cada captura lleva un encabezado con
  el criterio, la URL y la cuenta. Revisé cada captura y su resultado
  antes de registrarlo aquí.
- La guía de pasos y la redacción de este registro se apoyaron en Claude
  (chat, Claude Opus 5.5).

## Preparación y controles

```powershell
git switch -c verificacion-s010 origin/s-010-acceso-seguridad
& ".\.venv\Scripts\python.exe" manage.py migrate
& ".\.venv\Scripts\python.exe" manage.py rebuild_synthetic_data
& ".\.venv\Scripts\python.exe" manage.py test accounts academics tutor
& ".\.venv\Scripts\python.exe" manage.py runserver
```

```text
git log --oneline -1: 3c3907a S-010: aclara revisión y fusión de la spec
migrate: No migrations to apply.
rebuild_synthetic_data: Datos sintéticos completos reconstruidos.
test: Ran 202 tests ... OK
```

## Resultados por criterio

| Criterio | Cómo se probó | Resultado | Evidencia |
| --- | --- | --- | --- |
| CA-1 | `estudiante_demo` inicia sesión y llega a `/` con la navegación "Inicio", "Perfil académico" y "Cerrar sesión". `docente_01` inicia sesión y llega a `/docente/panel/` con "Panel docente", "Administrar cursos" y "Cerrar sesión". | Cumple | [estudiante](img/ca1-estudiante.png), [docente](img/ca1-docente.png) |
| CA-2 | Contraseña incorrecta para `estudiante_demo` y usuario inexistente: en ambos casos el mismo mensaje "Las credenciales ingresadas no son válidas.", sin indicar si el usuario existe. | Cumple | [contraseña](img/ca2-contrasena-incorrecta.png), [usuario](img/ca2-usuario-inexistente.png) |
| CA-3 | Como `estudiante_demo`, la navegación no muestra opciones de docente; `/docente/panel/` y `/docente/cursos/` responden 403 "Acceso denegado". | Cumple | [panel](img/ca3-panel-403.png), [cursos](img/ca3-cursos-403.png) |
| CA-4 | Como `docente_01`, la navegación muestra las herramientas de docente; `/perfil/` (perfil de estudiante) responde 403. | Cumple | [panel](img/ca1-docente.png), [perfil](img/ca4-perfil-403.png) |
| CA-5 | Sin sesión, `/perfil/`, `/docente/panel/` y `/docente/cursos/PROG-COM/notas/` redirigen a `/acceso/?next=…` sin mostrar datos. | Cumple | [perfil](img/ca5-perfil-sin-sesion.png), [notas](img/ca5-notas-sin-sesion.png) |
| CA-6 | Como `docente_01`, URL modificada a un curso que no imparte: `/docente/cursos/BD-APL/temas/` y `/docente/cursos/BD-APL/notas/` responden 403. El rechazo de envíos POST ajenos está cubierto por las pruebas automatizadas. | Cumple | [temas](img/ca6-bdapl-temas-403.png), [notas](img/ca6-bdapl-notas-403.png) |
| CA-7 | "Cerrar sesión" desde la navegación lleva a `/acceso/`. Después, volver atrás o abrir `/perfil/` redirige a `/acceso/?next=/perfil/`. Lo mismo con `docente_01` y `/docente/panel/`. | Cumple | [cierre](img/ca7-cierre-sesion.png), [volver](img/ca7-volver-privada.png) |
| CA-8 | Recorrido de perfil, mis cursos y notas: textos en español y la misma navegación en todas las páginas privadas. | Cumple, con observaciones | [perfil](img/ca8-perfil.png), [cursos](img/ca8-mis-cursos.png), [notas](img/ca8-notas.png) |

## Observaciones (no bloquean)

- Al cargar `bootstrap.min.css` en `base.html`, cambia el aspecto de las
  pantallas existentes respecto de `main`: los títulos pierden la
  negrita, los selectores de la pantalla de notas ya no muestran la
  flecha de despliegue y los enlaces "Administrar temas" de Mis cursos
  toman el color azul por defecto. Todo sigue funcionando y en español.

## Correcciones y repetición de pruebas

No se encontraron fallos que requieran corrección.

## Ampliación de interfaz (CA-9) · verificación

Verificador: AlexDLG1 · Computadora: equipo de AlexDLG1, Windows, Python 3.12.10 · Commit: e871bbb · Fecha: 11-11-2026

CA-9 se añadió a S-010 el 11-11-2026: el rediseño visual cubre todas las
pantallas. Las capturas de CA-8 muestran el aspecto anterior al rediseño;
el aspecto actual queda en las capturas de esta sección.

### Procedencia de la evidencia

- Las pruebas automatizadas las ejecuté yo en mi computadora (rama local
  `verificacion-s010`), primero sobre `dca29aa` y al final sobre
  `e871bbb`.
- Las capturas las tomó Claude (Claude Opus 5.5) controlando el navegador
  integrado de la app de Claude en mi computadora, contra mi servidor
  local, con las cuentas `estudiante_demo` y `docente_01`, en tamaño de
  teléfono (375 px) y de escritorio (1100 px). En cada pantalla midió el
  ancho del documento frente al ancho de la ventana. Cada captura lleva
  un encabezado con la pantalla, la URL, la cuenta, la medida y el commit.
  Revisé cada captura y su resultado antes de registrarlo aquí.
- La primera ronda fue sobre `dca29aa` y encontró la observación 2. La
  segunda fue sobre `e871bbb`: se repitieron en el navegador las pantallas
  que cambiaron (panel del curso y práctica) y se volvió a medir en
  teléfono cada pantalla de la tabla. Las capturas de pantallas que
  `e871bbb` no modifica son de `dca29aa`.
- Antes, sobre `196df60`, Claude hizo una revisión previa en un entorno en
  la nube (no en mi computadora). Ahí encontró la observación 1 y comparó
  texto, enlaces y campos de formulario entre `f2753cf` y `196df60` sin
  encontrar pérdidas.
- La redacción de este registro se apoyó en Claude (chat, Claude Opus 5.5).

### Controles

```powershell
git switch verificacion-s010
git pull --ff-only origin s-010-acceso-seguridad
git log --oneline -1
& ".\.venv\Scripts\python.exe" manage.py migrate
& ".\.venv\Scripts\python.exe" manage.py test accounts academics tutor
& ".\.venv\Scripts\python.exe" manage.py runserver
```

```text
dca29aa: Ran 202 tests in 155.389s ... OK
4698763 (merge de main con S-007): migrate aplicó tutor.0002_practiceexercise; Ran 223 tests in 190.869s ... OK
e871bbb: git log --oneline -1: e871bbb S-010: corrige panel movil y encabezado de practica
e871bbb: Ran 223 tests in 155.447s ... OK
manage.py check (al iniciar las pruebas y el servidor): System check identified no issues (0 silenced).
```

### Resultados

| Paso | Pantalla | Resultado | Evidencia |
| --- | --- | --- | --- |
| 1 | `/acceso/` con contraseña incorrecta en teléfono | Cumple: título centrado, tarjeta y mensaje "Las credenciales ingresadas no son válidas." legible; 375 px. | [acceso](img/ca9-pc-acceso-error-movil.png) |
| 2 | Inicio y perfil de `estudiante_demo` en teléfono | Cumple: cabecera común, títulos centrados y tarjetas; 375 px. | [inicio](img/ca9-pc-inicio-movil.png), [perfil](img/ca9-pc-perfil-movil.png) |
| 3 | Práctica de `estudiante_demo` (`/practica/PROG-COM/`, llegó con S-007) en teléfono | Cumple en `e871bbb`: título centrado como en las demás pantallas; 375 px. | [práctica](img/ca9-pc-practica-movil.png) |
| 4 | `/docente/cursos/` y `/docente/panel/` como estudiante | Cumple: 403 en tarjeta centrada con "Volver al inicio"; 375 px en ambas (captura de la primera). | [403](img/ca9-pc-403-movil.png) |
| 5 | Panel docente, mis cursos, temas y estudiantes de `docente_01` en teléfono | Cumple: misma cabecera, títulos centrados, botones identificables; 375 px. | [panel](img/ca9-pc-panel-movil.png), [cursos](img/ca9-pc-mis-cursos-movil.png), [temas](img/ca9-pc-temas-movil.png), [estudiantes](img/ca9-pc-estudiantes-movil.png) |
| 6 | Notas del curso en teléfono | Cumple (corregido en `dca29aa`): 375 px; la tabla de notas se desplaza dentro de su propio recuadro. | [formulario](img/ca9-pc-notas-movil.png), [tabla](img/ca9-pc-notas-tabla-movil.png) |
| 7 | Panel del curso (PROG-COM y DES-WEB) en teléfono | Cumple en `e871bbb`: 375 px en ambos cursos; las tablas se desplazan dentro de su recuadro y todas las columnas siguen accesibles. En `dca29aa` medía 523 px (observación 2). | [PROG-COM](img/ca9-pc-panel-curso-movil.png), [tabla](img/ca9-pc-panel-curso-tabla-movil.png), [DES-WEB](img/ca9-pc-panel-des-web-movil.png), [antes](img/ca9-pc-panel-curso-movil-antes.png) |
| 8 | Detalle del estudiante desde el panel del curso en teléfono | Cumple: 375 px. | [detalle](img/ca9-pc-detalle-estudiante-movil.png) |
| 9 | Notas y panel del curso en escritorio | Cumple: título centrado, tarjetas y tabla legible. | [notas](img/ca9-pc-notas-escritorio.png), [panel del curso](img/ca9-pc-panel-curso-escritorio.png) |

### Observaciones

1. **Notas en teléfono: corregida en `dca29aa`.** Con
   `.teacher-layout > * { min-width: 0; }` el documento vuelve al ancho de
   la ventana.
2. **Panel del curso en teléfono: corregida en `e871bbb`.** En `dca29aa`
   el documento medía 523 px en una ventana de 375 px y el título y la
   tabla quedaban cortados. El autor envolvió las dos tablas de
   `teacher_course_panel.html` en `<div class="table-scroll">` y añadió
   `.student-layout > * { min-width: 0; }`. En la misma corrección centró
   el encabezado de la práctica (`templates/tutor/practice.html`), que
   había llegado con S-007 alineado a la izquierda.
3. Los selectores de la pantalla de notas siguen sin flecha de despliegue
   (observación ya anotada sobre `3c3907a`). El selector de curso del
   inicio del estudiante sí la muestra. No bloquea.

CA-9: **cumple** en escritorio y en teléfono sobre `e871bbb`. CA-1 a CA-8
siguen verificados sobre `3c3907a`.
