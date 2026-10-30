import json
from uuid import uuid4
from auxiliaries.audit import Audit
from auxiliaries.database import Repository
from tests.test_core import config_tmp


def test_crash_after_commit_before_ack_replays_same_event(tmp_path,monkeypatch):
    a=Audit(config_tmp(tmp_path))
    with a.step('SQL'): pass
    db={}; summaries=[]; repo=Repository(a.cfg)
    monkeypatch.setattr(repo,'save_execution',lambda s:summaries.append(s))
    def save(e): db.setdefault(e['event_id'],e)
    monkeypatch.setattr(repo,'save_event',save)
    assert repo.replay(a.folder)==1
    assert repo.replay(a.folder)==0
    pending=next((a.folder/'outbox').glob('*.json'))
    pending.with_suffix('.ack').unlink() # Simula ACK perdido tras commit; no SQL real.
    assert repo.replay(a.folder)==1 and len(db)==1
    assert len(summaries)==3


def test_failed_delivery_preserves_queue(tmp_path,monkeypatch):
    import pytest
    a=Audit(config_tmp(tmp_path))
    with a.step('SQL'): pass
    repo=Repository(a.cfg)
    def down(*_): raise ConnectionError('SIMULADO')
    monkeypatch.setattr(repo,'save_execution',down)
    with pytest.raises(ConnectionError):repo.replay(a.folder)
    assert len(a.pending())==1


def test_reconcile_does_not_match_unknown_currency_silently():
    from tests.test_core import row,statuses
    w=row(web_id='A');m=row(web_id='A');m['currency']='USD'
    assert statuses([w],[m])==['DISCREPANCIA']
