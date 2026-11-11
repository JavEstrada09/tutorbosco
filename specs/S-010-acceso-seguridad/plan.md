# Plan S-010

Propuesto por: OpenCode · `openai/gpt-5.6-sol` · modo Plan
Revisado y aprobado por: Brayan11Hernandez · 10-11-2026

## Enfoque

Consolidar el acceso seguro ya implementado por S-001, S-003, S-004, S-005
y S-008 sin crear otro sistema de permisos. S-010 reutilizará `role_home`,
los perfiles académicos y las comprobaciones de autorización existentes;
completará la navegación común por rol, el cierre de sesión disponible desde
toda página privada y una matriz identificable de pruebas de regresión.

## Archivos que se crean o modifican

### Archivos nuevos

- `static/css/bootstrap.min.css`: Bootstrap 5.3 almacenado localmente.
- `specs/S-010-acceso-seguridad/plan.md`: este plan aprobado.

### Archivos existentes que se modificarán parcialmente

- `templates/base.html`: carga local de Bootstrap, marca dirigida a
  `role_home`, navegación por perfiles y cierre de sesión POST con CSRF.
- `templates/academics/*.html`: retirar formularios de cierre de sesión
  duplicados, ahora disponibles en la cabecera común.
- `static/css/tutobosco.css`: estilos de la navegación común en escritorio y
  móvil, conservando el diseño existente sobre Bootstrap.
- `accounts/tests.py`: pruebas integrales de acceso, navegación, prioridad de
  perfiles, páginas privadas y cierre de sesión.
- `specs/S-010-acceso-seguridad/spec.md`: estado, decisiones verificables y
  registro del plan aprobado.
- `docs/plan.md` y `docs/registro-ia.md`: avance y uso real de IA.

## Cambios al modelo de datos

Ninguno. Se reutilizan `User`, `StudentProfile`, `TeacherProfile`,
`TeachingAssignment` y las sesiones de Django.

## Decisiones técnicas

- Se conserva `LOGIN_REDIRECT_URL = "role_home"` y la vista `role_home` de
  S-008; S-010 no crea otro redirect ni duplica la detección del rol.
- Una cuenta con ambos perfiles llega primero al inicio estudiantil, como ya
  definió S-008, y conserva las operaciones autorizadas de ambos perfiles.
- Una persona anónima recibe redirección al login con `next`; una persona
  autenticada sin el perfil o la asignación exigidos recibe HTTP 403.
- El cierre de sesión continúa aceptando solo POST y exige un token CSRF.
- La cabecera muestra únicamente enlaces respaldados por los perfiles de la
  cuenta. No sustituye ninguna comprobación de permisos en el servidor.
- Bootstrap 5.3 se sirve desde `static/`; la aplicación no depende de CDN,
  fuentes externas ni autenticación remota.

## Tareas en orden

1. Sincronizar la rama con `main` y registrar el plan aprobado.
2. Incorporar Bootstrap 5.3 local antes del CSS propio.
3. Implementar la cabecera y navegación común por rol.
4. Retirar cierres de sesión duplicados de las páginas particulares.
5. Agregar pruebas de regresión específicas de S-010.
6. Ejecutar checks, pruebas y comprobaciones de migraciones y dependencias.
7. Actualizar documentación y preparar el PR para verificación independiente.

## Cómo se verificará cada criterio

CA-1 → iniciar sesión con credenciales reales de estudiante y docente,
comprobar la sesión y seguir `role_home` hasta la pantalla correspondiente.

CA-2 → intentar con contraseña incorrecta, usuario inexistente y cuenta
inactiva; todos deben recibir el mismo mensaje general en español.

CA-3 → comprobar que una cuenta solo estudiantil ve inicio y perfil, no
enlaces docentes, y recibe 403 al solicitar funciones docentes.

CA-4 → comprobar que una cuenta docente ve panel y administración de cursos,
no enlaces estudiantiles, y solo accede a cursos que imparte.

CA-5 → solicitar las rutas privadas sin sesión y comprobar la redirección al
login sin contenido académico.

CA-6 → reutilizar y ejecutar las pruebas de S-003, S-004, S-005 y S-008 que
envían URLs y POST directos sin autorización y comprueban que no hay cambios.

CA-7 → comprobar GET rechazado, POST sin CSRF rechazado, POST válido que
elimina la sesión y nueva solicitud privada redirigida al login.

CA-8 → recorrer la navegación común en escritorio y móvil, verificar textos
en español y confirmar que Bootstrap se carga desde un recurso local.

## Correcciones humanas al plan del agente

1. Brayan11Hernandez aprobó el alcance mínimo propuesto el 10-11-2026.
2. Brayan11Hernandez decidió conservar para cuentas con ambos perfiles la
   prioridad estudiantil de S-008, sin retirar sus permisos docentes válidos.
