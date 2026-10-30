# Inventario nativo comprobado

Revision 18/10/2026. Export oficial generado mediante Studio /projectto en modo editable (produccion=0), con padre y dos hijos. No incluye framework ni modulos externos: las acciones son nativas y las dependencias Python se instalan separadamente. Se volvio a abrir cada robot del export mediante Studio; no se acredita otro equipo.

Ejecucion 076648bf-3612-42b9-b915-d14cd7982d57: 1502 respuestas de comando, todas True. La corrida incluye invocacion real de los hijos y cierre del navegador. SHA256 export: 7c099c29935b76701a46c15951774a654311e73306db6756af93489d28ed2a08.

Importar/abrir `rocketbot/MAIN_TESTFIRE_EP2/EXPORT_TESTFIRE_EP2.db` con Studio conservando esa ubicacion relativa dentro del proyecto; los auxiliares se resuelven desde `%project_path%`. Las variables declaradas del export estan vacias, incluidas usuario/clave. MAIN las carga desde .env local y los hijos las heredan. ROOT se fija en PROJECT_ROOT.

Exito web: presencia de elementos esperados, contrato de tabla validado y web_ok. Exito datos: valid/rejected y cinco clasificaciones controladas por IF/For. Exito HTTP: contrato, codigo y acuse iguales. Fallos: Try Catch registra el error; las respuestas originales estan en studio_web_responses.json. Export Excel y cierre conservan PARCIAL por MySQL pendiente; no se presenta un paso omitido como ejecutado.

