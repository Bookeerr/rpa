> Estado vigente: ver [ESTADO_ACTUAL.md](ESTADO_ACTUAL.md). Este documento conserva diseno o evidencia historica; las referencias a web pendiente anteriores al 18/10 quedaron superadas.

# Montaje MAIN_TESTFIRE_EP2

**Estado del flujo web integral: PENDIENTE de montaje y ejecucion.** Studio esta instalado; proyecto real y DEMO_LOCAL_EP2 sintetica ejecutados. MAIN conserva el humo de runtime. No existe aun export completo padre/hijos del flujo web. El catalogo real se conserva en `docs/evidencias/catalogo_comandos_instalado.json`.

## Entorno y variables

Distribucion 2025.07.01, package.json build `2025.07.01_qa`; servicios segun manifiesto: web 1.7.4, logic 1.5.0, scripts 1.9.0, system 1.4.0. Los nombres siguientes son los del catalogo en espanol, incluso `Execute  Python` y `Click en objecto`. Version de cada servicio es de manifiesto, no compatibilidad de ejecucion acreditada.

Crear proyecto en Studio y padre MAIN_TESTFIRE_EP2. Crear hijos INIT_CONFIG, AUDIT_START, WEB_LOGIN, EXTRACT_ACCOUNTS, EXTRACT_TRANSACTIONS, VALIDATE_DATA, READ_REFERENCES, RECONCILE, SAVE_DATABASE, HTTP_INTEGRATION, EXPORT_EXCEL, ERROR_HANDLER, FINALIZE. Llamar con **Scripts / Ejecuta otro script RocketBot**, parametro command = nombre del hijo. El hijo hereda variables; no volver a declararlas con igual nombre.

Variables padre: PROJECT_ROOT (seleccionada al inicio, absoluta solo en memoria), execution_id, cfg, evento, intento, sesion_ok, tabla_ok, cuentas_web, cuentas_seleccionadas, cuenta, tabla, fila, indice, raw, validacion, reglas, master, pares, par, clasificacion, payload, respuesta, estado_global, error_original, captura_rel, captura_abs, reporte_rel. Inicializar estado_global='EN_CURSO', intento=1; contador de filas por cuenta estable.

`PROJECT_ROOT` debe apuntar a la carpeta que contiene README.md y auxiliaries; no al directorio de Studio. Se permite seleccionarla al iniciar. Las demas rutas se resuelven contra ella. Nunca usar `__file__` en el bloque embebido. `.env` lo lee el auxiliar, no Studio.

Antes del montaje, ejecutar `setup` y pruebas externas. Runtime real 3.13.5 e importaciones de auxiliares verificados mediante la demo nativa. Se instalo dotenv 1.2.4 y pytz 2026.5 en modules/libs; el runtime congelado no incluye zoneinfo. Ver ENTORNO.md. No agregar todo el site-packages externo a sys.path ni copiar binarios al runtime. El entorno `.venv-ep2` de API/pruebas es independiente.

Resolucion de raiz comprobada en la demo: `Path(r'%project_path%').resolve().parents[1]`, conservando la estructura `rocketbot/MAIN_TESTFIRE_EP2/robot.db`. `%project_path%` lo sustituye Studio. Solo la raiz resuelta vive en memoria; las referencias internas permanecen relativas.

## Tabla de comandos para construir

P = Scripts/Execute Python (scripts 1.9.0); L = Logica (1.5.0); W = Web (1.7.4); D = Desktop (version de manifiesto por registrar). Cada fila es un comando o bloque contenedor con numero estable; las llamadas auxiliares exactas estan en `rocketbot/BLOQUES_STUDIO.md`. Todos requieren prueba en Studio.

