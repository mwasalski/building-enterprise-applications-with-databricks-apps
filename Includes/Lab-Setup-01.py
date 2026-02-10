# Databricks notebook source
# MAGIC %run ./Classroom-Setup-Common

# COMMAND ----------

from os.path import abspath

@DBAcademyHelper.add_init
def app_config_lab(self):
    # calculate default app name and add it to the display list
    self.app_name = self.app_name + '-lab'

    self.app_code_path = abspath("./lab_code")
    self.display_config_add("app_code_path", "App code template")

# COMMAND ----------

DA = DBAcademyHelper()