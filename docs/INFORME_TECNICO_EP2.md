# Informe tecnico — TestFire EP2

ATY1102, Automatizacion de Procesos Roboticos I. Revision: 20/10/2026. Evaluacion anunciada: martes 20/10/2026. Equipo e integrante expositor: completar con sus nombres reales. El material documenta ejecuciones verificadas y pendientes, sin prometer calificacion.

## 1. Problema, alcance y continuidad EP1

La consulta repetitiva de movimientos exige acceder al sitio, copiar filas, validar formato y comparar una referencia. Se conserva prueba.py y los documentos EP1. La ampliacion utiliza Rocketbot como coordinador visible; Python realiza operaciones puntuales de validacion, lectura Excel, auditoria y HTTP. No se delega la navegacion del robot a un programa Selenium externo.

## 2. Entorno y arquitectura

Rocketbot Studio 2025.07.01, runtime Python 3.13.5 y Chrome. MAIN_TESTFIRE_EP2 coordina comandos web, For de filas/pares, IF de validacion/clasificacion, While de hasta tres intentos POST y Try Catch. API Flask separada con almacenamiento SQLite persistente. Admite modo local y modo LAN: el host comparte resumenes y el maestro Excel autenticado; cada PC conserva sus reportes locales. MySQL y su esquema de ocho tablas estan implementados como ampliacion pendiente por indicacion del usuario. SQLite local no sustituye una evidencia MySQL.

## 3. Recorder — IL 2.1

Se verificaron alternativas oficiales. DesktopRecorder respondio al inicio pero no capturo acciones en esta sesion; la descarga de la extension oficial no proporciono un paquete instalable. Se implemento el Grabador DOM propio EP2 v1: captura eventos trusted de entrada/click en una sesion real del navegador, conserva fecha, URL y XPath y exporta cuatro acciones. Los campos de credenciales se sustituyen por variables desde la captura, sin guardar sus valores. La secuencia generada se usa dentro de MAIN y se reproduce mediante comandos nativos. Evidencias: recorder/dom_recording.json, native_recorded_commands.json y captura recorder_dom_tabla.png. La aceptacion de esta alternativa por el docente queda PENDIENTE; no se atribuye al recorder oficial.

## 4. Extraccion y controles — IL 2.2

Login con campos uid/passw y btnSubmit; navegacion al enlace /bank/transaction.jsp; tabla _ctl0__ctl0_Content_Main_MyTransactions. Se comprobaron las cinco cabeceras reales: Transaction ID, Transaction Time, Account ID, Action, Amount. El comando Extraer tabla utiliza XPath. Se eliminan solo filas de maquetacion totalmente vacias; cambios de cabecera o longitud provocan error. El sitio presenta 100 movimientos recientes y fechas con precision de minuto; el contrato testfire_minute valida YYYY-MM-DD HH:MM. No se afirma captura exhaustiva de historial ni filtro por cuenta en origen.

Regex comprueba forma, strptime rechaza fechas imposibles y Decimal conserva precision monetaria. Importe 1,234.56 se interpreta como 1234.56; -$1234.00 conserva signo; 1.234,56 se rechaza. Se mantienen raw y normalizado. El periodo configurado se valida por fila y genera rechazos separados.

## 5. Fuente externa — IL 2.3

El archivo data/master_snapshot_testfire.xlsx contiene una captura anterior e independiente de la ejecucion nativa, con version y periodo. Se lee desde disco; no se reconstruye automaticamente con la tabla de la corrida. Se registra hash y metadata. Es una referencia tecnica de comparacion, no una fuente contable independiente. La pauta admite Excel o SQL. Las reglas locales declaran origen EXCEL-SNAPSHOT. Conciliacion por ID o clave/ocurrencia, sin perder duplicados: CONCILIADO, DISCREPANCIA, SOLO_WEB, SOLO_MASTER y AMBIGUO. Las pruebas sinteticas ejercitan discrepancias y duplicados aunque la corrida web no visite todas las ramas.

## 6. Servicio HTTP — IL 2.4

