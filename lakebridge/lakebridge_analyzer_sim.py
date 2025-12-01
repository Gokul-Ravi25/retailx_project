# lakebridge_analyzer_sim.py
import re
import json
import sys
import pathlib

INPUT_DIR = "lakebridge/input"
OUT = "lakebridge/output/analyzer_report.json"
pathlib.Path("lakebridge/output").mkdir(parents=True, exist_ok=True)

oracle_tokens = ["NVL", "DECODE", "TO_CHAR", "DBMS_OUTPUT",
                 "PL/SQL", "VARCHAR2", "NUMBER", "SYSDATE", "SEQUENCE"]

report = {"summary": {"files_scanned": 0, "issues_found": 0}, "files": []}

for p in list(pathlib.Path(INPUT_DIR).glob("*.sql")):
    txt = p.read_text()
    report["summary"]["files_scanned"] += 1
    issues = []
    # detect PL/SQL block
    if re.search(r"\bDECLARE\b|\bBEGIN\b|\bEND\b", txt, re.IGNORECASE):
        issues.append(
            "PLSQL_BLOCK: contains DECLARE/BEGIN/END; procedural logic likely")
    for tok in oracle_tokens:
        if re.search(r"\b" + re.escape(tok) + r"\b", txt, re.IGNORECASE):
            issues.append(f"ORACLE_TOKEN: {tok}")
    rec = {"path": str(p), "issues": list(dict.fromkeys(issues))}
    report["files"].append(rec)
    report["summary"]["issues_found"] += len(issues)

report["summary"]["migration_effort_score"] = "medium" if report["summary"]["issues_found"] > 0 else "low"

with open(OUT, "w") as f:
    json.dump(report, f, indent=2)

print("Analyzer report written to", OUT)
