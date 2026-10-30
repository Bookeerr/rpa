"""Inicia la API propia o verifica el servidor compartido antes de abrir Studio."""
import subprocess,sys,time
import requests
from auxiliaries.config import ROOT,load_config
from scripts.network_services import service_target, sync_master
def main():
    cfg=load_config(require_secrets=False)
    if not cfg.get('API_TOKEN') or cfg['API_TOKEN']=='REEMPLAZAR':raise SystemExit('Completar .env local antes de ejecutar.')
    role,host,port=service_target(cfg)
    def ready():
        try:
            with requests.get(cfg['API_BASE_URL'].rstrip('/')+'/health',headers={'Authorization':'Bearer '+cfg['API_TOKEN']},timeout=2,allow_redirects=False) as r:
                return r.status_code==200 and r.json().get('storage')=='sqlite-local'
        except (requests.RequestException,ValueError):return False
    if role=='client':
        if not ready():raise SystemExit('Servidor no disponible: revisar IP, Wi-Fi, token y firewall. No se inicia una API alternativa.')
        sync_master(cfg)
        print('API compartida lista; maestro descargado y verificado.');return
    if ready():print('API lista: '+cfg['API_BASE_URL']);return
    logs=ROOT/'output/private';logs.mkdir(parents=True,exist_ok=True)
    with (logs/'api.stdout.log').open('ab') as out,(logs/'api.stderr.log').open('ab') as err:
        subprocess.Popen([sys.executable,'-m','scripts.api_local'],cwd=ROOT,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
    for _ in range(20):
        if ready():print('API iniciada: '+cfg['API_BASE_URL']);return
        time.sleep(.25)
    raise SystemExit('API no disponible. Revisar output/private/api.stderr.log e IP/puerto configurados.')
if __name__=='__main__':main()