| Robot:comando | Comando real | Modulo/version | Parametros y variables entrada/salida |
|---|---|---|---|
| MAIN_TESTFIRE_EP2:1 | execScriptPython | scripts 1.9.0 | `import sys<br>from pathlib import Path<br>root=Path(r'%project_path%').resolve().parents[1]<br>if str(root) not in sys.path:sys.path.insert(0,str(root))<br>import importlib<br>import auxiliaries.studio_web as web_adapter<br>importlib.reload(web_adapter)<br>from auxiliaries.studio_web import initialize<br>from auxiliaries import bridge<br>eid=initialize(root)<br>SetVar('execution_id',eid)<br>c=bridge.session(eid)['cfg']<br>SetVar('url_login',c['TESTFIRE_URL'].rstrip('/')+'/login.jsp')<br>SetVar('usuario',c['TESTFIRE_USER'])<br>SetVar('clave',c['TESTFIRE_PASSWORD'])<br>print('WEB_ROCKETBOT_INICIO',eid)<br>SetVar('PROJECT_ROOT',str(root))` |
| MAIN_TESTFIRE_EP2:2 | trycatch | logic 1.5.0 | `` |
| MAIN_TESTFIRE_EP2:2.1 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>SetVar('evento_web',bridge.begin(eid,'WEB_LOGIN_EXTRACT'))` |
| MAIN_TESTFIRE_EP2:2.2 | execRocketBotDB | scripts 1.9.0 | `WEB_LOGIN` |
| MAIN_TESTFIRE_EP2:2.3 | execRocketBotDB | scripts 1.9.0 | `EXTRACT_TRANSACTIONS` |
| MAIN_TESTFIRE_EP2:2.4 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>from auxiliaries.studio_web import rows<br>SetVar('filas_web',rows(eid,GetVar('tabla_web')))<br>bridge.end(eid,GetVar('evento_web'))` |
| MAIN_TESTFIRE_EP2:2.5 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>SetVar('evento',bridge.begin(eid,'VALIDATE_DATA'))` |
| MAIN_TESTFIRE_EP2:2.6 | for | logic 1.5.0 | `{"iterable": "{filas_web}", "count": 0}` |
| MAIN_TESTFIRE_EP2:2.6.1 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>r=bridge.validate(eid,variable(GetVar('fila')),'testfire_minute')<br>SetVar('validacion',r)<br>SetVar('es_valido',r['valid'])` |
| MAIN_TESTFIRE_EP2:2.6.2 | evaluateIf | logic 1.5.0 | `{es_valido}` |
| MAIN_TESTFIRE_EP2:2.6.2.1 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>bridge.append_valid(eid,variable(GetVar('validacion'))['row'])` |
| MAIN_TESTFIRE_EP2:2.6.2.else.1 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>bridge.append_rejected(eid,variable(GetVar('validacion')))` |
| MAIN_TESTFIRE_EP2:2.7 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>bridge.end(eid,GetVar('evento'))<br>SetVar('evento',bridge.begin(eid,'READ_REFERENCES'))<br>__import__('auxiliaries.studio_web',fromlist=['read_reference']).read_reference(eid)<br>bridge.end(eid,GetVar('evento'))<br>SetVar('pares',bridge.pairs(eid))<br>SetVar('evento',bridge.begin(eid,'RECONCILE'))` |
| MAIN_TESTFIRE_EP2:2.8 | for | logic 1.5.0 | `{"iterable": "{pares}", "count": 0}` |
| MAIN_TESTFIRE_EP2:2.8.1 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>p=variable(GetVar('par'))<br>SetVar('es_ambiguo',p['ambiguous'])<br>SetVar('sin_web',p['web'] is None)<br>SetVar('sin_master',p['master'] is None)<br>SetVar('con_diferencias',bool(p['differences']))` |
| MAIN_TESTFIRE_EP2:2.8.2 | evaluateIf | logic 1.5.0 | `{es_ambiguo}` |
| MAIN_TESTFIRE_EP2:2.8.2.1 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>bridge.append_result(eid,variable(GetVar('par')),'AMBIGUO')` |
| MAIN_TESTFIRE_EP2:2.8.2.else.1 | evaluateIf | logic 1.5.0 | `{sin_web}` |
| MAIN_TESTFIRE_EP2:2.8.2.else.1.1 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>bridge.append_result(eid,variable(GetVar('par')),'SOLO_MASTER')` |
| MAIN_TESTFIRE_EP2:2.8.2.else.1.else.1 | evaluateIf | logic 1.5.0 | `{sin_master}` |
| MAIN_TESTFIRE_EP2:2.8.2.else.1.else.1.1 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>bridge.append_result(eid,variable(GetVar('par')),'SOLO_WEB')` |
| MAIN_TESTFIRE_EP2:2.8.2.else.1.else.1.else.1 | evaluateIf | logic 1.5.0 | `{con_diferencias}` |
| MAIN_TESTFIRE_EP2:2.8.2.else.1.else.1.else.1.1 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>bridge.append_result(eid,variable(GetVar('par')),'DISCREPANCIA')` |
| MAIN_TESTFIRE_EP2:2.8.2.else.1.else.1.else.1.else.1 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>bridge.append_result(eid,variable(GetVar('par')),'CONCILIADO')` |
| MAIN_TESTFIRE_EP2:2.9 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>bridge.end(eid,GetVar('evento'))<br>SetVar('respuesta',bridge.http(eid,'GET','/health'))<br>SetVar('http_valid',variable(GetVar('respuesta'))['valid'])` |
| MAIN_TESTFIRE_EP2:2.10 | evaluateIf | logic 1.5.0 | `{http_valid}` |
| MAIN_TESTFIRE_EP2:2.10.1 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>SetVar('payload',bridge.api_payload(eid))<br>SetVar('intento',1)<br>SetVar('http_valid',False)` |
| MAIN_TESTFIRE_EP2:2.10.2 | evaluatewhile | logic 1.5.0 | `{intento} <= 3 and not {http_valid}` |
| MAIN_TESTFIRE_EP2:2.10.2.1 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>r=bridge.http(eid,'POST','/executions',variable(GetVar('payload')),int(GetVar('intento')))<br>SetVar('http_valid',r['valid'])<br>SetVar('retryable',r['retryable'])` |
| MAIN_TESTFIRE_EP2:2.10.2.2 | evaluateIf | logic 1.5.0 | `{retryable}` |
| MAIN_TESTFIRE_EP2:2.10.2.2.1 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>SetVar('intento',int(GetVar('intento'))+1)` |
| MAIN_TESTFIRE_EP2:2.10.2.2.else.1 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>SetVar('intento',4)` |
| MAIN_TESTFIRE_EP2:2.10.3 | evaluateIf | logic 1.5.0 | `{http_valid}` |
| MAIN_TESTFIRE_EP2:2.10.3.1 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>r=bridge.http(eid,'POST','/executions',variable(GetVar('payload')),2)<br>assert r['valid'] and r['http_status']==200<br>r=bridge.http(eid,'GET','/executions/'+eid)<br>SetVar('acuse_ok',r['valid'] and r['body']==variable(GetVar('payload')))` |
| MAIN_TESTFIRE_EP2:2.10.3.2 | evaluateIf | logic 1.5.0 | `{acuse_ok}` |
| MAIN_TESTFIRE_EP2:2.10.3.2.1 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>bridge.session(eid)['http_ok']=True` |
| MAIN_TESTFIRE_EP2:2.10.3.2.else.1 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>print('ACUSE DIFERENTE: PARCIAL')` |
| MAIN_TESTFIRE_EP2:2.10.3.else.1 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>print('POST no confirmado: PARCIAL')` |
| MAIN_TESTFIRE_EP2:2.10.else.1 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>print('API demo no disponible: PARCIAL')` |
| MAIN_TESTFIRE_EP2:2.11 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>SetVar('evento',bridge.begin(eid,'EXPORT_EXCEL'))<br>SetVar('reporte_rel',bridge.export_excel(eid,'PARCIAL'))<br>bridge.end(eid,GetVar('evento'))<br>bridge.queue_bundle(eid)` |
| MAIN_TESTFIRE_EP2:2.else.1 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>a=bridge.session(eid)['audit']<br>for event in list(a.active):a.end(event,'ERROR','Fallo de comando nativo; revisar evidencia Studio')<br>a.write_json('native_error.json',{'status':'ERROR'})` |
| MAIN_TESTFIRE_EP2:3 | trycatch | logic 1.5.0 | `` |
| MAIN_TESTFIRE_EP2:3.1 | killdriver | web 1.7.4 | `` |
| MAIN_TESTFIRE_EP2:3.else.1 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>bridge.session(eid)['audit'].write_json('browser_close.json',{'status':'ADVERTENCIA','detail':'Navegador no disponible para cierre'})` |
| MAIN_TESTFIRE_EP2:4 | execScriptPython | scripts 1.9.0 | `from auxiliaries import bridge<br>from auxiliaries.studio_demo import variable<br>eid=GetVar('execution_id')<br>from auxiliaries.studio_web import finalize<br>SetVar('reporte_rel',finalize(eid))<br>s=bridge.session(eid)<br>print('WEB_ROCKETBOT_FIN',eid,'web_excel_api_complete='+str(s['audit'].summary['web_excel_api_complete']),GetVar('reporte_rel'))` |
| WEB_LOGIN:1 | openbrowser | web 1.7.4 | `{"url": "{url_login}", "id_driver": "", "profile": ""}` |
| WEB_LOGIN:2 | waitforobject | web 1.7.4 | `{"object": "//input[@name='uid']", "wait_time": 30, "wait_for": "present", "before": 0, "after": 0}` |
| WEB_LOGIN:3 | sendkey_web | web 1.7.4 | `{"data": "//*[@id=\"uid\"]", "data_type": "xpath", "wait_time": 30, "text": "{usuario}", "special": ""}` |
| WEB_LOGIN:4 | sendkey_web | web 1.7.4 | `{"data": "//*[@id=\"passw\"]", "data_type": "xpath", "wait_time": 30, "text": "{clave}", "special": ""}` |
| WEB_LOGIN:5 | click_web | web 1.7.4 | `{"data": "//input[@name=\"btnSubmit\"]", "data_type": "xpath", "before": "0", "wait_time": "30", "after": "1", "move": false}` |
| WEB_LOGIN:6 | waitforobject | web 1.7.4 | `{"object": "//a[@href='/bank/transaction.jsp']", "wait_time": 30, "wait_for": "present", "before": 0, "after": 0}` |
| EXTRACT_TRANSACTIONS:1 | click_web | web 1.7.4 | `{"data": "//*[@id=\"MenuHyperLink2\"]", "data_type": "xpath", "before": "0", "wait_time": "30", "after": "1", "move": false}` |
| EXTRACT_TRANSACTIONS:2 | waitforobject | web 1.7.4 | `{"object": "//table[@id='_ctl0__ctl0_Content_Main_MyTransactions']", "wait_time": 30, "wait_for": "present", "before": 0, "after": 0}` |
| EXTRACT_TRANSACTIONS:3 | gettable_extend | web 1.7.4 | `{"identificator": "//table[@id=\"_ctl0__ctl0_Content_Main_MyTransactions\"]", "option": "xpath", "encode": false, "code": "", "result": "tabla_web"}` |
