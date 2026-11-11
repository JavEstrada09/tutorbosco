# S-009 Respuestas a ejercicios y retroalimentación personalizada

Requisito: RF-05 parcial; RNF-04 · Issue: #13
Autor: Jeffersson Ramos (ramosdeleon555)
Verificador: Brayan11Hernandez
Estado: terminada; PR #60 aprobado por Brayan11Hernandez y fusionado en `64e8043`.

## Problema

Después de resolver un ejercicio, el estudiante necesita comprender
sus aciertos y dificultades para mejorar. La devolución debe estar
relacionada con el ejercicio, su respuesta y su perfil académico,
sin exponer información de otros estudiantes.

## Comportamiento esperado

Como estudiante, quiero responder los ejercicios de mi práctica y
recibir retroalimentación personalizada para comprender mis errores
y reforzar mis conocimientos.

El estudiante responde un ejercicio propio generado en S-007.
El sistema valida la respuesta y la relaciona con el ejercicio y
con el estudiante autenticado antes de solicitar retroalimentación.
El backend recupera el enunciado, el curso, el tema y el contexto
académico pertinente del propietario, sin confiar en identificadores
de propietario o datos académicos enviados por el navegador.

La retroalimentación explica los aciertos o aspectos por mejorar
y proporciona una orientación relacionada con la respuesta.
Se muestra en español, con trato de usted y el curso identificado.
No modifica las notas académicas oficiales.

El modo demo permite responder los ejercicios grabados de S-007
y recibir devoluciones locales pertinentes. Debe demostrar casos
de acierto y error, sin devolver una evaluación genérica que
ignore la respuesta. Si no existe una devolución grabada aplicable,
se informa que no se pudo obtener retroalimentación.

## Criterios de aceptación

CA-1 Dado un estudiante autenticado con un ejercicio propio generado
     por S-007 en un curso que tiene asignado,
     cuando envíe una respuesta válida,
     entonces se registrará su contenido asociado al identificador
     del ejercicio y al estudiante autenticado, conservando la
     relación con el curso y el tema del ejercicio.

CA-2 Dada una respuesta vacía o compuesta únicamente por espacios,
     cuando el estudiante intente enviarla,
     entonces verá un mensaje de validación, no se registrará
     como respuesta válida y no se consultará al proveedor de IA.

CA-3 Dada una respuesta válida a un ejercicio propio,
     cuando el proveedor devuelva retroalimentación válida,
     entonces se mostrará una explicación relacionada con el
     enunciado y la respuesta, que identifique aciertos o aspectos
     por mejorar y una orientación concreta para continuar.

CA-4 Dados dos estudiantes sintéticos con distintos niveles
     académicos en un mismo tema,
     cuando respondan ejercicios y soliciten retroalimentación,
     entonces el contexto preparado para cada solicitud utilizará
     únicamente el perfil vigente del estudiante correspondiente.
     La devolución adaptará el detalle o apoyo a sus dificultades;
     el modo demo permitirá demostrar esa diferencia con casos
     grabados de ambos perfiles.

CA-5 Dados varios ejercicios respondidos por un estudiante,
     cuando consulte los resultados de cada respuesta,
     entonces verá la retroalimentación del ejercicio y respuesta
     seleccionados, sin intercambiarlos con los de otra respuesta,
     curso o estudiante.

CA-6 Dada una solicitud sin autenticación, con rol docente o con
     identificadores de ejercicios o respuestas ajenos, inexistentes
     o de un curso no asignado al estudiante,
     cuando el servidor procese el envío o consulta,
     entonces rechazará la operación sin revelar datos ajenos,
     registrar respuestas no autorizadas ni consultar al proveedor.
     Manipular el propietario en la petición no cambiará a quién
     pertenece la respuesta.

CA-7 Dado el modo demo activo, sin red ni clave de IA, y ejercicios
     grabados de S-007 con casos de respuesta correcta e incorrecta,
     cuando el estudiante envíe las respuestas de esos casos,
     entonces recibirá retroalimentación grabada pertinente que
     distinga el acierto del error, sin llamadas externas ni recursos
     visuales que dependan de Internet.

