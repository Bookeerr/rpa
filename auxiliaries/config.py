from pathlib import Path
from urllib.parse import urlsplit
import hashlib
import json
import os
from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[1]
SECRET_KEYS = {"TESTFIRE_PASSWORD", "DB_PASSWORD", "API_TOKEN", "TESTFIRE_USER"}


def resolve_path(root, value, external=False):
    root = Path(root).resolve()
    path = Path(value)
    result = (root / path).resolve()
    if not external and (path.is_absolute() or not result.is_relative_to(root)):
        raise ValueError("Ruta interna debe ser relativa a PROJECT_ROOT")
    return result


def load_config(root=None, require_secrets=True):
    root = Path(root or ROOT).resolve()
    cfg = dict(dotenv_values(root / ".env.example"))
    cfg.update(dotenv_values(root / ".env"))
    cfg.update({k: os.environ[k] for k in cfg if k in os.environ})
    for key in ("DB_PORT", "API_PORT", "WEB_TIMEOUT_SECONDS", "HTTP_TIMEOUT_SECONDS", "MAX_RETRIES"):
        cfg[key] = int(cfg[key])
    if not 0 <= cfg["MAX_RETRIES"] <= 5:
        raise ValueError("MAX_RETRIES debe estar entre 0 y 5")
    for key in ("WEB_TIMEOUT_SECONDS", "HTTP_TIMEOUT_SECONDS"):
        if not 0 < cfg[key] <= 120:
            raise ValueError("Timeout fuera de rango: " + key)
    for key in ("DB_PORT", "API_PORT"):
        if not 1 <= cfg[key] <= 65535:
            raise ValueError("Puerto invalido: " + key)
    for key in ("TESTFIRE_URL", "API_BASE_URL"):
        parsed = urlsplit(cfg[key])
        if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username or parsed.query:
            raise ValueError("Endpoint invalido: " + key)
    if cfg["DB_USER"].lower() == "root":
        raise ValueError("El robot no debe usar root")
    if require_secrets and any(not cfg.get(k) or cfg[k] == "REEMPLAZAR" for k in SECRET_KEYS):
        raise ValueError("Completar credenciales en .env local")
    public = {k: v for k, v in cfg.items() if k not in SECRET_KEYS}
    cfg["config_hash"] = hashlib.sha256(json.dumps(public, sort_keys=True).encode()).hexdigest()
    cfg["PROJECT_ROOT"] = str(root)
    cfg["master_path"] = str(resolve_path(root, cfg["MASTER_EXCEL_PATH"], external=True))
    cfg["output_path"] = str(resolve_path(root, cfg["OUTPUT_ROOT"]))
    return cfg


def public_config(cfg):
    return {k: ("[REDACTADO]" if k in SECRET_KEYS else v) for k, v in cfg.items()
            if k not in ("PROJECT_ROOT", "master_path", "output_path")}
