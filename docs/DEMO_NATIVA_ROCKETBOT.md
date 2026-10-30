> Estado vigente: ver [ESTADO_ACTUAL.md](ESTADO_ACTUAL.md). Este documento conserva diseno o evidencia historica; las referencias a web pendiente anteriores al 18/10 quedaron superadas.

# Demo nativa verificada: DEMO_LOCAL_EP2

Ejecucion del 2026-10-16; documentacion consolidada el 2026-10-17. **SINTETICA y PARCIAL**: no navega TestFire, no usa MySQL y no acredita recorder. Se guardo por Studio usando un proyecto real y plantillas de sus formularios; no se fabrico el formato SQLite.

UUID `e967c39e-3b8a-4df1-9d11-87dfcff8ac97`. Intervalo medido por Audit: **11.206 s** (una muestra, desde crear Audit hasta cerrar la ejecucion; no incluye arranque Studio ni reescritura final del Excel). No es una medicion de ahorro ni del proceso web completo.

38 comandos declarados; 61 solicitudes de ejecucion registradas por el editor, todas con status True. Las condiciones False normales no son fallos del comando. El For visita 4 filas; IF conserva 3 validas y 1 rechazo. Otro For clasifica 4 pares: CONCILIADO, DISCREPANCIA, SOLO_MASTER y SOLO_WEB. AMBIGUO tiene rama nativa y pruebas unitarias; esta muestra no recorre esa rama.

HTTP real desde comandos del robot hacia un proceso Flask separado: GET /health 200, POST /executions 201, POST identico 200 y GET /executions/UUID 200. El acuse coincide con el payload. API con memoria efimera, loopback 127.0.0.1:18080; no atribuir persistencia MySQL. While admite hasta tres intentos solo ante fallos transitorios; en esta ejecucion el primer POST fue suficiente.

Evidencia: `docs/evidencias/studio_demo.png`, `studio_demo_responses.json`, `demo_nativa_resumen.json`, y `output/e967c39e-3b8a-4df1-9d11-87dfcff8ac97/`. Excel de cinco hojas, execution.json, audit.jsonl, results.json, valid_rows.json, rejected_rows.json y HTTP redactado. El directorio output se conserva localmente; el paquete incluye esta ejecucion seleccionada.

Repetir: `ejecutar_ep2.bat -Action api-demo`; luego abrir `rocketbot/MAIN_TESTFIRE_EP2/MAIN_TESTFIRE_EP2.bat`, seleccionar DEMO_LOCAL_EP2 y pulsar Run. Mantener el editor abierto hasta finalizar. Ctrl+C detiene la API. Studio resuelve la raiz desde `%project_path%`; nunca guardar una ruta personal en comandos.

MAIN_TESTFIRE_EP2 aun es el humo de runtime. El flujo web real y sus subrobots estan especificados en MONTAJE_ROCKETBOT.md y BLOQUES_STUDIO.md, pendientes de montaje completo, DOM y credenciales.

## Comandos reales guardados

Robot: DEMO_LOCAL_EP2. Entradas/salidas son las variables declaradas en cada SetVar/GetVar del codigo y los parametros siguientes. Para Python, el texto exacto se conserva en el proyecto editable y el generador scripts/build_native_demo.py. EXITO: respuesta de comando status True y aserciones finales. ERROR: Try Catch salta a la rama de manejo; API invalida queda en auditoria y el cierre sigue PARCIAL. El cierre integral de recursos web no aplica a esta demo.

