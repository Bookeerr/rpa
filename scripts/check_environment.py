import argparse
import json
import sys
from pathlib import Path
from auxiliaries.config import load_config, public_config
from auxiliaries.database import Repository
from auxiliaries.validation import valid_uuid


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay")
    args = parser.parse_args()
    cfg = load_config(require_secrets=False)
    print(json.dumps(public_config(cfg), ensure_ascii=True, indent=2))
    if any(cfg.get(k) == "REEMPLAZAR" for k in ("DB_PASSWORD","API_TOKEN","TESTFIRE_USER","TESTFIRE_PASSWORD")):
        print("PENDIENTE: completar .env local. No se intento autenticar con valores de ejemplo.")
        return 2
    try:
        repo = Repository(cfg)
        if args.replay:
            folder = Path(cfg["output_path"]) / valid_uuid(args.replay)
            print("Eventos reenviados:", repo.replay(folder))
        else:
            print("SQL autenticado:", repo.execute("SELECT CURRENT_USER() AS principal,VERSION() AS version", fetch=True))
            print("Reglas leidas:", len(repo.rules()))
    except Exception as exc:
        print("ERROR SQL:", type(exc).__name__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
