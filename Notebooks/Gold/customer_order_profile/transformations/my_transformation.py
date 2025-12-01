import dlt
from pyspark.sql.functions import col, to_date, max as max_, sum as sum_, countDistinct

@dlt.table(
    name="retailx.gold.customer_order_profile",
    comment="Customer dimension enriched with order behavior and LTV metrics."
)
def customer_order_profile():

    customers = spark.table("retailx.silver.customers") \
                     .withColumn("created_date", to_date(col("created_date")))

    orders = spark.table("retailx.silver.orders") \
                  .withColumn("order_date", to_date(col("order_date")))

    metrics = orders.groupBy("customer_id").agg(
        max_("order_date").alias("last_order_date"),
        sum_("amount").alias("total_lifetime_value"),
        countDistinct("order_sk").alias("total_orders")
    )

    return customers.join(metrics, "customer_id", "left")
