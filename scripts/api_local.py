"""API persistente de laboratorio; LAN solo con API_ROLE=server."""
from api.app import create_app
from api.local_store import SQLiteReceiptStore
from auxiliaries.config import load_config,ROOT
from scripts.network_services import service_target
if __name__=='__main__':
    cfg=load_config(require_secrets=False)
    role,host,port=service_target(cfg)
    if role=='client':raise SystemExit('Un cliente no debe iniciar otra API.')
    create_app(cfg,SQLiteReceiptStore(ROOT/'output/api_local/receipts.db')).run(host=host,port=port,debug=False,use_reloader=False)
