# S-007 Identificación de temas débiles y generación de ejercicios

Requisito: RF-05 parcial; RNF-04 · Autor: ramosdeleon555 · Verificador: Brayan11Hernandez · Issue: #11
Estado: Terminada

## Problema

El estudiante necesita practicar los temas en los que presenta
dificultades, utilizando sus calificaciones vigentes como referencia.
La práctica debe estar limitada a sus propios cursos y funcionar
también sin conexión mediante ejercicios grabados.

## Comportamiento esperado

Como estudiante, quiero solicitar ejercicios de uno de mis cursos
para reforzar los temas cuya nota sea inferior al umbral configurado.

El sistema identifica los temas débiles del curso seleccionado usando
las notas vigentes del estudiante autenticado. Un tema es débil cuando
tiene una nota estrictamente menor que WEAK_TOPIC_THRESHOLD, cuyo
valor inicial es 60. Los temas sin nota no se consideran débiles.

La práctica se genera desde el backend mediante el proveedor de IA
y se valida antes de mostrarla. Cada ejercicio identifica su curso y
tema, contiene un enunciado y cuenta con un identificador estable
para su posterior uso en S-009.

Si no hay temas débiles, se informa al estudiante sin solicitar
ejercicios al proveedor. Si no existen notas, se explica que aún
no hay calificaciones para identificar los temas que debe reforzar.

El modo demo utiliza ejercicios grabados locales, seleccionados
según los temas débiles del estudiante. Ante fallos de conexión o
cuota agotada se activa esa alternativa y se informa del cambio.

## Criterios de aceptación

CA-1 Dado un estudiante autenticado, asignado a un curso con notas
     45, 59, 60 y 85 en cuatro temas y un umbral de 60,
     cuando solicite práctica del curso,
     entonces solo se identificarán como débiles los temas con
     notas 45 y 59; los temas con 60 y 85 quedarán excluidos.

CA-2 Dado un umbral configurado en 70 y temas con notas 60, 69 y 70,
     cuando el estudiante solicite práctica,
     entonces se considerarán débiles los temas con 60 y 69,
     pero no el tema con 70.

CA-3 Dado un curso con un tema sin nota y otro con nota menor
     al umbral,
     cuando se identifiquen los temas débiles,
     entonces se excluirá el tema sin nota sin tratarlo como cero
     y se incluirá el tema calificado bajo el umbral.

CA-4 Dados uno o más temas débiles del estudiante en el curso,
     cuando el proveedor devuelva una práctica válida,
     entonces se mostrará al menos un ejercicio, cada uno con
     enunciado, curso y tema; todos pertenecerán exclusivamente
     a los temas débiles identificados de ese curso.

CA-5 Dado un curso donde todas las notas registradas sean iguales
     o superiores al umbral,
     cuando el estudiante solicite práctica,
     entonces verá un aviso de que no tiene temas débiles y no se
     consultará al proveedor de IA ni se generarán ejercicios.
     Si el curso no tiene notas, verá un aviso que explique esa
     situación, sin afirmar que ya domina los temas y sin generar
     ejercicios ni consultar al proveedor de IA.

CA-6 Dado un tema inicialmente bajo el umbral cuya nota se corrige
     para igualarlo o superarlo,
     cuando el estudiante solicite una nueva práctica,
     entonces ese tema quedará excluido de los ejercicios nuevos.
     Si una corrección deja otro tema bajo el umbral, la nueva
     selección lo incluirá entre los temas débiles.

CA-7 Dada una solicitud sin autenticación, realizada por un docente
     o dirigida a un curso no asignado al estudiante autenticado,
     cuando el servidor la procese, incluso mediante una petición
     directa con identificadores manipulados,
     entonces rechazará la operación sin revelar datos académicos
     ni generar ejercicios. En solicitudes válidas, el contexto
     enviado al proveedor contendrá únicamente datos del estudiante
     autenticado y del curso seleccionado.

