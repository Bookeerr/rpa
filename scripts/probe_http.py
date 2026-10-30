"""Evidencia HTTP real por loopback, almacen de prueba explicitamente etiquetado."""
from threading import Thread
from pathlib import Path
from uuid import uuid4
import json
import time
import requests
from flask import jsonify
from werkzeug.serving import make_server
from api.app import create_app, MemoryReceiptStore
from auxiliaries.config import ROOT, load_config
from auxiliaries.audit import Audit
from auxiliaries.http_client import call_http


def main():
    cfg=load_config(require_secrets=False)
    cfg['API_TOKEN']=str(uuid4())
    store=MemoryReceiptStore(); app=create_app(cfg,store)
    @app.get('/fault/500')
    def fail(): return jsonify(error='SIMULADO_500'),500
    @app.get('/fault/text')
    def text(): return 'SIMULADO_NO_JSON',200
    @app.get('/fault/timeout')
    def timeout(): time.sleep(0.2);return jsonify(status='ok')
    server=make_server('127.0.0.1',0,app,threaded=True)
    thread=Thread(target=server.serve_forever,daemon=True);thread.start()
    cfg['API_BASE_URL']=f'http://127.0.0.1:{server.server_port}'
    a=Audit(cfg,mode='HTTP_LOCAL_MEMORIA_PRUEBA')
    headers={'Authorization':'Bearer '+cfg['API_TOKEN']}
    p=dict(execution_id=a.id,equipo=a.summary['hostname'],estado_proceso='CONCILIACION_COMPLETADA',
           movimientos_validos=3,movimientos_rechazados=1,discrepancias=2,duracion_hasta_envio_ms=0)
    results=[]
    try:
        for method,url,body in [('GET','/health',None),('POST','/executions',p),('POST','/executions',p),('GET','/executions/'+a.id,None),('GET','/executions/'+str(uuid4()),None)]:
            results.append(call_http(cfg,a,method,url,body))
        for endpoint in ('500','text','timeout'):
            begin=time.perf_counter_ns();status=None;body=None;error=None
            try:
                r=requests.get(cfg['API_BASE_URL']+'/fault/'+endpoint,headers=headers,timeout=0.05 if endpoint=='timeout' else 2)
                status=r.status_code
                try:body=r.json()
                except ValueError:body=r.text;error='NON_JSON'
            except requests.Timeout:error='TIMEOUT'
            results.append(dict(simulated=True,endpoint='/fault/'+endpoint,status=status,body=body,error=error,duration_ms=(time.perf_counter_ns()-begin)/1e6))
        a.write_json('http_scenarios.json',results)
        a.finish('PARCIAL',scope='API local real; memoria de prueba; sin MySQL/Studio')
    finally:
        server.shutdown();thread.join(timeout=2);server.server_close()
    evidence=dict(execution_id=a.id,scope='HTTP real loopback con MemoryReceiptStore',
                  results=results,artifacts=(a.folder.relative_to(ROOT)).as_posix())
    (ROOT/'docs/evidencias/http_local.json').write_text(json.dumps(evidence,indent=2,ensure_ascii=False),encoding='utf-8')
    print('Evidencia HTTP:',a.id)


if __name__=='__main__':main()
