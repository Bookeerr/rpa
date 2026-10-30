"""Paquete EP2 sin entornos, credenciales, fuentes ajenas ni historial Git."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
DELIVERY=ROOT/'entrega'
EXECUTION=json.loads((ROOT/'docs/evidencias/web_nativa_resumen.json').read_text(encoding='utf8'))['execution_id']
DIRS=('auxiliaries','api','config','data','database','docs','recorder','rocketbot','scripts','tests')
FILES=('README.md','GUIA_COMPLETA_PROYECTO.md','.env.example','.gitignore','ejecutar_ep2.bat','INICIAR_EP2.bat','HABILITAR_RED.bat','PREPARAR_OTRA_PC.bat','requirements-ep2.txt','requirements-dev-ep2.txt')


def main():
    DELIVERY.mkdir(exist_ok=True)
    chosen=[ROOT/name for name in FILES]
    for name in DIRS:
        for p in (ROOT/name).rglob('*'):
            if not p.is_file():continue
            rel=p.relative_to(ROOT)
            if any(part in ('.git','__pycache__','private','logs','fuentes_extraidas') for part in rel.parts):continue
            if p.suffix in ('.pyc','.log','.tmp') or p.name.startswith('.env'):continue
            if p.name=='revision_pdf.png':continue  # Contacto historico anterior a la revision final.
            if '_AVANCE' in p.name:continue
            chosen.append(p)
    chosen += [p for p in (ROOT/'output'/EXECUTION).rglob('*') if p.is_file()]
    review=ROOT/'docs/evidencias/revision_funcional.json'
    if review.exists():
        from uuid import UUID
        review_id=str(UUID(json.loads(review.read_text(encoding='utf8'))['execution_id']))
        chosen += [p for p in (ROOT/'output'/review_id).rglob('*') if p.is_file()]
    chosen=sorted(set(chosen))
    manifest={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in chosen}
    archive=DELIVERY/'TestFire_EP2_20261020.zip'
    prefix='TestFire_EP2/'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for p in chosen:z.write(p,prefix+p.relative_to(ROOT).as_posix())
        z.writestr(prefix+'MANIFEST_SHA256.json',json.dumps(manifest,indent=2))
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for name,digest in manifest.items():
            assert hashlib.sha256(z.read(prefix+name)).hexdigest()==digest
        assert not any('/.env' in n and not n.endswith('/.env.example') for n in z.namelist())
    receipt=dict(archive=archive.relative_to(ROOT).as_posix(),files=len(chosen),bytes=archive.stat().st_size,
                 sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),crc_and_hashes_verified=True)
    (DELIVERY/'paquete_verificado.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
