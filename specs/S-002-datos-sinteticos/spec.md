# S-002 Modelo de datos y datos sintéticos

Requisito: RNF-01; soporte de RF-02 y RF-03
Autor: douglas-yasser · Verificador: JavEstrada09 · Issue: #6
Estado: borrador

## Problema

Sin un modelo académico reproducible ni datos sintéticos, no se puede
demostrar el perfil, las notas, el panel ni el tutor sin usar datos reales.

## Comportamiento esperado

Como equipo, quiero reconstruir la base con datos sintéticos mediante
un único comando, para que cualquier computadora pueda ejecutar y
demostrar la aplicación.

## Criterios de aceptación

CA-1 Dado que ejecuto el comando de reconstrucción,
     cuando borro y regenero la base,
     entonces se crean al menos 30 estudiantes, 3 docentes y 4 cursos
     con 6 temas cada uno, uno de ellos Programación Comercial
     con los 6 temas del enunciado.

CA-2 Dado que genero los datos,
     cuando consulto la base,
     entonces hay notas variadas que producen perfiles claramente
     distintos, con y sin temas débiles.

CA-3 Dado que el script está versionado,
     cuando un integrante lo ejecuta en su computadora,
     entonces obtiene la misma base reproducible sin pasos manuales.

CA-4 Dado que el modelo admite varios cursos,
     cuando se define un curso,
     entonces se asocian docentes, estudiantes, temas, asignaciones
     y notas.

## Fuera de alcance

Pantalla de perfil (S-003), tutor (S-006), panel del docente (S-008)
y acceso por rol (S-001/S-010). El script no inserta datos reales.

## Datos y restricciones

- Solo datos sintéticos (RNF-01).
- No versionar la base SQLite; versionar migraciones y el script.
- Reconstrucción con un único comando documentado en el README.
- Dependencias: estructura de apps definida en S-001;
  decisiones D-003, D-004 y D-007.
- No usa IA.

## Registro de cambios

[se completa en cada cambio]
