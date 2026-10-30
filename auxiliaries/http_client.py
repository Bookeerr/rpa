"""Una llamada por comando: los reintentos y decisiones pertenecen a Studio."""
from urllib.parse import urlsplit
from uuid import uuid4
import time
import requests
from auxiliaries.validation import valid_uuid


def call_http(cfg, audit, method, path, payload=None, attempt=1):
    if method not in ("GET", "POST"):
        raise ValueError("Metodo fuera de alcance")
    if path not in ("/health", "/executions"):
        prefix = "/executions/"
        if not path.startswith(prefix):
            raise ValueError("Endpoint fuera de contrato")
        valid_uuid(path[len(prefix):])
    url = cfg["API_BASE_URL"].rstrip("/") + path
    call_id = str(uuid4())
    request_ref = audit.write_json(f"http/{call_id}_request.json", {"method":method,"path":path,
        "headers":{"Authorization":"[REDACTADO]","Content-Type":"application/json"},"body":payload})
    event_id = audit.start("HTTP_" + method, attempt)
    start = time.perf_counter_ns()
    status, body, error, valid = None, None, None, False
    try:
        with requests.request(method,url,json=payload,headers={"Authorization":"Bearer "+cfg["API_TOKEN"]},
                              timeout=cfg["HTTP_TIMEOUT_SECONDS"],allow_redirects=False) as r:
            status = r.status_code
            try:
                body = r.json()
            except ValueError:
                body = {"non_json": r.text[:4000]}
                error = "NON_JSON"
            if error is None:
                if path == "/health":
                    valid = status == 200 and isinstance(body,dict) and body.get("status") == "ok"
                elif method == "POST":
                    valid = status in (200,201) and isinstance(body,dict) and body.get("accepted") is True and body.get("execution_id") == payload["execution_id"]
                else:
                    valid = status == 200 and isinstance(body,dict) and body.get("execution_id") == path.rsplit("/",1)[-1]
                if not valid:
                    error = "HTTP_STATUS_OR_SCHEMA"
    except requests.Timeout:
        error = "TIMEOUT"
    except requests.RequestException:
        error = "CONNECTION_ERROR"
    duration = round((time.perf_counter_ns()-start)/1e6,3)
    response_ref = audit.write_json(f"http/{call_id}_response.json", {"status":status,"body":body,"error":error})
    audit.end(event_id,"OK" if valid else "ERROR",error or "Contrato validado",response_ref)
    return dict(call_id=call_id,execution_id=audit.id,method=method,endpoint=path,attempt=attempt,
                duration_ms=duration,http_status=status,error=error,request_ref=request_ref,response_ref=response_ref,
                valid=valid,body=body,retryable=error in ("TIMEOUT","CONNECTION_ERROR") or status in (502,503,504))
