# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

# MAGIC %fs
# MAGIC ls "/mnt/expense"

# COMMAND ----------

source_path = "/mnt/expense/"

df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(source_path)

# COMMAND ----------

df_with_metadata = df.withColumn("ingestion_timestamp", current_timestamp())
df_with_metadata.show()

# COMMAND ----------

bronze_table_name = "expense_bronze"
df_with_metadata.write.format("delta").mode("overwrite").saveAsTable(bronze_table_name)

print(f"Bronze table '{bronze_table_name}' created successfully.")

# COMMAND ----------


