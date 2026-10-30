# Validacion de la segunda PC - 19 de octubre de 2026

La ejecucion `6d450ccd-3e4a-4c19-a03d-d0f3aa9bdcc4` corresponde a **DESKTOP-OFQ9QLA**, la segunda PC. Su `execution.json`, recibido del usuario, informa cierre del flujo web/Excel/API. El resumen de esa misma ejecucion se encontro en SQLite del host y se recupero mediante GET autenticado con HTTP 200. Coinciden UUID, hostname y conteos.

| Comprobacion | Resultado |
|---|---|
| Modo | ROCKETBOT_WEB_EXCEL_API_LAN |
| Filas validas / rechazadas | 96 / 4 |
| Conciliacion | 100 SOLO_MASTER, 96 SOLO_WEB |
| Duracion total | 103,525 segundos, aproximadamente 1 min 44 s |
| Cierre informado | web_excel_api_complete=true, http_ok=true |
| Resumen en servidor | Encontrado; GET 200 y contenido coincidente con SQLite |
| Estado original | PARCIAL; se conserva sin modificar |

`SOLO_MASTER` y `SOLO_WEB` identifican registros presentes en una sola fuente. No demuestran por si solos un fallo del robot. El maestro es un snapshot previo y TestFire es compartido. Este archivo no detalla las causas de los cuatro rechazos; para verificarlas se necesitan `rejected.json` o la hoja Rechazados del Excel de esta corrida.

El cierre antiguo escribe siempre los pendientes `MYSQL_POR_INDICACION_USUARIO` y `SEGUNDA_PC`. La segunda etiqueta queda superada por esta evidencia y no es un error de conexion. MySQL sigue pendiente por indicacion del usuario. No se modifica retrospectivamente el resumen original ni se cambia PARCIAL a OK.

## Evidencias y limites

- [Resumen original de la segunda PC](evidencias/segunda_pc_execution.json), conservado byte por byte.
- [Verificacion contra el servidor](evidencias/segunda_pc_verificada.json), con SHA-256 del resumen y acuse recuperado.
- El Excel detallado permanece en `D:\TestFire_CLIENTE\output\6d450ccd-3e4a-4c19-a03d-d0f3aa9bdcc4` del cliente. Su generacion esta informada por el robot; el archivo no fue recibido ni inspeccionado directamente en esta revision.
- Se acredita una ejecucion desde la segunda PC con persistencia en el host. No se acredita una corrida simultanea de ambos robots ni una conexion MySQL.
- El hostname informado inicialmente por chat tenia una transposicion (`DESKTPO`); el JSON y el acuse del servidor coinciden en `DESKTOP-OFQ9QLA`.
