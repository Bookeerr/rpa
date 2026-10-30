"""Guarda mediante Studio, partiendo del proyecto real y sus formularios.

No escribe SQLite ni genera un .db fuera de Rocketbot. Requiere Studio local.
"""
import base64
from copy import deepcopy
import json
from pathlib import Path
from uuid import uuid4
import requests

ROOT = Path(__file__).resolve().parents[1]
DB = base64.b64encode(str(ROOT/'rocketbot/MAIN_TESTFIRE_EP2/robot.db').encode()).decode()
URL = 'http://localhost:5000'


def main():
    original = requests.post(URL+'/getbot', data={'name':'DEMO_LOCAL_EP2','db':DB},timeout=15).json()
    project = json.loads(original[0]['data'])['project']
    templates = json.loads((ROOT/'docs/evidencias/studio_command_templates.json').read_text())
    templates['execScriptPython'] = project['commands'][0]
    def command(father, value='', children=None, otherwise=None, **kwargs):
        c = deepcopy(templates[father])
        for k in ('line','execute','index','execute_debugg','img','message','screenshot'):c.pop(k,None)
        c.update(id=str(uuid4()),command=value,children=children or [],**kwargs)
        c['else']=otherwise or []
        return c
    def py(code):return command('execScriptPython',code)
    prefix="from auxiliaries import bridge\nfrom auxiliaries.studio_demo import variable\neid=GetVar('execution_id')\n"
    def op(code):return py(prefix+code)
    def classify(status):return op("bridge.append_result(eid,variable(GetVar('par')),"+repr(status)+")")
    classify_tree=command('evaluateIf','{es_ambiguo}',children=[classify('AMBIGUO')],otherwise=[
        command('evaluateIf','{sin_web}',children=[classify('SOLO_MASTER')],otherwise=[
            command('evaluateIf','{sin_master}',children=[classify('SOLO_WEB')],otherwise=[
                command('evaluateIf','{con_diferencias}',children=[classify('DISCREPANCIA')],otherwise=[classify('CONCILIADO')])])])])
    operations=[
        op("SetVar('evento',bridge.begin(eid,'VALIDATE_DATA'))"),
        command('for',json.dumps({'iterable':'{filas_demo}','count':0}),var='fila',children=[
            op("r=bridge.validate(eid,variable(GetVar('fila')),'iso')\nSetVar('validacion',r)\nSetVar('es_valido',r['valid'])"),
            command('evaluateIf','{es_valido}',children=[op("bridge.append_valid(eid,variable(GetVar('validacion'))['row'])")],
                    otherwise=[op("bridge.append_rejected(eid,variable(GetVar('validacion')))")])]),
        op("bridge.end(eid,GetVar('evento'))\nSetVar('evento',bridge.begin(eid,'READ_REFERENCES'))\nbridge.read_excel(eid,{'800003'})\nbridge.end(eid,GetVar('evento'))\nSetVar('pares',bridge.pairs(eid))\nSetVar('evento',bridge.begin(eid,'RECONCILE'))"),
        command('for',json.dumps({'iterable':'{pares}','count':0}),var='par',children=[
            op("p=variable(GetVar('par'))\nSetVar('es_ambiguo',p['ambiguous'])\nSetVar('sin_web',p['web'] is None)\nSetVar('sin_master',p['master'] is None)\nSetVar('con_diferencias',bool(p['differences']))"),classify_tree]),
        op("bridge.end(eid,GetVar('evento'))\nSetVar('respuesta',bridge.http(eid,'GET','/health'))\nSetVar('http_valid',variable(GetVar('respuesta'))['valid'])"),
        command('evaluateIf','{http_valid}',children=[
            op("SetVar('payload',bridge.api_payload(eid))\nSetVar('intento',1)\nSetVar('http_valid',False)"),
            command('evaluatewhile','{intento} <= 3 and not {http_valid}',children=[
                op("r=bridge.http(eid,'POST','/executions',variable(GetVar('payload')),int(GetVar('intento')))\nSetVar('http_valid',r['valid'])\nSetVar('retryable',r['retryable'])"),
                command('evaluateIf','{retryable}',children=[op("SetVar('intento',int(GetVar('intento'))+1)")],otherwise=[op("SetVar('intento',4)")])]),
            command('evaluateIf','{http_valid}',children=[
                op("r=bridge.http(eid,'POST','/executions',variable(GetVar('payload')),2)\nassert r['valid'] and r['http_status']==200\nr=bridge.http(eid,'GET','/executions/'+eid)\nSetVar('acuse_ok',r['valid'] and r['body']==variable(GetVar('payload')))"),
                command('evaluateIf','{acuse_ok}',children=[op("bridge.session(eid)['http_ok']=True")],otherwise=[op("print('ACUSE DIFERENTE: PARCIAL')")])
            ],otherwise=[op("print('POST no confirmado: PARCIAL')")])
        ],otherwise=[op("print('API demo no disponible: PARCIAL')")]),
        op("SetVar('evento',bridge.begin(eid,'EXPORT_EXCEL'))\nSetVar('reporte_rel',bridge.export_excel(eid,'PARCIAL'))\nbridge.end(eid,GetVar('evento'))\nbridge.queue_bundle(eid)")]
    project['commands']=[
        py("import sys,json\nfrom pathlib import Path\nroot=Path(r'%project_path%').resolve().parents[1]\nassert (root/'auxiliaries').is_dir(), 'Raiz del proyecto incorrecta'\nif str(root) not in sys.path: sys.path.insert(0,str(root))\nfrom auxiliaries.studio_demo import initialize\nSetVar('execution_id',initialize(root))\nSetVar('filas_demo',json.loads((root/'data/filas_demo.json').read_text(encoding='utf-8')))\nprint('DEMO_ROCKETBOT_INICIO',GetVar('execution_id'))"),
        command('trycatch',children=operations,otherwise=[op("a=bridge.session(eid)['audit']\nfor event in list(a.active): a.end(event,'ERROR','Fallo en demo nativa; ver respuesta original de Studio')\na.write_json('native_error.json',{'status':'ERROR','detail':'Ver respuestas de Studio'})")]),
        op("from auxiliaries.studio_demo import finalize\nSetVar('reporte_rel',finalize(eid))\ns=bridge.session(eid)\nassert len(s['valid'])==3 and len(s['rejected'])==1 and len(s['results'])==4\nprint('DEMO_ROCKETBOT_FIN',eid,GetVar('reporte_rel'),s['audit'].summary['status'])")]
    project['profile'].update(name='DEMO_LOCAL_EP2',description='Prueba sintetica local de controles. No acredita flujo web, SQL ni recorder.')
    project['vars']=[dict(name=n,data='',type='string',category='',disabled=False) for n in (
        'execution_id','filas_demo','fila','validacion','es_valido','evento','pares','par','es_ambiguo',
        'sin_web','sin_master','con_diferencias','respuesta','http_valid','payload','intento','retryable','acuse_ok','reporte_rel')]
    project['ifs']=[]
    response=requests.post(URL+'/addbot',data=dict(name='DEMO_LOCAL_EP2',code=json.dumps({'project':project}),description=project['profile']['description'],version='0.1.0',father='',db=DB),timeout=15)
    response.raise_for_status()
    print('Studio guardo DEMO_LOCAL_EP2; HTTP',response.status_code)


if __name__=='__main__':main()