| N / step_id | Robot | Comando real / modulo | Parametros e entrada -> salida | Exito | Error |
|---|---|---|---|---|---|
| 01 / S01 | MAIN | Ejecuta otro script RocketBot / Scripts | command=INIT_CONFIG; PROJECT_ROOT -> cfg, execution_id | JSON y UUID | detener preflight, conservar mensaje local |
| 02 / S01 | INIT_CONFIG | Execute Python / P | bloque inicializacion; raiz -> cfg/UUID | dependencias importadas | no iniciar web |
| 03 / S01 | AUDIT_START | Execute Python / P | begin/end INIT_CONFIG; sync UUID | execution local y SQL | marcar PARCIAL/cola, sin falsear SQL |
| 04 / S02 | MAIN | Try Catch / L | Try: hijos 05–35; Catch: ERROR_HANDLER | completar o manejar excepcion | continuar siempre al cierre 36 |
| 05 / S02 | WEB_LOGIN | Execute Python / P | begin(WEB_LOGIN) -> evento | inicio UTC/ns | error local |
| 06 / S02 | WEB_LOGIN | Abrir navegador / W | option=firefox; url=cfg TESTFIRE_URL + login.jsp; id_driver=testfire | navegador creado | catch TLS/driver |
| 07 / S02 | WEB_LOGIN | Esperar por Objeto / W | object=XPath uid; option=xpath; wait_for=visible; wait_time=30; before=after=0 -> sesion_ok | True | IF False -> ERROR_HANDLER |
| 08 / S02 | WEB_LOGIN | Enviar texto Web / W | data=XPath uid; data_type=xpath; text=cfg TESTFIRE_USER; wait_time=30 | campo completado | catch |
| 09 / S02 | WEB_LOGIN | Enviar texto Web / W | data=XPath passw; text=cfg TESTFIRE_PASSWORD; data_type=xpath; wait_time=30 | campo completado | catch, nunca capturar password |
| 10 / S02 | WEB_LOGIN | Click en objecto / W | data=XPath btnSubmit; data_type=xpath; before=after=0; wait_time=30 | click | catch |
| 11 / S02 | WEB_LOGIN | Esperar por Objeto / W | selector unico de sesion por verificar; visible; 30 -> sesion_ok | sesion real | IF False -> credenciales/sesion/TLS segun evidencia |
| 12 / S02 | WEB_LOGIN | IF / L | sesion_ok; True end OK + web_ok=True | autentica | False end ERROR, error_original, ERROR_HANDLER |
| 13 / S03 | EXTRACT_ACCOUNTS | Extraer texto / W | selector opciones de cuenta verificado; option=xpath -> cuentas_web | cuentas no vacias | selector pendiente, no adivinar |
| 14 / S03 | EXTRACT_ACCOUNTS | Execute Python / P | read_rules(UUID) -> reglas | SQL autentica | PARCIAL, omitir conciliacion si sin referencias |
| 15 / S03 | EXTRACT_ACCOUNTS | For + IF / L | iterable=cuentas_web; var=cuenta; IF habilitada y seleccionada | lista exacta | cuenta ausente -> error; nunca sustituir |
| 16 / S04 | MAIN | For / L | iterable=cuentas_seleccionadas; var=cuenta; hijo EXTRACT_TRANSACTIONS | todas cuentas | catch por cuenta |
| 17 / S04 | EXTRACT_TRANSACTIONS | Click en objecto / W | enlace /bank/transaction.jsp; XPath comprobado | vista movimientos | catch |
| 18 / S04 | EXTRACT_TRANSACTIONS | Esperar por Objeto + IF / W,L | tabla y sesion; presente; 30 -> tabla_ok | ambas presentes | distinguir sesion vencida/selector/TLS |
| 19 / S04 | EXTRACT_TRANSACTIONS | Extraer tabla / W | identificator=XPath tabla; option=xpath; encode=False; code=utf-8 -> tabla | array con encabezados observados | rechazar estructura inesperada |
| 20 / S04 | EXTRACT_TRANSACTIONS | For / L | iterable=tabla sin encabezado validado; var=fila | recorrer todas | conservar fila malformada |
| 21 / S04 | EXTRACT_TRANSACTIONS | IF / L | fila cuenta == cuenta; fecha dentro periodo si parseable | raw cuenta/fecha/accion/importe/id/indice/url | descartar otra cuenta con conteo; invalida a rechazo |
| 22 / S05 | VALIDATE_DATA | Execute Python / P | validate(UUID,raw,date_format verificado) -> validacion | objeto valid/error | catch |
| 23 / S05 | VALIDATE_DATA | IF / L | validacion.valid; append_valid o append_rejected | conserva ambas salidas | no convertir a cero |
| 24 / S06 | READ_REFERENCES | Execute Python / P | read_excel(UUID,cuentas_seleccionadas) -> master | hash/cuenta/periodo validos | PARCIAL, omitir RECONCILE |
| 25 / S07 | RECONCILE | Execute Python / P | pairs(UUID) -> pares | candidatos conservan multiplicidad | catch |
| 26 / S07 | RECONCILE | For / L | iterable=pares; var=par | todos pares | catch |
| 27 / S07 | RECONCILE | IF / L | par.ambiguous -> AMBIGUO | clasificacion | siguiente IF |
| 28 / S07 | RECONCILE | IF / L | sin web -> SOLO_MASTER; sin master -> SOLO_WEB | clasificacion | siguiente IF |
| 29 / S07 | RECONCILE | IF / L | differences no vacio -> DISCREPANCIA; else CONCILIADO | append_result(UUID,par,estado) | catch |
| 30 / S08 | SAVE_DATABASE | Execute Python / P | queue_bundle(UUID), sync(UUID) separados | ACK comprobados | cola + PARCIAL |
| 31 / S09 | HTTP_INTEGRATION | Execute Python / P | http GET /health -> respuesta | valid y HTTP 200 | IF transitorio/reintentar o PARCIAL |
| 32 / S09 | HTTP_INTEGRATION | Execute Python / P | api_payload(UUID) -> payload congelado | resumen hasta envio | no estado final |
| 33 / S09 | HTTP_INTEGRATION | While + IF / L | intento <=1+MAX_RETRIES; POST mismo payload; respuesta.valid | 201/200 y UUID | retryable False -> salir; sin ciclo infinito |
| 34 / S09 | HTTP_INTEGRATION | Execute Python + IF / P,L | GET /executions/UUID; body == payload | http_ok=True | PARCIAL si diferencia/404 |
| 35 / S10 | EXPORT_EXCEL | Execute Python / P | export_excel(UUID,estado_global) -> reporte_rel | cinco hojas | ERROR, preservar JSON |
| 36 / S11 | FINALIZE | Try Catch + Cerrar navegador / L,W | cerrar id activo testfire | driver cerrado | registrar fallo secundario sin borrar original |
| 37 / S11 | FINALIZE | Execute Python / P | end paso; queue_bundle; sync; finalize(UUID,estado_global) | cierre local/SQL coherente | PARCIAL con cierre SQL pendiente |
| 38 / ERR | ERROR_HANDLER | Execute Python / P | end(evento,ERROR,error_original) | log original | no ocultar error primario |
| 39 / ERR | ERROR_HANDLER | Captura de Pantalla / D | path=captura_abs resuelta a output/UUID/capturas/evento.png | imagen sin secretos | Try Catch -> evento ADVERTENCIA |
| 40 / ERR | ERROR_HANDLER | IF / L | datos disponibles -> EXPORT_EXCEL PARCIAL; error login -> ERROR | cierre en 36 siempre | no declarar OK |

