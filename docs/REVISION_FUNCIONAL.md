# Revision funcional del proyecto ? 18/10/2026

Resultado: el alcance actual **Rocketbot + web real + Excel externo + API local persistente** se ejecuto correctamente. No se declara validada la ampliacion MySQL ni otra computadora.

## Fallos encontrados y corregidos

| Hallazgo | Correccion | Evidencia |
|---|---|---|
| El comprobador de Studio podia terminar con salida exitosa tras un error o agotar el tiempo, y reconocer solo el texto de un comando final | Verifica todas las respuestas, cierre persistido, UUID de la corrida y confirmacion web/Excel/API; falla con codigo distinto de cero si no se cumplen | scripts/studio_verification.cjs y 6 pruebas Node |
| Una espera fija podia intentar pulsar Run antes de cargar el editor; ocurrio durante esta revision | Espera por presencia de boton habilitado, con limite de 45 segundos | scripts/studio_run_smoke.cjs y ejecucion real posterior |
| El contexto de sqlite3.Connection confirma/revierte, pero no garantiza cerrar la conexion al salir | Cierre explicito en constructor, health, GET y POST, incluido retorno por duplicado y excepcion | api/local_store.py; prueba de cierre de todas las conexiones |
| El cierre web podia conservar web_excel_api_complete=true si fallaba la escritura final del reporte o existia un error nativo registrado | Marca ERROR y false ante fallo final; rechaza completar una corrida con native_error.json | auxiliaries/studio_web.py; pruebas de Excel inaccesible y error nativo |

## Nueva ejecucion real

- UUID: `8227c107-4f77-45c8-a2c8-457b51249ff4`.
- Modo: `ROCKETBOT_WEB_EXCEL_API_LOCAL`.
- 1502 respuestas nativas, todas exitosas; login, navegacion, extraccion, For/IF/While, API, reporte y cierre de navegador.
- 96 filas validas y 4 rechazadas. Causas: {'Importe fuera de DECIMAL(18,2)': 4}.
- Clasificaciones: {'SOLO_WEB': 96, 'SOLO_MASTER': 100}. El maestro previo y el sitio compartido tienen movimientos diferentes; no se fabricaron coincidencias.
- Duracion Audit: 163.549 segundos.
- GET/POST/repeticion/GET: 200 / 201 / 200 / 200. Consulta adicional del acuse persistido: 200, payload identico.
- Reporte: `output/8227c107-4f77-45c8-a2c8-457b51249ff4/Reporte_TestFire_20261018_152220_8227c107-4f77-45c8-a2c8-457b51249ff4.xlsx`. Cinco hojas, conteos y SHA-256 comprobados.
- Pasos activos al cerrar: ninguno. Estado global PARCIAL por pendientes declarados, con web_excel_api_complete=true.

Respuestas y captura: `docs/evidencias/studio_revision_20261018_responses.json` y `studio_revision_20261018.png`. Resumen verificable: `docs/evidencias/revision_funcional.json`.

## Cobertura de revision

| Componente | Comprobacion | Resultado |
|---|---|---|
| Codigo Python | Sintaxis de modulos, scripts, tests y EP1 | Correcta |
| PowerShell y Node | Analisis sintactico de scripts activos | Correcto |
| Dependencias | pip check en .venv y .venv-ep2 | Sin dependencias rotas |
| Pruebas Python | Suite existente y regresiones nuevas | 48 aprobadas; pytest_revision.xml |
| Verificador Studio | Pruebas Node de errores, timeout, UUID y cierre | 6 aprobadas |
| Configuracion | Parametros locales, maestro de 100 filas, periodo y presencia de secretos sin publicarlos | Consistente para el modo local |
| Bases nativas | Integridad SQLite y presencia de MAIN/WEB_LOGIN/EXTRACT_TRANSACTIONS en proyecto y export | Correctas |
| API local | Health, acuse nuevo y acuse previo tras reiniciar el servicio propio | Persistencia confirmada |
| Base de acuses | PRAGMA integrity_check en modo lectura | ok |
| Robot y auxiliares | Corrida real identificada arriba | Correctos dentro del alcance declarado |
| Excel | Cinco hojas, cantidad de movimientos/rechazos y huella del artefacto | Correctos |
| Documentos | 12 paginas de informe, 8 de presentacion; lienzo/notas de 8 diapositivas | Comprobacion estructural correcta; no render de PowerPoint |
| Enlaces | Enlaces locales Markdown de docs | Sin destinos faltantes en la comprobacion |
| Portabilidad | Auxiliares del ZIP desde ruta con espacios y otro directorio de trabajo | Correcta; no acredita otra PC |

## Alcance pendiente

MySQL real sigue pendiente por indicacion del usuario. No se uso una cuenta SQL inventada ni se modifico .env. La prueba en segunda PC, la aceptacion docente del grabador alternativo y el render/ensayo en PowerPoint continuan pendientes. EP1 se reviso estaticamente y por dependencias; no se volvio a ejecutar en navegador.

El flujo actual usa el snapshot Excel previo y API SQLite local; cambiar credenciales SQL no activa automaticamente otro modo. Las esperas web y los intentos nativos actuales siguen fijados en el constructor, como explica GUIA_COMPLETA_PROYECTO.md. No se validaron todos los posibles cambios del sitio ni se promete ausencia absoluta de errores.

## Como repetir la revision

```powershell
.\.venv-ep2\Scripts\python.exe -m pytest tests -q -p no:cacheprovider
node --test tests/test_studio_verification.cjs
.\INICIAR_EP2.bat
```

Pulsar Run en MAIN y revisar la carpeta del UUID nuevo. Para la comprobacion automatizada de Studio, configurar PUPPETEER_MODULE, STUDIO_ROBOT=MAIN_TESTFIRE_EP2 y STUDIO_EVIDENCE con un nombre nuevo antes de ejecutar `node scripts/studio_run_smoke.cjs`; asi se conserva la evidencia historica.

El paquete incorpora la corrida original de entrega y esta revision. Los documentos de entrega originales mantienen sus cifras historicas; este informe registra las comprobaciones posteriores.
