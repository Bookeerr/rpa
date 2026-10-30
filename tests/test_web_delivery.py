from uuid import uuid4
import pytest
from auxiliaries.validation import parse_date
from api.local_store import SQLiteReceiptStore
from api.app import create_app

def test_live_date_contract():
    assert parse_date('2026-10-18 06:24','testfire_minute')=='2026-10-18'
    with pytest.raises(ValueError):parse_date('2026-02-30 06:24','testfire_minute')

def test_receipts_survive_restart_and_reject_changed_payload(tmp_path):
    path=tmp_path/'receipts.db';eid=str(uuid4())
    payload=dict(execution_id=eid,equipo='PC-EP2',estado_proceso='CONCILIACION_COMPLETADA',movimientos_validos=100,
        movimientos_rechazados=0,discrepancias=0,duracion_hasta_envio_ms=10)
    def client():return create_app({'API_TOKEN':'local-test'},SQLiteReceiptStore(path)).test_client()
    headers={'Authorization':'Bearer local-test'}
    assert client().post('/executions',json=payload,headers=headers).status_code==201
    assert client().get('/executions/'+eid,headers=headers).json==payload
    assert client().post('/executions',json=payload,headers=headers).status_code==200
    assert client().post('/executions',json=dict(payload,discrepancias=1),headers=headers).status_code==409
    assert client().get('/health',headers=headers).json['storage']=='sqlite-local'

def test_dom_contract_and_empty_layout_rows(tmp_path,monkeypatch):
    from auxiliaries import studio_web,bridge
    class Audit:
        def write_json(self,*args):pass
    eid=str(uuid4());monkeypatch.setitem(bridge._sessions,eid,dict(audit=Audit(),cfg={'TESTFIRE_URL':'http://demo.testfire.net'},web_ok=False))
    rows=studio_web.rows(eid,[studio_web.HEADERS,['1','2026-10-18 06:24','800030','Deposit','$1.00'],[]])
    assert len(rows)==1 and rows[0]['date_raw']=='2026-10-18 06:24'
    with pytest.raises(ValueError):studio_web.rows(eid,[['Changed header']])

def test_sqlite_closes_connections_including_duplicate_and_error(tmp_path,monkeypatch):
    import sqlite3
    from api import local_store
    original=sqlite3.connect;opened=[]
    class Tracked(sqlite3.Connection):
        closed=False
        def close(self):self.closed=True;super().close()
    def connect(*args,**kwargs):
        c=original(*args,**kwargs,factory=Tracked);opened.append(c);return c
    monkeypatch.setattr(local_store.sqlite3,'connect',connect)
    store=SQLiteReceiptStore(tmp_path/'receipts.db')
    store.health();store.put({'execution_id':'test'});store.get('test');store.put({'execution_id':'test'})
    with pytest.raises(KeyError):store.put({})
    assert opened and all(c.closed for c in opened)

@pytest.mark.parametrize('failure',['final_report','native_error'])
def test_web_close_does_not_claim_completion_after_failure(tmp_path,monkeypatch,failure):
    import json
    from auxiliaries import bridge,studio_web
    from tests.test_core import config_tmp
    monkeypatch.setattr(studio_web,'load_config',lambda *a,**kw:config_tmp(tmp_path))
    eid=studio_web.initialize(tmp_path);s=bridge.session(eid)
    try:
        bridge.export_excel(eid);s.update(web_ok=True,http_ok=True,master={'rows':[]})
        if failure=='final_report':
            def fail(*a,**kw):raise PermissionError('Excel abierto SIMULADO')
            monkeypatch.setattr(bridge,'export_excel',fail)
            with pytest.raises(PermissionError):studio_web.finalize(eid)
        else:
            s['audit'].write_json('native_error.json',{'status':'ERROR'})
            studio_web.finalize(eid)
        result=json.loads((s['audit'].folder/'execution.json').read_text())
        assert result['status']=='ERROR' and result['web_excel_api_complete'] is False
    finally:bridge._sessions.pop(eid)
