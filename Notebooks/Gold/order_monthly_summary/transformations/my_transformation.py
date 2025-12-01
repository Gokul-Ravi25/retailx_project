import dlt
from pyspark.sql.functions import col, to_date, date_format, sum as sum_, count, avg

@dlt.table(
    name="retailx.gold.order_monthly_summary",
    comment="Monthly revenue aggregations per customer."
)
def order_monthly_summary():
    df = spark.table("retailx.silver.orders")

    df = df.withColumn("order_date", to_date(col("order_date"))) \
           .withColumn("year_month", date_format(col("order_date"), "yyyy-MM"))

    return df.groupBy("customer_id", "year_month").agg(
        sum_("amount").alias("total_revenue"),
        count("*").alias("order_count"),
        avg("amount").alias("avg_order_value")
    )
