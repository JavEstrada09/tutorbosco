# S-006 Tutor personalizado

Requisito: RF-04; RNF-05 · Autor: JavEstrada09 · Verificador: douglas-yasser · Issue: #10
Estado: Terminada

## Problema

Una respuesta genérica del tutor puede explicar un tema, pero no
orienta al estudiante sobre qué debe reforzar según sus notas.
Además, el estudiante necesita hacer preguntas de seguimiento sin
volver a explicar de qué tema estaba hablando.

## Comportamiento esperado

Como estudiante, quiero conversar con el tutor sobre uno de mis
cursos para recibir explicaciones y ejemplos acordes con mis notas
y seguir preguntando sobre el mismo tema.

Al iniciar una conversación, el tutor consulta las notas vigentes
del estudiante autenticado para el curso seleccionado. Cuando la
pregunta lo permite, profundiza en los temas con nota inferior al
umbral configurado. Si faltan notas, puede explicar el tema
solicitado e indica que aún no tiene calificaciones suficientes
cuando el estudiante le pide identificar qué necesita reforzar.

La conversación pertenece al estudiante y al curso seleccionado.
El tutor usa el historial de esa conversación para las preguntas
de seguimiento. Cambiar de curso mantiene separados los hilos.
Al volver a un curso durante la misma sesión, el estudiante puede
retomar su conversación activa. La opción «Nueva conversación»
reinicia el hilo del curso seleccionado y vuelve a consultar las
notas. Cerrar sesión termina todas las conversaciones activas.

En modo demo, el tutor utiliza respuestas grabadas que distinguen
perfiles, permiten hacer preguntas de seguimiento y cubren las
solicitudes de datos de otro estudiante. Cada respuesta del tutor
identifica el curso y se dirige al estudiante de usted, en español.

## Criterios de aceptación

CA-1 Dado que dos estudiantes están inscritos en el mismo curso y
     tienen notas bajas en temas distintos,
     cuando ambos inician su propia conversación y preguntan
     «¿Qué tema debería repasar?»,
     entonces cada uno recibe una explicación o un ejemplo sobre
     su propio tema con nota baja. La diferencia se observa en el
     tema que se recomienda y en el ejemplo o la explicación.

CA-2 Dado que el tutor explicó un tema del curso,
     cuando el estudiante pregunta «¿Me da otro ejemplo?»,
     entonces recibe un ejemplo adicional sobre ese mismo tema.
     Si cambia de curso, el tutor utiliza solo el hilo de ese
     curso. Al volver al primero en la misma sesión, puede
     continuar el hilo que dejó allí.

CA-3 Dado que la nota de un tema cambió y esa corrección modifica
     qué tema debe reforzar el estudiante,
     cuando selecciona «Nueva conversación» para el mismo curso,
     entonces el tutor usa las notas corregidas y orienta al
     estudiante según ellas, sin reutilizar los mensajes del hilo
     anterior. Si cierra sesión y vuelve a entrar, también inicia
     sin los mensajes de la sesión anterior.

CA-4 Dada una solicitud sin sesión, de un docente o dirigida a un
     curso no asignado o a una conversación de otro estudiante,
     cuando el servidor procesa la solicitud, incluso si se
     modificaron identificadores en la petición,
     entonces bloquea el acceso a esa operación sin mostrar notas
     ni historial y sin consultar al proveedor. En una solicitud
     válida, el contexto académico y el historial enviados al
     proveedor corresponden al estudiante autenticado y al curso
     seleccionado.

CA-5 Dado que un estudiante pide al tutor las notas o el perfil de
     otra persona,
     cuando el tutor responde en modo real o en modo demo,
     entonces explica que solo puede hablar del perfil del
     estudiante que consulta. No revela ni inventa datos de
     terceros.

CA-6 Dado que el modo demo está activo, sin conexión y sin clave
     de IA,
     cuando dos estudiantes con distintos temas de dificultad
     hacen la misma pregunta y luego piden otro ejemplo,
     entonces cada uno recibe respuestas grabadas acordes con su
     curso y perfil, y el seguimiento conserva el tema tratado.
     El recorrido se completa sin llamadas externas.

