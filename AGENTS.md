# AGENTS.md — TutoBosco

## 1. Propósito

TutoBosco es una plataforma web educativa que utiliza inteligencia
artificial para acompañar al estudiante según su perfil académico.

El producto tiene dos roles:
- Estudiante: consulta su perfil, conversa con el tutor y practica
  sus temas débiles.
- Docente: administra temas, asigna estudiantes, registra notas
  y consulta el avance de sus estudiantes.

El curso piloto es Programación Comercial.
El modelo de datos debe admitir varios cursos.

## 2. Stack

- Python 3.12.
- Django 5.2 LTS.
- SQLite local.
- Plantillas Django, HTML, CSS y JavaScript básico.
- Bootstrap 5.3 almacenado localmente.
- Gemini API como proveedor inicial propuesto.
- Proveedor local de respuestas grabadas para el modo demo.

La elección y sus alternativas se documentan en:
docs/adr/ADR-001-stack.md

Las versiones exactas de las dependencias se fijarán al implementar
y verificar el esqueleto del proyecto.

## 3. Estado actual

El repositorio está en preparación documental.
Todavía no existe una aplicación ejecutable.

No presentar como implementadas funcionalidades pendientes.
No ejecutar generadores de código para adelantar funcionalidades
sin seguir el proceso de especificación y planificación.

## 4. Método de trabajo obligatorio

Cada funcionalidad sigue este orden:

1. Redactar spec.md con el problema, comportamiento esperado,
   criterios Dado/Cuando/Entonces, exclusiones y restricciones.
2. Fusionar la spec a main mediante un PR revisado por otro integrante,
   antes de escribir código de esa funcionalidad.
3. Proponer plan.md en modo de solo lectura.
4. Obtener revisión y aprobación humana del plan antes de implementar.
5. Implementar en la rama correspondiente.
6. El autor lee y ejecuta cada cambio antes del commit.
7. Otro integrante prueba cada criterio en su computadora.
8. Registrar resultados y evidencia en verificacion.md.
9. Fusionar el PR únicamente con la verificación completa.

El plan identifica archivos, cambios al modelo de datos, tareas
ordenadas y cómo verificar cada criterio.

Registrar correcciones humanas reales al plan.
No inventar aprobaciones, pruebas, evidencia ni resultados.

Si el código y la spec difieren, resolver la diferencia y actualizar
la spec, su registro de cambios y la descripción del PR.

## 5. Git y colaboración

- Un solo repositorio para toda la aplicación.
- main es la rama de integración y debe mantenerse ejecutable
  desde que se incorpore el primer esqueleto funcional.
- No realizar commits directos a main.
- El arranque inicial está documentado en docs/decisiones.md.
- Una rama por spec: s-NNN-nombre-corto.
- Commits pequeños con prefijo S-NNN:.
- Ejemplo: S-004: muestra notas y promedio del estudiante.
- Mantener cada PR dentro de un tamaño revisable.
- Referencia: aproximadamente 400 líneas cambiadas,
  excluyendo datos y archivos generados.
- Dividir specs demasiado grandes antes de implementar.
- Usar git worktree si una persona trabaja en dos specs simultáneas.
- No reescribir el historial compartido mediante force push.
- No fusionar cambios ajenos a la spec.
- Usar la plantilla de pull requests del repositorio.
- Cada spec tiene un issue, un autor y un verificador distinto.
- El PR final de implementación cierra el issue con Closes #N.
- El PR inicial de especificación referencia el issue sin cerrarlo.

Cada integrante debe ser autor de al menos dos specs y verificador
de al menos dos specs de otros integrantes.

## 6. Seguridad y datos

- Utilizar únicamente datos sintéticos.
- Guardar contraseñas mediante los mecanismos de hash de Django.
- No guardar contraseñas en texto plano en la base de datos.
- No subir claves, contraseñas ni archivos .env.
- Mantener .env.example con nombres de variables y valores vacíos.
- No versionar bases SQLite ni entornos virtuales.
- Versionar migraciones y scripts de generación de datos.
- Verificar permisos en el servidor en cada operación.
- Un estudiante solo accede a sus propios datos.
- Un docente solo administra los cursos que imparte.
- No confiar en ocultar botones como mecanismo de autorización.
- No desactivar la protección CSRF para facilitar formularios.
- Si se expone una clave, revocarla inmediatamente y registrar
  el incidente en docs/incidentes.md.

Los datos completos deben incluir como mínimo:
- 30 estudiantes.
- 3 docentes.
- 4 cursos.
- 6 temas por curso.
- Notas variadas y perfiles claramente distintos.

