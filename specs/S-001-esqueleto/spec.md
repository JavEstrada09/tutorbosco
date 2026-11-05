# S-001 — Esqueleto funcional

Requisito: RF-01, RF-02 y RF-04 parciales; RNF-04 y RNF-06 parciales.
Autor: JavEstrada09.
Verificador: douglas-yasser.
Issue: #4.
Estado: borrador.

## Problema

TutoBosco todavía no tiene un recorrido ejecutable que conecte
el inicio de sesión, la base de datos local y el servicio de IA.

Se necesita un esqueleto mínimo para comprobar esa integración
y establecer una base común para las siguientes funcionalidades.

## Comportamiento esperado

Como estudiante, quiero iniciar sesión con una cuenta sintética,
consultar un dato de mi perfil académico y recibir una respuesta
del tutor sobre Programación Comercial.

También quiero utilizar una respuesta grabada cuando esté activo
el modo demo, sin necesitar conexión a Internet ni una clave de IA.

## Criterios de aceptación

### CA-1 — Inicio de sesión correcto

Dado que existe un estudiante sintético con credenciales válidas,
cuando introduce correctamente su usuario y contraseña,
entonces inicia una sesión y accede a la pantalla del esqueleto.

### CA-2 — Inicio de sesión incorrecto

Dado que una persona está en la pantalla de acceso,
cuando introduce credenciales incorrectas,
entonces permanece sin autenticar y ve un mensaje de error
en español que no revela si el usuario existe.

### CA-3 — Dato propio del perfil y acceso protegido

Dado que un estudiante inició sesión,
cuando abre la pantalla del esqueleto,
entonces ve su carrera académica obtenida de la base local
y correspondiente a su cuenta.

Dado que una persona no ha iniciado sesión,
cuando intenta abrir directamente esa pantalla,
entonces el servidor le exige autenticarse antes de mostrar
información académica.

### CA-4 — Respuesta real de IA

Dado que el estudiante está autenticado, el modo real está activo
y el proveedor Gemini está disponible y configurado,
cuando envía una pregunta sobre Programación Comercial,
entonces recibe una respuesta obtenida mediante una llamada real
desde el servidor al proveedor.

La respuesta se muestra en español, utiliza el trato de usted
e identifica el curso Programación Comercial.

Una respuesta grabada no cuenta como evidencia de este criterio.

### CA-5 — Respuesta grabada sin conexión

Dado que el modo demo está activo, no existe conexión a Internet
y no se ha configurado una clave de IA,
cuando el estudiante inicia sesión, consulta su dato académico
y envía una pregunta incluida en los casos de demostración,
entonces completa el recorrido y recibe la respuesta grabada
correspondiente sin realizar llamadas al proveedor.

La interfaz identifica que está utilizando el modo demo.

### CA-6 — Error del proveedor

Dado que el estudiante está autenticado y el modo real está activo,
cuando el proveedor falla, agota su cuota o no puede responder,
entonces la aplicación muestra un mensaje comprensible en español,
no expone información técnica sensible y permite continuar
mediante el modo demo.

### CA-7 — Ejecución local reproducible

Dado que el verificador dispone de una copia del proyecto
y de los requisitos indicados en el README,
cuando sigue las instrucciones de instalación, configuración,
migraciones, preparación de datos mínimos y ejecución,
entonces puede iniciar la aplicación y completar el recorrido demo
en su computadora.

Los recursos visuales necesarios están disponibles localmente
y el recorrido demo no depende de servicios externos.

## Fuera de alcance

- Perfil académico completo, notas por tema y promedios de S-003.
- Modelo académico completo y generación masiva de datos de S-002.
- Pantallas y operaciones del docente.
- Tutor personalizado completo, contraste de perfiles e historial
  de conversación de S-006.
- Detección de temas débiles, ejercicios y retroalimentación.
- Panel docente y plan de estudio.
- Cumplimiento completo de RF-01, RF-02 y RF-04.

Los controles básicos de autenticación y protección de datos
necesarios para este recorrido sí forman parte del esqueleto.

## Datos y restricciones

- Utilizar únicamente datos sintéticos.
- Preparar al menos una cuenta de estudiante, su carrera académica
  y los datos mínimos necesarios para demostrar el recorrido.
- Coordinar el modelo mínimo con douglas-yasser, autor de S-002,
  para evitar modelos duplicados o migraciones incompatibles.
- Definir la estructura de apps de Django en el plan técnico.
- Utilizar Django, SQLite local y el stack aprobado en ADR-001.
- Guardar las contraseñas con los mecanismos de hash de Django.
- Verificar la autenticación y los permisos en el servidor.
- Mantener activa la protección CSRF.
- Obtener el dato académico de la cuenta autenticada.
- Consultar Gemini únicamente desde el backend.
- Mantener el modelo configurable y confirmar la disponibilidad
  del identificador indicado en ADR-001 antes de implementar.
- Guardar claves y contraseñas locales fuera del repositorio.
- Mantener .env.example con nombres de variables y valores vacíos.
- Priorizar el nivel gratuito y respetar el presupuesto global
  de USD 10 del proyecto.
- Declarar el uso real de IA y registrar el consumo correspondiente.
- Mostrar la interfaz en español y dirigirse al estudiante de usted.
- Conservar localmente las respuestas grabadas y los recursos
  necesarios para ejecutar la demostración sin red.

## Registro de cambios

2026-11-05 · Borrador inicial de S-001 · Define el recorrido mínimo,
sus criterios de aceptación y sus límites respecto de otras specs.