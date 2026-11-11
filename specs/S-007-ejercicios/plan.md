# Plan S-007 — Práctica de temas débiles

Estado: aprobado por el autor en la conversación de trabajo del 2026-11-10.
Propuesto por: asistente de IA, revisado por el autor ramosdeleon555.
El autor confirmó primero el contrato con S-009 y después aprobó el plan
completo, la estructura y el inicio de la implementación en s-007-ejercicios.
La aprobación no sustituye la verificación independiente de Brayan11Hernandez.

## Enfoque

Pantalla por curso inscrito, con GET para consultar ejercicios propios y POST
con CSRF para generar. Recuperar notas vigentes mediante get_course_summaries
y get_weak_topics; no duplicar el umbral ni convertir notas ausentes a cero.
No consultar proveedores cuando no hay notas o no hay temas débiles.

Reutilizar configuración, cliente Gemini, límite de 60 segundos, un intento
y traducción de errores. Separar instrucciones de ejercicios de las del tutor.
Validar el lote completo antes de persistir: JSON estructurado, tamaño,
enunciado y tema permitido. Mostrar texto escapado. Ante indisponibilidad o
cuota, seleccionar grabaciones aplicables e informar el cambio a demo.
Una respuesta inválida se rechaza con aviso; nunca se muestra como práctica.

## Contrato confirmado con S-009 y modelo de datos

PracticeExercise en tutor: UUID estable, student, course, topic, statement,
mode (real/demo), demo_key opcional y created_at. Propietario, curso y tema
se resuelven en el servidor. S-009 referenciará este modelo para respuestas;
demo_key identifica el caso grabado sin exponer respuestas en esta entrega.
El servicio comprueba que topic pertenece a course y que student está inscrito.
No se modifica Grade ni se crean modelos de respuestas o retroalimentación.

## Archivos

- tutor/models.py y migrations/0002_*.py: persistencia de ejercicios.
- tutor/providers.py: permitir instrucciones específicas reutilizando transporte.
- tutor/exercise_providers.py: proveedor de ejercicios real y demo.
- tutor/demo_exercises.py: catálogo por curso/tema, con claves estables.
- tutor/exercise_services.py: autorización, contexto, validación y persistencia.
- tutor/exercise_views.py y academics/urls.py: pantalla, generación y consulta.
- templates/tutor/practice.html: ejercicios, estados vacíos y errores.
- templates/academics/student_home.html: enlace a práctica del curso.
- tutor/test_exercises.py: pruebas de criterios y regresión.
- README.md, docs/plan.md, docs/registro-ia.md y verificacion.md:
  recorrido y resultados reales, sin anticipar aprobación independiente.

## Tareas en orden y entregas revisables

1. Integrar main en la rama S-007 y registrar este plan aprobado.
2. Modelo, migración y catálogo demo (entrega de persistencia/datos).
3. Servicio y proveedores con pruebas de reglas y aislamiento.
4. Interfaz y pruebas de integración; comprobar el recorrido en localhost.
5. Documentar resultados; el autor revisa y ejecuta antes de solicitar commits.
6. Preparar PRs de tamaño revisable; Brayan verifica cada criterio en su equipo.
   El PR final cierra #11 solo al completar la verificación.

## Verificación por criterio

| Criterio | Prueba prevista |
| --- | --- |
| CA-1 | 45/59 incluidos; 60/85 excluidos con umbral 60. |
| CA-2 | Umbral 70: 60/69 incluidos; 70 excluido. |
| CA-3 | Tema sin nota excluido, sin convertirlo en cero. |
| CA-4 | Lote válido con enunciado y pertenencia a temas débiles del curso. |
| CA-5 | Sin notas/sin temas débiles: avisos distintos y cero consultas. |
| CA-6 | Corregir notas entre solicitudes cambia la selección. |
| CA-7 | Anónimo, docente, curso ajeno y manipulación rechazados; CSRF e aislamiento. |
| CA-8 | Demo sin cliente Gemini ni red, perfiles y cursos distintos. |
| CA-9 | Conexión/cuota simuladas; respuesta vacía/ajena rechazada; catálogo ausente. |
| CA-10 | UUID persistente, propietario, texto escapado; revisión de español/usted. |

Comandos: manage.py check; manage.py test accounts academics tutor;
manage.py makemigrations --check --dry-run; pip check. Gemini se simula
en pruebas; no se realizan consultas pagadas ni se instalan dependencias.

## Correcciones humanas al plan del agente

2026-11-10: el autor confirmó el contrato y precisó trabajar en
s-007-ejercicios. Posteriormente aprobó todo el plan y solicitó comenzar.
No se atribuye revisión ni evidencia al verificador antes de que la realice.

### Corrección tras el reporte de Brayan sobre a6bd399

Jeffersson trasladó el reporte de 2 fallos y 14 errores y solicitó corregir
la suite como autor, dejando la evidencia independiente a cargo de Brayan.
Aprobó modificar test_exercises.py, este plan y docs/registro-ia.md,
repetir ambas suites sin depender de una clave local y crear un nuevo commit.

- Cada prueba declara AI_MODE explícitamente; la configuración común de
  PracticeTests no selecciona proveedor y no impone demo a los casos reales.
- La configuración común usa GEMINI_API_KEY sintética. Es necesaria porque
  el constructor se ejecuta antes del método generate simulado: sin clave,
  el servicio activa demo y el mock real no se alcanza.
- Se conservan los casos existentes y sus aserciones; no se modifica la
  lógica de producción, la spec ni la evidencia del verificador.
- Repetir tutor.test_exercises y accounts/academics/tutor con la variable
  GEMINI_API_KEY explícitamente vacía en el proceso externo. Los casos
  simulados obtienen únicamente la clave sintética del override de pruebas.
- Brayan repetirá las suites sobre el nuevo commit antes de aprobar.

### Corrección de trato formal tras la revisión de código del PR #56

Jeffersson trasladó la revisión que detectó el rechazo de enunciados formales
válidos sin palabras de una lista literal y aprobó modificar el servicio,
sus pruebas, este plan y el registro de IA.

- Retirar la exigencia de palabras como «usted», «su» o «explique», de acuerdo
  con la decisión de S-006 (`30ad0c3`). «Defina» y «Diseñe» son formas válidas.
- Conservar detección de tuteo explícito y validaciones de estructura, tamaño,
  enunciado, HTML, duplicados y pertenencia del tema. Conservar la validación
  atómica del lote: un contenido realmente inválido impide persistirlo.
- El español y el trato formal se exigen en las instrucciones al proveedor
  y se revisan humanamente en CA-10, sin afirmar que una lista de palabras
  identifique de forma fiable el idioma o todas las formas de tratamiento.
- Añadir regresiones para «Defina…», el enunciado real sin «su» y un lote
  completo de seis enunciados formales sin los marcadores anteriores.
- Sustituir el caso en inglés que dependía de la lista retirada por más
  casos de tuteo explícito. Comprobar que las instrucciones enviadas a Gemini
  siguen exigiendo español y trato de usted.
- Repetir ambas suites sin clave real y registrar resultados del autor;
  Brayan debe realizar la repetición independiente antes de aprobar.

Es una corrección de implementación para cumplir CA-4 y CA-10; no modifica
el comportamiento especificado ni requiere cambios en spec.md.
