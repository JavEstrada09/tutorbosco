# Verificación S-002 — Modelo de datos y datos sintéticos

Verificador: JavEstrada09 · Computadora: equipo propio con Windows y
PowerShell · Commit probado: `fa5b5ff` · PR #35.

Fecha de verificación: 09-11-2026.

| Criterio | Cómo lo probé | Resultado | Evidencia |
| --- | --- | --- | --- |
| CA-1 | Ejecuté `rebuild_synthetic_data` en una base SQLite nueva y consulté los datos. | Cumple | 30 estudiantes, 3 docentes, 4 cursos y 24 temas. Cada curso tiene 6 temas. En Programación Comercial aparecen los seis temas del enunciado. |
| CA-2 | Consulté las notas de tres perfiles sintéticos y conté los temas con nota menor que 60. | Cumple | `estudiante_demo` tiene 6 notas y 2 temas débiles. `estudiante_01` tiene 12 notas y 0 temas débiles. `estudiante_02` tiene 0 notas. |
| CA-3 | Preparé una copia aislada en mi computadora, instalé las dependencias, configuré el entorno local y ejecuté la reconstrucción sobre SQLite. | Cumple | El comando terminó con «Datos sintéticos completos reconstruidos» y produjo las cantidades y los perfiles indicados en CA-1 y CA-2. |
| CA-4 | Consulté las asignaciones de docentes y comprobé que cada nota pertenece a un curso en el que el estudiante está inscrito. | Cumple | 59 inscripciones, 4 asignaciones y 342 notas. Los 30 estudiantes están inscritos en Programación Comercial. Las asignaciones son `docente_01` → `DES-WEB` y `PROG-COM`, `docente_02` → `BD-APL`, `docente_03` → `REDES`. |
| CA-5 | Agregué registros temporales fuera del manifiesto, volví a ejecutar la reconstrucción y comparé los datos antes y después. | Cumple | Las cantidades, las claves de negocio y las notas coincidieron. Se conservaron las notas de 77 y 88, sus inscripciones y la asignación externa. Los datos temporales se revirtieron al terminar. |

## Comprobaciones adicionales

- `manage.py check` terminó sin problemas.
- `manage.py makemigrations --check --dry-run` informó `No changes detected`.
- `manage.py test accounts academics tutor` ejecutó 49 pruebas en 21.345 segundos, con resultado `OK`.

## Correcciones y repetición de pruebas

En la revisión previa se identificó que la reconstrucción podía borrar
notas y relaciones fuera del manifiesto. En `fa5b5ff` repetí la prueba con
una nota de 77 de un usuario ajeno en Programación Comercial y una nota de
88 de `estudiante_demo` en un curso ajeno. Ambas notas y sus relaciones se
conservaron. El mismo commit incorpora la resolución del conflicto en
`README.md`.
