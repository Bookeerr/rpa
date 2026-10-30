# Excel, SQL y conciliacion

`data/conciliacion_master.xlsx` es **SINTETICO**. Contiene Master y Metadata con periodo/version. `plantilla_master_real.xlsx` exige completar version y filas; no se sobrescribe. La lectura valida columnas, fechas, importes, cuentas seleccionadas y periodo exacto; registra SHA-256 y fecha UTC. Por defecto rechaza un maestro sintetico en flujo real.

SQL aporta `account_rules`: enabled, tolerance decimal y version. Studio lee reglas, decide cuentas y solo concilia las habilitadas. No reemplazar una cuenta ausente por otra disponible; esa conducta del antecedente EP1 se corrige en el diseno EP2.

Clave: con ID web, `(cuenta, ID)`; sin ID, `(cuenta, fecha, importe, descripcion normalizada, moneda)`. Los pares sin ID con misma multiplicidad se concilian por ocurrencia conservando todas las filas. Si la multiplicidad difiere, el grupo se marca AMBIGUO. IDs web repetidos tambien son ambiguos. No se usa hash para eliminar movimientos iguales. Si no hay ID y difiere el importe, no se presume identidad: aparecen SOLO_WEB/SOLO_MASTER. DISCREPANCIA corresponde a igual identidad web con diferencias de fecha, descripcion, moneda o importe mayor que tolerancia SQL.

`plan_pairs` calcula candidatos; Studio recorre con For y decide, en este orden: ambiguo, falta web, falta master, hay diferencias, conciliado. Ninguna decision de negocio debe esconderse en un unico script de ejecucion global.

MySQL usa DECIMAL(18,2), DATETIME(6), FKs, indices y parametros `%s`. `save_bundle` abre una transaccion corta y la cierra antes de volver a web. `(execution_id, cuenta, row_index)` identifica la extraccion y evita duplicar reintentos. Un UUID nuevo conserva el historial. Los IDs deterministas de resultados requieren conservar el mismo orden de pares al reintentar; la cola guarda ese snapshot.

Outbox: `output/<UUID>/outbox/*.json`; cada item inmutable tiene ACK separado. `replay` hace INSERT idempotente y solo luego ACK. Si hay caida antes del ACK, repetir no duplica. Reenviar con `ejecutar_ep2.bat -Action replay -ExecutionId <UUID>`. Revisar el estado global: reenviar evidencia no convierte retroactivamente una ejecucion PARCIAL en OK. `execution.json` es reenviado tambien al recuperar SQL.

Excel final: Movimientos, Conciliacion, Rechazados, Auditoria y Resumen. Encabezados/filtros, fechas tipadas, importes numericos y cadenas forzadas a texto para evitar formulas. Se actualiza la proyeccion final de auditoria al terminar exportacion/cierre; su escritura es sobrecarga local y no parte del paso de negocio medido. JSON es la autoridad si la proyeccion final falla. El resumen API se envia antes del cierre y nunca se confunde con el estado final.

Tablas de negocio y archivo/export nativo Rocketbot son independientes. `api_receipts` es adicional, sin FK a executions, para que la API tenga su propio contrato de recepcion. Cinco tablas enlazan executions: step_audit, transactions, reconciliation_results, api_calls y artifacts; account_rules es referencia independiente. Ver ER generado desde schema.sql.

MySQL real permanece **PENDIENTE por indicacion del usuario**. El cierre y reenvio de artefactos se probaron con repositorio inyectado: tras un fallo, artifacts.json conserva el hash del Excel ya marcado PARCIAL y replay recupera esa proyeccion final. Es evidencia de logica local, no de permisos, transacciones o concurrencia en el servidor existente.
