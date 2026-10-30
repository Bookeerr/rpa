# Diagramas ? revision 18/10/2026

00_flujo_resumen representa el alcance ejecutado: login, tabla, Excel externo, API local y reporte. 05_mejora_proceso contrasta EP1 y resultado EP2. 06_demo_nativa es evidencia historica sintetica del 16/10, no la corrida web actual. 01/01a/01b/02/03/04 representan el alcance ampliado, incluido MySQL y cuentas/rango en origen pendientes. No son BPMN formal.

| Actividad | Implementacion real | step_id | Evidencia |
|---|---|---|---|
| Inicio | MAIN comando 1; raiz y UUID | Inicio Audit | execution.json |
| Login/extraccion | WEB_LOGIN y EXTRACT_TRANSACTIONS | WEB_LOGIN_EXTRACT | dom_table.json, web_rows_raw.json |
| Validacion | For filas + IF | VALIDATE_DATA | valid.json, rejected.json |
| Fuente externa | Maestro Excel previo | READ_REFERENCES | master_metadata.json |
| Conciliacion | For pares + IF anidados | RECONCILE | results.json |
| API | GET/POST/While/GET | HTTP_GET, HTTP_POST | api_calls.json y http/ |
| Reporte | Exportar Excel | EXPORT_EXCEL | Reporte_TestFire*.xlsx |
| Cierre | Cerrar navegador + finalizar | Resumen Audit | execution.json, artifacts.json |

UUID vigente y valores en ../evidencias/web_nativa_resumen.json. Inventario exacto de 54 comandos padre/hijos: ../NATIVO_MAIN_VERIFICADO.md. La evidencia de otra PC y lectura/escritura MySQL sigue pendiente.

Regenerar: powershell -File scripts/render_diagrams.ps1. Fuentes Mermaid con SVG/PDF/PNG; modelo ER derivado de database/schema.sql. Las ramas no recorridas por la corrida normal se comprueban mediante tests y demo sintetica, no se atribuyen a evidencia web.