En cada hijo, envolver actividad con begin/end, incluido lectura SQL, captura y cada intento. `step_id` usa el nombre del subrobot; IDs S01–S11 son agrupaciones del diagrama, no eventos adicionales obligatorios. Agregar attempt y detalle de cuenta/fila a eventos cuando se repita un subrobot. Si cfg falla antes de Audit, conservar log de preflight y no afirmar que hubo ejecucion UUID.

## Orden de cierre

Cerrar navegador en un bloque independiente que se ejecute tanto tras Try como tras Catch. Terminar evento FINALIZE, guardar bundle HTTP y vaciar outbox; luego evaluar estado. Solo OK si web, referencias, SQL, HTTP y Excel confirmados y sin eventos de error pendientes; rechazos/discrepancias pueden dar ADVERTENCIA segun regla documentada. Esta version conservadora impide OK si quedo un ERROR incluso si un reintento posterior funciona. `finalize` protege la coherencia y guarda cierre local antes de intentar SQL final. Si falla SQL al cierre, deja PARCIAL y execution.json pendiente de reenvio.

Exportar desde padre incluyendo hijos y modulos, sin produccion; ver rocketbot/README.md. La interfaz nativa y su formato no se reemplazan por la base MySQL de negocio. No se entrega lanzador de runner porque no se verifico su licencia/sintaxis; usar Studio.
