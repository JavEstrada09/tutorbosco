# S-003 Perfil académico del estudiante

Requisito: RF-02 · Autor: AlexDLG1 · Verificador: ramosdeleon555 · Issue: #7
Estado: en verificación; implementación fusionada, registro independiente en revisión.

## Problema

La información académica de cada estudiante existe dispersa en notas y hojas de cálculo. El estudiante no tiene un lugar donde ver, en conjunto, sus datos, los cursos que lleva y cómo le va en cada tema.

## Comportamiento esperado

Como estudiante, quiero ver mi perfil académico para saber en qué temas voy bien y en cuáles necesito reforzar.

El perfil muestra:

- Mis datos: nombre, carné, carrera y semestre.
- Los cursos que llevo.
- Dentro de cada curso: mi nota (escala de 0 a 100) en cada tema y mi promedio del curso.

Reglas de presentación (tomadas de las decisiones D-003 y D-004 de docs/decisiones.md, ya confirmadas por el equipo):

- El promedio del curso es el promedio simple de las notas registradas en los temas del curso, redondeado a dos decimales.
- Un tema sin nota se muestra como "Sin nota" y no entra al promedio.
- Si no tengo ninguna nota en el curso, el promedio se muestra como "Sin notas".
- El promedio se calcula con la función única de cálculo que define el proyecto (AGENTS.md, sección 9); esta spec no define cómo se implementa.

## Criterios de aceptación

CA-1 Dado que inicié sesión como estudiante,
     cuando abro mi perfil,
     entonces veo mi nombre, carné, carrera y semestre, y coinciden con los registrados en la base de datos para mi usuario.

CA-2 Dado que estoy inscrito en los cursos A y B según la base de datos,
     cuando abro mi perfil,
     entonces veo los cursos A y B, y ningún otro.

CA-3 Dado que en un curso tengo las notas 80, 65 y 70 en sus tres temas,
     cuando abro ese curso en mi perfil,
     entonces veo cada tema con su nota y mi promedio del curso es 71.67.

CA-4 Dado que en un curso tengo las notas 80 y 60 en dos temas, y el tercer tema no tiene nota,
     cuando abro ese curso en mi perfil,
     entonces el tercer tema aparece como "Sin nota" y mi promedio del curso es 70.00.

CA-5 Dado que ninguno de los temas de un curso tiene nota para mí,
     cuando abro ese curso en mi perfil,
     entonces todos sus temas aparecen como "Sin nota" y el promedio dice "Sin notas".

CA-6 Dado que no tengo ningún curso asignado,
     cuando abro mi perfil,
     entonces veo mis datos personales y un aviso en español de que aún no tengo cursos asignados.

CA-7 Dado que dos estudiantes distintos tienen datos y notas distintos en la base de datos,
     cuando cada uno inicia sesión y abre su perfil,
     entonces cada uno ve sus propios datos y notas, y los perfiles son diferentes.

CA-8 Dado que la nota de un tema cambió en la base de datos,
     cuando el estudiante recarga su perfil,
     entonces ve la nota nueva y el promedio recalculado.

## Fuera de alcance

- Editar mis datos personales o mis notas.
- Ver el perfil de otro estudiante.
- Impedir que un estudiante abra el perfil de otro escribiendo la dirección (lo cubre S-010).
- Marcar o recomendar temas débiles (S-007).
- Gráficas, historial de notas o exportar el perfil.

## Datos y restricciones

- Solo datos sintéticos (RNF-01). El formato de carné, carrera y semestre sigue D-007.
- Todo texto dirigido al estudiante, en español y de usted (RNF-07).
- Uso de IA: no. No aplica modo demo.
- Depende del inicio de sesión (S-001) y del modelo y datos de prueba (S-002).

## Registro de cambios

05-11-2026 · Versión inicial · —
09-11-2026 · Estado: aprobada (spec fusionada en PR #21); plan aprobado por AlexDLG1 · —
09-11-2026 · Implementación fusionada en PR #40; se documentan controles sobre `9f8c6e2` y evidencia disponible. Estado: en verificación, pendiente de confirmar el registro independiente y revisar el PR documental. No cambia el comportamiento especificado.
09-11-2026 · Tras el PR #41, se agrega evidencia complementaria sobre `7b2a79b`: pruebas dirigidas de CA-4, CA-6 y CA-8 y capturas automatizadas de CA-1 a CA-8. Se documenta la inversión del orden de verificación y merge; sigue pendiente la confirmación explícita del verificador. No cambia el comportamiento especificado.
