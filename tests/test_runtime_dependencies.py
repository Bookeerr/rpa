"""El runtime debe cargar dotenv sin depender del venv ni del PATH del usuario."""
import subprocess
import sys
from auxiliaries.config import ROOT


def test_runtime_dependencies_without_site_packages(tmp_path):
    code = f'''
import sys
from pathlib import Path
root = Path({str(ROOT)!r})
sys.path.insert(0, str(root))
import auxiliaries
import dotenv, pytz
from auxiliaries.config import load_config
assert Path(dotenv.__file__).is_relative_to(root / 'auxiliaries/_vendor')
assert Path(pytz.__file__).is_relative_to(root / 'auxiliaries/_vendor')
assert pytz.timezone('America/Santiago')
assert load_config(require_secrets=False)['PROJECT_ROOT'] == str(root)
print('DEPENDENCIAS_PORTABLES_OK')
'''
    result = subprocess.run([sys.executable, '-I', '-S', '-B', '-c', code],
                            cwd=tmp_path, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == 'DEPENDENCIAS_PORTABLES_OK'
