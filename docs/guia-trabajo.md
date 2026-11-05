# Guía de trabajo — TutoBosco

> Referencia rápida para el equipo. No es normativa: si hay alguna
> diferencia con `AGENTS.md` o `docs/plan.md`, prevalecen esos documentos.

## ¿La carpeta `specs/…` es una rama?

No. Son dos cosas distintas:

| Elemento | Ejemplo para S-001 |
|---|---|
| Rama Git | `s-001-esqueleto` |
| Carpeta de documentos | `specs/S-001-esqueleto/` |
| Archivo de especificación | `specs/S-001-esqueleto/spec.md` |

La rama es donde se trabaja con Git. La carpeta es donde viven los tres
documentos de cada spec: `spec.md`, `plan.md` y `verificacion.md`.

## ¿Cada spec lleva una rama hecha por su autor?

Sí. Una rama por spec, con nombre `s-NNN-nombre-corto`, creada por el autor.

El autor la lleva desde la especificación hasta el PR final:

1. Crear la rama (por ejemplo, `s-001-esqueleto`).
2. Redactar `spec.md` y abrir PR a `main` con `Ref #N`.
3. Cuando la spec se fusiona, seguir el código en la misma rama.
4. El PR de implementación cierra el issue con `Closes #N`.

El verificador es otra persona; prueba en su computadora y no crea la rama
del autor.

Nota: el enunciado escribe a veces `sNNN-nombre` y a veces
`s-NNN-nombre-corto`; en este repositorio se usa la forma con guiones.

## Tabla completa por spec

| Spec | Nombre | Requisito | Rama | Carpeta | Issue | Autor | Verificador |
|---|---|---|---|---|---|---|---|
| S-001 | Esqueleto | RF-01, RF-02 y RF-04 parciales; RNF-04 y RNF-06 parciales | `s-001-esqueleto` | `specs/S-001-esqueleto/` | #4 | JavEstrada09 | douglas-yasser |
| S-002 | Modelo y datos sintéticos | RNF-01; soporte de RF-02 y RF-03 | `s-002-datos-sinteticos` | `specs/S-002-datos-sinteticos/` | #6 | douglas-yasser | JavEstrada09 |
| S-003 | Perfil académico | RF-02 | `s-003-perfil-academico` | `specs/S-003-perfil-academico/` | #7 | AlexDLG1 | ramosdeleon555 |
| S-004 | Temas y asignación | RF-03 parcial | `s-004-temas-asignacion` | `specs/S-004-temas-asignacion/` | #8 | Brayan11Hernandez | AlexDLG1 |
| S-005 | Registro y corrección de notas | RF-03 parcial | `s-005-registro-notas` | `specs/S-005-registro-notas/` | #9 | AlexDLG1 | ramosdeleon555 |
| S-006 | Tutor personalizado | RF-04; RNF-05 | `s-006-tutor` | `specs/S-006-tutor/` | #10 | JavEstrada09 | douglas-yasser |
| S-007 | Temas débiles y ejercicios | RF-05 parcial; RNF-04 | `s-007-ejercicios` | `specs/S-007-ejercicios/` | #11 | ramosdeleon555 | Brayan11Hernandez |
| S-008 | Panel del docente | RF-06 | `s-008-panel-docente` | `specs/S-008-panel-docente/` | #12 | douglas-yasser | JavEstrada09 |
| S-009 | Respuestas y retroalimentación | RF-05 parcial; RNF-04 | `s-009-retroalimentacion` | `specs/S-009-retroalimentacion/` | #13 | ramosdeleon555 | Brayan11Hernandez |
| S-010 | Acceso, seguridad e interfaz | RF-01; RNF-07 | `s-010-acceso-seguridad` | `specs/S-010-acceso-seguridad/` | #14 | Brayan11Hernandez | AlexDLG1 |

## Responsabilidades por integrante

| Integrante | Autor de | Verificador de |
|---|---|---|
| JavEstrada09 | S-001, S-006 | S-002, S-008 |
| douglas-yasser | S-002, S-008 | S-001, S-006 |
| AlexDLG1 | S-003, S-005 | S-004, S-010 |
| Brayan11Hernandez | S-004, S-010 | S-007, S-009 |
| ramosdeleon555 | S-007, S-009 | S-003, S-005 |

Cada integrante queda con dos autorías y dos verificaciones de otros,
como exige el enunciado.

## Flujo por cada spec

1. Usar el issue ya creado y confirmar autor y verificador.
2. Redactar `spec.md` (qué y por qué; criterios Dado/Cuando/Entonces; exclusiones).
3. PR de especificación a `main` con `Ref #N`; revisor distinto aprueba y fusiona.
4. El agente propone `plan.md` en modo lectura; el autor lo corrige y aprueba.
5. Implementar en la misma rama con commits `S-NNN:`.
6. El autor lee y ejecuta cada cambio antes del commit.
7. El verificador prueba cada criterio en su computadora.
8. Llenar `verificacion.md` con resultados y evidencia.
9. PR de implementación con `Closes #N`; se fusiona solo con verificación completa.
