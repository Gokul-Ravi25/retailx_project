# sample_plsql.py
from pyspark.sql.functions import sum as sum_

orders = spark.table("retailx.silver.orders")
v_total_row = orders.agg(sum_("amount").alias("total_amount")).collect()
v_total = v_total_row[0]["total_amount"] if v_total_row else 0
print(f"Total Amount: {v_total}")
