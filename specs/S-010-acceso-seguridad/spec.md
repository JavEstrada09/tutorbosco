# S-010 — Acceso, seguridad e interfaz

**Requisitos:** RF-01 y RNF-07  
**Issue:** #14  
**Autor:** Brayan11Hernandez  
**Verificador:** AlexDLG1  
**Estado:** Borrador de especificación

## Problema

TutoBosco necesita garantizar que los usuarios ingresen a la plataforma de forma segura y puedan acceder únicamente a las funcionalidades e información correspondientes a sus responsabilidades.

Los estudiantes y docentes necesitan interfaces distintas. Sin un control adecuado de autenticación y permisos, podrían producirse accesos no autorizados, exposición de información académica o modificaciones indebidas.

Además, la interfaz debe ser comprensible, estar disponible en español y ofrecer una navegación consistente.

## Comportamiento esperado

Como usuario de TutoBosco, quiero iniciar sesión de forma segura y visualizar las funcionalidades correspondientes a mi rol, para utilizar la plataforma sin acceder a información restringida.

El sistema deberá permitir:

1. Iniciar sesión mediante credenciales válidas.
2. Identificar el rol del usuario autenticado.
3. Mostrar las funcionalidades correspondientes al rol de estudiante o docente.
4. Restringir el acceso a las funciones que no correspondan al usuario.
5. Proteger las páginas privadas contra accesos sin autenticación.
6. Cerrar sesión e impedir que se sigan realizando operaciones con la sesión finalizada.
7. Mostrar mensajes claros cuando las credenciales sean incorrectas o exista un error de acceso.
8. Proporcionar una interfaz en español, consistente y comprensible.

## Criterios de aceptación

### CA-1. Inicio de sesión correcto

**Dado** que existe un usuario activo con credenciales válidas,

**cuando** ingresa sus credenciales en el formulario de acceso,

**entonces** el sistema autentica al usuario y le permite ingresar a las funcionalidades correspondientes a su rol.

### CA-2. Credenciales incorrectas

**Dado** que un usuario intenta iniciar sesión,

**cuando** proporciona credenciales incorrectas,

**entonces** el sistema rechaza el acceso y muestra un mensaje comprensible sin revelar información sensible.

### CA-3. Acceso del estudiante

**Dado** que un estudiante ha iniciado sesión correctamente,

**cuando** accede a la plataforma,

**entonces** el sistema presenta las opciones autorizadas para estudiantes y no permite utilizar funcionalidades exclusivas del docente.

### CA-4. Acceso del docente

**Dado** que un docente ha iniciado sesión correctamente,

**cuando** accede a la plataforma,

**entonces** el sistema presenta las herramientas autorizadas para docentes, respetando las restricciones de acceso a la información académica.

### CA-5. Protección de páginas privadas

**Dado** que una persona no ha iniciado sesión,

**cuando** intenta acceder directamente a una página o funcionalidad privada,

**entonces** el servidor impide el acceso y solicita autenticación, sin revelar información restringida.

### CA-6. Restricción por roles

**Dado** que un usuario autenticado intenta ejecutar una operación que no corresponde a su rol,

**cuando** envía la solicitud directamente al servidor, incluso mediante una URL modificada,

**entonces** el sistema rechaza la operación sin realizar modificaciones no autorizadas.

### CA-7. Cierre de sesión

**Dado** que un usuario mantiene una sesión activa,

**cuando** selecciona la opción de cerrar sesión,

**entonces** el sistema finaliza la sesión y no permite continuar utilizando las operaciones privadas sin autenticarse nuevamente.

### CA-8. Interfaz y mensajes en español

**Dado** que un usuario accede a una pantalla de TutoBosco,

**cuando** interactúa con formularios, menús, botones o mensajes,

**entonces** encuentra textos comprensibles en español, navegación consistente y mensajes apropiados para la operación realizada.

## Restricciones y consideraciones de seguridad

- La autenticación y las sesiones deberán utilizar las herramientas de seguridad proporcionadas por Django.
- Las contraseñas deberán almacenarse mediante mecanismos seguros de hash, nunca como texto plano.
- Los permisos deberán comprobarse en el servidor y no solamente ocultando botones de la interfaz.
- Las solicitudes que modifiquen información deberán contar con protección CSRF cuando corresponda.
- No deberán exponerse contraseñas, tokens, claves de API ni información sensible en mensajes de error.
- Se utilizarán únicamente datos sintéticos para las pruebas.
- Las credenciales de configuración se gestionarán mediante variables de entorno.
- Los formularios deberán validar la información recibida.
- La interfaz deberá utilizar los componentes y tecnologías aprobados para el proyecto.
- Los textos dirigidos a estudiantes deberán respetar el trato de usted establecido por el equipo.

## Fuera de alcance

Esta especificación no incluye:

- Desarrollo de mecanismos externos de autenticación como Google o Facebook.
- Recuperación de contraseñas mediante servicios externos.
- Autenticación multifactor.
- Administración avanzada de usuarios y permisos personalizados.
- Gestión de temas académicos, correspondiente a S-004.
- Registro y corrección de notas, correspondiente a S-005.
- Implementación de las funcionalidades de inteligencia artificial.
- Desarrollo completo de los módulos académicos de estudiantes y docentes.

## Dependencias

### S-001 — Esqueleto funcional

Proporciona la estructura inicial de Django, las páginas básicas y los componentes de autenticación que deberán integrarse con esta especificación.

### S-002 — Modelo de datos y datos sintéticos

Define las entidades necesarias para representar a estudiantes, docentes y sus relaciones académicas.

### S-003 — Perfil académico

Sus funcionalidades deberán respetar las restricciones de acceso establecidas para los estudiantes.

### S-004 — Temas y asignación

Las operaciones de gestión académica deberán comprobar que el docente tenga autorización sobre los cursos correspondientes.

### S-008 — Panel del docente

El panel deberá estar disponible únicamente para usuarios con el rol y los permisos requeridos.

## Requisitos técnicos

- **Lenguaje:** Python 3.12.
- **Framework:** Django 5.2 LTS.
- **Base de datos:** SQLite.
- **Interfaz:** HTML, CSS y JavaScript.
- **Estilos:** Bootstrap 5.3.
- **Idioma:** español.
- **Entorno:** funcionamiento local, sin requerir servicios externos para la autenticación.

La implementación deberá integrarse con la estructura existente del proyecto y evitar duplicar componentes desarrollados por otros integrantes.

## Verificación prevista

La verificación estará a cargo de AlexDLG1.

Durante la implementación deberán probarse, como mínimo, los siguientes escenarios:

1. Inicio de sesión con usuario válido.
2. Rechazo de credenciales incorrectas.
3. Visualización de las opciones de estudiante.
4. Visualización de las opciones de docente.
5. Bloqueo de páginas privadas sin autenticación.
6. Rechazo de operaciones no autorizadas.
7. Cierre de sesión y bloqueo de operaciones posteriores.
8. Validación de textos y mensajes de la interfaz.

Los resultados, comandos y evidencias se documentarán posteriormente en `verificacion.md`.

## Registro de cambios

05-11-2026 — Creación del borrador inicial de S-010. Se definieron los comportamientos de acceso, seguridad por roles, protección de sesiones, interfaz y criterios de aceptación. Pendiente de revisión y aprobación del equipo.