"""Lectura documental de archivos proporcionados; no altera originales."""
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


def main():
    downloads = Path.home() / "Downloads"
    paths = list(downloads.glob("*EP2*pdf")) + list(downloads.glob("*Parcial_I_ATY*pdf"))
    paths += list(downloads.glob("CASO2*docx"))
    paths += [ROOT / "PDD_TestFire.docx", ROOT / "Informe_Tecnico_TestFire.docx"]
    out = ROOT / "docs/fuentes_extraidas"
    out.mkdir(parents=True, exist_ok=True)
    for n, path in enumerate(paths, 1):
        if path.suffix == ".pdf":
            text = "\n".join(f"PAGINA {i+1}\n" + (page.extract_text() or "")
                             for i, page in enumerate(PdfReader(path).pages))
        else:
            with zipfile.ZipFile(path) as z:
                doc = ET.fromstring(z.read("word/document.xml"))
            ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
            text = "\n".join("".join(t.text or "" for t in p.findall(".//w:t", ns))
                             for p in doc.findall(".//w:p", ns))
        (out / f"fuente_{n}.txt").write_text(path.name + "\n" + text, encoding="utf-8")
        print(f"fuente_{n}.txt: {len(text)} caracteres")


if __name__ == "__main__":
    main()
