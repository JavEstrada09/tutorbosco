# Decisiones de interpretación

## D-001 — Inicialización del repositorio

Requisito: N1 y N2.

Duda: el enunciado exige pull requests y no describe cómo
inicializar un repositorio vacío sin una rama base.

Decisión: crear un único commit inicial con README,
.gitignore y este registro. Después, proteger main
y realizar todos los cambios mediante pull requests.

Justificación: establecer una base documental para poder
abrir y revisar los siguientes pull requests.
Este commit no incluye código de la aplicación.

## Propuestas pendientes de confirmar

Las decisiones D-002 a D-007 son propuestas para revisión
en el PR de ajustes de estructura. El equipo las confirma
o corrige antes de redactar las specs que dependen de ellas.

## D-002 · 27-10-2026

Requisito: RF-05 y RF-06.

Duda: el enunciado pide un umbral configurable de tema débil,
pero no indica su valor.

Decisión propuesta: un tema es débil cuando su nota es
estrictamente menor que 60. El valor se configura con
WEAK_TOPIC_THRESHOLD y se documenta en el README.

Por qué: 60 es la nota mínima de aprobación habitual
en la escala de 0 a 100.

## D-003 · 27-10-2026

Requisito: RF-02, RF-05 y RF-06.

Duda: un estudiante asignado a un curso puede no tener
nota en alguno de sus temas.

Decisión propuesta: un tema sin nota se muestra como
"Sin nota", no entra al promedio y no se considera débil.
Si el estudiante no tiene notas en el curso, el promedio
se muestra como "Sin notas".

Por qué: contar la ausencia de nota como 0 falsea el promedio
y genera práctica sobre temas no evaluados.

## D-004 · 27-10-2026

Requisito: RF-02 y RF-06.

Duda: el enunciado no indica cómo calcular el promedio.

Decisión propuesta: promedio simple de las notas registradas
del estudiante en los temas del curso, redondeado a dos
decimales. Se calcula en una sola función reutilizada
por el perfil, el panel y el tutor.

Por qué: no existen ponderaciones por tema en el enunciado
y un cálculo centralizado evita diferencias entre pantallas.

## D-005 · 27-10-2026

Requisito: RF-04.

Duda: el enunciado pide conservar el historial "mientras dure
la conversación", pero no define cuándo termina.

Decisión propuesta: una conversación pertenece a un estudiante
y a un curso. Dura hasta que el estudiante inicia una nueva
conversación o cierra sesión. Cada nueva conversación
recupera las notas vigentes del estudiante.

Por qué: permite la pregunta de seguimiento de RF-04 y
asegura que un cambio de nota se refleje en la siguiente
conversación (RF-03).

## D-006 · 27-10-2026

Requisito: RNF-05.

Duda: qué debe responder el tutor cuando un estudiante pide
datos de otro estudiante.

Decisión propuesta: el contexto enviado al modelo contiene
solo los datos del estudiante autenticado. El tutor responde
que únicamente puede hablar del perfil de quien consulta.
El modo demo incluye una respuesta grabada para este caso.

Por qué: el aislamiento se garantiza por los datos enviados,
no solo por la instrucción al modelo.

## D-007 · 27-10-2026

Requisito: RF-02 y RNF-01.

Duda: el enunciado no define el formato de carné, carrera
ni semestre.

Decisión propuesta: carné sintético con formato AAAA-NNNNN
(año de ingreso y correlativo), carrera tomada de una lista
fija de carreras inventadas o genéricas y semestre entero
de 1 a 10.

Por qué: son datos claramente sintéticos y suficientes para
distinguir perfiles en RF-02.
