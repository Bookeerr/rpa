"""Operaciones puntuales del MAIN web. Navegacion y decisiones en Studio."""
import hashlib
import json
from auxiliaries import bridge
from auxiliaries.audit import Audit
from auxiliaries.config import load_config
from auxiliaries.reconciliation import counts
from auxiliaries.studio_demo import variable

HEADERS=['Transaction ID','Transaction Time','Account ID','Action','Amount']

def initialize(root):
    cfg=load_config(root,require_secrets=False)
    for key in ('TESTFIRE_USER','TESTFIRE_PASSWORD','API_TOKEN'):
        if not cfg.get(key) or cfg[key]=='REEMPLAZAR':raise ValueError('Configurar '+key+' localmente')
    mode='ROCKETBOT_WEB_EXCEL_API_LAN' if cfg.get('API_ROLE') in ('server','client') else 'ROCKETBOT_WEB_EXCEL_API_LOCAL'
    a=Audit(cfg,mode=mode)
    bridge._sessions[a.id]=dict(cfg=cfg,audit=a,repo=None,valid=[],rejected=[],results=[],api_calls=[],
        rules={},master=None,report=None,sql_ok=False,http_ok=False,web_ok=False)
    return a.id

def rows(execution_id, table):
    s=bridge.session(execution_id)
    table=variable(table)
    s['audit'].write_json('dom_table.json',table)
    if not isinstance(table,list) or not table:raise ValueError('Tabla vacia o formato inesperado')
    if [str(c).strip() for c in table[0]]!=HEADERS:raise ValueError('Cabeceras DOM distintas del contrato')
    result=[]
    for i,cells in enumerate(table[1:],1):
        if not cells or all(not str(c).strip() for c in cells):continue
        if len(cells)!=5:raise ValueError('Cambio de estructura DOM')
        ident,dt,account,desc,amount=[str(c).strip() for c in cells]
        result.append(dict(web_id=ident,date_raw=dt,account=account,description=desc,amount_raw=amount,
            row_index=i,currency=None,source_url=s['cfg']['TESTFIRE_URL'].rstrip('/')+'/bank/transaction.jsp'))
    if not result:raise ValueError('Sin movimientos; no acreditar extraccion')
    s['web_ok']=True
    s['audit'].write_json('web_rows_raw.json',result)
    return result

def read_reference(execution_id):
    s=bridge.session(execution_id)
    from openpyxl import load_workbook
    w=load_workbook(s['cfg']['master_path'],read_only=True)
    try: accounts={str(r[0]) for r in list(w['Master'].values)[1:] if r[0] is not None}
    finally:w.close()
    accounts.update(r['account'] for r in s['valid'])
    # La pauta admite Excel O SQL. Sin simular reglas consultadas a MySQL.
    s['rules']={a:dict(enabled=True,tolerance='0.00',version='EXCEL-SNAPSHOT') for a in accounts}
    return bridge.read_excel(execution_id,accounts)

def finalize(execution_id):
    s=bridge.session(execution_id);a=s['audit']
    complete=bool(s['web_ok'] and s['http_ok'] and s['master'] is not None and s['report']
                  and not (a.folder/'native_error.json').exists())
    for name in ('results','valid','rejected','api_calls'):a.write_json(name+'.json',s[name])
    a.finish('PARCIAL' if complete else 'ERROR',web_excel_api_complete=complete,
        valid_rows=len(s['valid']),rejected_rows=len(s['rejected']),classifications=counts(s['results']),
        http_ok=s['http_ok'],pending=['MYSQL_POR_INDICACION_USUARIO','SEGUNDA_PC'],
        reference='Snapshot externo previo; no representa contabilidad independiente')
    try:
        report=bridge.export_excel(execution_id,a.summary['status'])
        a.write_json('artifacts.json',[a.artifact(s['report'],'EXCEL')])
    except Exception:
        a.summary.update(status='ERROR',web_excel_api_complete=False,report_projection='FAILED')
        a.save_summary()
        raise
    return report
