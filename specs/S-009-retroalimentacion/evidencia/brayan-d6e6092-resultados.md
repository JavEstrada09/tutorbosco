# Verificación asistida de d6e6092

Fecha: 2026-11-11. Verificador designado: Brayan11Hernandez.
Ejecución técnica: OpenCode en el equipo del verificador.
Commit exacto: `d6e6092e2fd243b1cfb45de15c7cc0d027af9331`.

El usuario aprobó la estructura de evidencia y las nueve capturas mediante
«Hazlo, apruebo». Esto autoriza esta ejecución; no constituye una aprobación
final de resultados, de la excepción de tamaño ni de una llamada real a Gemini.

## Resultados reproducidos

- Python 3.12.10 reutilizado, sin instalar dependencias.
- `manage.py check`: sin problemas.
- `manage.py makemigrations --check --dry-run`: sin cambios.
- `python -m pip check`: sin incompatibilidades.
- `manage.py test tutor.test_feedback --verbosity 2`: 27 pruebas, OK, 1.785 s.
- `manage.py test accounts academics tutor`: 244 pruebas, OK, 147.893 s.
- Nueve PNG reales obtenidos en Edge mediante CDP, sin Selenium ni Playwright.
- Cinco intentos persistidos en la base final; 342 notas sin cambios durante
  el recorrido. Consultas en `brayan-d6e6092-consultas.json`.

| Criterio | Evidencia nueva | Resultado técnico y alcance |
| --- | --- | --- |
| CA-1 | Prueba de persistencia/propiedad; capturas 01/03; consultas JSON | PASS: asociaciones derivadas del ejercicio. |
| CA-2 | Prueba de entradas vacías y excesivas; captura 02; cinco intentos finales | PASS: validación, sin respuesta vacía ni llamada al proveedor. |
| CA-3 | Pruebas de respuesta y transporte; capturas 03/04 | PASS demo y transporte simulado. Calidad de Gemini real pendiente en este commit. |
| CA-4 | Pruebas de contexto privado vigente y apoyo; capturas 05/06 | PASS: nota 25 recibe «Construya cuatro líneas»; nota 55 recibe «Pruebe el prompt». |
| CA-5 | Prueba de intentos/cursos separados; captura 06; UUID distintos en JSON | PASS: consultar el acierto conserva su devolución tras registrar el error. |
| CA-6 | Pruebas de anónimo, docente, ajeno, inexistente, curso, CSRF y relaciones; captura 07 | PASS: rechazo sin escrituras ni llamadas no autorizadas en pruebas instrumentadas. |
| CA-7 | Prueba offline y 24 casos; capturas 03/04 | PASS automatizado: demo sin clave; bloqueo de sockets en prueba. El navegador no se ejecutó con la red física desconectada. |
| CA-8 | Pruebas de fallos simulados y alternativa demo; captura 08 | PASS simulado. La captura demuestra ausencia de caso aplicable, no una cuota real agotada. |
| CA-9 | Prueba de salidas inválidas conservando respuesta | PASS simulado; la captura 08 no sustituye esta prueba. |
| CA-10 | Prueba de escape/notas; captura 09; comparación de 342 notas | PASS técnico demo: contenido literal, español, trato formal y curso. |

## Procedencia y aislamiento

El worktree aprobado ya existía, limpio y fijado al commit exacto. También
existía la base con el nombre originalmente propuesto; se eligieron bases
nuevas con sufijo aleatorio, sin reconstruir aquella base. La ruta de la base
final está en `brayan-d6e6092-entorno.txt`. Cada repetición de capturas utilizó
una base nueva. Las pruebas Django utilizaron su base temporal en memoria.
Las notas 25/55 se prepararon como datos sintéticos antes de medir cambios.
Los ejercicios del navegador se prepararon con el catálogo demo de S-007;
el recorrido visual no pretende verificar de nuevo su generación.

Los archivos `brayan-360da36-*` son copias byte a byte de los tres archivos
históricos del worktree anterior. Sus resultados y llamada real pertenecen
exclusivamente a `360da36`. No se trasladan a este commit.

## Correcciones del arnés y observaciones

El registro conserva los intentos fallidos y la ejecución final correcta.
Se corrigieron: limpieza de perfil Edge bloqueado; puertos fijos que podían
conectar a procesos previos; espera de carga; comparación de etiqueta afectada
por mayúsculas CSS; texto detallado correspondiente a otro ejercicio; y texto
esperado «Acceso no permitido», cuyo valor real es «Acceso denegado».
No se modificó código de la aplicación para superar esas comprobaciones.
Las suites ya correctas no se repitieron para corregir el arnés visual.

Observación visual: el aviso de guardado correcto aparece en rojo, igual que
avisos de error. Es comprensible por su texto, pero conviene que el autor
revise la distinción visual de éxito/error. La captura 09 prioriza el texto
escapado y no incluye todo el historial inferior; el historial se ve en 06.

## Pendientes y decisión de tamaño

No se hizo ninguna llamada real nueva. La corrección de instrucciones y sus
aserciones no demuestran que Gemini haya corregido el exceso de exigencia
pedagógica observado en `360da36`. Esa comprobación requiere autorización
separada y una revisión humana de la respuesta.

El tamaño previamente informado del PR (1924 adiciones, 31 eliminaciones,
18 archivos) excede la referencia revisable. La decisión expresa de aceptar
esa excepción sigue pendiente; esta ejecución no equivale a una revisión
técnica completa de todos los cambios del PR ni a su aprobación final.

Uso de IA: OpenCode preparó el arnés temporal, ejecutó pruebas, automatizó
Edge y redactó esta evidencia. El usuario debe revisar los resultados y
capturas antes de registrar su aprobación. No se realizaron commits ni push.
