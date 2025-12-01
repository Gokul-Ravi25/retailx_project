# lakebridge_transpiler_sim.py
import pathlib
import re
INPUT = "lakebridge/input"
OUT = "lakebridge/output/transpiled_sql"
pathlib.Path(OUT).mkdir(parents=True, exist_ok=True)

# simple DDL transpile
ddl_map = {
    "NUMBER": "BIGINT",
    "VARCHAR2": "STRING",
    "DATE": "TIMESTAMP"
}

for p in pathlib.Path(INPUT).glob("*.sql"):
    txt = p.read_text()
    # naive DDL conversion
    converted = txt
    for k, v in ddl_map.items():
        converted = re.sub(r"\b"+k+r"\b", v, converted, flags=re.IGNORECASE)
    # write simple targets: if contains CREATE TABLE ORDERS -> orders.sql
    name = p.stem.lower()
    outf = pathlib.Path(OUT) / f"{name}.sql"
    outf.write_text(converted)
    print("Wrote", outf)

# simple PL/SQL -> pyspark mapping
plsql = pathlib.Path(INPUT) / "sample_plsql.sql"
if plsql.exists():
    py_out = pathlib.Path(OUT) / "sample_plsql.py"
    pysrc = """from pyspark.sql.functions import sum as sum_\norders = spark.table(\"retailx.silver.orders\")\nv_total_row = orders.agg(sum_(\"amount\").alias(\"total_amount\")).collect()\nv_total = v_total_row[0][\"total_amount\"] if v_total_row else 0\nprint(f\"Total Amount: {v_total}\")\n"""
    py_out.write_text(pysrc)
    print("Wrote", py_out)
