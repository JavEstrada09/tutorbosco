# Verificación S-004 — Gestión académica del docente

Verificador: AlexDLG1 · Computadora: equipo de AlexDLG1, Windows, Python 3.12.10 · Commit: d86b6fe

## Alcance

La implementación principal de S-004 entró a `main` en el PR #47 sin
verificación previa. Esta verificación cubre S-004 completa sobre
`d86b6fe` (PR #48), que incluye el PR #47 y la integración con
`get_taught_course` de S-005.

## Procedencia de la evidencia

- La preparación y los controles automatizados los ejecuté yo en mi
  computadora, sobre `d86b6fe` (rama local `verificacion-s004`).
- Las capturas de CA-1 a CA-8 las generó Claude (Anthropic) controlando
  el navegador en mi computadora, contra mi servidor local, con la
  cuenta `docente_01`. Revisé cada captura y su resultado antes de
  registrarlo aquí.
- La guía de pasos y la revisión de este registro se apoyaron en Claude
  (chat, Claude Opus 5.5).

## Preparación y controles

```powershell
git switch -c verificacion-s004 d86b6fe
& ".\.venv\Scripts\python.exe" manage.py migrate
& ".\.venv\Scripts\python.exe" manage.py rebuild_synthetic_data
& ".\.venv\Scripts\python.exe" manage.py test accounts academics tutor
& ".\.venv\Scripts\python.exe" manage.py check
& ".\.venv\Scripts\python.exe" manage.py makemigrations --check --dry-run
```

```text
migrate: No migrations to apply.
rebuild_synthetic_data: Datos sintéticos completos reconstruidos.
test: Ran 173 tests ... OK
check: System check identified no issues (0 silenced).
makemigrations --check --dry-run: No changes detected
```

## Resultados por criterio

| Criterio | Cómo se probó | Resultado | Evidencia |
| --- | --- | --- | --- |
| CA-1 | `docente_01` abre `/docente/cursos/`: aparecen solo DES-WEB y PROG-COM, cada uno con "Administrar temas", "Ver estudiantes" y "Consultar notas". No aparecen BD-APL ni REDES. | Cumple | [01](img/01_CA-1_mis_cursos.png) |
| CA-2 | Temas de PROG-COM: se muestran sus 6 temas. | Cumple | [02](img/02_CA-2_temas_PROG-COM_6.png) |
| CA-3 | Registro del tema "Pruebas unitarias" en PROG-COM: mensaje "El tema académico se registró correctamente." y el tema aparece en la lista. | Cumple | [03a](img/03a_CA-3_formulario_pruebas_unitarias.png), [03b](img/03b_CA-3_mensaje_registro_ok.png), [03c](img/03c_CA-3_lista_con_pruebas_unitarias.png) |
| CA-4 | El tema se modifica a "Pruebas automatizadas": mensaje "El tema académico se actualizó correctamente." y la lista muestra el nombre nuevo. | Cumple | [04a](img/04a_CA-4_edicion_pruebas_automatizadas.png), [04b](img/04b_CA-4_mensaje_actualizado_ok.png), [04c](img/04c_CA-4_lista_actualizada.png) |
| CA-5 | DES-WEB → Estudiantes: se asigna 2026-00002 (Estudiante 01); mensaje "El estudiante fue asignado correctamente." y aparece en "Estudiantes asignados". | Cumple | [06a](img/06a_CA-5_DES-WEB_estudiantes_antes.png), [06b](img/06b_CA-5_asignado_estudiante_01_ok.png) |
| CA-6 | Se repite la asignación de 2026-00002 en DES-WEB: mensaje "Este estudiante ya está asignado a este curso." y no se duplica. | Cumple | [07a](img/07a_CA-6_seleccion_repetida.png), [07b](img/07b_CA-6_asignacion_duplicada_rechazada.png) |
| CA-7 | `docente_01` abre `/docente/cursos/BD-APL/temas/` y `/docente/cursos/BD-APL/estudiantes/` (curso que no imparte): 403 "Acceso denegado" sin mostrar datos. La modificación de un tema de otro curso por POST está cubierta por las pruebas automatizadas. | Cumple | [08a](img/08a_CA-7_BD-APL_temas_403.png), [08b](img/08b_CA-7_BD-APL_estudiantes_403.png) |
| CA-8 | Tema vacío: el navegador lo bloquea ("Completa este campo"). Tema repetido "Git y GitHub avanzado": "Este tema ya está registrado en el curso." El rechazo del nombre vacío en el servidor está cubierto por las pruebas automatizadas (no se envió manualmente sin la validación del navegador). | Cumple | [05a](img/05a_CA-8_tema_vacio_rechazado.png), [05b](img/05b_CA-8_tema_duplicado_rechazado.png) |

Integración con S-005: desde `/docente/cursos/`, "Consultar notas" de
PROG-COM abre `/docente/cursos/PROG-COM/notas/`. Cumple.
[09](img/09_Notas_PROG-COM_desde_mis_cursos.png)

## Observaciones (no bloquean)

- En DES-WEB → Estudiantes, la lista para asignar muestra solo el carné
  (por ejemplo "2026-00002"), sin el nombre, e incluye estudiantes que ya
  están asignados al curso. En la pantalla de notas sí aparece
  "carné – nombre".
- `rebuild_synthetic_data` no borra el tema ni la asignación creados
  durante la prueba (mismo comportamiento reportado a douglas-yasser
  para S-002). Se borraron con `manage.py shell` al terminar.

## Integración posterior con main

Después de esta verificación, el autor integró `main` en el commit
`650bc21` (conflicto solo en `docs/registro-ia.md`). Comparé los cambios
de código de S-004 respecto de `main` en ambos commits y son idénticos;
las diferencias entre `d86b6fe` y `650bc21` provienen de lo ya fusionado
en `main` (S-006). La verificación sobre `d86b6fe` sigue siendo válida
para `650bc21`.

## Correcciones y repetición de pruebas

No se encontraron fallos que requieran corrección.