CA-8 Dado un fallo de conexión o cuota agotada al solicitar
     retroalimentación de una respuesta válida,
     cuando se procese la solicitud,
     entonces se activará la alternativa demo y se informará al
     estudiante. Si existe una devolución grabada aplicable al
     ejercicio y a la respuesta, se mostrará; de lo contrario,
     se indicará que no se pudo obtener retroalimentación sin
     inventar una evaluación ni perder la respuesta registrada.

CA-9 Dada una salida del proveedor vacía o con estructura inválida,
     cuando el backend la valide,
     entonces no se mostrará ni registrará como retroalimentación
     válida y se presentará un mensaje comprensible, conservando
     la respuesta del estudiante.

CA-10 Dada retroalimentación válida de IA o del modo demo,
      cuando se muestre al estudiante,
      entonces estará en español, utilizará el trato de usted e
      identificará el curso. El contenido de respuestas y
      devoluciones se mostrará sin ejecutar código ni HTML activo
      y las notas académicas oficiales permanecerán sin cambios.

## Fuera de alcance

- Identificar temas débiles o generar ejercicios: corresponde a S-007.
- Registrar o corregir notas académicas oficiales: corresponde a S-005.
- Crear exámenes, calificación oficial o un plan de estudio persistente.
- Ejecutar o compilar código enviado por el estudiante o la IA.
- Implementar el historial de conversación general del tutor de S-006.

## Datos y restricciones

- Utilizar únicamente datos sintéticos (RNF-01).
- Dependencia directa: S-007, que entrega ejercicios identificables
  y asociados a un estudiante, curso y tema.
- Reutilizar los modelos académicos de S-002, los proveedores y
  configuración de S-001 y los componentes compartidos disponibles
  de S-006. No duplicar modelos ni integración con IA.
- Contrato propuesto a coordinar con S-007 antes de implementar:
  - Ejercicio: identificador estable, estudiante propietario,
    curso, tema y enunciado.
  - Respuesta: ejercicio asociado, estudiante y contenido enviado.
  - Retroalimentación: respuesta asociada, contenido y procedencia
    (IA o demo).
- El servidor debe validar que el propietario de la respuesta sea
  el del ejercicio. Curso y tema se obtienen del ejercicio, no de
  valores arbitrarios enviados por el cliente.
- Definir persistencia, modelos, campos, migraciones, límites de
  entrada y tratamiento de nuevos intentos en el plan técnico,
  de acuerdo con la estructura aprobada y el contrato de S-007.
- Validar permisos en cada envío y consulta y mantener CSRF.
- Consultar la IA únicamente desde el backend y limitar el contexto
  a los datos pertinentes del estudiante autenticado (RNF-05).
- Utilizar el modelo configurable establecido en AGENTS.md y
  validar la salida antes de utilizarla o mostrarla.
- Mantener secretos fuera del repositorio (RNF-02), respetar el
  presupuesto global y registrar el gasto real (RNF-03).
- Completar el recorrido demo sin red ni clave, usando recursos
  locales y casos coordinados con S-007 (RNF-04).
- Mantener la interfaz en español y el trato de usted (RNF-07).
- No implementar hasta fusionar esta especificación a main,
  aprobar el plan técnico y disponer de las dependencias.

## Registro de cambios

2026-11-11 · Cierre documental tras la aprobación y fusión del PR #60.
Jeffersson confirmó su revisión final y que Brayan completó sus verificaciones.
Se actualiza el estado sin modificar comportamiento ni criterios. La evidencia
y sus límites se conservan en verificacion.md.

2026-11-05 · Borrador inicial para Jeffersson Ramos (ramosdeleon555),
basado en docs/plan.md y docs/guia-trabajo.md; delimita la recepción
de respuestas y retroalimentación frente a la generación de S-007.
