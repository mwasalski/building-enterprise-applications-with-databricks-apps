# Databricks notebook source
# MAGIC %run ./Classroom-Setup-Common

# COMMAND ----------

# create a small table in user schema 
@DBAcademyHelper.add_init
def create_sample_table(self):
    spark.sql('CREATE OR REPLACE TABLE trips AS SELECT * FROM samples.nyctaxi.trips LIMIT 1000')

# COMMAND ----------

DA = DBAcademyHelper()