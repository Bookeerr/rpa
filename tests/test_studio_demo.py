"""Adaptacion de variables Studio y aislamiento de la demo respecto de MySQL."""
import json
from pathlib import Path
from auxiliaries import bridge, studio_demo
from auxiliaries.excel import create_masters
from auxiliaries.reconciliation import classify_pair
from tests.test_core import config_tmp


def test_studio_variable_preserves_native_and_serialized_values():
    value={'valid':True,'row':None,'amount':'-12.00'}
    assert studio_demo.variable(value) is value
    assert studio_demo.variable(json.dumps(value))==value
    assert studio_demo.variable(str(value))==value


def test_synthetic_close_exports_without_sql(tmp_path,monkeypatch):
    create_masters(tmp_path)
    monkeypatch.setattr(studio_demo,'load_config',lambda *args,**kwargs:config_tmp(tmp_path))
    eid=studio_demo.initialize(tmp_path)
    try:
        s=bridge.session(eid)
        assert s['repo'] is None and s['cfg']['API_BASE_URL']=='http://127.0.0.1:18080'
        bridge.read_excel(eid,{'800003'})
        # Una muestra de referencia se conserva como movimiento sintetico.
        bridge.append_valid(eid,s['master']['rows'][0])
        for pair in bridge.pairs(eid):bridge.append_result(eid,pair,classify_pair(pair))
        report=studio_demo.finalize(eid)
        assert (tmp_path/report).is_file()
        summary=json.loads((s['audit'].folder/'execution.json').read_text())
        assert summary['mode']=='ROCKETBOT_SINTETICO' and summary['status']=='PARCIAL'
        assert 'MYSQL' in summary['pending'] and not summary['http_ok']
    finally:
        bridge._sessions.pop(eid)
