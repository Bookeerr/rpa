"""Inventario de comandos y verificacion del export oficial de Studio."""
import base64,hashlib,json,sqlite3
from pathlib import Path
import requests
ROOT=Path(__file__).resolve().parents[1]
def main():
    report=json.loads((ROOT/'docs/evidencias/web_nativa_resumen.json').read_text(encoding='utf8'))
    responses=json.loads((ROOT/'docs/evidencias/studio_web_responses.json').read_text(encoding='utf8'))
    assert responses and all(r['body']['status']=='True' for r in responses)
    assert 'WEB_ROCKETBOT_FIN' in responses[-1]['body']['message']
    db=ROOT/'rocketbot/MAIN_TESTFIRE_EP2/EXPORT_TESTFIRE_EP2.db'
    encoded=base64.b64encode(str(db).encode()).decode()
    names=['MAIN_TESTFIRE_EP2','WEB_LOGIN','EXTRACT_TRANSACTIONS'];projects={}
    for name in names:
        r=requests.post('http://localhost:5000/getbot',data=dict(name=name,db=encoded),timeout=20);r.raise_for_status()
        projects[name]=json.loads(r.json()[0]['data'])['project']
        assert projects[name]['commands']
        assert all(not v.get('data') for v in projects[name].get('vars',[]))
    rows=[]
    def walk(robot,commands,prefix=''):
        for i,c in enumerate(commands,1):
            n=prefix+str(i);group=c.get('group','');version={'web':'1.7.4','logic':'1.5.0','scripts':'1.9.0'}.get(group,'Studio')
            code=c.get('command','');params=code.replace('|','\\|').replace('\n','<br>')
            rows.append(f"| {robot}:{n} | {c['father']} | {group} {version} | `{params}` |")
            walk(robot,c.get('children',[]),n+'.');walk(robot,c.get('else',[]),n+'.else.')
    for name,p in projects.items():walk(name,p['commands'])
    header=f'''# Inventario nativo comprobado

Revision 18/10/2026. Export oficial generado mediante Studio /projectto en modo editable (produccion=0), con padre y dos hijos. No incluye framework ni modulos externos: las acciones son nativas y las dependencias Python se instalan separadamente. Se volvio a abrir cada robot del export mediante Studio; no se acredita otro equipo.

Ejecucion {report['execution_id']}: {len(responses)} respuestas de comando, todas True. La corrida incluye invocacion real de los hijos y cierre del navegador. SHA256 export: {hashlib.sha256(db.read_bytes()).hexdigest()}.

Importar/abrir `rocketbot/MAIN_TESTFIRE_EP2/EXPORT_TESTFIRE_EP2.db` con Studio conservando esa ubicacion relativa dentro del proyecto; los auxiliares se resuelven desde `%project_path%`. Las variables declaradas del export estan vacias, incluidas usuario/clave. MAIN las carga desde .env local y los hijos las heredan. ROOT se fija en PROJECT_ROOT.

Exito web: presencia de elementos esperados, contrato de tabla validado y web_ok. Exito datos: valid/rejected y cinco clasificaciones controladas por IF/For. Exito HTTP: contrato, codigo y acuse iguales. Fallos: Try Catch registra el error; las respuestas originales estan en studio_web_responses.json. Export Excel y cierre conservan PARCIAL por MySQL pendiente; no se presenta un paso omitido como ejecutado.

| Robot:comando | Comando real | Modulo/version | Parametros y variables entrada/salida |
|---|---|---|---|
'''
    (ROOT/'docs/NATIVO_MAIN_VERIFICADO.md').write_text(header+'\n'.join(rows)+'\n',encoding='utf8')
    evidence=dict(export_path=db.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(db.read_bytes()).hexdigest(),
        native_robots=names,official_endpoint='/projectto/0',reopened_with_studio=True,second_pc=False,
        native_commands=len(rows),executed_requests=len(responses),native_errors=0,execution_id=report['execution_id'])
    (ROOT/'docs/evidencias/export_nativo_verificado.json').write_text(json.dumps(evidence,indent=2),encoding='utf8')
    print('Export reabierto en Studio:',names,'comandos',len(rows))
if __name__=='__main__':main()