## 7. Tutor e integración con IA

- Consultar la IA desde el backend.
- Enviar únicamente datos del estudiante autenticado.
- Recuperar información académica vigente al preparar el contexto.
- Considerar cambios de notas en la siguiente conversación.
- Separar conversaciones por estudiante y curso.
- Conservar historial durante la conversación.
- Indicar el curso en cada respuesta del tutor.
- Adaptar explicaciones al perfil académico.
- Generar práctica únicamente sobre temas bajo el umbral configurado.
- Informar cuando el estudiante no tenga temas débiles.
- Hacer configurable el modelo y el umbral de temas débiles.
- Manejar errores de conexión, cuota y respuestas inválidas.
- Validar la salida de IA antes de utilizarla o mostrarla.
- No ejecutar contenido generado por el modelo como código.

El presupuesto máximo del servicio de IA del producto es
USD 10 para todo el equipo durante el proyecto.
Registrar el gasto real en docs/gasto.md.

## 8. Modo demo

Un interruptor de configuración selecciona respuestas grabadas.

El modo demo debe:
- Funcionar sin red y sin clave de IA.
- Permitir demostrar RF-04 y RF-05.
- Distinguir perfiles académicos diferentes.
- Permitir seguimiento dentro de la conversación.
- Incluir ejercicios y retroalimentación.
- Utilizar recursos visuales disponibles localmente.

No depender de CDN, fuentes externas ni autenticación remota
para ejecutar la demostración local.

## 9. Interfaz y convenciones

- Toda la interfaz está en español.
- Todo texto dirigido al estudiante utiliza usted.
- Mantener estilos, navegación y formularios consistentes.
- Mostrar estados vacíos, errores y confirmaciones comprensibles.
- Validar notas en escala de 0 a 100.
- Centralizar el cálculo de promedios y temas débiles.
- Utilizar nombres descriptivos y funciones de responsabilidad clara.
- Evitar cambios de formato ajenos al trabajo de la spec.
- Mantener las reglas de negocio fuera de las plantillas.
- El administrador técnico de Django no sustituye las pantallas
  requeridas para el docente.

## 10. Estructura documental

- AGENTS.md: contexto y reglas para agentes.
- CLAUDE.md: referencia @AGENTS.md para Claude Code.
- README.md: instalación y ejecución en una computadora limpia.
- .github/pull_request_template.md: plantilla de PR.
- specs/_plantilla/: plantillas de spec.md, plan.md y
  verificacion.md. Cada spec nueva se crea copiando esta carpeta.
- specs/S-NNN-nombre/spec.md: comportamiento y aceptación.
- specs/S-NNN-nombre/plan.md: implementación aprobada.
- specs/S-NNN-nombre/verificacion.md: pruebas y evidencia.
- docs/plan.md: organización de specs y responsables.
- docs/adr/ADR-001-stack.md: decisión del stack.
- docs/decisiones.md: interpretaciones de requisitos.
- docs/registro-ia.md: uso real de IA por spec.
- docs/gasto.md: gasto y consumo del servicio de IA.
- docs/incidentes.md: incidentes reportados.

La estructura de código se definirá en el primer plan aprobado.
Actualizar este archivo en el mismo PR que cambie una convención.

## 11. Comandos de instalación y ejecución

Todavía no están disponibles: el repositorio es documental.

La primera implementación deberá documentar y verificar:
- Creación del entorno virtual.
- Instalación de dependencias con versiones fijadas.
- Configuración local de variables de entorno.
- Aplicación de migraciones.
- Generación de datos sintéticos.
- Reconstrucción de datos con un único comando.
- Ejecución del servidor.
- Ejecución de pruebas.

Actualizar esta sección y README.md con los comandos reales
cuando existan. No afirmar que un comando funciona sin probarlo.

## 12. Verificación y terminado

Comprobar los criterios de aceptación de la spec correspondiente.
Priorizar pruebas de permisos, aislamiento, datos, promedios,
temas débiles, tutor y funcionamiento sin red.

Registrar:
- Verificador.
- Computadora utilizada.
- Commit probado.
- Resultado por criterio.
- Evidencia.
- Correcciones y repetición de pruebas, cuando corresponda.

Una spec está terminada cuando:
- La spec y el plan están en main.
- Todos los criterios tienen verificación ajena y evidencia.
- Funciona desde main en otra computadora.
- El PR fue revisado y fusionado.
- El uso de IA está declarado.

Cada integrante debe poder explicar el sistema,
incluidas partes que no haya implementado.