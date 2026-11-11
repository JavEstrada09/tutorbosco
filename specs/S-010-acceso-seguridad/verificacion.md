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

## Ampliación de interfaz · pendiente de verificación

El 11-11-2026 se amplió S-010 con CA-9: el rediseño visual cubre todas las
pantallas y ya no solo la navegación común. El informe anterior sigue siendo
válido para CA-1 a CA-8 sobre `3c3907a`, pero las capturas de CA-8 ya no
reflejan el aspecto actual y CA-9 no tiene evidencia todavía.

Estado: **sin verificar**. No se registran resultados, capturas ni
aprobaciones de esta ampliación hasta que AlexDLG1 la ejecute en su
computadora.

Pasos previstos para la nueva verificación:

```powershell
git switch verificacion-s010
git pull --ff-only
& ".\.venv\Scripts\python.exe" manage.py check
& ".\.venv\Scripts\python.exe" manage.py test accounts academics tutor
& ".\.venv\Scripts\python.exe" manage.py makemigrations --check --dry-run
& ".\.venv\Scripts\python.exe" manage.py runserver
```

Recorrido de CA-9 en escritorio y en ancho reducido:

1. `/acceso/` y credenciales incorrectas.
2. Inicio y perfil de `estudiante_demo`.
3. `/docente/panel/` y `/docente/cursos/` como estudiante (403).
4. Panel, mis cursos, notas, temas y estudiantes con `docente_01`.
5. Comprobar títulos centrados, botones identificables, tablas legibles y la
   misma cabecera en todas las pantallas.

Pendiente de completar por el verificador: commit probado, resultado de cada
paso, capturas y observaciones.
