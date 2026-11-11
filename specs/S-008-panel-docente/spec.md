# S-008 Panel del docente

Requisito: RF-06
Autor: douglas-yasser · Verificador: JavEstrada09 · Issue: #12
Estado: terminada

## Problema

El docente no tiene una vista rápida del avance y de los temas débiles
de sus estudiantes por curso.

## Comportamiento esperado

Como docente, quiero ver, por cada curso que imparto, la lista de
estudiantes con su promedio y temas débiles, ordenable por promedio,
y por tema cuántos estudiantes lo tienen débil.

## Criterios de aceptación

CA-1 Dado que imparto un curso,
     cuando abro el panel de ese curso,
     entonces veo la lista de estudiantes con promedio y temas débiles,
     coincidiendo con la base de datos.

CA-2 Dado que veo la lista,
     cuando ordeno por promedio,
     entonces el orden cambia según el promedio calculado.

CA-3 Dado que selecciono un estudiante,
     cuando abro su detalle,
     entonces veo su promedio y sus temas débiles.

CA-4 Dado que consulto por tema,
     cuando abro el panel,
     entonces veo cuántos estudiantes lo tienen débil.

CA-5 Dado que solo imparto algunos cursos,
     cuando intento ver otro curso,
     entonces el sistema lo impide (permiso verificado en servidor).

## Fuera de alcance

Registro y corrección de notas (S-005), administración de temas y
asignación (S-004) y tutor (S-006).

## Datos y restricciones

- Promedio y tema débil calculados de forma centralizada
  (decisiones D-002, D-003 y D-004).
- Los números deben coincidir con la base de datos.
- Permisos verificados en servidor, no solo ocultando botones.
- Dependencia: S-002 (modelo y datos).
- No usa IA.

## Registro de cambios

10-11-2026 · Plan aprobado por douglas-yasser e implementación del panel del docente · —

10-11-2026 · Implementación fusionada mediante el PR #44, que cerró el
issue #12. JavEstrada09 verificó CA-1 a CA-5 en Windows y registró
capturas y resultados en `verificacion.md`. La revisión técnica de apoyo
comprobó `9126626` en Linux con 110 pruebas de `accounts academics tutor`
correctas y validó los números contra la base de datos.
