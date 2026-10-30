"""Almacen local persistente para la demostracion, independiente de MySQL."""
import json
import sqlite3
from contextlib import closing
from pathlib import Path

class SQLiteReceiptStore:
    storage_name='sqlite-local'
    def __init__(self,path):
        self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True)
        with closing(self.connect()) as c, c:c.execute('CREATE TABLE IF NOT EXISTS receipts (id TEXT PRIMARY KEY, payload TEXT NOT NULL)')
    def connect(self):return sqlite3.connect(self.path,timeout=15)
    def health(self):
        with closing(self.connect()) as c:c.execute('SELECT 1').fetchone()
    def get(self,eid):
        with closing(self.connect()) as c:r=c.execute('SELECT payload FROM receipts WHERE id=?',(eid,)).fetchone()
        return json.loads(r[0]) if r else None
    def put(self,payload):
        body=json.dumps(payload,sort_keys=True,ensure_ascii=False)
        with closing(self.connect()) as c, c:
            c.execute('BEGIN IMMEDIATE')
            old=c.execute('SELECT payload FROM receipts WHERE id=?',(payload['execution_id'],)).fetchone()
            if old:return 'repeat' if old[0]==body else 'conflict'
            c.execute('INSERT INTO receipts VALUES (?,?)',(payload['execution_id'],body))
        return 'created'
