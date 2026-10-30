"""ER generado leyendo las tablas y FKs reales de schema.sql."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]


def main():
    sql=(ROOT/'database/schema.sql').read_text(encoding='utf-8')
    text=['erDiagram']
    links=[]
    for name,body in re.findall(r'CREATE TABLE IF NOT EXISTS (\w+) \((.*?)\) ENGINE=InnoDB;',sql,re.S):
        text.append('  '+name+' {')
        for m in re.finditer(r'\b(\w+)\s+(CHAR|VARCHAR|DATETIME|DECIMAL|INT|DATE|TEXT|JSON|BOOLEAN|ENUM)\b',body):
            col,kind=m.groups()
            tail=body[m.end():].split('\n',1)[0]
            text.append('    '+kind+' '+col+(' PK' if re.match(r'\([^)]*\) PRIMARY KEY',tail) else ''))
        text.append('  }')
        for fk,parent,pk in re.findall(r'FOREIGN KEY \((\w+)\) REFERENCES (\w+)\((\w+)\)',body):
            links.append(f'  {parent} ||--o{{ {name} : "{fk}"')
    text.extend(links)
    (ROOT/'docs/diagramas/03_modelo_datos.mmd').write_text('\n'.join(text)+'\n',encoding='utf-8')


if __name__=='__main__': main()
