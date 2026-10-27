# Decisiones de interpretación

## D-001 — Inicialización del repositorio

Requisito: N1 y N2.

Duda: el enunciado exige pull requests y no describe cómo
inicializar un repositorio vacío sin una rama base.

Decisión: crear un único commit inicial con README,
.gitignore y este registro. Después, proteger main
y realizar todos los cambios mediante pull requests.

Justificación: establecer una base documental para poder
abrir y revisar los siguientes pull requests.
Este commit no incluye código de la aplicación.