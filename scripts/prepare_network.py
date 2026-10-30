"""Configura este host y crea una copia PRIVADA para el cliente, sin MySQL."""
import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
import shutil
import zipfile
from dotenv import dotenv_values, set_key
from auxiliaries.config import ROOT, load_config
from scripts.network_services import lan_ip


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', required=True, type=lan_ip)
    args = parser.parse_args()
    cfg = load_config(require_secrets=False)
    for key in ('API_TOKEN', 'TESTFIRE_USER', 'TESTFIRE_PASSWORD'):
        if not cfg.get(key) or cfg[key] == 'REEMPLAZAR':
            raise SystemExit('Completar ' + key + ' en .env local.')
    master = Path(cfg['master_path'])
    if not master.is_file():
        raise SystemExit('Falta el maestro configurado.')
    private = ROOT / 'output/private'
    private.mkdir(parents=True, exist_ok=True)
    backup = private / ('env_antes_red_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '.bak')
    shutil.copy2(ROOT / '.env', backup)
    url = f'http://{args.host}:18081'
    for key, value in dict(API_ROLE='server', API_BASE_URL=url, API_BIND_HOST=args.host, API_PORT='18081').items():
        set_key(str(ROOT / '.env'), key, value, quote_mode='always')
    # Lista explicita: nunca copiar claves de MySQL ni el resto del .env del host.
    client = dict(dotenv_values(ROOT / '.env.example'))
    for key in ('API_TOKEN', 'TESTFIRE_URL', 'TESTFIRE_USER', 'TESTFIRE_PASSWORD', 'PERIOD_START',
                'PERIOD_END', 'ALLOW_SYNTHETIC_MASTER', 'DISPLAY_TIMEZONE', 'ROBOT_VERSION'):
        client[key] = str(cfg[key])
    client.update(API_ROLE='client', API_BASE_URL=url, API_BIND_HOST='127.0.0.1', API_PORT='18081',
                  MASTER_EXCEL_PATH='data/master_snapshot_testfire.xlsx', DB_PASSWORD='REEMPLAZAR')
    client_env = private / 'cliente.env'
    client_env.write_text('', encoding='utf-8')
    for key, value in client.items():
        set_key(str(client_env), key, str(value), quote_mode='always')
    archive = private / 'TestFire_CLIENTE_PRIVADO.zip'
    roots = ('.env.example', 'INICIAR_EP2.bat', 'PREPARAR_OTRA_PC.bat', 'requirements-ep2.txt',
             'requirements-dev-ep2.txt', 'ejecutar_ep2.bat', 'README.md', 'GUIA_COMPLETA_PROYECTO.md')
    files = [ROOT / name for name in roots]
    for folder in ('auxiliaries', 'api', 'scripts', 'config', 'data', 'rocketbot', 'docs', 'tests'):
        files.extend(p for p in (ROOT / folder).rglob('*') if p.is_file()
                     and not any(part in ('private', '__pycache__', 'logs', 'fuentes_extraidas') for part in p.relative_to(ROOT).parts)
                     and p.suffix not in ('.pyc', '.log', '.tmp') and not p.name.startswith('.env'))
    files.extend(ROOT / 'docs' / name for name in ('CONFIGURACION_SEGUNDA_PC.md', 'INSTALACION_HOST_WINDOWS.md'))
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(set(files)):
            # Siempre se usa la referencia elegida por el host.
            rel = p.relative_to(ROOT).as_posix()
            if rel != 'data/master_snapshot_testfire.xlsx':
                z.write(p, 'TestFire_CLIENTE/' + rel)
        z.write(master, 'TestFire_CLIENTE/data/master_snapshot_testfire.xlsx')
        z.write(client_env, 'TestFire_CLIENTE/.env')
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
    firewall_file = private / 'firewall_red.json'
    firewall = json.loads(firewall_file.read_text(encoding='utf-8-sig')) if firewall_file.exists() else {}
    receipt = dict(server=url, role='server', archive=str(archive.relative_to(ROOT)),
                   private_contains_api_token=True, sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
                   firewall_configured=firewall.get('ip') == args.host and firewall.get('port') == 18081,
                   second_pc_verified=False, mysql='PENDIENTE')
    (private / 'preparacion_red.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
