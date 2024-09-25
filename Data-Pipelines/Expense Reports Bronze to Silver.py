# Databricks notebook source
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# COMMAND ----------

# Initialize Spark session
spark = SparkSession.builder.appName("BronzeToSilverConversion").getOrCreate()

# COMMAND ----------

bronze_table = spark.read.table("default.expense_bronze")

bronze_table

# COMMAND ----------

# Define constraints for removing null values
constraints = [
    col("Date").isNotNull() &
    col("Name").isNotNull() &
    col("Category").isNotNull() & 
    col("Amount").isNotNull() &
    col("ingestion_timestamp").isNotNull()
]

# COMMAND ----------

silver_table = bronze_table.filter(*constraints)

# COMMAND ----------

silver_table.write.mode("overwrite").saveAsTable("expense_silver")

# COMMAND ----------

silver_table.show()

# COMMAND ----------


