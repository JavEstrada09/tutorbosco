# Verificación S-008 · Panel del docente

- PR #44 · Issue #12.
- Autor: douglas-yasser · Verificador asignado: JavEstrada09.
- Commit comprobado en la revisión técnica: `9126626`.
- Revisión funcional de JavEstrada09 en Windows: completada para CA-1 a CA-5.

## Revisión técnica de apoyo

Codex ejecutó esta revisión el 10-11-2026 en una copia aislada de Linux
con Python 3.12.14, Django 5.2.19, SQLite nueva y datos sintéticos
reconstruidos. Se instalaron las dependencias fijadas por el repositorio.
Se usó el cliente HTTP de Django para iniciar sesión y solicitar las
vistas. Los resultados académicos se cotejaron con las notas almacenadas
en SQLite y con cálculos independientes del servicio del panel.

| Criterio | Comprobación técnica | Resultado en Linux |
| --- | --- | --- |
| CA-1 | Inicié sesión como `docente_01` y abrí el panel de `PROG-COM`. Cotejé todas las filas, promedios y temas débiles contra las notas de la base de prueba. | Cumple. 30 estudiantes. `estudiante_demo` tiene promedio 78.00 y dos temas débiles, Git y GitHub avanzado y Código limpio y refactoring. La página indica «Sin notas» cuando corresponde. |
| CA-2 | Solicité el panel ordenado por promedio ascendente y descendente y comparé las secuencias completas contra los promedios calculados de forma independiente. | Cumple. El primer promedio ascendente fue 64.17 y el descendente 80.83. Los estudiantes sin notas quedaron al final en ambos casos. |
| CA-3 | Abrí el detalle de `estudiante_demo` desde su ruta en `PROG-COM` y comparé el promedio y los temas con las notas de la base. | Cumple. El detalle muestra 78.00 y los mismos dos temas débiles. |
| CA-4 | Conté por tema los estudiantes inscritos con nota menor de 60 y comparé los seis resultados con el desglose del panel. | Cumple. En orden de aparición, 6, 7, 5, 6, 6 y 6 estudiantes. |
| CA-5 | Solicité directamente el panel y el detalle de un curso ajeno, el detalle de un estudiante sin inscripción en un curso propio y las rutas del panel con una cuenta estudiantil. | Cumple. Las solicitudes devolvieron HTTP 403. El inicio de sesión del estudiante siguió dirigiendo a su espacio. |

Las 110 pruebas de `accounts academics tutor` pasaron. También se
completaron `migrate` y `rebuild_synthetic_data`. `manage.py check`
terminó sin incidencias, `makemigrations --check --dry-run` sin cambios
y `python -m pip check` sin dependencias rotas.

## Verificación de JavEstrada09 en Windows

Revisión funcional del 10-11-2026 en Windows. Las capturas y
confirmaciones de JavEstrada09 sustentan los resultados de esta sección.
La versión exacta de Python y el commit del entorno local no se registraron
en las capturas.

Con una base sintética reconstruida y umbral 60, iniciar sesión como
`docente_01` en `/acceso/`. Debe aparecer el panel con `PROG-COM` y
`DES-WEB`. Los resultados de la sección anterior sirven de referencia
para las siguientes comprobaciones.

| Criterio | Qué comprobar en Windows | Resultado y evidencia |
| --- | --- | --- |
| CA-1 | Abrir `/docente/panel/PROG-COM/`. Buscar el carné `2026-00001` desde «Ver detalle» si el listado muestra el nombre en vez del usuario. Cotejar el promedio con las notas 55, 58, 90, 92, 88 y 85. Las dos primeras corresponden a los dos temas bajo el umbral. | Cumple en la comprobación visual. Las capturas muestran los promedios y los temas débiles del listado. Estudiante Demo aparece con 78.00 y dos temas débiles, en concordancia con los datos de referencia. El listado completo se cotejó en la revisión técnica de Linux. |
| CA-2 | Pulsar ambos enlaces de orden por promedio. Comprobar el primer promedio y que «Sin notas» permanece al final en ambos órdenes. | Cumple. Las capturas muestran 64.17 al inicio del orden ascendente y 80.83 al inicio del descendente. JavEstrada09 confirmó que Estudiante 02 («Sin notas») queda al final en ambos órdenes. |
| CA-3 | Abrir «Ver detalle» de un estudiante y cotejar promedio y temas débiles con su fila. | Cumple según la captura. El detalle de Estudiante 20, carné `2026-00021`, muestra 64.17, Git y GitHub avanzado y El LLM por dentro y su API. Coincide con su fila del orden ascendente. |
| CA-4 | Revisar la tabla «Temas débiles por tema» y cotejar los seis conteos con la revisión técnica. | Cumple según la captura. Los seis conteos son 6, 7, 5, 6, 6 y 6, en el orden mostrado. |
| CA-5 | Como `docente_01`, abrir directamente `/docente/panel/BD-APL/` y su ruta de detalle con el identificador tomado de un enlace válido. Luego cerrar sesión, entrar como `estudiante_demo` e intentar abrir `/docente/panel/PROG-COM/`. Confirmar HTTP 403 en la pestaña Red del navegador para cada solicitud denegada. | Cumple en las dos comprobaciones de acceso al panel. Con `docente_01`, Bases de Datos Aplicadas devolvió 403. En una sesión nueva de incógnito con `estudiante_demo`, la captura muestra «403 · Acceso denegado» en `/docente/panel/PROG-COM/`. Las comprobaciones adicionales de la ruta de detalle se ejecutaron en Linux. |

## Correcciones y repetición de pruebas

Se repitió el acceso a Programación Comercial en una sesión nueva de
incógnito para confirmar qué cuenta estaba activa. Con la cuenta
estudiantil, el servidor denegó el acceso según lo esperado.