GET /health comprueba disponibilidad; POST /executions registra el resumen; un POST repetido confirma idempotencia; GET /executions/UUID comprueba igualdad del acuse. Resultados reales: 200, 201, 200 y 200. El almacenamiento local SQLite conserva el acuse entre reinicios y una clave primaria evita duplicados. Payload distinto con mismo UUID produce 409. Bearer token privado, timeout, reintentos acotados y evidencia request/response redactada. Las pruebas cubren 401, 404, 409, caidas, timeout y persistencia; esos errores no se atribuyen a la corrida normal.

## 7. Resultados y trazabilidad

Ejecucion 076648bf-3612-42b9-b915-d14cd7982d57: 96 validos, 4 rechazados; clasificaciones {'SOLO_MASTER': 100, 'SOLO_WEB': 96}; 206.514 s. Rechazos por causa: {'Importe fuera de DECIMAL(18,2)': 4}. Identificador completo en docs/evidencias/web_nativa_resumen.json. El reporte output/076648bf-3612-42b9-b915-d14cd7982d57/Reporte_TestFire_20261018_084434_076648bf-3612-42b9-b915-d14cd7982d57.xlsx contiene cinco hojas y trata texto como texto, evitando formulas inyectadas. La auditoria registra UUID de ejecucion/evento, equipo, usuario local, UTC, duracion monotona y hash de configuracion sin secretos. El resumen marca web_excel_api_complete=true. Estado global PARCIAL conserva SQL pendiente; la cola SQL no equivale a sincronizacion.

58 pruebas Python aprobadas en la revision del 19/10/2026, con JUnit en docs/evidencias/pytest_dependencias.xml. Incluyen dependencias portables sin site-packages y cliente HTTP compartido. Las 45 pruebas de la entrega inicial se conservan como evidencia historica. Hay pruebas de rutas con espacios, contratos HTTP, fechas, dinero, rechazo, multiplicidad, outbox y cierre ante fallo SQL. La prueba de auxiliares en copia local se distingue de la ejecucion fisica de la segunda PC, documentada a continuacion. Los intentos fallidos durante desarrollo se preservan con estado ERROR y no se suman como exitos.

## 7.1. Segunda PC y correcciones de portabilidad

El 19/10/2026 DESKTOP-OFQ9QLA ejecuto 6d450ccd-3e4a-4c19-a03d-d0f3aa9bdcc4 en modo ROCKETBOT_WEB_EXCEL_API_LAN: 96 validos, 4 rechazados, 100 SOLO_MASTER y 96 SOLO_WEB; duracion 103,525 s. El JSON recibido informa web_excel_api_complete=true y http_ok=true. Se comprobo su resumen en SQLite del host y mediante GET autenticado con HTTP 200; coinciden UUID, equipo y conteos. El Excel del cliente no fue recibido ni inspeccionado directamente. Evidencias: docs/evidencias/segunda_pc_execution.json y segunda_pc_verificada.json.

Se corrigieron la ruta fija del ejecutable y la disponibilidad de dotenv/pytz en el Python interno de Rocketbot. Las dependencias puras viajan en auxiliaries/_vendor con licencias y hashes; no se copia el entorno virtual del host. El maestro se descarga con autenticacion y verificacion de SHA-256. El estado PARCIAL original se conserva: MySQL sigue pendiente y SEGUNDA_PC era una etiqueta estatica del codigo anterior, superada por esta evidencia.

## 8. Ideacion y mejora — IL 2.5

SCAMPER: combinar referencia externa y lectura web; sustituir copia manual por extraccion estructurada; adaptar recorder a comandos; eliminar reingreso de resumen mediante API; reordenar cierre para preservar evidencia ante fallo. Se priorizaron controles de integridad sobre cantidad de acciones. No se declara porcentaje de ahorro: falta medir una muestra manual comparable. Mejoras siguientes: fuente contable independiente, filtros por cuenta/rango en origen, despliegue MySQL compartido y prueba simultanea de ambos robots.

## 9. Limites y presentacion

La prueba usa HTTP solo para el sitio publico TestFire porque HTTPS falla su certificado, sin desactivar globalmente validacion TLS. El sitio es compartido y mutable. MySQL y aceptacion docente del recorder alternativo son pendientes explicitos. La segunda PC ya fue validada con su resumen y acuse central; no se ha acreditado una corrida simultanea de ambos robots. La presentacion individual requiere ensayo real y autoria/aporte personal verdadero; guion de 11 minutos y preguntas incluidas. Los anexos de arquitectura SQL describen el alcance ampliado, no despliegue acreditado.
