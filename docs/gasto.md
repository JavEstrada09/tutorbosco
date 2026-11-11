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
| 10-11-2026 | ramosdeleon555, prueba ejecutada mediante OpenCode | Gemini / `gemini-3.5-flash-lite` | S-007: generación real por HTTP para estudiante_03, PROG-COM, Ingeniería de prompts (nota 58; umbral 60) | Nivel gratuito; 1 solicitud real; 1 ejercicio; HTTP 200 en 6,12 s; tokens no recuperados | 0.00 | Gratuidad confirmada por Jeffersson el 11-11-2026; UUID `04ee22d6-a90a-485a-ae8e-0d227530cb94`; recorrido en `specs/S-007-ejercicios/verificacion.md` |
| 11-11-2026 | ramosdeleon555, prueba ejecutada mediante OpenCode | Gemini / `gemini-3.5-flash-lite` | S-009: retroalimentación real por HTTP de una respuesta de estudiante_03, PROG-COM, Ingeniería de prompts, nota 58 | Nivel gratuito; 1 solicitud real; 1 devolución; HTTP 200 en 4,69 s; tokens no recuperados | 0.00 | Gratuidad confirmada por Jeffersson el 11-11-2026; respuesta `54017c97-a5d1-4db7-8a61-551a057087db`; recorrido en `specs/S-009-retroalimentacion/verificacion.md` |

Las entradas anteriores a la prueba real de S-007 registran uso del nivel
gratuito sin habilitar facturación de pago. Para las llamadas de S-007 y S-009,
Jeffersson Daniel Ramos confirmó el 11-11-2026: «sí, usaron todo gratuitamente
con el modelo 3.5 flash lite de gemini, mediante su api correspondiente».
Se registra nivel gratuito y USD 0.00 con esa declaración como fuente,
no como una consulta del asistente al panel de Google ni un cálculo por tokens.
No se cambió la configuración de facturación durante las pruebas.

Gasto monetario de las llamadas registradas, incluidas S-007 y S-009: USD 0.00.
El total global de solicitudes y los tokens consumidos no están confirmados.
Costo cero no significa ausencia de llamadas ni de consumo de cuota gratuita.

### Detalle de consumo de la prueba real S-007

- Fecha local: 10-11-2026, 19:44, Guatemala (UTC−06:00).
- Registro persistido: `2026-11-11T01:44:04.025239+00:00`.
- Una generación real con el modelo configurado `gemini-3.5-flash-lite`.
  No se utilizó la alternativa demo y no se efectuaron reintentos de la prueba.
- Fuente disponible: ejecución HTTP del asistente y ejercicio guardado con
  procedencia `real`. No se conservó respuesta cruda ni metadata de tokens.
- Modalidad y costo: nivel gratuito, USD 0.00, confirmados por Jeffersson
  Daniel Ramos el 11-11-2026 en la conversación de cierre. No se consultó el
  panel del proveedor; los tokens permanecen como no recuperados.
- La latencia HTTP de 6,12 segundos no permite calcular tokens ni costo.

### Detalle de consumo de la prueba real S-009

- Fecha local del intento: 11-11-2026, 01:11:39, Guatemala (UTC−06:00).
- Respuesta creada: `2026-11-11T07:11:39.846621+00:00`.
- Una solicitud de retroalimentación a gemini-3.5-flash-lite, con un
  intento y sin fallback demo. No se solicitó generar un ejercicio nuevo.
- Fuente: recorrido HTTP del asistente, respuesta del estudiante y
  devolución persistida con source=real. No se recuperó metadata de tokens
  ni se conservó la respuesta HTTP cruda del proveedor.
- Duración observada: 4,69 segundos incluyendo envío y redirección HTTP;
  no permite deducir tokens ni costo.
- Modalidad y costo: nivel gratuito, USD 0.00, confirmados por Jeffersson
  Daniel Ramos el 11-11-2026 en la conversación de cierre. No se consultó el
  panel del proveedor; los tokens permanecen como no recuperados.

## Reglas

- Registrar las llamadas reales, incluidas las de cuota gratuita.
- Identificar si el costo es confirmado o estimado.
- No confundir ausencia de registros con ausencia de consumo.
- Revisar el consumo conjunto antes de realizar pruebas pagadas.
- Registrar la fuente utilizada para calcular o confirmar el gasto.
- No incluir claves ni información de pago en las evidencias.
- El modo demo utiliza respuestas locales y no debe llamar a la API.
