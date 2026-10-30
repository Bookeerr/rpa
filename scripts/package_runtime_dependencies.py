"""Copia solo dotenv y pytz, Python puro, desde el entorno instalado al proyecto."""
import hashlib
from importlib.metadata import distribution
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def main():
    target = ROOT / 'auxiliaries/_vendor'
    target.mkdir(parents=True, exist_ok=True)
    versions = {}
    for name, package in (('python-dotenv', 'dotenv'), ('pytz', 'pytz')):
        dist = distribution(name)
        source = Path(dist.locate_file(package))
        if not (source / '__init__.py').is_file():
            raise RuntimeError('No se encuentra el paquete instalado: ' + name)
        shutil.copytree(source, target / package, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        licenses = [p for p in dist.files or [] if '.dist-info/' in str(p)
                    and (p.name.upper().startswith('LICENSE') or '/licenses/' in str(p))]
        if not licenses:
            raise RuntimeError('Falta licencia de distribucion: ' + name)
        for item in licenses:
            dest = target / 'licenses' / name / item.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dist.locate_file(item), dest)
        versions[name] = dist.version
    hashes = {p.relative_to(target).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in target.rglob('*') if p.is_file() and p.name != 'manifest.json'
              and '__pycache__' not in p.parts and p.suffix != '.pyc'}
    (target / 'manifest.json').write_text(json.dumps(dict(versions=versions, files=hashes), indent=2), encoding='utf-8')
    print('Dependencias portables preparadas: ' + ', '.join(versions))


if __name__ == '__main__':
    main()
