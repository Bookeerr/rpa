"""Adaptadores SOLO para DEMO_LOCAL_EP2. Sin navegador ni conexion MySQL."""
import ast
import hashlib
import json
from pathlib import Path
from auxiliaries import bridge
from auxiliaries.audit import Audit
from auxiliaries.config import load_config
from auxiliaries.reconciliation import counts

DEMO_TOKEN = 'SINTETICO-SOLO-LOOPBACK'


def variable(value):
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except ValueError:
        return ast.literal_eval(value)


def initialize(root):
    cfg=load_config(root,require_secrets=False)
    cfg.update(PERIOD_START='2026-10-01',PERIOD_END='2026-10-31',ALLOW_SYNTHETIC_MASTER='true',
               master_path=str(Path(root)/'data/conciliacion_master.xlsx'),
               API_BASE_URL='http://127.0.0.1:18080',API_TOKEN=DEMO_TOKEN)
    from auxiliaries.config import public_config
    public=public_config(cfg)
    public.pop('config_hash',None)
    cfg['config_hash']=hashlib.sha256(json.dumps(public,sort_keys=True).encode()).hexdigest()
    audit=Audit(cfg,mode='ROCKETBOT_SINTETICO')
    bridge._sessions[audit.id]=dict(cfg=cfg,audit=audit,repo=None,valid=[],rejected=[],results=[],api_calls=[],
        rules={'800003':dict(enabled=True,tolerance='0.00',version='SINTETICO-NO-SQL')},
        master=None,report=None,sql_ok=False,http_ok=False,web_ok=False)
    return audit.id


def finalize(execution_id):
    s=bridge.session(execution_id);a=s['audit']
    a.write_json('results.json',s['results'])
    a.write_json('valid_rows.json',s['valid'])
    a.write_json('rejected_rows.json',s['rejected'])
    a.write_json('api_calls.json',s['api_calls'])
    a.finish('PARCIAL',valid_rows=len(s['valid']),rejected_rows=len(s['rejected']),
        classifications=counts(s['results']),http_ok=s['http_ok'],
        pending=['WEB_REAL','RECORDER','MYSQL','FLUJO_REAL_COMPLETO','SEGUNDA_PC'])
    report=bridge.export_excel(execution_id,'PARCIAL')
    a.write_json('artifacts.json',[a.artifact(s['report'],'EXCEL')])
    return report
