"""Cierre del puente con fallo SQL inyectado; no acredita MySQL real."""
import hashlib
import json
import pytest
from openpyxl import load_workbook
from auxiliaries import bridge
from auxiliaries.database import Repository
from tests.test_core import config_tmp


def start(tmp_path, monkeypatch):
    monkeypatch.setattr(bridge, 'load_config', lambda _: config_tmp(tmp_path))
    result = bridge.initialize(tmp_path)
    return result['execution_id'], bridge.session(result['execution_id'])


def test_bridge_refuses_success_without_integrations(tmp_path, monkeypatch):
    execution_id, s = start(tmp_path, monkeypatch)
    try:
        with pytest.raises(ValueError, match='incompletas'):
            bridge.finalize(execution_id, 'OK')
        assert s['audit'].summary['status'] == 'EN_CURSO'
    finally:
        bridge._sessions.pop(execution_id)


def test_failed_sql_close_keeps_final_report_hash_replayable(tmp_path, monkeypatch):
    execution_id, s = start(tmp_path, monkeypatch)
    try:
        bridge.export_excel(execution_id)
        s.update(sql_ok=True, http_ok=True, web_ok=True)
        def unavailable(*_):
            raise ConnectionError('SQL caido SIMULADO')
        monkeypatch.setattr(s['repo'], 'replay', unavailable)
        summary = bridge.finalize(execution_id, 'OK')
        assert summary['status'] == 'PARCIAL' and summary['sql_final_pending']
        a = s['audit']
        artifacts = json.loads((a.folder / 'artifacts.json').read_text())
        assert artifacts[0]['sha256'] == hashlib.sha256(s['report'].read_bytes()).hexdigest()
        wb = load_workbook(s['report'])
        assert any('PARCIAL' == cell.value for row in wb['Resumen'] for cell in row)
        wb.close()
        delivered = []
        repo = Repository(s['cfg'])
        monkeypatch.setattr(repo, 'save_execution', lambda value: delivered.append(value))
        monkeypatch.setattr(repo, 'save_bundle', lambda *args, **kwargs: delivered.append(kwargs))
        assert repo.replay(a.folder) == 0  # No eventos: aun asi recupera artefactos.
        assert delivered[0]['status'] == 'PARCIAL'
        assert delivered[1]['artifacts'] == artifacts
    finally:
        bridge._sessions.pop(execution_id)


def test_bridge_records_out_of_period_as_rejected(tmp_path, monkeypatch):
    execution_id, s = start(tmp_path, monkeypatch)
    try:
        raw = dict(account='800003', date_raw='2025-01-01', description='DEMO',
                   amount_raw='10.00', row_index=1, source_url='SINTETICO')
        result = bridge.validate(execution_id, raw, 'iso')
        assert not result['valid'] and 'periodo' in result['error']
        bridge.append_rejected(execution_id, result)
        assert len(s['rejected']) == 1 and not s['valid']
    finally:
        bridge._sessions.pop(execution_id)
