from pathlib import Path
import json
import shutil
import subprocess
import sys
from auxiliaries.config import ROOT


def test_copied_project_spaces_other_cwd(tmp_path):
    target=tmp_path/'Copia del proyecto con espacios'
    target.mkdir()
    for folder in ('auxiliaries','api','scripts','database'):
        shutil.copytree(ROOT/folder,target/folder,ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copy(ROOT/'.env.example',target/'.env.example')
    # Ejecutar desde fuera de la copia: el archivo real calcula ROOT con __file__.
    code="import sys;sys.path.insert(0,sys.argv[1]);from scripts.demo import main;sys.argv=[sys.argv[0]];main()"
    completed=subprocess.run([sys.executable,'-c',code,str(target)],cwd=tmp_path,check=True,capture_output=True,text=True)
    result=json.loads(completed.stdout)
    assert result['status']=='PARCIAL' and (target/result['report']).is_file()
    folder=target/'output'/result['execution_id']
    assert (folder/'audit.jsonl').exists() and (folder/'results.json').exists()
    assert (target/'data/conciliacion_master.xlsx').exists()
    assert (target/'database/schema.sql').read_text(encoding='utf-8').startswith('-- MySQL')
