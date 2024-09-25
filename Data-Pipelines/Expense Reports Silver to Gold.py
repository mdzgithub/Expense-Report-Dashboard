# Databricks notebook source
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, avg, count

# COMMAND ----------

silver_df = spark.read.table("default.expense_silver")

# COMMAND ----------

# Perform aggregations to create the gold table
gold_df = silver_df

# COMMAND ----------

gold_df.show()

# COMMAND ----------


# Write the gold table
gold_df.write.mode("overwrite").saveAsTable("expense_gold")

# COMMAND ----------


