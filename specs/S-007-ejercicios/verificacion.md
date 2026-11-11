# Verificación S-007

Estado: implementación local probada en demo y con Gemini real;
pendiente de revisión final y verificación independiente.
Verificador previsto: Brayan11Hernandez.
Computadora: pendiente · Commit probado: pendiente.

| Criterio | Cómo lo probé | Resultado | Evidencia |
| --- | --- | --- | --- |
| CA-1 | Pendiente | No ejecutado | Pendiente |
| CA-2 | Pendiente | No ejecutado | Pendiente |
| CA-3 | Pendiente | No ejecutado | Pendiente |
| CA-4 | Pendiente | No ejecutado | Pendiente |
| CA-5 | Pendiente | No ejecutado | Pendiente |
| CA-6 | Pendiente | No ejecutado | Pendiente |
| CA-7 | Pendiente | No ejecutado | Pendiente |
| CA-8 | Pendiente | No ejecutado | Pendiente |
| CA-9 | Pendiente | No ejecutado | Pendiente |
| CA-10 | Pendiente | No ejecutado | Pendiente |

## Correcciones y repetición de pruebas

Pendientes de la verificación independiente. Las comprobaciones locales
del asistente se registran en las secciones siguientes.

El verificador debe ser distinto del autor y ejecutar cada criterio
en su computadora con el commit indicado. Registrará los fallos,
el commit de corrección y el resultado de la nueva prueba.

## Comprobaciones locales de implementación · 2026-11-10

Ejecutadas por el asistente OpenCode en la sesión del autor, Windows,
workspace `C:\Users\Canche\Desktop\tutorbosco`, rama s-007-ejercicios.
Cambios sin commit, sobre main `47a7977`; no se atribuye un commit probado
ni una verificación independiente a Brayan11Hernandez.

- `manage.py test tutor.test_exercises --verbosity 1`: 19 pruebas,
  OK, 0.673 segundos. CA-1 a CA-10 se cubren mediante casos automatizados;
  español, trato de usted y presentación requieren además revisión humana.
- `manage.py test accounts academics tutor --noinput`: 215 pruebas,
  OK, 254.688 segundos. La primera ejecución fue interrumpida por el límite
  de 120 segundos de la herramienta; la repetición con mayor tiempo terminó.
- `manage.py check`: sin errores.
- `manage.py makemigrations --check --dry-run`: sin cambios pendientes.
- `python -m pip check`: sin requisitos incompatibles.
- `manage.py migrate`: tutor.0002_practiceexercise aplicada correctamente.
- Recorrido HTTP real en `127.0.0.1:8000`, con cookies y CSRF: inicio de
  sesión de estudiante_03, GET de práctica, POST de generación demo y
  consulta individual por UUID. HTTP 200; se creó un ejercicio propio
  grabado y se comprobó la etiqueta del modo demo. No se imprimieron
  contraseñas ni claves. Se conserva ese ejercicio sintético en la base local.

En esta primera comprobación, las pruebas de proveedor real simularon
las respuestas y el error 429, sin consultar Gemini ni consumir cuota.
La llamada real posterior se detalla a continuación.
El recorrido se comprobó mediante HTTP, sin revisión visual en navegador.

## Prueba real con Gemini · 2026-11-10

Ejecutada por OpenCode en la sesión del autor, a solicitud de este.
Equipo y rama: mismo workspace Windows y s-007-ejercicios de la comprobación
local anterior. Cambios todavía sin commit; no constituye verificación
independiente ni aprobación de Brayan11Hernandez.

### Preparación y recorrido

1. Se comprobó la presencia de una clave local sin mostrarla y el modelo
   configurado `gemini-3.5-flash-lite`.
2. Se inició un servidor temporal en `127.0.0.1:8001` con `AI_MODE=real`
   únicamente en su entorno de proceso. No se modificó `.env`.
3. Se inició sesión mediante HTTP como `estudiante_03`, usando cookies y
   la contraseña local sin imprimirla. Se consultó la pantalla de práctica.
4. Se envió una sola solicitud de generación mediante POST con token CSRF
   a `/practica/PROG-COM/`. Se compararon los UUID anteriores y posteriores
   para identificar el ejercicio nuevo.
5. Se comprobó la respuesta HTTP, el aviso y la etiqueta de procedencia,
   y se consultó el registro persistido para recuperar el enunciado completo,
   propietario, curso, tema, fecha y modo.
