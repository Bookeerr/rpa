# TestFire EP2 — Robot, informe y presentacion

Para entender la ejecucion, la responsabilidad de cada archivo y como modificar el proyecto, leer [GUIA_COMPLETA_PROYECTO.md](GUIA_COMPLETA_PROYECTO.md).

Actualizacion 19/10/2026: [segunda PC validada](docs/VALIDACION_SEGUNDA_PC.md), con resumen persistido en este host y recuperado por la API. MySQL sigue pendiente. Las cifras de revisiones anteriores se conservan como historial.

Revision funcional mas reciente: [REVISION_FUNCIONAL.md](docs/REVISION_FUNCIONAL.md), con correcciones, 48 pruebas Python, 6 pruebas Node y una nueva ejecucion real. Las cifras de entrega siguientes corresponden a la corrida original identificada por UUID.

Actualizado el 18/10/2026. MAIN_TESTFIRE_EP2 ejecuta login y navegacion reales con comandos Rocketbot, extrae la tabla por XPath, valida filas, compara con un Excel externo y registra un resumen mediante GET/POST en una API local persistente. La EP1 original se conserva.

## Iniciar en este equipo

1. Abrir `INICIAR_EP2.bat` en la raiz. Inicia la API local y abre Studio.
2. Pulsar Run en MAIN_TESTFIRE_EP2 y mantener el editor abierto hasta finalizar. Si Studio estaba cerrado, responder la pregunta opcional de drivers y volver a abrir el lanzador.
3. Abrir el Excel de cinco hojas en `output/<UUID>/`. Revisar execution.json y las respuestas HTTP de esa misma carpeta.

Ejecucion 076648bf-3612-42b9-b915-d14cd7982d57: 96 validos, 4 rechazados; clasificaciones {'SOLO_MASTER': 100, 'SOLO_WEB': 96}; 206.514 s. Rechazos por causa: {'Importe fuera de DECIMAL(18,2)': 4}.

Reporte comprobado: `output/076648bf-3612-42b9-b915-d14cd7982d57/Reporte_TestFire_20261018_084434_076648bf-3612-42b9-b915-d14cd7982d57.xlsx`. GET health 200; POST 201; repeticion 200; GET acuse 200. API en 127.0.0.1:18081 con SQLite local explicita; no se presenta como MySQL. Token y cuenta se leen de .env privado.

## Entrega

- `docs/entrega/Informe_Tecnico_EP2.pdf`
- `docs/entrega/Presentacion_EP2.pptx` y `Presentacion_EP2.pdf`
- `docs/GUION_PRESENTACION.md`: 11 minutos y preguntas de defensa.
- `docs/MATRIZ_TRAZABILIDAD.md`: evidencia por indicador.
- `rocketbot/MAIN_TESTFIRE_EP2/robot.db`: proyecto nativo guardado por Studio.
- `rocketbot/MAIN_TESTFIRE_EP2/EXPORT_TESTFIRE_EP2.db`: export oficial editable con MAIN, WEB_LOGIN y EXTRACT_TRANSACTIONS, reabierto en Studio. Mantenerlo en esa carpeta relativa.
- `recorder/`: grabacion DOM real, comandos generados y procedimiento.
- `entrega/TestFire_EP2_20261018.zip`: paquete sin credenciales ni instalaciones.

## Limites que deben declararse

MySQL queda pendiente por indicacion del usuario. Segunda PC y aceptacion docente del grabador alternativo siguen pendientes. El estado tecnico PARCIAL conserva estas limitaciones; web_excel_api_complete=true acredita el alcance ejecutado. No se promete nota ni cumplimiento integral del prompt ampliado. La pauta permite Excel o SQL como fuente externa.

El maestro es un snapshot previo de TestFire, no una contabilidad independiente. El sitio compartido muestra los 100 movimientos mas recientes; no se afirma haber extraido todo su historial ni saldos. HTTP se usa exclusivamente en el sitio publico de demostracion porque su certificado HTTPS falla; no usar cuentas reales. El robot no realiza pagos ni transferencias.

Para otro equipo: instalar Rocketbot y dependencias con `ejecutar_ep2.bat -Action setup`; configurar .env local siguiendo `docs/ENTREGA_Y_PENDIENTES.md`; abrir el proyecto y comprobar antes de presentar. 45 pruebas: `ejecutar_ep2.bat -Action test`.
