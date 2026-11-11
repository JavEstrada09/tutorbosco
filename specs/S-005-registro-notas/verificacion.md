# Verificación S-005 — Registro y corrección de notas

Verificador: ramosdeleon555, según la asignación y la confirmación del usuario.
Computadora: equipo local de Canche, Windows 10 (compilación 19045), Python 3.12.10.
Commit probado: `1c26d94` (`1c26d94c73a7f8d2f9c475eac77852d615994c30`).
Fecha: 10-11-2026. Rama: `s-005-registro-notas`.

## Preparación y procedencia

- `git fetch origin`, `git checkout s-005-registro-notas`, `git pull` y
  `git log --oneline -1`: rama actualizada, commit `1c26d94`.
- `manage.py migrate`: no había migraciones pendientes.
- `manage.py rebuild_synthetic_data`: datos sintéticos completos reconstruidos.
- `manage.py test accounts academics tutor`: **150 pruebas OK en 208.926 s**;
  comprobación de Django sin problemas. La base de pruebas se destruyó al finalizar.
- Se comprobó la presencia de `DJANGO_SECRET_KEY`, `DEMO_STUDENT_PASSWORD`
  y `DEMO_TEACHER_PASSWORD` sin mostrar sus valores.
- Ya había un `manage.py runserver --noreload` activo en el puerto 8000;
  se identificó su proceso padre con el Python de `.venv` de este repositorio
  y se reutilizó. Se conservó ese servidor al terminar.

OpenCode ejecutó la suite y automatizó Chrome instalado mediante CDP, con
Python y Node.js existentes y auxiliares temporales autorizados fuera del
repositorio. No se instalaron dependencias. Los accesos se realizaron mediante
el formulario real con las contraseñas locales; los cierres de sesión,
mediante POST. Se desactivó la caché del navegador durante el recorrido,
en lugar de pulsar manualmente Ctrl+F5.

Las capturas provienen de la aplicación real, con sus recursos locales,
y no están editadas. CA-1 a CA-7 son capturas de página completa de Chrome;
CA-8 es una captura del escritorio con Chrome maximizado y la barra de
direcciones visible. Se comprobaron el DOM y los valores esperados antes
de capturar. Esta ejecución asistida no se presenta como un recorrido
manual realizado por el verificador ni como una aprobación de GitHub.

## Resultados por criterio

