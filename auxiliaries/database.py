from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID, uuid5
import json
import pymysql


def dumps(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def sql_time(value):
    return datetime.fromisoformat(value).astimezone(timezone.utc).replace(tzinfo=None) if value else None


def connect(cfg):
    return pymysql.connect(host=cfg["DB_HOST"], port=int(cfg["DB_PORT"]), user=cfg["DB_USER"],
                           password=cfg["DB_PASSWORD"], database=cfg["DB_NAME"],
                           charset="utf8mb4", connect_timeout=5, read_timeout=10, write_timeout=10,
                           autocommit=False, cursorclass=pymysql.cursors.DictCursor)


class Repository:
    def __init__(self, cfg):
        self.cfg = cfg

    def execute(self, sql, params=(), fetch=False):
        conn = connect(self.cfg)
        try:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                result = cur.fetchall() if fetch else cur.rowcount
            conn.commit()
            return result
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def rules(self):
        rows = self.execute("SELECT account,enabled,tolerance,version FROM account_rules ORDER BY account", fetch=True)
        return {r["account"]: dict(r, enabled=bool(r["enabled"]), tolerance=str(r["tolerance"])) for r in rows}

    def save_execution(self, s):
        return self.execute("""INSERT INTO executions
          (execution_id,hostname,os_user,robot_version,config_hash,started_at,ended_at,duration_ms,status,summary)
          VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
          ON DUPLICATE KEY UPDATE ended_at=VALUES(ended_at),duration_ms=VALUES(duration_ms),
          status=VALUES(status),summary=VALUES(summary)""",
          (s["execution_id"], s["hostname"], s["os_user"], s["robot_version"], s["config_hash"],
           sql_time(s["started_at"]), sql_time(s.get("ended_at")), s.get("duration_ms"), s["status"], dumps(s)))

    def save_event(self, e):
        return self.execute("""INSERT INTO step_audit
          (event_id,execution_id,step_id,step_order,attempt,started_at,ended_at,duration_ms,status,detail,evidence)
          VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE event_id=event_id""",
          (e["event_id"],e["execution_id"],e["step_id"],e["step_order"],e["attempt"],sql_time(e["started_at"]),
           sql_time(e["ended_at"]),e["duration_ms"],e["status"],e["detail"],e["evidence"]))

    def save_bundle(self, execution_id, movements, results, api_calls=(), artifacts=()):
        conn = connect(self.cfg)
        try:
            with conn.cursor() as cur:
                for r in movements:
                    identity = str(uuid5(UUID(execution_id), f"row:{r['account']}:{r['row_index']}"))
                    cur.execute("""INSERT INTO transactions
                      (extraction_id,execution_id,account,row_index,transaction_date,description_norm,amount,
                       currency,balance,web_id,source_url,raw_data) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                       ON DUPLICATE KEY UPDATE extraction_id=extraction_id""",
                      (identity,execution_id,r["account"],r["row_index"],r["date"],r["description_norm"],r["amount"],
                       r.get("currency"),r.get("balance"),r.get("web_id"),r.get("source_url"),dumps(r["raw"])))
                for i, r in enumerate(results):
                    identity = str(uuid5(UUID(execution_id), f"result:{i}"))
                    cur.execute("""INSERT INTO reconciliation_results
                      (result_id,execution_id,status,web_ref,master_ref,detail) VALUES (%s,%s,%s,%s,%s,%s)
                      ON DUPLICATE KEY UPDATE result_id=result_id""",
                      (identity,execution_id,r["status"],dumps(r.get("web")),dumps(r.get("master")),dumps(r)))
                for c in api_calls:
                    cur.execute("""INSERT INTO api_calls (call_id,execution_id,method,endpoint,attempt,duration_ms,
                      http_status,error,request_ref,response_ref) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                      ON DUPLICATE KEY UPDATE call_id=call_id""", tuple(c.get(k) for k in
                      ("call_id","execution_id","method","endpoint","attempt","duration_ms","http_status","error","request_ref","response_ref")))
                for a in artifacts:
                    cur.execute("""INSERT INTO artifacts
                      (artifact_id,execution_id,hostname,relative_path,kind,sha256,availability)
                      VALUES (%s,%s,%s,%s,%s,%s,%s)
                      ON DUPLICATE KEY UPDATE sha256=VALUES(sha256)""",
                      (str(uuid5(UUID(execution_id),a["path"])),execution_id,a["hostname"],a["path"],a["kind"],a["sha256"],a["availability"]))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def replay(self, execution_folder):
        """Un reenvio por invocacion. Studio controla los reintentos y los audita."""
        folder = Path(execution_folder)
        self.save_execution(json.loads((folder / "execution.json").read_text(encoding="utf-8")))
        count = 0
        for p in sorted((folder / "outbox").glob("*.json")):
            if p.with_suffix(".ack").exists():
                continue
            item = json.loads(p.read_text(encoding="utf-8"))
            if item["kind"] == "step_audit":
                self.save_event(item["data"])
            elif item["kind"] == "bundle":
                self.save_bundle(**item["data"])
            else:
                raise ValueError("Tipo de outbox desconocido")
            # Si el proceso cae antes del ACK, la PK evita duplicar al repetir.
            p.with_suffix(".ack").write_text("ACK", encoding="utf-8")
            count += 1
        # Proyeccion final recuperable incluso si SQL fallo despues del Excel.
        # Se lee al final: puede haber cambiado su hash al marcar PARCIAL.
        artifacts_file = folder / "artifacts.json"
        if artifacts_file.exists():
            artifacts = json.loads(artifacts_file.read_text(encoding="utf-8"))
            summary = json.loads((folder / "execution.json").read_text(encoding="utf-8"))
            self.save_bundle(summary["execution_id"], [], [], artifacts=artifacts)
        return count
