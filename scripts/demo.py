"""Demostracion SINTETICA de auxiliares, NO robot ni evidencia Studio."""
import argparse
from datetime import datetime
from pathlib import Path
import json
from auxiliaries.timezones import ZoneInfo
from auxiliaries.audit import Audit
from auxiliaries.config import ROOT, load_config
from auxiliaries.excel import create_masters, read_master, write_report
from auxiliaries.reconciliation import plan_pairs, classify_pair, counts
from auxiliaries.validation import validate_row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--create-data", action="store_true")
    args = parser.parse_args()
    create_masters(ROOT)
    if args.create_data:
        print("Maestro SINTETICO y plantilla disponibles en data/")
        return
    cfg = load_config(require_secrets=False)
    # Demo independiente de endpoints privados y del maestro real configurado.
    audit = Audit(cfg, mode="SINTETICO_SIN_ROCKETBOT")
    valid, rejected, results = [], [], []
    with audit.step("INIT_CONFIG"):
        audit.write_json("config.json", {k:v for k,v in cfg.items() if k not in ('PROJECT_ROOT','master_path','output_path')})
    with audit.step("READ_REFERENCES"):
        master = read_master(ROOT / "data/conciliacion_master.xlsx", audit.id, {"800003"}, "2026-10-01", "2026-10-31", True)
        rules = {"800003":{"enabled":True,"tolerance":"0.00","version":"SINTETICO-1"}}
        audit.write_json("master_metadata.json",master["metadata"])
    raw_rows = [dict(account="800003",date_raw="2026-10-01",description="Deposito demo",amount_raw="100.00",web_id="DEMO-1"),
                dict(account="800003",date_raw="2026-10-02",description="Cargo demo",amount_raw="-24.00",web_id="DEMO-2"),
                dict(account="800003",date_raw="2026-10-04",description="Solo web",amount_raw="8.00",web_id="DEMO-4"),
                dict(account="800003",date_raw="2026-02-30",description="Invalido",amount_raw="1.234,56",web_id=None)]
    with audit.step("VALIDATE_DATA"):
        for index, row in enumerate(raw_rows,1):
            row.update(row_index=index,source_url="SINTETICO")
            r = validate_row(row,audit.id)
            (valid if r["valid"] else rejected).append(r["row"] if r["valid"] else r)
    with audit.step("RECONCILE"):
        for pair in plan_pairs(valid,master["rows"],rules):
            results.append(dict(pair,status=classify_pair(pair)))
    for step in ("WEB_LOGIN","EXTRACT_ACCOUNTS","EXTRACT_TRANSACTIONS","SAVE_DATABASE","HTTP_INTEGRATION"):
        e=audit.start(step)
        audit.end(e,"OMITIDO","Demo sintetica de auxiliares; requiere ejecucion real en Studio")
    stamp=datetime.now(ZoneInfo(cfg["DISPLAY_TIMEZONE"])).strftime("%Y%m%d_%H%M%S")
    report=audit.folder/f"Reporte_TestFire_{stamp}_{audit.id}.xlsx"
    with audit.step("EXPORT_EXCEL"):
        write_report(report,valid,results,rejected,audit.events,dict(audit.summary,**counts(results),status="PARCIAL"))
    with audit.step("FINALIZE"):
        audit.write_json("results.json",results)
    summary=audit.finish("PARCIAL",valid_rows=len(valid),rejected_rows=len(rejected),classifications=counts(results),
                         pending=["ROCKETBOT","RECORDER","MYSQL","HTTP","SEGUNDA_PC"])
    # Proyeccion final de auditoria tras cierre; no cambia datos de negocio.
    write_report(report,valid,results,rejected,audit.events,summary)
    audit.write_json("artifacts.json",[audit.artifact(report,"EXCEL")])
    print(json.dumps({"execution_id":audit.id,"status":"PARCIAL","mode":summary["mode"],
                      "report":report.relative_to(ROOT).as_posix(),"classifications":counts(results)},ensure_ascii=True,indent=2))


if __name__ == "__main__":
    main()
