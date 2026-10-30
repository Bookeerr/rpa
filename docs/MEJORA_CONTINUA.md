# Ideacion y mejora continua

Tecnica aplicada: **SCAMPER**, registro de decisiones de esta ampliacion.

| Accion | Alternativa | Decision y evidencia |
|---|---|---|
| Sustituir | Selenium central por Rocketbot | Demo nativa ejecutada con For/IF/While/Try Catch; flujo web integral en montaje. Auxiliares no navegan. |
| Combinar | Tabla web + Excel maestro + reglas SQL | Implementado en validation/excel/reconciliation; pruebas sinteticas cambian clasificacion con tolerancia. |
| Adaptar | Logs EP1 a eventos UUID con monotono | Audit implementado; errores conservados y outbox. |
| Modificar | Duplicado por hash o por ocurrencia | Elegida ocurrencia para preservar multiplicidad; ambiguos separados. |
| Proponer otro uso | Resumen HTTP verificable | GET/POST/GET coordinado en demo nativa con memoria; SQL real pendiente. |
| Eliminar | Transferencias, correo, VM y orquestador inicial | Fuera de alcance; se reduce trabajo sin sacrificar consulta/conciliacion solicitada. |
| Reordenar | Exito antes de HTTP o cierre al final | Cierre global despues de integraciones/export; fallo queda PARCIAL/ERROR. |

Criterios: adecuacion a IL 2.1–2.5 del prompt, visibilidad en Studio, trazabilidad, portabilidad, costo de montaje y evidencia reproducible. Se descarta envolver `prueba.py` completo en un comando Rocketbot porque ocultaria controles y navegacion.

Antecedente comprobado: codigo Selenium, SQLite, graficos, Excel y logs historicos de septiembre. No se reejecuto EP1. El resumen historico informa 36.80 segundos para una corrida de una cuenta/un movimiento; no se usa como comparacion de rendimiento EP2, cuyo alcance es distinto.

Medicion manual y robot mismo alcance: **PENDIENTE**. Hacer tres repeticiones por modo, misma cuenta/periodo/numero de filas y mismas integraciones. Registrar preparacion aparte, inicio/fin monotono, errores y reintentos. Informar mediana y rango; no calcular ahorro hasta disponer de datos comparables. La duracion de pytest o de la demo sintetica no mide productividad del robot.

Dato observado: DEMO_LOCAL_EP2 registro 11.206 s en una muestra sintetica (UUID e967c39e-3b8a-4df1-9d11-87dfcff8ac97). Incluye validacion, conciliacion, HTTP y primer Excel entre inicio/cierre Audit; excluye arranque Studio, web, MySQL y reescritura final. Se usa para explicar instrumentacion, no para compararlo con los 36.80 s historicos de EP1.
