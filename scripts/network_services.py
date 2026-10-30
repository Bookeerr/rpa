"""Contrato de red y descarga atomica del maestro compartido."""
import hashlib
import ipaddress
import json
import tempfile
from pathlib import Path
from urllib.parse import urlsplit
import requests
from openpyxl import load_workbook
from auxiliaries.excel import COLUMNS


def lan_ip(value):
    address = ipaddress.IPv4Address(value)
    networks = ('10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16')
    if not any(address in ipaddress.ip_network(n) for n in networks):
        raise ValueError('Usar una IPv4 privada de la red local.')
    return str(address)


def service_target(cfg):
    role = cfg.get('API_ROLE', 'local')
    url = urlsplit(cfg['API_BASE_URL'])
    if role == 'local':
        if cfg['API_BASE_URL'] != 'http://127.0.0.1:18081':
            raise ValueError('API_ROLE=local requiere http://127.0.0.1:18081')
        return role, '127.0.0.1', 18081
    if role not in ('server', 'client'):
        raise ValueError('API_ROLE debe ser local, server o client.')
    host = lan_ip(url.hostname)
    port = url.port or 80
    if url.scheme != 'http' or url.username or url.password or url.query or url.fragment or url.path not in ('', '/'):
        raise ValueError('La API de laboratorio requiere http://IPv4_privada:puerto')
    if role == 'server' and (cfg['API_BIND_HOST'] != host or cfg['API_PORT'] != port):
        raise ValueError('API_BASE_URL, API_BIND_HOST y API_PORT deben coincidir en el servidor.')
    return role, host, port


def sync_master(cfg):
    target = Path(cfg['master_path'])
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = None
    try:
        with requests.get(cfg['API_BASE_URL'].rstrip('/') + '/master',
                          headers={'Authorization': 'Bearer ' + cfg['API_TOKEN']},
                          timeout=cfg['HTTP_TIMEOUT_SECONDS'], stream=True, allow_redirects=False) as response:
            if response.status_code != 200:
                raise ValueError('No se pudo descargar el maestro: HTTP ' + str(response.status_code))
            expected = response.headers.get('X-Content-SHA256', '')
            digest = hashlib.sha256()
            size = 0
            with tempfile.NamedTemporaryFile(dir=target.parent, suffix='.xlsx', delete=False) as f:
                temp = Path(f.name)
                for chunk in response.iter_content(65536):
                    size += len(chunk)
                    if size > 5 * 1024 * 1024:
                        raise ValueError('Maestro excede 5 MB')
                    digest.update(chunk)
                    f.write(chunk)
        actual = digest.hexdigest()
        if actual != expected:
            raise ValueError('Hash del maestro incorrecto; se conserva la copia anterior.')
        wb = load_workbook(temp, read_only=True, data_only=False)
        try:
            meta = dict(list(wb['Metadata'].values)[1:])
            if list(next(iter(wb['Master'].values))) != COLUMNS:
                raise ValueError('Columnas del maestro incorrectas')
            if (meta.get('period_start'), meta.get('period_end')) != (cfg['PERIOD_START'], cfg['PERIOD_END']):
                raise ValueError('El periodo del servidor no coincide con el cliente')
            if not meta.get('version') or meta['version'] == 'COMPLETAR':
                raise ValueError('Maestro sin version')
            if meta.get('synthetic') == 'true' and cfg['ALLOW_SYNTHETIC_MASTER'].lower() != 'true':
                raise ValueError('Maestro sintetico no autorizado')
        finally:
            wb.close()
        temp.replace(target)
        receipt = dict(server=cfg['API_BASE_URL'], sha256=actual, bytes=size, version=meta['version'])
        folder = Path(cfg['output_path']) / 'private'
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'maestro_compartido.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
        return receipt
    finally:
        if temp and temp.exists():
            temp.unlink()