CA-8 Dado el modo demo activo, sin red y sin clave de IA,
     cuando estudiantes con diferentes temas débiles soliciten
     práctica de sus cursos,
     entonces recibirán ejercicios grabados correspondientes a
     sus respectivos temas débiles, sin llamadas externas ni
     recursos visuales que dependan de Internet.

CA-9 Dado un fallo de conexión o cuota agotada del proveedor de IA,
     cuando el estudiante solicite práctica,
     entonces se utilizarán ejercicios grabados válidos para sus
     temas débiles y se informará que se está usando el modo demo.
     Si el proveedor devuelve una respuesta sin enunciado o con
     temas ajenos a la selección, no se mostrará como práctica
     válida y se presentará un aviso comprensible. Si no existe
     una respuesta grabada aplicable, se informará que no se pudo
     generar la práctica, sin sustituirla por temas no permitidos.

CA-10 Dados ejercicios válidos generados por IA o por el modo demo,
      cuando se muestren al estudiante,
      entonces los enunciados y mensajes estarán en español y
      utilizarán el trato de usted. Cada ejercicio tendrá un
      identificador estable que permita relacionarlo con su
      estudiante propietario, curso y tema para integrar S-009.

## Fuera de alcance

- Recibir respuestas, calificarlas o generar retroalimentación:
  corresponde a S-009.
- Registrar o corregir notas: corresponde a S-005.
- Implementar el perfil académico, el panel del docente o el
  historial de conversación del tutor.
- Generar ejercicios de temas sin nota o que no estén bajo el umbral.
- Crear un plan de estudio persistente (RF-07).
- Ejecutar como código los enunciados o contenido generado por IA.

## Datos y restricciones

- Solo datos sintéticos (RNF-01).
- Cumplir D-002 y D-003 de docs/decisiones.md: umbral configurable,
  comparación estricta y exclusión de temas sin nota.
- Reutilizar el cálculo centralizado de temas débiles; no duplicar
  reglas en vistas, plantillas o proveedores.
- Validar autenticación, rol y asignación al curso en el servidor.
  Mantener la protección CSRF en las solicitudes de generación.
- Uso de IA del producto: sí, mediante el proveedor compartido del
  backend y el modelo configurable establecido en AGENTS.md.
- Validar estructura, enunciado y pertenencia de los temas antes de
  utilizar la respuesta. Mostrar el contenido sin ejecutar código.
- El modo demo debe funcionar sin red, sin clave y con recursos
  locales (RNF-04). No debe elegir temas ajenos para suplir ejercicios.
- Mantener secretos fuera del repositorio (RNF-02), respetar el
  presupuesto global y registrar el gasto real (RNF-03).
- Limitar el contexto al estudiante autenticado (RNF-05).
- Interfaz en español y trato de usted (RNF-07).
- Dependencias: estructura, configuración y proveedores de S-001;
  modelo académico y datos sintéticos de S-002; integración con las
  notas vigentes de S-005 y los componentes compartidos del tutor
  de S-006, conforme al orden de docs/plan.md.
- Antes de implementar, acordar con S-009 la representación del
  ejercicio: identificador estable, estudiante propietario, curso,
  tema y enunciado. La persistencia y los nombres concretos de
  modelos, campos y archivos se resolverán en el plan aprobado,
  usando la estructura disponible y sin duplicar modelos comunes.
- No implementar hasta que esta especificación esté fusionada a
  main, el plan técnico esté aprobado y existan las dependencias.

## Registro de cambios

2026-11-05 · Borrador inicial basado en docs/plan.md, la guía de
trabajo y las decisiones D-002 y D-003; separa la generación de
ejercicios de las respuestas y retroalimentación de S-009.

2026-11-11 · Cierre documental por ramosdeleon555 tras la verificación
independiente de Brayan11Hernandez. Los diez criterios quedaron
confirmados; CA-4, CA-9 y CA-10 se repitieron sobre `acf58d0`, donde
pasaron las 21 pruebas específicas y las 217 totales con
`GEMINI_API_KEY` vacía. Brayan11Hernandez aprobó el PR #56 sobre ese
commit. El detalle está en `verificacion.md`.
