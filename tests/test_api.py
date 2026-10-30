from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from uuid import uuid4
import time
import pytest
import requests
from werkzeug.serving import make_server
from flask import jsonify
from api.app import create_app, MemoryReceiptStore
from auxiliaries.http_client import call_http
from auxiliaries.audit import Audit
from tests.test_core import config_tmp


def payload():
    return dict(execution_id=str(uuid4()),equipo='SINTETICO',estado_proceso='CONCILIACION_COMPLETADA',
                movimientos_validos=3,movimientos_rechazados=1,discrepancias=2,duracion_hasta_envio_ms=10)


@pytest.fixture
def server(tmp_path):
    cfg=config_tmp(tmp_path); cfg['API_TOKEN']='test-secret'; cfg['HTTP_TIMEOUT_SECONDS']=0.05
    store=MemoryReceiptStore(); app=create_app(cfg,store)
    # Endpoints de fallo solo existen en esta app de prueba.
    @app.get('/fault/500')
    def fail(): return jsonify(error='simulated'),500
    @app.get('/fault/text')
    def text(): return 'not json',200
    @app.get('/fault/timeout')
    def timeout(): time.sleep(0.15); return jsonify(status='ok')
    srv=make_server('127.0.0.1',0,app,threaded=True)
    thread=Thread(target=srv.serve_forever,daemon=True); thread.start()
    cfg['API_BASE_URL']=f'http://127.0.0.1:{srv.server_port}'
    yield cfg,store
    srv.shutdown(); thread.join(timeout=2); srv.server_close()


def test_real_http_get_post_idempotency_conflict_auth(server):
    cfg,store=server; url=cfg['API_BASE_URL']; headers={'Authorization':'Bearer test-secret'}
    p=payload()
    assert requests.get(url+'/health',timeout=2).status_code==401
    assert requests.get(url+'/health',headers=headers,timeout=2).json()['storage']=='memory-test-only'
    a=requests.post(url+'/executions',json=p,headers=headers,timeout=2)
    b=requests.post(url+'/executions',json=p,headers=headers,timeout=2)
    assert (a.status_code,b.status_code)==(201,200)
    assert b.json()['duplicate'] is True
    assert requests.get(url+'/executions/'+p['execution_id'],headers=headers,timeout=2).json()==p
    assert requests.post(url+'/executions',json=dict(p,discrepancias=5),headers=headers,timeout=2).status_code==409
    assert len(store.data)==1
    assert requests.get(url+'/executions/'+str(uuid4()),headers=headers,timeout=2).status_code==404
    assert requests.get(url+'/fault/500',headers=headers,timeout=2).status_code==500
    with pytest.raises(requests.Timeout): requests.get(url+'/fault/timeout',headers=headers,timeout=0.03)


def test_parallel_same_post(server):
    cfg,store=server; p=payload()
    def send(_):
        return requests.post(cfg['API_BASE_URL']+'/executions',json=p,headers={'Authorization':'Bearer test-secret'},timeout=2).status_code
    with ThreadPoolExecutor(max_workers=4) as pool: codes=list(pool.map(send,range(4)))
    assert sorted(codes)==[200,200,200,201] and len(store.data)==1


@pytest.mark.parametrize('field,value', [('movimientos_validos',True),('discrepancias',-1),('execution_id','broken'),('estado_proceso','OK')])
def test_invalid_contract(server,field,value):
    cfg,_=server; p=payload(); p[field]=value
    r=requests.post(cfg['API_BASE_URL']+'/executions',json=p,headers={'Authorization':'Bearer test-secret'},timeout=2)
    assert r.status_code==400


def test_client_evidence_and_sql_failure(server):
    cfg,_=server; a=Audit(cfg)
    result=call_http(cfg,a,'GET','/health')
    assert result['valid'] and (a.folder/'http').exists()
    p=payload(); result=call_http(cfg,a,'POST','/executions',p)
    assert result['valid']
    assert 'test-secret' not in ''.join(f.read_text() for f in (a.folder/'http').glob('*.json'))
    class BrokenStore:
        def health(self): raise ConnectionError('secret')
    app=create_app(cfg,BrokenStore())
    r=app.test_client().get('/health',headers={'Authorization':'Bearer test-secret'})
    assert r.status_code==503 and 'secret' not in r.text


@pytest.mark.parametrize('kind', ['non_json','timeout','connection','500','404'])
def test_client_failures(monkeypatch,tmp_path,kind):
    cfg=config_tmp(tmp_path); a=Audit(cfg)
    class Response:
        status_code=500 if kind=='500' else 404 if kind=='404' else 200
        text='SIMULADO: not JSON'
        def __enter__(self): return self
        def __exit__(self,*a): pass
        def json(self):
            if kind=='non_json': raise ValueError('not JSON')
            return {'error':'SIMULADO'}
    def req(*args,**kwargs):
        if kind=='timeout': raise requests.Timeout()
        if kind=='connection': raise requests.ConnectionError()
        return Response()
    monkeypatch.setattr(requests,'request',req)
    r=call_http(cfg,a,'GET','/health')
    assert not r['valid'] and a.events[-1]['status']=='ERROR'
    assert r['error']