6. Se detuvo el servidor temporal. El servidor habitual en el puerto 8000
   continuó disponible, en modo demo y con el ejercicio real guardado.

### Datos y resultados

| Dato | Resultado observado |
| --- | --- |
| Fecha local | 10-11-2026, 19:44, Guatemala (UTC−06:00) |
| Fecha de persistencia UTC | `2026-11-11T01:44:04.025239+00:00` |
| Modelo configurado para la llamada | `gemini-3.5-flash-lite` |
| Usuario sintético | `estudiante_03` |
| Curso | `PROG-COM` — Programación Comercial |
| Tema débil permitido | Ingeniería de prompts |
| Nota consultada al comprobar el ejercicio | 58 |
| Umbral configurado | 60; el tema cumple `58 < 60` |
| Duración HTTP de la generación y redirección | 6,12 segundos |
| Respuesta HTTP final | 200 |
| Ejercicios nuevos persistidos | 1 |
| Procedencia persistida | `real` |
| `demo_key` | Vacío |
| Aviso de alternativa demo | No apareció |
| Aviso de práctica inválida | No apareció |
| Etiqueta en el HTML recibido | Ejercicio generado por IA |
| UUID | `04ee22d6-a90a-485a-ae8e-0d227530cb94` |

### Respuesta completa de Gemini: enunciado validado y guardado

> Diseñe un prompt estructurado utilizando la técnica de pocos ejemplos (few-shot prompting) para que un modelo de lenguaje extraiga correctamente los datos fiscales de una factura en formato de texto libre y los devuelva en un formato JSON estandarizado para su posterior registro contable.

Esta es la respuesta a la solicitud de generar práctica: un ejercicio para
que lo resuelva el estudiante. Su solución y posterior retroalimentación
corresponden a S-009. El texto se recuperó del registro persistido; no se
conservó la respuesta HTTP original ni el JSON crudo del proveedor.

Consulta local, tras iniciar sesión con la misma cuenta:
`http://127.0.0.1:8000/practica/PROG-COM/?exercise=04ee22d6-a90a-485a-ae8e-0d227530cb94`.
El UUID identifica un registro de esta base local; otra instalación no lo
contendrá automáticamente y deberá generar sus propios ejercicios.

### Alcance de la evidencia

- La llamada real produjo un enunciado válido y pertinente al tema débil
  del curso seleccionado, aportando evidencia local para CA-4.
- El texto está en español y usa trato formal («Diseñe»); se comprobó
  UUID, propietario, curso y tema, aportando evidencia local para CA-10.
- La persistencia y la etiqueta `real`, sin aviso de fallback y sin
  `demo_key`, distinguen este resultado de la generación grabada.
- El autor informó previamente que probó el modo demo y que le pareció
  correcto; no se atribuye a ese comentario la verificación de cada criterio.
- El recorrido real se comprobó mediante HTTP; no se adjunta captura ni se
  declara revisión visual de esta llamada en navegador.
- Se realizó una solicitud real. Tokens y costo monetario no recuperados:
  pendientes de confirmar con los registros del proveedor (véase docs/gasto.md).
- No se provocaron fallos reales de cuota ni conexión en esta llamada.
  Esos casos se cubrieron mediante simulaciones automatizadas.
- Una generación exitosa no prueba los diez criterios completos; la matriz
  de verificación independiente permanece pendiente.

### Guía para la verificación independiente

1. Registrar equipo y commit recibido; aplicar migraciones en su instalación.
2. Ejecutar las pruebas y recorrer la pantalla con estudiantes distintos.
3. Para CA-1 a CA-3, preparar notas sintéticas 45/59/60/85 y un tema sin
   nota; repetir con umbral 70 y notas 60/69/70.
4. Para CA-4/CA-5/CA-6, generar, comprobar curso/tema, probar estados sin
   notas y sin temas débiles, corregir notas desde el docente y regenerar.
5. Para CA-7, comprobar rechazo de docente, curso ajeno, UUID ajeno,
   propietario manipulado y POST sin CSRF; revisar contexto con proveedor simulado.
6. Para CA-8/CA-9, ejecutar demo sin clave y sin red; revisar pruebas de
   cuota/conexión, salida inválida y catálogo ausente.
7. Para CA-10, revisar español/usted, UUID estable y propietario, escape de
   texto y que las notas oficiales no cambien.
8. Completar la matriz anterior con evidencia propia; no sustituirla por
   estos resultados locales del asistente.
