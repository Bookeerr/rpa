import hashlib
import hmac
import json
import threading
from io import BytesIO
from pathlib import Path
from flask import Flask, jsonify, request, send_file
from auxiliaries.config import load_config
from auxiliaries.database import Repository, connect, dumps
from auxiliaries.validation import valid_uuid


class MySQLReceiptStore:
    def __init__(self, cfg):
        self.cfg = cfg

    def health(self):
        Repository(self.cfg).execute("SELECT 1 AS ok", fetch=True)

    def get(self, execution_id):
        rows = Repository(self.cfg).execute("SELECT payload FROM api_receipts WHERE execution_id=%s", (execution_id,), True)
        return json.loads(rows[0]["payload"]) if rows else None

    def put(self, payload):
        body = dumps(payload)
        digest = hashlib.sha256(body.encode()).hexdigest()
        conn = connect(self.cfg)
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT payload_hash FROM api_receipts WHERE execution_id=%s", (payload["execution_id"],))
                previous = cur.fetchone()
                if previous:
                    conn.commit()
                    return "repeat" if previous["payload_hash"] == digest else "conflict"
                try:
                    cur.execute("INSERT INTO api_receipts(execution_id,payload_hash,payload) VALUES (%s,%s,%s)",
                                (payload["execution_id"],digest,body))
                    conn.commit()
                    return "created"
                except Exception as exc:
                    conn.rollback()
                    if getattr(exc, "args", [None])[0] != 1062:
                        raise
            return "repeat" if self.get(payload["execution_id"]) == payload else "conflict"
        finally:
            conn.close()


class MemoryReceiptStore:
    """Solo pruebas; nunca seleccionado por configuracion de produccion."""
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()

    def health(self):
        return None

    def get(self, execution_id):
        with self.lock:
            return self.data.get(execution_id)

    def put(self, payload):
        with self.lock:
            old = self.data.get(payload["execution_id"])
            if old is not None:
                return "repeat" if old == payload else "conflict"
            self.data[payload["execution_id"]] = payload.copy()
            return "created"


def validate_payload(p):
    required = {"execution_id", "equipo", "estado_proceso", "movimientos_validos", "movimientos_rechazados",
                "discrepancias", "duracion_hasta_envio_ms"}
    if not isinstance(p, dict) or set(p) != required:
        raise ValueError("Campos de resumen incorrectos")
    valid_uuid(p["execution_id"])
    if not isinstance(p["equipo"], str) or not 1 <= len(p["equipo"]) <= 255:
        raise ValueError("Equipo invalido")
    if p["estado_proceso"] != "CONCILIACION_COMPLETADA":
        raise ValueError("No enviar estado global definitivo")
    for field in required - {"execution_id", "equipo", "estado_proceso"}:
        if type(p[field]) is not int or p[field] < 0:
            raise ValueError("Conteo/duracion invalida")


def create_app(cfg=None, store=None):
    cfg = cfg or load_config()
    token = cfg["API_TOKEN"]
    if not token or token == "REEMPLAZAR":
        raise ValueError("Configurar API_TOKEN")
    store = store if store is not None else MySQLReceiptStore(cfg)
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 16384

    @app.before_request
    def authenticate():
        if not hmac.compare_digest(request.headers.get("Authorization", ""), "Bearer " + token):
            return jsonify(error="unauthorized"), 401

    @app.get("/health")
    def health():
        try:
            store.health()
            return jsonify(status="ok", storage=getattr(store,'storage_name',"memory-test-only" if isinstance(store, MemoryReceiptStore) else "mysql"))
        except Exception:
            return jsonify(error="storage_unavailable"), 503

    @app.get("/master")
    def master():
        # Solo el host LAN publica el archivo configurado; no acepta rutas del cliente.
        if cfg.get("API_ROLE") != "server":
            return jsonify(error="not_found"), 404
        try:
            path = Path(cfg["master_path"])
            if path.stat().st_size > 5 * 1024 * 1024:
                return jsonify(error="master_too_large"), 503
            data = path.read_bytes()
        except OSError:
            return jsonify(error="master_unavailable"), 503
        response = send_file(BytesIO(data), download_name="master.xlsx", as_attachment=True,
                             mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response.headers["X-Content-SHA256"] = hashlib.sha256(data).hexdigest()
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.post("/executions")
    def post_execution():
        p = request.get_json(silent=True)
        try:
            validate_payload(p)
        except (ValueError, TypeError, AttributeError) as exc:
            return jsonify(error=str(exc)), 400
        try:
            status = store.put(p)
        except Exception:
            return jsonify(error="storage_unavailable"), 503
        if status == "conflict":
            return jsonify(error="idempotency_conflict"), 409
        return jsonify(execution_id=p["execution_id"], accepted=True, duplicate=status == "repeat"), 201 if status == "created" else 200

    @app.get("/executions/<execution_id>")
    def get_execution(execution_id):
        try:
            execution_id = valid_uuid(execution_id)
        except ValueError:
            return jsonify(error="invalid_id"), 400
        try:
            p = store.get(execution_id)
        except Exception:
            return jsonify(error="storage_unavailable"), 503
        return (jsonify(p), 200) if p else (jsonify(error="not_found"), 404)

    return app


if __name__ == "__main__":
    config = load_config()
    create_app(config).run(host=config["API_BIND_HOST"], port=config["API_PORT"], debug=False, use_reloader=False)