| Criterio | Cómo lo probé | Resultado | Evidencia |
| --- | --- | --- | --- |
| CA-1 | `docente_01`, PROG-COM: seleccioné `2026-00003 – Estudiante 02` (`estudiante_02`) y “Git y GitHub avanzado”, inicialmente sin nota, y envié 85. Aparecieron “Se guardó la nota 85 de Estudiante 02 en Git y GitHub avanzado.” y 85 en la planilla. Una consulta ORM confirmó un registro con 85. | Cumple en navegador automatizado y consulta de base. | [ca1.png](img/ca1.png) |
| CA-2 | En el mismo tema, `2026-00009 – Estudiante 08` (`estudiante_08`) tenía 60. Envié 75: apareció “Se actualizó la nota 75 de Estudiante 08 en Git y GitHub avanzado.” y la celda pasó a 75. La consulta ORM devolvió un solo registro y conservó su PK, de 60 a 75. | Cumple en navegador automatizado y consulta de base. | [Antes](img/ca2-antes.png), [después](img/ca2-despues.png) |
| CA-3 | Intenté reemplazar el 85 de `estudiante_02` con -5, 101, vacío y 85.5. Los errores fueron “La nota debe estar entre 0 y 100.”, “Ingrese una nota.” y “La nota debe ser un número entero.”, respectivamente. Después de cada envío comprobé 85 en la planilla y en la base. La suite también rechazó `abc`. | Cumple; los valores inválidos no cambiaron la nota. | [-5](img/ca3-menos5.png), [101](img/ca3-101.png), [vacío](img/ca3-vacio.png), [decimal](img/ca3-decimal.png); `TeacherCourseGradesViewTests.test_ca3_invalid_values_show_spanish_error_and_keep_grade` |
| CA-4 | Cerré la sesión docente, inicié sesión con `estudiante_02` y abrí `/perfil/`. En PROG-COM comprobé 85 en el tema y promedio 85.00; los otros temas continuaban sin nota. | Cumple en navegador automatizado. | [ca4.png](img/ca4.png) |
| CA-5 | Cerré la sesión del estudiante, volví a iniciar sesión con `docente_01` y abrí nuevamente la planilla de PROG-COM. Las celdas de `2026-00003` y `2026-00009` conservaron 85 y 75. | Cumple en navegador automatizado. | [ca5.png](img/ca5.png) |
| CA-6 | Abrí DES-WEB. Comprobé que `2026-00001` (Estudiante Demo) y `2026-00002` (Estudiante 01) no estuvieran ni entre las filas ni entre las opciones del selector Estudiante. | Cumple en navegador automatizado. | [ca6.png](img/ca6.png) |
| CA-7 | En DES-WEB comparé las columnas y las opciones del selector Tema con sus seis temas en la base: HTML semántico, CSS y diseño adaptable, JavaScript básico, Formularios y validación, Accesibilidad web y Despliegue local. Ambas listas coincidieron exactamente, sin temas de otros cursos. | Cumple en navegador automatizado y consulta de base. | [ca7.png](img/ca7.png) |
| CA-8 | Con `docente_01` abrí `/docente/cursos/BD-APL/notas/`: la respuesta HTTP fue 403 y mostró “Acceso denegado”. Las dos notas bajo seguimiento no cambiaron. El rechazo de POST a un curso ajeno, de estudiante no inscrito y de tema de otro curso se comprobó con las pruebas indicadas abajo; no reenvié manualmente esos formularios. | Cumple: GET en navegador y guardados no autorizados mediante la suite. | [ca8.png](img/ca8.png), con barra de direcciones; pruebas de CA-8 indicadas abajo |

### Guardados no autorizados de CA-8

Las tres pruebas de `academics.tests.TeacherCourseGradesViewTests` formaron
parte de la suite de 150 pruebas que terminó en OK:

- `test_ca8_rejects_student_not_enrolled_in_course`: POST rechazado con 400,
  mensaje en español y comparación de todas las notas antes y después.
- `test_ca8_rejects_topic_from_another_course`: POST rechazado con 400,
  mensaje en español y comparación de todas las notas antes y después.
- `test_ca8_rejects_course_taught_by_another_teacher`: POST rechazado con 403,
  “Acceso denegado” y comparación de todas las notas antes y después.

## Limpieza posterior

Después de capturar los resultados se ejecutó:

```powershell
& ".\.venv\Scripts\python.exe" manage.py rebuild_synthetic_data
& ".\.venv\Scripts\python.exe" manage.py shell -c "from academics.models import Grade; print(Grade.objects.filter(student__user__username='estudiante_02').delete())"
```

El segundo comando eliminó una nota: `(1, {'academics.Grade': 1})`.
Una consulta posterior confirmó que `estudiante_02` quedó sin notas y
`estudiante_08` volvió a tener exactamente un 60 en Git y GitHub avanzado de
PROG-COM. Las capturas reflejan los escenarios anteriores a esta limpieza.

## Correcciones y repetición de pruebas

- No se detectaron fallos de la aplicación ni se modificó su código.
- La primera ejecución de la suite fue interrumpida por el límite de
  240 segundos del comando, tras 80 puntos de progreso sin fallo visible.
  No se contó como aprobada. Se repitió completa con un límite mayor y
  finalizó con 150 pruebas OK en 208.926 segundos.
- El primer intento del auxiliar de navegador se detuvo al encontrar el
  puerto 8000 ocupado, antes de probar criterios o cambiar notas. Tras
  identificar el servidor existente, se completó el recorrido reutilizándolo.
- Se repitió únicamente la captura de CA-8 porque Chrome mostraba su aviso
  de guardar contraseña. La captura final se obtuvo con ese aviso desactivado
  en el perfil temporal del navegador, sin alterar la aplicación ni la imagen.

El commit y la publicación de esta evidencia y la aprobación del PR se
gestionan después de esta ejecución; no se registran como realizadas aquí.
