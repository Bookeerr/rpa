import hashlib
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from uuid import uuid4
import pytest
import requests
from werkzeug.serving import make_server
from api.app import create_app
from api.local_store import SQLiteReceiptStore
from auxiliaries.excel import create_masters
from scripts.network_services import service_target, sync_master
from tests.test_core import config_tmp


@pytest.fixture
def shared_server(tmp_path):
    cfg = config_tmp(tmp_path)
    create_masters(tmp_path)
    cfg.update(API_ROLE='server', API_TOKEN='network-test-secret',
               master_path=str(tmp_path/'data/conciliacion_master.xlsx'), ALLOW_SYNTHETIC_MASTER='true')
    app = create_app(cfg, SQLiteReceiptStore(tmp_path/'receipts.db'))
    srv = make_server('127.0.0.1', 0, app, threaded=True)
    thread = Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    client = dict(cfg, API_ROLE='client', API_BASE_URL=f'http://127.0.0.1:{srv.server_port}',
                  master_path=str(tmp_path/'client/master.xlsx'))
    yield cfg, client, app
    srv.shutdown()
    thread.join(timeout=2)
    srv.server_close()


def test_master_auth_exact_hash_and_atomic_download(shared_server):
    server, client, app = shared_server
    from pathlib import Path
    assert app.test_client().get('/master').status_code == 401
    result = sync_master(client)
    expected = Path(server['master_path']).read_bytes()
    assert Path(client['master_path']).read_bytes() == expected
    assert result['sha256'] == hashlib.sha256(expected).hexdigest()


@pytest.mark.parametrize('failure', ['period', 'token', 'hash'])
def test_failed_download_preserves_previous_master(shared_server, failure):
    from pathlib import Path
    server, client, app = shared_server
    old = Path(client['master_path'])
    old.parent.mkdir(parents=True)
    old.write_bytes(b'previous master')
    if failure == 'period':
        client['PERIOD_START'] = '2020-01-01'
    elif failure == 'token':
        client['API_TOKEN'] = 'wrong-token'
    else:
        @app.after_request
        def bad_hash(response):
            response.headers['X-Content-SHA256'] = 'wrong'
            return response
    with pytest.raises(ValueError):
        sync_master(client)
    assert old.read_bytes() == b'previous master'
    assert list(old.parent.glob('*.xlsx')) == [old]


def test_two_clients_persist_in_single_store(shared_server):
    server, client, app = shared_server
    ids = [str(uuid4()), str(uuid4())]
    headers = {'Authorization': 'Bearer ' + client['API_TOKEN']}
    def send(index):
        p = dict(execution_id=ids[index], equipo='SIMULADO-PC-'+str(index),
                 estado_proceso='CONCILIACION_COMPLETADA', movimientos_validos=3,
                 movimientos_rechazados=0, discrepancias=1, duracion_hasta_envio_ms=10)
        url = client['API_BASE_URL'] + '/executions'
        assert requests.post(url, json=p, headers=headers, timeout=3).status_code == 201
        assert requests.post(url, json=p, headers=headers, timeout=3).status_code == 200
        assert requests.get(url+'/'+ids[index], headers=headers, timeout=3).json() == p
    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(send, range(2)))


@pytest.mark.parametrize('role', ['server', 'client'])
def test_network_target_is_explicit_private_ipv4(role):
    cfg = dict(API_ROLE=role, API_BASE_URL='http://192.168.1.91:18081',
               API_BIND_HOST='192.168.1.91', API_PORT=18081)
    assert service_target(cfg) == (role, '192.168.1.91', 18081)
    for url in ('http://0.0.0.0:18081', 'http://8.8.8.8:18081', 'http://192.168.1.91:18081/#bad'):
        with pytest.raises(ValueError):
            service_target(dict(cfg, API_BASE_URL=url))
    if role == 'server':
        with pytest.raises(ValueError):
            service_target(dict(cfg, API_BIND_HOST='0.0.0.0'))


def test_client_does_not_spawn_local_fallback(monkeypatch):
    from scripts import start_local_services as launcher
    cfg = dict(API_ROLE='client', API_TOKEN='test', API_BASE_URL='http://192.168.1.91:18081')
    monkeypatch.setattr(launcher, 'load_config', lambda **kw: cfg)
    def unavailable(*args, **kwargs):
        raise requests.ConnectionError('simulated')
    def forbidden(*args, **kwargs):
        pytest.fail('Client must never start a local API')
    monkeypatch.setattr(launcher.requests, 'get', unavailable)
    monkeypatch.setattr(launcher.subprocess, 'Popen', forbidden)
    with pytest.raises(SystemExit, match='Servidor no disponible'):
        launcher.main()


def test_local_api_does_not_publish_master():
    from api.app import MemoryReceiptStore
    app = create_app({'API_TOKEN':'test'}, MemoryReceiptStore())
    assert app.test_client().get('/master', headers={'Authorization':'Bearer test'}).status_code == 404
