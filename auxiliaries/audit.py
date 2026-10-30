from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
import getpass
import hashlib
import json
import socket
import time
from uuid import uuid4


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def clean(value, secrets=()):
    if isinstance(value, dict):
        return {k: "[REDACTADO]" if any(s in k.lower() for s in ("password", "token", "cookie", "authorization"))
                else clean(v, secrets) for k, v in value.items()}
    if isinstance(value, list):
        return [clean(v, secrets) for v in value]
    if isinstance(value, str):
        for secret in secrets:
            if secret and secret != "REEMPLAZAR":
                value = value.replace(str(secret), "[REDACTADO]")
    return value


class Audit:
    """Instancia viva durante la ejecucion Studio; no reiniciar entre pasos."""
    def __init__(self, cfg, mode="ROCKETBOT"):
        self.id = str(uuid4())
        self.cfg = cfg
        self.folder = Path(cfg["output_path"]) / self.id
        self.folder.mkdir(parents=True)
        self.secrets = [cfg.get(k) for k in ("TESTFIRE_PASSWORD", "DB_PASSWORD", "API_TOKEN", "TESTFIRE_USER")]
        self.started_ns = time.perf_counter_ns()
        self.events = []
        self.active = {}
        self.summary = dict(execution_id=self.id, hostname=socket.gethostname(), os_user=getpass.getuser(),
                            robot_version=cfg["ROBOT_VERSION"], config_hash=cfg["config_hash"],
                            started_at=utc_now(), ended_at=None, duration_ms=None, status="EN_CURSO", mode=mode)
        self.save_summary()

    def write_json(self, name, data):
        path = self.folder / name
        if not path.resolve().is_relative_to(self.folder.resolve()):
            raise ValueError("Evidencia fuera de ejecucion")
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(json.dumps(clean(data, self.secrets), ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        tmp.replace(path)
        return path.relative_to(Path(self.cfg["PROJECT_ROOT"])).as_posix()

    def save_summary(self):
        self.write_json("execution.json", self.summary)

    def start(self, step_id, attempt=1):
        event = dict(event_id=str(uuid4()), execution_id=self.id, hostname=self.summary["hostname"],
                     step_id=step_id, step_order=len(self.events)+len(self.active)+1, attempt=attempt,
                     started_at=utc_now(), ended_at=None, duration_ms=None, status="EN_CURSO", detail="", evidence=None)
        self.active[event["event_id"]] = (event, time.perf_counter_ns())
        self.write_json("active_steps.json", [e for e, _ in self.active.values()])
        return event["event_id"]

    def end(self, event_id, status="OK", detail="", evidence=None):
        if status not in ("OK", "ERROR", "ADVERTENCIA", "OMITIDO"):
            raise ValueError("Estado de paso invalido")
        event, ns = self.active.pop(event_id)
        event.update(ended_at=utc_now(), duration_ms=round((time.perf_counter_ns()-ns)/1e6, 3),
                     status=status, detail=clean(detail, self.secrets), evidence=evidence)
        self.events.append(event)
        with (self.folder / "audit.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
        # Outbox completo e inmutable; ACK separado permite repetir sin perder eventos.
        self.write_json("outbox/" + event_id + ".json", {"kind": "step_audit", "data": event})
        self.write_json("active_steps.json", [e for e, _ in self.active.values()])
        return event

    @contextmanager
    def step(self, step_id, attempt=1):
        event_id = self.start(step_id, attempt)
        try:
            yield event_id
        except Exception as exc:
            self.end(event_id, "ERROR", type(exc).__name__ + ": " + str(exc))
            raise
        else:
            self.end(event_id)

    def finish(self, status, **counts):
        if status not in ("OK", "PARCIAL", "ERROR", "INTERRUMPIDO"):
            raise ValueError("Estado global invalido")
        if self.active:
            raise ValueError("Cerrar pasos abiertos antes de finalizar")
        if status == "OK" and (self.pending() or any(e["status"] == "ERROR" for e in self.events)):
            raise ValueError("No puede declarar OK con errores o SQL pendiente")
        self.summary.update(status=status, ended_at=utc_now(),
                            duration_ms=round((time.perf_counter_ns()-self.started_ns)/1e6, 3), **counts)
        self.save_summary()
        return self.summary

    def pending(self):
        return [p for p in (self.folder / "outbox").glob("*.json") if not p.with_suffix(".ack").exists()]

    def artifact(self, path, kind):
        path = Path(path).resolve()
        return dict(execution_id=self.id, hostname=self.summary["hostname"],
                    path=path.relative_to(Path(self.cfg["PROJECT_ROOT"])).as_posix(), kind=kind,
                    sha256=hashlib.sha256(path.read_bytes()).hexdigest(), availability="LOCAL")