CA-7 Dado que un estudiante tiene un curso sin notas o cuyas
     notas registradas alcanzan el umbral,
     cuando pregunta qué tema debe reforzar,
     entonces el tutor distingue entre falta de notas y ausencia
     de temas bajo el umbral. Si el estudiante pide una
     explicación, el tutor puede ayudarle con el tema del curso.
     Los temas sin nota no se tratan como si tuvieran cero.

CA-8 Dado que el proveedor real devuelve una respuesta vacía o
     inválida, falla la conexión o se agota la cuota,
     cuando el estudiante envía una pregunta,
     entonces el tutor muestra un aviso en español y ofrece
     continuar en modo demo, según el flujo de S-001. Si el
     estudiante usa esa opción, conserva el curso y el hilo
     válidos. Si no existe una respuesta grabada aplicable,
     se indica esa situación sin mostrar datos de otro perfil.

CA-9 Dada una respuesta válida en modo real o en modo demo,
     cuando se muestra al estudiante,
     entonces identifica el curso, está en español y usa el
     trato de usted.

## Fuera de alcance

- Registrar o corregir notas y administrar cursos o asignaciones
  desde las pantallas del docente.
- Generar ejercicios, recibir respuestas a ejercicios o calificarlas.
- Consultar conversaciones de sesiones anteriores o exportarlas.
- Cambiar el modelo predeterminado, el presupuesto o el proveedor
  de IA del proyecto.

## Datos y restricciones

- Usar únicamente datos sintéticos (RNF-01).
- Aplicar D-005 y D-006 de `docs/decisiones.md` para el ciclo de la
  conversación y el aislamiento de datos. Aplicar el umbral
  configurable de D-002 y el tratamiento de temas sin nota de D-003.
- Validar en el servidor el rol, la inscripción al curso y la
  pertenencia de la conversación. Mantener la protección CSRF.
- Enviar desde el backend solo las notas, los temas y los datos de
  perfil necesarios para orientar al estudiante autenticado en el
  curso elegido, junto con los mensajes pertinentes de ese hilo.
  Excluir claves, contraseñas, identificadores personales
  innecesarios y datos académicos de otras personas (RNF-02 y RNF-05).
- Uso de IA del producto: sí. Mantener el modelo configurable con
  Gemini 3.5 Flash-Lite como valor predeterminado. Validar las
  respuestas antes de mostrarlas. Mantener los límites y el manejo
  de fallos de S-001, y registrar el gasto real (RNF-03).
- Utilizar respuestas y recursos locales en modo demo (RNF-04).
  Todo texto dirigido al estudiante debe estar en español y usar
  el trato de usted (RNF-07).
- Dependencias del issue #10: S-001 para la autenticación y los
  proveedores de IA y demo, y S-002 para el modelo académico y los
  datos sintéticos. El servicio académico ya integrado por S-003
  se puede reutilizar. La actualización de notas se verifica con
  datos sintéticos, de forma independiente a la pantalla de S-005.

## Registro de cambios

10-11-2026 · Borrador inicial a partir del issue #10, el plan del
equipo y las decisiones D-005 y D-006. Se propone conservar el
hilo de cada curso al cambiar entre cursos durante la misma sesión.

10-11-2026 · JavEstrada09 aprobó el plan técnico. Se inicia el bloque de
validación del umbral y acceso al tutor por curso inscrito.


10-11-2026 · Cierre documental por JavEstrada09 tras la verificación
independiente de douglas-yasser. Los nueve criterios tienen resultado
satisfactorio: CA-2, CA-3, CA-4, CA-6, CA-7 y CA-8 se comprobaron sobre
`ece9dee`; CA-1, CA-5 y CA-9 se repitieron satisfactoriamente con Gemini
real sobre `30ad0c3`, que también pasó las 191 pruebas. El fallo inicial
y su corrección se conservan en `verificacion.md`. Implementación y
evidencia integradas en `main` mediante el PR #53 (`6bf31b6`).
