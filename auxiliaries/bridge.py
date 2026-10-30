"""Fachada de operaciones puntuales para comandos Ejecutar Python de Studio.

El modulo conserva el reloj Audit en memoria. El robot contiene For, IF,
Try Catch, navegacion, seleccion y politica de reintentos.
"""
from datetime import datetime
from pathlib import Path
from uuid import uuid4
from auxiliaries.timezones import ZoneInfo
import time
from auxiliaries.config import load_config
from auxiliaries.audit import Audit
from auxiliaries.database import Repository
from auxiliaries.excel import read_master, write_report
from auxiliaries.http_client import call_http
from auxiliaries.validation import validate_row
from auxiliaries.reconciliation import plan_pairs

_sessions = {}


def initialize(project_root):
    cfg = load_config(project_root)
    audit = Audit(cfg)
    _sessions[audit.id] = dict(cfg=cfg,audit=audit,repo=Repository(cfg),valid=[],rejected=[],results=[],api_calls=[],
                              rules={},master=None,report=None,sql_ok=False,http_ok=False,web_ok=False)
    return dict(execution_id=audit.id,config=cfg)


def session(execution_id):
    if execution_id not in _sessions:
        raise RuntimeError("Sesion auxiliar perdida. Marcar ejecucion INTERRUMPIDO y reiniciar MAIN")
    return _sessions[execution_id]


def begin(execution_id, step_id, attempt=1):
    return session(execution_id)['audit'].start(step_id,attempt)


def end(execution_id,event_id,status='OK',detail='',evidence=None):
    return session(execution_id)['audit'].end(event_id,status,detail,evidence)


def read_rules(execution_id):
    s=session(execution_id)
    s['rules']=s['repo'].rules()
    s['audit'].write_json('account_rules.json',s['rules'])
    return s['rules']


def read_excel(execution_id,selected_accounts):
    s=session(execution_id); c=s['cfg']
    s['master']=read_master(c['master_path'],execution_id,selected_accounts,c['PERIOD_START'],c['PERIOD_END'],
                            c.get('ALLOW_SYNTHETIC_MASTER','false').lower()=='true')
    s['audit'].write_json('master_metadata.json',s['master']['metadata'])
    return s['master']


def validate(execution_id,raw,date_format='testfire'):
    s=session(execution_id)
    result=validate_row(raw,execution_id,date_format)
    if result['valid']:
        r=result['row']
        if not s['cfg']['PERIOD_START']<=r['date']<=s['cfg']['PERIOD_END']:
            return dict(valid=False,row=raw,error='Fecha fuera del periodo solicitado')
    return result


def append_valid(execution_id,row):
    session(execution_id)['valid'].append(row)


def append_rejected(execution_id,result):
    session(execution_id)['rejected'].append(result)


def pairs(execution_id):
    s=session(execution_id)
    if s['master'] is None: raise ValueError('Maestro no leido')
    return plan_pairs(s['valid'],s['master']['rows'],s['rules'])


def append_result(execution_id,pair,status):
    if status not in ('CONCILIADO','SOLO_WEB','SOLO_MASTER','DISCREPANCIA','AMBIGUO'):
        raise ValueError('Clasificacion invalida')
    session(execution_id)['results'].append(dict(pair,status=status))


def queue_bundle(execution_id):
    s=session(execution_id)
    name='outbox/'+str(uuid4())+'.json'
    return s['audit'].write_json(name,dict(kind='bundle',data=dict(execution_id=execution_id,
        movements=s['valid'],results=s['results'],api_calls=s['api_calls'],artifacts=[])))


def sync(execution_id):
    s=session(execution_id)
    s['sql_ok']=False
    count=s['repo'].replay(s['audit'].folder)
    s['sql_ok']=True
    return count


def http(execution_id,method,path,payload=None,attempt=1):
    s=session(execution_id)
    result=call_http(s['cfg'],s['audit'],method,path,payload,attempt)
    s['api_calls'].append(result)
    return result


def api_payload(execution_id):
    s=session(execution_id)
    return dict(execution_id=execution_id,equipo=s['audit'].summary['hostname'],
        estado_proceso='CONCILIACION_COMPLETADA',movimientos_validos=len(s['valid']),
        movimientos_rechazados=len(s['rejected']),
        discrepancias=sum(r['status']!='CONCILIADO' for r in s['results']),
        duracion_hasta_envio_ms=int((time.perf_counter_ns()-s['audit'].started_ns)/1e6))


def export_excel(execution_id,status='PARCIAL'):
    s=session(execution_id); a=s['audit']
    if s['report'] is None:
        stamp=datetime.now(ZoneInfo(s['cfg']['DISPLAY_TIMEZONE'])).strftime('%Y%m%d_%H%M%S')
        s['report']=a.folder/f'Reporte_TestFire_{stamp}_{execution_id}.xlsx'
    write_report(s['report'],s['valid'],s['results'],s['rejected'],a.events,dict(a.summary,status=status))
    return s['report'].relative_to(Path(s['cfg']['PROJECT_ROOT'])).as_posix()


def finalize(execution_id,status):
    s=session(execution_id); a=s['audit']
    if status=='OK' and not (s['sql_ok'] and s['http_ok'] and s['web_ok'] and s['report']):
        raise ValueError('Integraciones obligatorias incompletas')
    a.finish(status,valid_rows=len(s['valid']),rejected_rows=len(s['rejected']))
    if s['report']:
        try:
            export_excel(execution_id,status)
            a.write_json('artifacts.json',[a.artifact(s['report'],'EXCEL')])
        except Exception:
            a.summary['status']='ERROR'
            a.summary['report_projection']='FAILED'
            a.save_summary()
            raise
    try:
        s['repo'].replay(a.folder)
    except Exception:
        a.summary['status']='PARCIAL' if status!='ERROR' else 'ERROR'
        a.summary['sql_final_pending']=True
        a.save_summary()
        if s['report']:
            export_excel(execution_id,a.summary['status'])
            a.write_json('artifacts.json',[a.artifact(s['report'],'EXCEL')])
    return a.summary
