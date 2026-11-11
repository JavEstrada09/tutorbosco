# S-005 Registro y corrección de notas

Requisito: RF-03 (parcial: registro y corrección de notas) · Autor: AlexDLG1 · Verificador: ramosdeleon555 · Issue: #9
Estado: terminada

## Problema

Las notas de los estudiantes viven en hojas de cálculo que nadie más puede usar. Mientras el docente no pueda registrarlas ni corregirlas dentro de la plataforma, el perfil del estudiante, el tutor y el panel del docente no tienen datos confiables.

## Comportamiento esperado

Como docente, quiero registrar la nota de cada estudiante en cada tema de un curso que imparto, y corregirla cuando me equivoque, para que el estudiante y la plataforma siempre trabajen con la nota vigente.

Reglas:

- La nota va de 0 a 100 y es un número entero.
- Cada estudiante tiene como máximo una nota por tema. Corregir una nota reemplaza la anterior.
- Solo puedo calificar a estudiantes asignados a un curso que imparto, en los temas de ese curso.

Que la nota sea entera y que corregir reemplace no está definido en el enunciado. Son propuestas registradas como D-008 en docs/decisiones.md, en este mismo PR, que el equipo debe confirmar.

## Criterios de aceptación

CA-1 Dado que soy docente de un curso y un estudiante asignado no tiene nota en un tema,
     cuando registro la nota 85 para ese estudiante en ese tema,
     entonces veo la confirmación del guardado, la nota 85 aparece en la lista del curso
     y queda guardada en la base de datos.

CA-2 Dado que un estudiante tiene 60 en un tema,
     cuando corrijo su nota a 75,
     entonces veo 75 en la lista, la nota anterior ya no aparece
     y la base de datos tiene un solo registro para ese estudiante en ese tema, con valor 75.

CA-3 Dado que estoy registrando una nota,
     cuando intento guardar un valor fuera de 0 a 100 (por ejemplo -5 o 101), un valor vacío o un valor que no es un número entero,
     entonces veo un mensaje de error en español y la nota que ya existía no cambia.

CA-4 Dado que registré o corregí la nota de un estudiante,
     cuando ese estudiante abre su perfil,
     entonces ve la nota nueva en ese tema y su promedio del curso recalculado.

CA-5 Dado que registré una nota y cerré mi sesión,
     cuando vuelvo a iniciar sesión y abro el mismo curso,
     entonces la nota sigue ahí.

CA-6 Dado que un estudiante no está asignado a mi curso,
     cuando abro la pantalla de notas de ese curso,
     entonces ese estudiante no aparece y no puedo registrarle nota desde la pantalla.

CA-7 Dado que un tema no pertenece al curso que estoy calificando,
     cuando abro la pantalla de notas de ese curso,
     entonces ese tema no aparece entre los temas calificables.

CA-8 Dado que intento guardar una nota para un estudiante que no está asignado a mi curso, para un tema que no es de mi curso, o en un curso que imparte otro docente (por ejemplo, reenviando el formulario con otros datos),
     cuando el sistema recibe la solicitud,
     entonces la rechaza, muestra un mensaje en español y no se guarda ni se modifica ninguna nota en la base de datos.

## Fuera de alcance

- Crear, editar o asignar temas y estudiantes a un curso (S-004).
- Ver el perfil desde el lado del estudiante (S-003).
- Que el tutor use la nota nueva en sus respuestas (RF-03 lo pide, pero lo cubre y verifica S-006).
- Controlar quién puede abrir la pantalla de notas escribiendo la dirección (S-010). Lo que sí cubre esta spec es que el guardado de una nota rechace datos que el docente no puede calificar (CA-8).
- Borrar una nota ya registrada, historial de cambios, notas con decimales, carga masiva desde hoja de cálculo.

## Datos y restricciones

- Solo datos sintéticos (RNF-01). Los datos de prueba (S-002) deben incluir al menos un estudiante asignado sin nota en un tema, para poder probar CA-1.
- Todo texto dirigido a personas usuarias, en español (RNF-07).
- Uso de IA: no. No aplica modo demo.
- Depende del inicio de sesión (S-001), del modelo y los datos de prueba (S-002) y de la asignación de temas y estudiantes (S-004).
- Coordinar con S-010 (Brayan11Hernandez) dónde termina cada responsabilidad de permisos.

## Registro de cambios

05-11-2026 · Versión inicial · —
09-11-2026 · Estado: aprobada (spec fusionada en PR #29); plan aprobado por AlexDLG1. Coordinación con S-004 y S-010 confirmada con Brayan11Hernandez: ruta /docente/cursos/<código>/notas/, get_taught_course compartida y 403 ante un curso que el docente no imparte · —
10-11-2026 · Estado: terminada. Implementación fusionada en PR #45 con la verificación independiente de ramosdeleon555 (commit `f133c0a`). No cambia el comportamiento especificado · —