"""Documenta el proyecto real leyendo SQLite en modo solo lectura."""
from collections import Counter
import base64
import hashlib
import json
from pathlib import Path
import sqlite3

ROOT=Path(__file__).resolve().parents[1]
EXECUTION='e967c39e-3b8a-4df1-9d11-87dfcff8ac97'


def main():
    db=ROOT/'rocketbot/MAIN_TESTFIRE_EP2/robot.db'
    with sqlite3.connect(db.as_uri()+'?mode=ro',uri=True) as conn:
        data=conn.execute('SELECT data FROM bots WHERE name=? ORDER BY id DESC LIMIT 1',('DEMO_LOCAL_EP2',)).fetchone()[0]
    project=json.loads(base64.b64decode(data))['project']
    responses=json.loads((ROOT/'docs/evidencias/studio_demo_responses.json').read_text())
    assert responses and all(r['body']['status']=='True' for r in responses)
    assert 'DEMO_ROCKETBOT_FIN' in responses[-1]['body']['message']
    folder=ROOT/'output'/EXECUTION
    summary=json.loads((folder/'execution.json').read_text())
    calls=json.loads((folder/'api_calls.json').read_text())
    assert summary['http_ok'] and summary['valid_rows']==3 and summary['rejected_rows']==1
    assert [c['http_status'] for c in calls]==[200,201,200,200]
    entries=[]
    def walk(commands,prefix=''):
        for n,c in enumerate(commands,1):
            number=prefix+str(n)
            entries.append((number,c))
            walk(c.get('children',[]),number+'.')
            walk(c.get('else',[]),number+'.else.')
    walk(project['commands'])
    evidence=dict(execution_id=EXECUTION,mode=summary['mode'],status=summary['status'],
        started_at=summary['started_at'],ended_at=summary['ended_at'],duration_ms=summary['duration_ms'],
        native_commands=len(entries),executed_requests=len(responses),native_errors=0,
        http_statuses=[c['http_status'] for c in calls],classifications=summary['classifications'],
        database='rocketbot/MAIN_TESTFIRE_EP2/robot.db',database_sha256=hashlib.sha256(db.read_bytes()).hexdigest())
    (ROOT/'docs/evidencias/demo_nativa_resumen.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
    titles={'execScriptPython':'Execute Python / scripts 1.9.0','for':'For / logic 1.5.0',
            'evaluateIf':'IF / logic 1.5.0','trycatch':'Try Catch / logic 1.5.0','evaluatewhile':'While / logic 1.5.0'}
    lines=['# Demo nativa verificada: DEMO_LOCAL_EP2','',
        'Ejecucion del 2026-10-16; documentacion consolidada el 2026-10-17. **SINTETICA y PARCIAL**: no navega TestFire, no usa MySQL y no acredita recorder. Se guardo por Studio usando un proyecto real y plantillas de sus formularios; no se fabrico el formato SQLite.','',
        f'UUID `{EXECUTION}`. Intervalo medido por Audit: **{summary["duration_ms"]/1000:.3f} s** (una muestra, desde crear Audit hasta cerrar la ejecucion; no incluye arranque Studio ni reescritura final del Excel). No es una medicion de ahorro ni del proceso web completo.','',
        f'{len(entries)} comandos declarados; {len(responses)} solicitudes de ejecucion registradas por el editor, todas con status True. Las condiciones False normales no son fallos del comando. El For visita 4 filas; IF conserva 3 validas y 1 rechazo. Otro For clasifica 4 pares: CONCILIADO, DISCREPANCIA, SOLO_MASTER y SOLO_WEB. AMBIGUO tiene rama nativa y pruebas unitarias; esta muestra no recorre esa rama.','',
        'HTTP real desde comandos del robot hacia un proceso Flask separado: GET /health 200, POST /executions 201, POST identico 200 y GET /executions/UUID 200. El acuse coincide con el payload. API con memoria efimera, loopback 127.0.0.1:18080; no atribuir persistencia MySQL. While admite hasta tres intentos solo ante fallos transitorios; en esta ejecucion el primer POST fue suficiente.','',
        'Evidencia: `docs/evidencias/studio_demo.png`, `studio_demo_responses.json`, `demo_nativa_resumen.json`, y `output/'+EXECUTION+'/`. Excel de cinco hojas, execution.json, audit.jsonl, results.json, valid_rows.json, rejected_rows.json y HTTP redactado. El directorio output se conserva localmente; el paquete incluye esta ejecucion seleccionada.','',
        'Repetir: `ejecutar_ep2.bat -Action api-demo`; luego abrir `rocketbot/MAIN_TESTFIRE_EP2/MAIN_TESTFIRE_EP2.bat`, seleccionar DEMO_LOCAL_EP2 y pulsar Run. Mantener el editor abierto hasta finalizar. Ctrl+C detiene la API. Studio resuelve la raiz desde `%project_path%`; nunca guardar una ruta personal en comandos.','',
        'MAIN_TESTFIRE_EP2 aun es el humo de runtime. El flujo web real y sus subrobots estan especificados en MONTAJE_ROCKETBOT.md y BLOQUES_STUDIO.md, pendientes de montaje completo, DOM y credenciales.','',
        '## Comandos reales guardados','',
        'Robot: DEMO_LOCAL_EP2. Entradas/salidas son las variables declaradas en cada SetVar/GetVar del codigo y los parametros siguientes. Para Python, el texto exacto se conserva en el proyecto editable y el generador scripts/build_native_demo.py. EXITO: respuesta de comando status True y aserciones finales. ERROR: Try Catch salta a la rama de manejo; API invalida queda en auditoria y el cierre sigue PARCIAL. El cierre integral de recursos web no aplica a esta demo.','',
        '| Nativo | Comando / version | Parametros o operacion |','|---|---|---|']
    for number,c in entries:
        value=c['command'].replace('\n','; ')
        if c['father']=='execScriptPython':
            value=value.replace('from auxiliaries import bridge; from auxiliaries.studio_demo import variable; eid=GetVar(\'execution_id\'); ','')
        if len(value)>280:value=value[:277]+'...'
        value=value.replace('|','/')
        if c.get('var'):value+=' -> '+c['var']
        lines.append(f'| {number} | {titles.get(c["father"],c["father"])} | `{value}` |')
    lines+=['','## Incidencias reales','',
        'El primer ensayo de controles fallo porque SetVar no crea variables no declaradas; se corrigio declarandolas en el padre. El primer montaje de auxiliares fallo por ausencia de zoneinfo en el runtime congelado; se agrego adaptador pytz. Un ensayo se interrumpio al cerrar demasiado pronto el navegador de inspeccion: UUID 1184a952-f209-40ec-bf36-1348cc58d539, marcado INTERRUMPIDO con fecha de deteccion, sin inventar duracion final. La ejecucion aprobada anterior termino despues de corregir la espera. No se presentan esos intentos como exitosos.']
    (ROOT/'docs/DEMO_NATIVA_ROCKETBOT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(evidence,indent=2))


if __name__=='__main__':main()
