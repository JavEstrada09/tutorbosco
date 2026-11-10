# S-004 Gestión académica del docente: temas y asignación

Requisito: RF-03 parcial · Autor: Brayan11Hernandez · Verificador: AlexDLG1 · Issue: #8

Estado: terminada

## Problema

Los docentes necesitan administrar los temas académicos y organizar a los estudiantes dentro de los cursos que imparten.

Sin una herramienta centralizada, la administración de los temas y las asignaciones puede resultar desorganizada y dificultar el seguimiento académico.

TutoBosco permitirá que cada docente gestione los temas y las asignaciones de sus propios cursos, manteniendo organizada la información académica que utilizarán las demás funcionalidades del sistema.

## Comportamiento esperado

Como docente, quiero consultar y administrar los temas académicos de mis cursos, así como asignar estudiantes a ellos, para organizar la información académica y facilitar el seguimiento del aprendizaje.

El sistema deberá permitir:

1. Consultar los cursos que imparte el docente autenticado.
2. Visualizar los temas correspondientes a cada curso.
3. Registrar nuevos temas académicos dentro de sus cursos.
4. Modificar la información de los temas existentes.
5. Consultar los estudiantes asignados a cada curso.
6. Asignar estudiantes a los cursos que imparte.
7. Evitar asignaciones duplicadas.
8. Impedir que un docente modifique cursos que no le corresponden.

Todas las operaciones deberán respetar los permisos establecidos para los usuarios del sistema.

## Criterios de aceptación

**CA-1. Consulta de cursos del docente**

Dado que un docente ha iniciado sesión correctamente,

cuando ingresa a la sección de gestión académica,

entonces el sistema muestra únicamente los cursos que tiene asignados.

**CA-2. Consulta de temas académicos**

Dado que el docente tiene acceso a un curso,

cuando selecciona dicho curso,

entonces el sistema muestra los temas académicos registrados y asociados a ese curso.

**CA-3. Registro de temas**

Dado que un docente está administrando uno de sus cursos,

cuando registra un nuevo tema con los datos obligatorios válidos,

entonces el sistema almacena el tema y lo muestra dentro del curso correspondiente.

**CA-4. Modificación de temas**

Dado que existe un tema académico en un curso administrado por el docente,

cuando el docente modifica su información utilizando datos válidos,

entonces el sistema guarda los cambios y muestra la información actualizada.

**CA-5. Asignación de estudiantes**

Dado que un docente administra un curso y existe un estudiante registrado,

cuando el docente asigna ese estudiante al curso,

entonces el sistema registra la asignación y muestra al estudiante dentro de la lista correspondiente.

**CA-6. Prevención de asignaciones duplicadas**

Dado que un estudiante ya está asignado a un curso,

cuando el docente intenta realizar nuevamente la misma asignación,

entonces el sistema evita duplicar el registro y muestra un mensaje comprensible.

**CA-7. Restricción de acceso**

Dado que un docente intenta consultar o modificar información académica de un curso que no imparte,

cuando realiza la solicitud,

entonces el servidor rechaza la operación sin mostrar ni modificar información restringida.

**CA-8. Validación de datos**

Dado que un docente intenta registrar o actualizar un tema con información obligatoria faltante o inválida,

cuando envía el formulario,

entonces el sistema rechaza los datos, conserva la información válida ingresada cuando corresponda y muestra un mensaje de error comprensible.

## Fuera de alcance

Esta especificación no incluye:

- Registro y corrección de notas, correspondiente a S-005.
- Cálculo y visualización del perfil académico, correspondiente a S-003.
- Generación de ejercicios mediante inteligencia artificial, correspondiente a S-007.
- Respuestas y retroalimentación personalizada, correspondiente a S-009.
- Panel de seguimiento del docente, correspondiente a S-008.
- Implementación general del sistema de autenticación y seguridad, correspondiente a S-010.
- Desarrollo del tutor personalizado de inteligencia artificial, correspondiente a S-006.

## Datos y restricciones

- Se utilizarán únicamente datos sintéticos, conforme a RNF-01.
- La aplicación utilizará Python 3.12, Django 5.2 LTS y SQLite, según AGENTS.md.
- Cada docente podrá administrar únicamente los cursos que imparte.
- Los permisos se validarán en el servidor y no solamente en la interfaz.
- Los estudiantes deberán existir previamente en el modelo de datos.
- No se permitirán asignaciones duplicadas de estudiantes a un mismo curso.
- Las pantallas, formularios y mensajes estarán en español.
- Los mensajes dirigidos a estudiantes utilizarán el trato de usted.
- Las operaciones deberán mostrar errores y confirmaciones comprensibles.
- No se almacenarán contraseñas ni credenciales en los archivos del repositorio.
- Uso de IA en esta funcionalidad: no requiere llamadas al proveedor de inteligencia artificial.
- Modo demo: la gestión académica deberá funcionar localmente sin depender de servicios externos.

### Dependencias

**S-001 — Esqueleto funcional**

Proporcionará la estructura inicial de Django y los componentes mínimos de autenticación.

**S-002 — Modelo de datos y datos sintéticos**

Proporcionará las entidades académicas y relaciones entre docentes, estudiantes, cursos y temas.

**S-010 — Control de acceso y seguridad**

Establecerá los controles de autorización y seguridad que deberán respetarse durante las operaciones académicas.

Las estructuras de datos y los permisos se coordinarán con los responsables de estas especificaciones antes de la implementación.

## Registro de cambios

05-11-2026 · Creación del borrador inicial de S-004 para definir la gestión de temas, asignación de estudiantes, criterios verificables y restricciones de acceso. Pendiente de revisión y aprobación del equipo.

09-11-2026 · Especificación aprobada y fusionada mediante
el PR #27. Se inicia la planificación de la implementación S-004.

10-11-2026 · Implementación y seguimiento fusionados mediante los PR #47
y #48. AlexDLG1 verificó CA-1 a CA-8 en Windows con Python 3.12.10 sobre
`d86b6fe`; ejecutó 173 pruebas correctamente y registró capturas y resultados
en `verificacion.md`. El PR #48 incorporó la evidencia, cerró el issue #8 y
dejó dos observaciones no bloqueantes documentadas para trabajo posterior.
