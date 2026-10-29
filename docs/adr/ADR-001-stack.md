# ADR-001: Stack de TutoBosco

## Estado

Aceptado. Revisado y fusionado en el PR #1 (27-10-2026).

La elección del modelo de ChatGPT sigue pendiente de confirmar
en S-001 según disponibilidad, cuota gratuita y calidad.

## Contexto

TutoBosco es una aplicación web educativa desarrollada
por un equipo de cinco integrantes.

El producto necesita autenticación, permisos por rol,
gestión académica, un tutor de IA, práctica personalizada
y un panel para docentes.

La elección tecnológica debe considerar:

- RF-01: acceso por rol y contraseñas almacenadas con hash.
- RF-02 y RF-03: perfiles, cursos, temas, asignaciones y notas.
- RF-04 y RF-05: integración con un servicio de IA.
- RF-06: consultas y cálculos para el panel docente.
- RNF-01: generación reproducible de datos sintéticos.
- RNF-02: secretos fuera del repositorio.
- RNF-03: presupuesto máximo global de USD 10 para la IA.
- RNF-04: demostración del tutor y la práctica sin red.
- RNF-05: aislamiento del contexto académico.
- RNF-06: un repositorio, base local e instalación
  siguiendo el README en menos de 30 minutos.
- RNF-07: interfaz en español y trato de usted al estudiante.

Se busca facilitar la instalación, la integración del trabajo
y la comprensión del código por todos los integrantes.

## Decisión propuesta

Desarrollar una aplicación Django con interfaz renderizada
en el servidor y base de datos SQLite local.

### Lenguaje y framework

- Python 3.12.
- Django 5.2 LTS.
- Fijar las versiones exactas de dependencias después
  de instalarlas y verificarlas.

Utilizar los componentes de Django para autenticación,
sesiones, formularios, acceso a datos, migraciones y pruebas.

Los permisos sobre cursos y estudiantes se implementarán
explícitamente en el servidor y se verificarán con pruebas.

### Interfaz

- Plantillas Django.
- HTML y CSS.
- JavaScript básico donde mejore la interacción.
- Bootstrap 5.3 y estilos propios.

Los archivos necesarios de Bootstrap, las imágenes y
los demás recursos de la demostración se guardarán localmente.

El docente tendrá pantallas propias para realizar sus tareas.
El administrador técnico de Django no sustituirá esas pantallas
ni representará un tercer rol del producto.

### Base de datos

Utilizar SQLite local.

Cada integrante tendrá su propia base de desarrollo.
El repositorio incluirá migraciones y el generador de datos,
pero no archivos de bases SQLite.

El modelo admitirá varios cursos y relaciones entre docentes,
estudiantes, temas, inscripciones y notas.

### Integración con IA

Usar ChatGPT API como proveedor inicial propuesto.

Evaluar inicialmente ChatGPT 2.5 Flash con perfiles sintéticos.
Confirmar disponibilidad, cuota y calidad antes de fijar el modelo.

El nombre del modelo y la clave se configurarán mediante
variables de entorno. La clave solo se utilizará en el backend.

Separar el acceso a IA de las vistas y de las reglas académicas,
para permitir cambiar el proveedor o seleccionar el modo demo.

Registrar el consumo y el gasto de todo el equipo.
El presupuesto de USD 10 es global durante el proyecto.

### Modo demo

Implementar un proveedor local de respuestas grabadas
seleccionado mediante configuración.

Debe permitir demostrar personalización, historial,
ejercicios y retroalimentación sin conexión ni clave de IA.

Se desarrollará desde el esqueleto y se ampliará junto
con las funcionalidades del tutor y la práctica.

### Herramientas de trabajo

- Git y GitHub para versiones, issues y pull requests.
- VS Code como editor recomendado.
- Herramientas de pruebas de Django.
- GitHub Actions cuando exista una aplicación verificable.

Cada integrante podrá utilizar su agente de programación
disponible, respetando AGENTS.md y declarando la herramienta
y el modelo realmente utilizados.

## Alternativas consideradas

### React con un backend API separado

Permite separar claramente la interfaz y el servidor,
y ofrece flexibilidad para una interfaz interactiva.

No se elige inicialmente porque requiere coordinar dos
aplicaciones, sus dependencias y su comunicación.
Para este alcance se prioriza una instalación local sencilla
y una sola aplicación que todos puedan comprender.

### PostgreSQL local

Ofrece mejores capacidades para escenarios con mayor
concurrencia de escritura.

No se elige inicialmente porque requiere instalar y configurar
un servicio adicional en las computadoras del equipo.

SQLite se considera suficiente para la demostración local.
Si aparecen limitaciones reales, se revisará esta decisión
mediante otro ADR.

### Base de datos alojada en la nube

No se elige porque RNF-06 exige que la base se ejecute localmente
y la demostración debe poder realizarse sin red.

## Consecuencias positivas

- Una sola aplicación y un único repositorio.
- Instalación local con menos servicios que configurar.
- Componentes integrados para tareas comunes del sistema.
- Migraciones y datos reproducibles entre computadoras.
- Interfaz consistente con recursos disponibles sin red.
- Posibilidad de sustituir el proveedor de IA.
- Organización del código alrededor de funcionalidades verificables.

## Costos y limitaciones aceptados

- SQLite tiene limitaciones ante escrituras concurrentes.
- Las interacciones dinámicas requieren JavaScript adicional.
- Django exige aprender y respetar sus convenciones.
- La cuota gratuita de IA tiene límites y puede cambiar.
- El modo demo requiere mantener casos grabados coherentes.
- Las herramientas integradas no sustituyen la implementación
  y verificación de los permisos propios de TutoBosco.

## Validación pendiente

La primera implementación deberá comprobar:

1. Instalación reproducible en otra computadora.
2. Acceso con usuario sintético.
3. Lectura de un dato académico desde SQLite.
4. Respuesta real del proveedor de IA.
5. Respuesta grabada con el modo demo activo.
6. Recursos visuales disponibles sin red.

Antes de la entrega final, otra persona deberá instalar
el sistema siguiendo únicamente el README en menos de 30 minutos.

## Referencias

- Enunciado del Proyecto Final de Programación Comercial.
- https://docs.djangoproject.com/en/5.2/releases/5.2/
- https://docs.djangoproject.com/en/5.2/topics/auth/default/
- https://docs.djangoproject.com/en/5.2/intro/tutorial02/
- https://getbootstrap.com/docs/5.3/getting-started/download/
- https://ai.google.dev/ChatGPT-api/docs/pricing
