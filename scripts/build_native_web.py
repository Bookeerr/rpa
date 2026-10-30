"""Construye MAIN mediante API de Studio y plantillas de formularios reales."""
import base64,json
from copy import deepcopy
from pathlib import Path
from uuid import uuid4
import requests
ROOT=Path(__file__).resolve().parents[1]
DB=base64.b64encode(str(ROOT/'rocketbot/MAIN_TESTFIRE_EP2/robot.db').encode()).decode()
URL='http://localhost:5000'
def main():
    r=requests.post(URL+'/getbot',data=dict(name='DEMO_LOCAL_EP2',db=DB),timeout=15);r.raise_for_status()
    p=json.loads(r.json()[0]['data'])['project']
    templates=json.loads((ROOT/'docs/evidencias/studio_command_templates.json').read_text())
    templates['execScriptPython']=p['commands'][0]
    def cmd(father,value='',**kw):
        c=deepcopy(templates[father])
        for k in ('line','execute','index','execute_debugg','img','message','screenshot'):c.pop(k,None)
        c.update(id=str(uuid4()),command=value,children=[],**kw);c['else']=[]
        return c
    def py(code):return cmd('execScriptPython',code)
    prefix="from auxiliaries import bridge\nfrom auxiliaries.studio_demo import variable\neid=GetVar('execution_id')\n"
    def op(code):return py(prefix+code)
    def web(father,data,**kw):return cmd(father,json.dumps(data),**kw)
    def send(selector,text):return web('sendkey_web',dict(data=selector,data_type='xpath',wait_time=30,text=text,special=''))
    def click(selector):return web('click_web',dict(data=selector,data_type='xpath',before='0',wait_time='30',after='1',move=False))
    def wait(selector):return web('waitforobject',dict(object=selector,wait_time=30,wait_for='present',before=0,after=0),option='xpath',getvar='objeto_listo')
    init=py("import sys\nfrom pathlib import Path\nroot=Path(r'%project_path%').resolve().parents[1]\nif str(root) not in sys.path:sys.path.insert(0,str(root))\nfrom auxiliaries.studio_web import initialize\nfrom auxiliaries import bridge\neid=initialize(root)\nSetVar('execution_id',eid)\nc=bridge.session(eid)['cfg']\nSetVar('url_login',c['TESTFIRE_URL'].rstrip('/')+'/login.jsp')\nSetVar('usuario',c['TESTFIRE_USER'])\nSetVar('clave',c['TESTFIRE_PASSWORD'])\nprint('WEB_ROCKETBOT_INICIO',eid)")
    flow=deepcopy(p['commands'][1])
    def adapt(c):
        c['id']=str(uuid4())
        value=c.get('command','')
        if isinstance(value,str):
            value=value.replace('filas_demo','filas_web').replace("'iso'","'testfire_minute'")
            value=value.replace("bridge.read_excel(eid,{'800003'})","__import__('auxiliaries.studio_web',fromlist=['read_reference']).read_reference(eid)")
            c['command']=value
        for ch in c.get('children',[])+c.get('else',[]):adapt(ch)
    adapt(flow)
    flow['children']=[op("SetVar('evento_web',bridge.begin(eid,'WEB_LOGIN_EXTRACT'))"),
        web('openbrowser',dict(url='{url_login}',id_driver='',profile=''),option='chrome'),
        wait("//input[@name='uid']"),send("//input[@name='uid']",'{usuario}'),send("//input[@name='passw']",'{clave}'),
        click("//input[@name='btnSubmit']"),wait("//a[@href='/bank/transaction.jsp']"),click("//a[@href='/bank/transaction.jsp']"),
        wait("//table[@id='_ctl0__ctl0_Content_Main_MyTransactions']"),
        web('gettable_extend',dict(identificator='//table[@id="_ctl0__ctl0_Content_Main_MyTransactions"]',option='xpath',encode=False,code='',result='tabla_web')),
        op("from auxiliaries.studio_web import rows\nSetVar('filas_web',rows(eid,GetVar('tabla_web')))\nbridge.end(eid,GetVar('evento_web'))")]+flow['children']
    recording=json.loads((ROOT/'recorder/dom_recording.json').read_text(encoding='utf8'))
    recorded=[]
    for e in recording['events']:
        if not e['trusted']:raise ValueError('Evento no confiable')
        recorded.append(send(e['selector'],'{'+e['variable']+'}') if e['action']=='input' else click(e['selector']))
    # Sustituye acciones manuales por el export del grabador. Las esperas son ajustes posteriores.
    flow['children'][4:9]=[recorded[1],recorded[2],wait("//a[@href='/bank/transaction.jsp']"),recorded[3],wait("//table[@id='_ctl0__ctl0_Content_Main_MyTransactions']")]
    flow['children'][3]=recorded[0]
    (ROOT/'recorder/native_recorded_commands.json').write_text(json.dumps(recorded,indent=2),encoding='utf8')
    init['command']=init['command'].replace('from auxiliaries.studio_web import initialize','import importlib\nimport auxiliaries.studio_web as web_adapter\nimportlib.reload(web_adapter)\nfrom auxiliaries.studio_web import initialize')
    flow['else']=[op("a=bridge.session(eid)['audit']\nfor event in list(a.active):a.end(event,'ERROR','Fallo de comando nativo; revisar evidencia Studio')\na.write_json('native_error.json',{'status':'ERROR'})")]
    init['command']+="\nSetVar('PROJECT_ROOT',str(root))"
    for name,commands in [('WEB_LOGIN',flow['children'][1:7]),('EXTRACT_TRANSACTIONS',flow['children'][7:10])]:
        child=deepcopy(p);child['commands']=commands;child['vars']=[];child['ifs']=[]
        child['profile'].update(name=name,description='Subrobot nativo invocado por MAIN_TESTFIRE_EP2; hereda variables.',deactivate_log=True)
        r=requests.post(URL+'/addbot',data=dict(name=name,code=json.dumps({'project':child}),description=child['profile']['description'],version='1.0.0',father='',db=DB),timeout=20);r.raise_for_status()
    flow['children'][1:10]=[cmd('execRocketBotDB','WEB_LOGIN'),cmd('execRocketBotDB','EXTRACT_TRANSACTIONS')]
    close=cmd('trycatch');close['children']=[cmd('killdriver')];close['else']=[op("bridge.session(eid)['audit'].write_json('browser_close.json',{'status':'ADVERTENCIA','detail':'Navegador no disponible para cierre'})")]
    p['commands']=[init,flow,close,op("from auxiliaries.studio_web import finalize\nSetVar('reporte_rel',finalize(eid))\ns=bridge.session(eid)\nprint('WEB_ROCKETBOT_FIN',eid,'web_excel_api_complete='+str(s['audit'].summary['web_excel_api_complete']),GetVar('reporte_rel'))")]
    p['profile'].update(name='MAIN_TESTFIRE_EP2',description='Web real TestFire + XPath + Excel externo + API local persistente. MySQL pendiente autorizado.',deactivate_log=True)
    p['vars']=[v for v in p['vars'] if v['name']!='filas_demo']
    for n in ('PROJECT_ROOT','filas_web','tabla_web','url_login','usuario','clave','objeto_listo','evento_web'):
        p['vars'].append(dict(name=n,data='',type='string',category='',disabled=False))
    p['ifs']=[]
    r=requests.post(URL+'/addbot',data=dict(name='MAIN_TESTFIRE_EP2',code=json.dumps({'project':p}),description=p['profile']['description'],version='1.0.0',father='',db=DB),timeout=20)
    r.raise_for_status();print('MAIN guardado mediante Studio',r.status_code)
if __name__=='__main__':main()
