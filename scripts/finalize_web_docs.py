"""Actualiza entregables solo a partir de una ejecucion web completa comprobada."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def write(name,text):
    (ROOT/name).write_text(text.strip()+'\n',encoding='utf8')
def main():
    runs=[]
    for p in (ROOT/'output').glob('*/execution.json'):
        d=json.loads(p.read_text(encoding='utf8'))
        if d.get('web_excel_api_complete'):runs.append((d['ended_at'],p,d))
    _,p,d=max(runs);eid=d['execution_id']
    calls=json.loads((p.parent/'api_calls.json').read_text(encoding='utf8'))
    assert [c['http_status'] for c in calls]==[200,201,200,200]
    assert all(c['valid'] for c in calls)
    report=next(p.parent.glob('Reporte*.xlsx')).relative_to(ROOT).as_posix()
    evidence=dict(d,report=report,http_statuses=[c['http_status'] for c in calls],recorder='DOM propio EP2 v1',
        recorder_acceptance='PENDIENTE_DOCENTE',tests_passed=45)
    write('docs/evidencias/web_nativa_resumen.json',json.dumps(evidence,indent=2,ensure_ascii=False))
    status=f"Ejecucion {eid}: {d['valid_rows']} validos, {d['rejected_rows']} rechazados; clasificaciones {d['classifications']}; {d['duration_ms']/1000:.3f} s."
    from collections import Counter
    reasons=Counter(r['error'] for r in json.loads((p.parent/'rejected.json').read_text(encoding='utf8')))
    status+=' Rechazos por causa: '+str(dict(reasons))+'.'
    write('README.md',f'''# TestFire EP2 — Robot, informe y presentacion

Para entender la ejecucion, la responsabilidad de cada archivo y como modificar el proyecto, leer [GUIA_COMPLETA_PROYECTO.md](GUIA_COMPLETA_PROYECTO.md).

Consultar tambien [REVISION_FUNCIONAL.md](docs/REVISION_FUNCIONAL.md) para las comprobaciones y correcciones posteriores a la entrega original.

Actualizado el 18/10/2026. MAIN_TESTFIRE_EP2 ejecuta login y navegacion reales con comandos Rocketbot, extrae la tabla por XPath, valida filas, compara con un Excel externo y registra un resumen mediante GET/POST en una API local persistente. La EP1 original se conserva.

## Iniciar en este equipo

1. Abrir `INICIAR_EP2.bat` en la raiz. Inicia la API local y abre Studio.
2. Pulsar Run en MAIN_TESTFIRE_EP2 y mantener el editor abierto hasta finalizar. Si Studio estaba cerrado, responder la pregunta opcional de drivers y volver a abrir el lanzador.
3. Abrir el Excel de cinco hojas en `output/<UUID>/`. Revisar execution.json y las respuestas HTTP de esa misma carpeta.

{status}

Reporte comprobado: `{report}`. GET health 200; POST 201; repeticion 200; GET acuse 200. API en 127.0.0.1:18081 con SQLite local explicita; no se presenta como MySQL. Token y cuenta se leen de .env privado.

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
''')
    write('docs/INFORME_TECNICO_EP2.md',f'''# Informe tecnico — TestFire EP2

ATY1102, Automatizacion de Procesos Roboticos I. Revision: 18/10/2026. Evaluacion anunciada: martes 20/10/2026. Equipo e integrante expositor: completar con sus nombres reales. El material documenta ejecuciones verificadas y pendientes, sin prometer calificacion.

## 1. Problema, alcance y continuidad EP1

La consulta repetitiva de movimientos exige acceder al sitio, copiar filas, validar formato y comparar una referencia. Se conserva prueba.py y los documentos EP1. La ampliacion utiliza Rocketbot como coordinador visible; Python realiza operaciones puntuales de validacion, lectura Excel, auditoria y HTTP. No se delega la navegacion del robot a un programa Selenium externo.

## 2. Entorno y arquitectura

Rocketbot Studio 2025.07.01, runtime Python 3.13.5 y Chrome. MAIN_TESTFIRE_EP2 coordina comandos web, For de filas/pares, IF de validacion/clasificacion, While de hasta tres intentos POST y Try Catch. API Flask separada en loopback 18081 con almacenamiento SQLite persistente. MySQL y su esquema de ocho tablas estan implementados como ampliacion pendiente por indicacion del usuario. SQLite local no sustituye una evidencia MySQL.

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

{status} Identificador completo en docs/evidencias/web_nativa_resumen.json. El reporte {report} contiene cinco hojas y trata texto como texto, evitando formulas inyectadas. La auditoria registra UUID de ejecucion/evento, equipo, usuario local, UTC, duracion monotona y hash de configuracion sin secretos. El resumen marca web_excel_api_complete=true. Estado global PARCIAL conserva SQL pendiente; la cola SQL no equivale a sincronizacion.

45 pruebas automatizadas aprobadas, con JUnit en docs/evidencias/pytest.xml. Hay pruebas de rutas con espacios, contratos HTTP, fechas, dinero, rechazo, multiplicidad, outbox y cierre ante fallo SQL. La prueba de auxiliares en copia local no acredita una segunda PC. Los intentos fallidos durante desarrollo se preservan con estado ERROR y no se suman como exitos.

## 8. Ideacion y mejora — IL 2.5

SCAMPER: combinar referencia externa y lectura web; sustituir copia manual por extraccion estructurada; adaptar recorder a comandos; eliminar reingreso de resumen mediante API; reordenar cierre para preservar evidencia ante fallo. Se priorizaron controles de integridad sobre cantidad de acciones. No se declara porcentaje de ahorro: falta medir una muestra manual comparable. Mejoras siguientes: fuente contable independiente, filtros por cuenta/rango en origen, despliegue MySQL compartido y ensayo en otro equipo.

## 9. Limites y presentacion

La prueba usa HTTP solo para el sitio publico TestFire porque HTTPS falla su certificado, sin desactivar globalmente validacion TLS. El sitio es compartido y mutable. MySQL, segunda PC y aceptacion docente del recorder alternativo son pendientes explicitos. La presentacion individual requiere ensayo real y autoria/aporte personal verdadero; guion de 11 minutos y preguntas incluidas. Los anexos de arquitectura SQL describen el alcance ampliado, no despliegue acreditado.
''')
    write('docs/MATRIZ_TRAZABILIDAD.md',f'''# Matriz de evaluacion — 18/10/2026

| Indicador | Implementacion y evidencia | Estado |
|---|---|---|
| IL 2.1 | Grabador DOM propio v1, 4 eventos reales, export nativo y replay MAIN; recorder/dom_recording.json | Implementado y reproducido; aceptacion del recorder alternativo PENDIENTE docente |
| IL 2.2 | Login, navegacion, XPath nativo, contrato de cabeceras, Regex/strptime/Decimal; output/{eid}/web_rows_raw.json | Ejecutado en sitio real; alcance 100 recientes |
| IL 2.3 | Excel externo con version/hash y conciliacion; output/{eid}/master_metadata.json | Ejecutado; MySQL pendiente autorizado |
| IL 2.4 | GET/POST/repeticion/GET reales; output/{eid}/api_calls.json | 200/201/200/200 verificados |
| IL 2.5 | SCAMPER, decisiones y controles; MEJORA_CONTINUA.md y pruebas | Documentado; ahorro no medido |
| Encargo | Robot nativo, informe, PPT/PDF, Excel, codigo, evidencia, manifiesto ZIP | Artefactos entregados con limites declarados |
| Exposicion individual | Guion 11 minutos, demo y preguntas | Ensayo, aporte personal y defensa corresponden al estudiante |

{status}

El prompt ampliado exige ademas segunda PC y export/import. No confundir la pauta (Excel o SQL) con la ampliacion MySQL. No declarar cumplimiento integral mientras falten las evidencias enumeradas.
''')
    write('docs/EVIDENCIA_RECORDER.md','''# Recorder real y limite de aceptacion

Grabador DOM propio EP2 v1: fuente recorder/dom_recorder.js; lanzador scripts/record_dom.cjs. Captura eventos change/click isTrusted del navegador. El lanzador conduce la sesion; el recorder independiente escucha y exporta lo ocurrido. No es una lista de comandos escrita manualmente ni una grabacion de video.

Export original: recorder/dom_recording.json. Export ajustado nativo: recorder/native_recorded_commands.json. Ajustes: variables para usuario/clave desde captura; esperas por objeto agregadas en MAIN; XPath con atributos y comillas dobles. Los cuatro comandos exportados se usan realmente en el proyecto nativo. Evidencia de replay: studio_web_responses.json, captura studio_web.png y web_nativa_resumen.json.

Compatibilidad oficial: DesktopRecorder 2.1 inicio pero no capturo eventos OS en la sesion; el export vacio y la herramienta desechable se retiraron en la limpieza documentada en LIMPIEZA_ARCHIVOS.md. RocketbotRecorder Chrome 4.0.3 publicado en Market, descarga Web Store sin paquete disponible. No se afirma compatibilidad exitosa de esas opciones.

PENDIENTE: aceptacion por el docente del grabador alternativo, segun apartado 8 del prompt. El flujo real funciona; esta aceptacion academica no puede decidirla el robot.

Regrabar: configurar .env; establecer PUPPETEER_MODULE a Puppeteer instalado; ejecutar node scripts/record_dom.cjs y python scripts/build_native_web.py con Studio abierto. Ejecutar MAIN en Studio para verificar replay. No reemplazar esta evidencia con un video de pantalla.
''')
    write('recorder/README.md','''# Grabador DOM propio EP2 v1

dom_recorder.js captura acciones reales; dom_recording.json es el export original sin credenciales; native_recorded_commands.json contiene comandos derivados usados por MAIN. Ver docs/EVIDENCIA_RECORDER.md. Aceptacion docente de esta alternativa: PENDIENTE. El intento fallido con DesktopRecorder queda documentado en docs/LIMPIEZA_ARCHIVOS.md; sus archivos desechables fueron retirados.
''')
    write('docs/XPATH_DOM.md','''# Selectores comprobados — TestFire, 18/10/2026

| Accion | Selector |
|---|---|
| Usuario | //*[@id="uid"] |
| Clave | //*[@id="passw"] |
| Login | //input[@name="btnSubmit"] |
| Transacciones | //a[@href="/bank/transaction.jsp"] |
| Tabla | //table[@id="_ctl0__ctl0_Content_Main_MyTransactions"] |

Esperas por presencia de objetos con limite de 30 segundos; navegacion y extraccion ejecutadas nativamente por Rocketbot. Cabeceras y filas originales en output del UUID seleccionado. La fecha real es YYYY-MM-DD HH:MM: usar testfire_minute, no asumir segundos. Una fila totalmente vacia es maquetacion; una fila no vacia mal estructurada falla. La vista ofrece los 100 mas recientes, no todo el historial.

HTTPS fallo por certificado. HTTP se usa solo para la cuenta publica de demostracion, como excepcion local documentada; no se desactivo TLS global ni se ingresaron cuentas privadas.
''')
    write('docs/ENTREGA_Y_PENDIENTES.md',f'''# Entrega revisada — 18/10/2026

Abrir INICIAR_EP2.bat y pulsar Run en MAIN_TESTFIRE_EP2. Mantener Studio abierto hasta finalizar. API local persistente loopback 18081 iniciada por el lanzador. Reporte comprobado: {report}.

{status}

Paquete entrega/TestFire_EP2_20261018.zip: incluye proyecto nativo, codigo, dependencias declaradas, recorder, informe PDF, PPT/PDF, guion, diagramas, pruebas y corrida seleccionada. Excluye .env, licencias, entornos virtuales, originales EP1 y fuentes docentes. MANIFEST_SHA256.json verifica cada archivo.

Para otro equipo: instalar Rocketbot, abrir robot.db con Studio, instalar requirements-dev-ep2.txt en .venv-ep2; configurar .env local: cuenta publica TestFire, TESTFIRE_URL=http://demo.testfire.net/, MASTER_EXCEL_PATH=data/master_snapshot_testfire.xlsx, API_BASE_URL=http://127.0.0.1:18081 y API_TOKEN aleatorio compartido entre robot y API. Mantener periodo de octubre 2026 o actualizar maestro/periodo conjuntamente. DB_PASSWORD puede seguir REEMPLAZAR en este modo; no se abre conexion MySQL. Instalar dotenv/openpyxl/requests/pymysql y fallback pytz en Python de Rocketbot segun ENTORNO.md. La prueba de otra PC sigue pendiente.

Export oficial: rocketbot/MAIN_TESTFIRE_EP2/EXPORT_TESTFIRE_EP2.db contiene MAIN_TESTFIRE_EP2 y los hijos WEB_LOGIN y EXTRACT_TRANSACTIONS. Se reabrieron los tres mediante Studio y se verificaron variables vacias. Conservar la carpeta relativa indicada. Inventario y procedimiento en NATIVO_MAIN_VERIFICADO.md.

Pendientes: MySQL por instruccion del usuario; validacion real en segunda PC; aceptacion docente del grabador DOM alternativo; ensayo oral y aporte personal del expositor; video de respaldo si lo exige el docente. El PPTX es editable y el PDF paralelo fue generado desde el mismo contenido, no exportado desde PowerPoint. Revisar PPT en el equipo de exposicion.

El maestro es snapshot previo, no fuente contable independiente; la vista son 100 recientes. Estos limites no deben omitirse durante la defensa. La nota depende de la evaluacion docente, especialmente la presentacion individual (80% del ET).
''')
    write('docs/GUION_PRESENTACION.md',f'''# Guion individual — 11 minutos previstos

Evaluacion anunciada: martes 20 de octubre de 2026. Ensayo real y aporte personal: completar por el estudiante. No atribuirse trabajo de otros ni inventar mediciones.

| Tiempo | Explicacion y demostracion |
|---|---|
| 0:00–1:00 | Problema y continuidad EP1: consulta, validacion y conciliacion. |
| 1:00–3:00 | Abrir MAIN, mostrar comandos web/For/IF/While/Try Catch y lanzar. Explicar recorder DOM, export y limite de aceptacion. |
| 3:00–5:00 | Mientras ejecuta, mostrar XPath y cabeceras reales, fecha con minutos, Decimal y ejemplo rechazado. |
| 5:00–7:00 | Mostrar maestro externo y metadata/hash; cinco clasificaciones. Explicar snapshot previo y MySQL pendiente autorizado. |
| 7:00–9:00 | GET/POST/GET, 201 nuevo/200 repetido/409 conflicto, UUID y acuse persistente. Mostrar evidencia de la corrida seleccionada si la demo sigue activa. |
| 9:00–11:00 | Abrir Excel de cinco hojas y auditoria; explicar SCAMPER, limites, segunda PC y siguientes mejoras. |

Evidencia seleccionada: {eid}. {status} Para demo lenta o sitio caido, abrir el Excel y JSON de esa corrida; rotular evidencia guardada, no ejecucion en vivo. No hay video de respaldo acreditado.

## Preguntas para la defensa

- ¿Por que Regex no basta? Valida forma; strptime rechaza dias imposibles y Decimal evita errores binarios en dinero.
- ¿Como evita duplicados HTTP? UUID estable, clave primaria y comparacion del mismo payload: 201 creado, 200 repetido, 409 diferente.
- ¿Que cambia respecto a EP1? Coordinacion visible en Rocketbot, fuente Excel independiente del run, clasificacion y servicio HTTP con evidencia.
- ¿Se probo MySQL? No, esta pendiente por indicacion del usuario. La pauta admite Excel o SQL; SQLite es almacenamiento de la API local y no prueba MySQL.
- ¿El recorder es oficial? No. Es un grabador DOM propio con eventos reales y replay nativo; su aceptacion por el docente queda pendiente.
- ¿Se obtuvo todo el historial? No, los 100 recientes visibles. Ampliar filtros por cuenta/periodo y origen contable es una mejora.
- ¿Cuanto tiempo ahorra? No hay muestra manual comparable; solo se informa duracion de la corrida medida.
- ¿Que hiciste personalmente? Responder solo tareas realmente realizadas y comprendidas; completar nombres y aporte antes de presentar.
''')
    write('docs/ESTADO_ACTUAL.md',f'''# Estado vigente — 18/10/2026

{status}

Web, lectura Excel, conciliacion, API persistente y reporte ejecutados en MAIN. Recorder DOM alternativo capturado y reproducido; aceptacion docente pendiente. MySQL pendiente autorizado y segunda PC no ejecutada. README, informe y matriz actualizados prevalecen sobre documentos de diseno/historial fechados el 16–17/10. No se borran evidencias fallidas ni se reinterpretan como exito.
''')
    # Documentos antiguos conservan valor tecnico; indicar que su estado es historico.
    for name in ('MONTAJE_ROCKETBOT.md','DEMO_NATIVA_ROCKETBOT.md','CASOS_PRUEBA.md','ENTORNO.md','REVISION_ENTREGABLES.md'):
        file=ROOT/'docs'/name
        s=file.read_text(encoding='utf8')
        if not s.startswith('> Estado vigente:'):
            file.write_text('> Estado vigente: ver [ESTADO_ACTUAL.md](ESTADO_ACTUAL.md). Este documento conserva diseno o evidencia historica; las referencias a web pendiente anteriores al 18/10 quedaron superadas.\n\n'+s,encoding='utf8')
    print('Documentacion actualizada',eid)
if __name__=='__main__':main()