| Nativo | Comando / version | Parametros o operacion |
|---|---|---|
| 1 | Execute Python / scripts 1.9.0 | `import sys,json; from pathlib import Path; root=Path(r'%project_path%').resolve().parents[1]; assert (root/'auxiliaries').is_dir(), 'Raiz del proyecto incorrecta'; if str(root) not in sys.path: sys.path.insert(0,str(root)); from auxiliaries.studio_demo import initialize; SetVa...` |
| 2 | Try Catch / logic 1.5.0 | `` |
| 2.1 | Execute Python / scripts 1.9.0 | `SetVar('evento',bridge.begin(eid,'VALIDATE_DATA'))` |
| 2.2 | For / logic 1.5.0 | `{"iterable": "{filas_demo}", "count": 0} -> fila` |
| 2.2.1 | Execute Python / scripts 1.9.0 | `r=bridge.validate(eid,variable(GetVar('fila')),'iso'); SetVar('validacion',r); SetVar('es_valido',r['valid'])` |
| 2.2.2 | IF / logic 1.5.0 | `{es_valido}` |
| 2.2.2.1 | Execute Python / scripts 1.9.0 | `bridge.append_valid(eid,variable(GetVar('validacion'))['row'])` |
| 2.2.2.else.1 | Execute Python / scripts 1.9.0 | `bridge.append_rejected(eid,variable(GetVar('validacion')))` |
| 2.3 | Execute Python / scripts 1.9.0 | `bridge.end(eid,GetVar('evento')); SetVar('evento',bridge.begin(eid,'READ_REFERENCES')); bridge.read_excel(eid,{'800003'}); bridge.end(eid,GetVar('evento')); SetVar('pares',bridge.pairs(eid)); SetVar('evento',bridge.begin(eid,'RECONCILE'))` |
| 2.4 | For / logic 1.5.0 | `{"iterable": "{pares}", "count": 0} -> par` |
| 2.4.1 | Execute Python / scripts 1.9.0 | `p=variable(GetVar('par')); SetVar('es_ambiguo',p['ambiguous']); SetVar('sin_web',p['web'] is None); SetVar('sin_master',p['master'] is None); SetVar('con_diferencias',bool(p['differences']))` |
| 2.4.2 | IF / logic 1.5.0 | `{es_ambiguo}` |
| 2.4.2.1 | Execute Python / scripts 1.9.0 | `bridge.append_result(eid,variable(GetVar('par')),'AMBIGUO')` |
| 2.4.2.else.1 | IF / logic 1.5.0 | `{sin_web}` |
| 2.4.2.else.1.1 | Execute Python / scripts 1.9.0 | `bridge.append_result(eid,variable(GetVar('par')),'SOLO_MASTER')` |
| 2.4.2.else.1.else.1 | IF / logic 1.5.0 | `{sin_master}` |
| 2.4.2.else.1.else.1.1 | Execute Python / scripts 1.9.0 | `bridge.append_result(eid,variable(GetVar('par')),'SOLO_WEB')` |
| 2.4.2.else.1.else.1.else.1 | IF / logic 1.5.0 | `{con_diferencias}` |
| 2.4.2.else.1.else.1.else.1.1 | Execute Python / scripts 1.9.0 | `bridge.append_result(eid,variable(GetVar('par')),'DISCREPANCIA')` |
| 2.4.2.else.1.else.1.else.1.else.1 | Execute Python / scripts 1.9.0 | `bridge.append_result(eid,variable(GetVar('par')),'CONCILIADO')` |
| 2.5 | Execute Python / scripts 1.9.0 | `bridge.end(eid,GetVar('evento')); SetVar('respuesta',bridge.http(eid,'GET','/health')); SetVar('http_valid',variable(GetVar('respuesta'))['valid'])` |
| 2.6 | IF / logic 1.5.0 | `{http_valid}` |
| 2.6.1 | Execute Python / scripts 1.9.0 | `SetVar('payload',bridge.api_payload(eid)); SetVar('intento',1); SetVar('http_valid',False)` |
| 2.6.2 | While / logic 1.5.0 | `{intento} <= 3 and not {http_valid}` |
| 2.6.2.1 | Execute Python / scripts 1.9.0 | `r=bridge.http(eid,'POST','/executions',variable(GetVar('payload')),int(GetVar('intento'))); SetVar('http_valid',r['valid']); SetVar('retryable',r['retryable'])` |
| 2.6.2.2 | IF / logic 1.5.0 | `{retryable}` |
| 2.6.2.2.1 | Execute Python / scripts 1.9.0 | `SetVar('intento',int(GetVar('intento'))+1)` |
| 2.6.2.2.else.1 | Execute Python / scripts 1.9.0 | `SetVar('intento',4)` |
| 2.6.3 | IF / logic 1.5.0 | `{http_valid}` |
| 2.6.3.1 | Execute Python / scripts 1.9.0 | `r=bridge.http(eid,'POST','/executions',variable(GetVar('payload')),2); assert r['valid'] and r['http_status']==200; r=bridge.http(eid,'GET','/executions/'+eid); SetVar('acuse_ok',r['valid'] and r['body']==variable(GetVar('payload')))` |
| 2.6.3.2 | IF / logic 1.5.0 | `{acuse_ok}` |
| 2.6.3.2.1 | Execute Python / scripts 1.9.0 | `bridge.session(eid)['http_ok']=True` |
| 2.6.3.2.else.1 | Execute Python / scripts 1.9.0 | `print('ACUSE DIFERENTE: PARCIAL')` |
| 2.6.3.else.1 | Execute Python / scripts 1.9.0 | `print('POST no confirmado: PARCIAL')` |
| 2.6.else.1 | Execute Python / scripts 1.9.0 | `print('API demo no disponible: PARCIAL')` |
| 2.7 | Execute Python / scripts 1.9.0 | `SetVar('evento',bridge.begin(eid,'EXPORT_EXCEL')); SetVar('reporte_rel',bridge.export_excel(eid,'PARCIAL')); bridge.end(eid,GetVar('evento')); bridge.queue_bundle(eid)` |
| 2.else.1 | Execute Python / scripts 1.9.0 | `a=bridge.session(eid)['audit']; for event in list(a.active): a.end(event,'ERROR','Fallo en demo nativa; ver respuesta original de Studio'); a.write_json('native_error.json',{'status':'ERROR','detail':'Ver respuestas de Studio'})` |
| 3 | Execute Python / scripts 1.9.0 | `from auxiliaries.studio_demo import finalize; SetVar('reporte_rel',finalize(eid)); s=bridge.session(eid); assert len(s['valid'])==3 and len(s['rejected'])==1 and len(s['results'])==4; print('DEMO_ROCKETBOT_FIN',eid,GetVar('reporte_rel'),s['audit'].summary['status'])` |

## Incidencias reales

El primer ensayo de controles fallo porque SetVar no crea variables no declaradas; se corrigio declarandolas en el padre. El primer montaje de auxiliares fallo por ausencia de zoneinfo en el runtime congelado; se agrego adaptador pytz. Un ensayo se interrumpio al cerrar demasiado pronto el navegador de inspeccion: UUID 1184a952-f209-40ec-bf36-1348cc58d539, marcado INTERRUMPIDO con fecha de deteccion, sin inventar duracion final. La ejecucion aprobada anterior termino despues de corregir la espera. No se presentan esos intentos como exitosos.
