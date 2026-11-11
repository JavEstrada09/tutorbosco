# Registro de gasto de IA

## Presupuesto

Tope global: USD 10 durante todo el proyecto.

El límite corresponde al servicio de IA utilizado por TutoBosco
y se comparte entre los cinco integrantes.

## Modalidad inicial

El modelo predeterminado es Gemini 3.5 Flash-Lite (`gemini-3.5-flash-lite`) en
Google Gemini API, priorizando el nivel gratuito.

No se habilitará facturación de pago en la etapa inicial.
Si el equipo evalúa habilitarla posteriormente, requerirá
acuerdo previo y el tope global de USD 10 seguirá vigente.
Al agotarse la cuota se utilizará el modo demo, sin activar
pagos automáticos.

## Registro

| Fecha | Responsable | Proveedor y modelo | Uso | Consumo o cuota | Costo USD | Evidencia |
| --- | --- | --- | --- | --- | --- | --- |
| 07-11-2026 | JavEstrada09 | Gemini simulado / `gemini-3.8-flash` | 44 pruebas automatizadas de Entrega 3 | No aplica; las pruebas usan simulaciones y el constructor usa un mock | No aplica | Suite automatizada, sin solicitudes al servicio |
| 08-11-2026 | JavEstrada09 | Gemini / `gemini-3.8-flash` | CA-4 en la interfaz y diagnóstico directo; se observaron errores 429 y 504 en otros intentos | Nivel gratuito; total de solicitudes y tokens no confirmados | 0.00 | Dos respuestas en la interfaz, una consulta directa exitosa y errores observados |
| 08-11-2026 | JavEstrada09 | Gemini simulado / `gemini-3.8-flash` | 48 pruebas y recorrido demo aislado de Entrega 4 | No aplica; Gemini y la red fueron simulados o bloqueados | No aplica | Suite completa y recorrido demo sin solicitudes al servicio |
| 08-11-2026 | JavEstrada09 | Gemini simulado / `gemini-3.8-flash` | 49 pruebas tras corregir espera y reintentos de Entrega 4 | No aplica; `429` y el cliente se simularon sin usar cuota | No aplica | Suite completa, un solo intento y sin solicitudes al servicio |
| 09-11-2026 | douglas-yasser | Gemini / `gemini-3.8-flash` | Tres intentos reales de CA-4 y diagnóstico en la verificación independiente | Nivel gratuito; 3 solicitudes; tokens no confirmados | 0.00 | `504 DEADLINE_EXCEEDED`, agotamiento del plazo y error del proveedor |
| 09-11-2026 | douglas-yasser | Gemini / `gemini-3.5-flash-lite` | Dos consultas reales de CA-4: servicio y interfaz | Nivel gratuito; 2 solicitudes; tokens no confirmados | 0.00 | Respuestas reales en 4.531 s y 4.12 s |
| 09-11-2026 | douglas-yasser | Gemini simulado / `gemini-3.5-flash-lite` | 50 pruebas y recorrido demo con Python 3.12.10 y 3.13.14 | No aplica; Gemini y la red fueron simulados o bloqueados | No aplica | Suite completa y recorrido demo sin solicitudes al servicio |
| 10-11-2026 | douglas-yasser | Gemini / `gemini-3.5-flash-lite` | Verificación independiente S-006: CA-1 y CA-5 en modo real, incluidos diagnósticos de respuestas crudas y repetición por HTTP | Nivel gratuito; 10 solicitudes reales; tokens no confirmados | 0.00 | Respuestas reales y análisis de validación; ver `specs/S-006-tutor/verificacion.md` |
| 10-11-2026 | douglas-yasser | Gemini / `gemini-3.5-flash-lite` | Repetición independiente S-006 sobre `30ad0c3`: CA-1 (2 solicitudes) y CA-5 (2 solicitudes) en modo real | Nivel gratuito; 4 solicitudes reales; tokens no confirmados | 0.00 | Respuestas reales mostradas en la interfaz; ver `specs/S-006-tutor/verificacion.md` |

Se utilizó el nivel gratuito sin habilitar facturación de pago. El total de
solicitudes y los tokens consumidos no están confirmados.

Gasto monetario registrado total: USD 0.00. Este valor registra que no hubo
cargo monetario; no afirma que el consumo de solicitudes o tokens fuera cero.

## Reglas

- Registrar las llamadas reales, incluidas las de cuota gratuita.
- Identificar si el costo es confirmado o estimado.
- No confundir ausencia de registros con ausencia de consumo.
- Revisar el consumo conjunto antes de realizar pruebas pagadas.
- Registrar la fuente utilizada para calcular o confirmar el gasto.
- No incluir claves ni información de pago en las evidencias.
- El modo demo utiliza respuestas locales y no debe llamar a la API.
