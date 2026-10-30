> Estado vigente: ver [ESTADO_ACTUAL.md](ESTADO_ACTUAL.md). Este documento conserva diseno o evidencia historica; las referencias a web pendiente anteriores al 18/10 quedaron superadas.

# Matriz de pruebas

Ultima corrida: **42 pruebas aprobadas en 11.25 s**. Evidencia vigente: `docs/evidencias/pytest.xml`. Primera corrida historica: 34 aprobadas en 10.52 s. Revision documental 2026-10-17; fechas de cada ejecucion en sus archivos. Datos sinteticos salvo inspeccion de entorno/archivos historicos. IMPLEMENTADO significa codigo disponible; PROBADO siempre indica alcance.

| ID | Precondicion / entrada | Esperado | Resultado real / estado | Evidencia |
|---|---|---|---|---|
| T01 | Studio + TLS valido + credenciales | Login/navegacion/extraccion comparada | BLOQUEADO web: certificado vencido; flujo pendiente | XPATH_DOM.md |
| T02 | Credenciales incorrectas | ERROR, captura segura, cierre | PENDIENTE Studio | MONTAJE_ROCKETBOT 12/38–40 |
| T03 | Selector roto/sesion vencida/vacio | distinguir los tres | PENDIENTE DOM | XPATH_DOM.md |
| T04 | Recorder compatible | export generado y replay real | PENDIENTE | EVIDENCIA_RECORDER.md |
| T05 | Controles nativos | For e IF visibles | PROBADO en DEMO_LOCAL_EP2: For, IF, While y Try Catch; flujo web/hijos pendiente | DEMO_NATIVA_ROCKETBOT |
| T06 | Fechas/importes validos e invalidos | Regex+semantica y Decimal | PROBADO auxiliares | test_core.py / pytest.xml |
| T07 | Maestro sintetico con metadata | lee, valida y cambia resultado | PROBADO auxiliares y demo nativa; datos web reales pendientes | test_master_and_report, demo nativa |
| T08 | MySQL autenticada + reglas | SQL altera flujo y persiste | IMPLEMENTADO; PENDIENTE credenciales/esquema | database/, auxiliares/database.py |
| T09 | Duplicados, ausentes, diferencia | 5 clases y multiplicidad intacta | PROBADO sintetico | test_classifications_and_duplicates |
| T10 | Export de datos tipados | 5 hojas, filtros, sin formulas | PROBADO lectura openpyxl; Excel GUI pendiente | demo reporte y test_master_and_report |
| T11 | Paso que lanza excepcion | inicio/fin/ms/equipo/error | PROBADO auxiliar; pasos exitosos de demo Studio probados; fallo web pendiente | test_audit_error_outbox_redaction_and_ids, demo nativa |
| T12 | Reenvio SQL/POST | no duplicar registros | POST PROBADO memoria concurrente; MySQL PENDIENTE | test_api.py; schema PK/UNIQUE |
| T13 | HTTP loopback GET/POST/GET | JSON/estado y acuse | PROBADO red local y coordinacion Studio con MemoryReceiptStore; MySQL PENDIENTE | test_api.py y DEMO_NATIVA_ROCKETBOT |
| T14 | 404/500/timeout/no JSON/conexion | ERROR diferenciado | PROBADO red/inyeccion controlada, ver HTTP_API | test_api.py |
| T15 | SQL/API caida | PARCIAL/ERROR + pendientes | PROBADO API 503 con storage inyectado y outbox; host real pendiente | test_client_evidence_and_sql_failure |
| T16 | Excepcion y cierre | recursos cerrados/estado coherente | PROBADO auxiliares; navegador Studio pendiente | audit/bridge; prueba real pendiente |
| T17 | Export padre/hijos | importar y editar completo | PENDIENTE export completo; proyecto creado por Studio | studio_creacion.json |
| T18 | Segunda PC fisica | SQL compartida y hostname distinto | PENDIENTE | CONFIGURACION_SEGUNDA_PC.md |
| T19 | Ejecuciones simultaneas | UUID/reportes diferentes | UUID local y POST concurrente PROBADOS; dos robots pendientes | test_core/test_api |
| T20 | Copia a ruta con espacios y otro cwd | leer config/SQL/maestro, generar JSON/log/Excel | PROBADO auxiliares y ZIP extraido; captura/Studio pendientes | test_portability.py, portabilidad_paquete.json |
| T21 | Documentos contra artefactos | estados fieles | IMPLEMENTADO, revision registrada | MATRIZ_TRAZABILIDAD |
| T22 | Informe/presentacion | PDF/PPT legibles | ver REVISION_ENTREGABLES | docs/entrega |
| T23 | Diagrama contra montaje | decisiones/errores consistentes | DISENO etiquetado; montaje real pendiente | diagramas/README |
| T24 | Mermaid/SVG/PDF | export visual sin cortes | renderizados; revision registrada | REVISION_ENTREGABLES |
| T25 | Ideacion + mediciones | decisiones y tiempos comparables | SCAMPER documentado; medicion manual/robot PENDIENTE | MEJORA_CONTINUA |

Demo nativa independiente de pytest: UUID e967c39e-3b8a-4df1-9d11-87dfcff8ac97, 38 comandos guardados y 61 solicitudes ejecutadas sin error de comando. Datos sinteticos, estado PARCIAL, 11.206 s del intervalo Audit; HTTP 200/201/200/200 y reporte Excel comprobados. Un ensayo previo interrumpido se conserva como tal. Las pruebas de outbox/cierre usan repositorio inyectado: no acreditan MySQL real.

Repetir: `ejecutar_ep2.bat -Action test`. No borrar historicos para mejorar evidencia. No ejecutar pruebas sobre datos reales sin configurar alcance. La prueba de servidor HTTP utiliza puerto aleatorio loopback y cierra sus recursos.
