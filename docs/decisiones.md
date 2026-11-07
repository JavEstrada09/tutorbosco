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

## Decisiones confirmadas

Las decisiones D-002 a D-007, propuestas el 27-10-2026, fueron
confirmadas el 05-11-2026. Se registran como decisiones vigentes
para redactar las specs que dependen de ellas.

## D-002 · 27-10-2026

Requisito: RF-05 y RF-06.

Duda: el enunciado pide un umbral configurable de tema débil,
pero no indica su valor.

Decisión: un tema es débil cuando su nota es
estrictamente menor que 60. El valor se configura con
WEAK_TOPIC_THRESHOLD y se documenta en el README.

Por qué: 60 es la nota mínima de aprobación habitual
en la escala de 0 a 100.

## D-003 · 27-10-2026

Requisito: RF-02, RF-05 y RF-06.

Duda: un estudiante asignado a un curso puede no tener
nota en alguno de sus temas.

Decisión: un tema sin nota se muestra como
"Sin nota", no entra al promedio y no se considera débil.
Si el estudiante no tiene notas en el curso, el promedio
se muestra como "Sin notas".

Por qué: contar la ausencia de nota como 0 falsea el promedio
y genera práctica sobre temas no evaluados.

## D-004 · 27-10-2026

Requisito: RF-02 y RF-06.

Duda: el enunciado no indica cómo calcular el promedio.

Decisión: promedio simple de las notas registradas
del estudiante en los temas del curso, redondeado a dos
decimales. Se calcula en una sola función reutilizada
por el perfil, el panel y el tutor.

Por qué: no existen ponderaciones por tema en el enunciado
y un cálculo centralizado evita diferencias entre pantallas.

## D-005 · 27-10-2026

Requisito: RF-04.

Duda: el enunciado pide conservar el historial "mientras dure
la conversación", pero no define cuándo termina.

Decisión: una conversación pertenece a un estudiante
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

Decisión: el contexto enviado al modelo contiene
solo los datos del estudiante autenticado. El tutor responde
que únicamente puede hablar del perfil de quien consulta.
El modo demo incluye una respuesta grabada para este caso.

Por qué: el aislamiento se garantiza por los datos enviados,
no solo por la instrucción al modelo.

## D-007 · 27-10-2026

Requisito: RF-02 y RNF-01.

Duda: el enunciado no define el formato de carné, carrera
ni semestre.

Decisión: carné sintético con formato AAAA-NNNNN
(año de ingreso y correlativo), carrera tomada de una lista
fija de carreras inventadas o genéricas y semestre entero
de 1 a 10.

Por qué: son datos claramente sintéticos y suficientes para
distinguir perfiles en RF-02.

## D-008 · 05-11-2026

Estado: confirmada el 06-11-2026.

Requisito: RF-03.

Duda: el enunciado no dice si la nota admite decimales ni qué
ocurre cuando el docente corrige una nota ya registrada.

Decisión: la nota es un número entero de 0 a 100.
Cada estudiante tiene una sola nota por tema; corregirla reemplaza
la anterior y no se guarda historial.

Por qué: la escala entera de 0 a 100 evita ambigüedades al registrar
y al comparar con el umbral de tema débil (D-002), y un único
registro por estudiante y tema asegura que el perfil, el tutor y
el panel lean siempre la nota vigente.

## D-009 · 05-11-2026

Requisito: RF-01, RF-04 y RF-06.

Duda: el enunciado exige dos roles, estudiante y docente, pero no
indica cómo representarlos en el modelo de usuario.

Decisión: el rol se determina por el perfil asociado. Un usuario con
StudentProfile es estudiante; uno con TeacherProfile es docente.
No se agrega un campo de rol a User. El sistema asume un perfil por
cuenta; si se necesitara una cuenta con ambos, se registrará una nueva
decisión. Un usuario sin perfil no accede a vistas de rol y los
permisos se verifican en el servidor.

Por qué: conserva User sin campos adicionales, usa los perfiles que
S-001 y S-002 ya necesitan y permite verificar el rol en cada operación.

Actualización: D-010 sustituye únicamente la suposición de un perfil por
cuenta. La representación de roles mediante perfiles y la verificación
de permisos en el servidor continúan vigentes.

## D-010 · 06-11-2026

Requisito: RF-01.

Estado: aprobada por JavEstrada09 el 06-11-2026, antes de implementar
S-001.

Antecedente: esta decisión se registró inicialmente como D-008 en la
rama de S-001. Al integrar `main`, se renumeró como D-010 porque D-008
y D-009 ya estaban ocupadas. La renumeración no cambia su fecha,
aprobación ni contenido.

Duda: cómo representar los roles de estudiante y docente sin acoplar
la autenticación a un único rol ni impedir casos en los que una misma
cuenta necesite ambos.

Decisión: `accounts.User` representa la cuenta de autenticación. Cada
rol se representa mediante un perfil relacionado, comenzando con
`academics.StudentProfile` para el estudiante. Los perfiles no son
mutuamente excluyentes: una cuenta puede tener más de uno.

D-010 sustituye únicamente la suposición de un perfil por cuenta de
D-009. La existencia de un perfil identifica el rol, pero no concede por
sí sola acceso a cursos o estudiantes. Los permisos se comprueban en el
servidor en cada operación.

Por qué: separar cuenta y perfiles permite compartir autenticación sin
duplicar usuarios, ampliar los datos propios de cada rol y evitar una
restricción de exclusividad que el equipo no ha requerido.
