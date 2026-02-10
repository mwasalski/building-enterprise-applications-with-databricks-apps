# Databricks notebook source
# code common to all notebooks belongs in this notebook. Please do not modify **_common**, as it may be dynamically manipulated
# and any changes you make to it may be lost at deploy time.

# COMMAND ----------

# MAGIC %pip install databricks-sdk>=0.36.0
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %run ./_common

# COMMAND ----------

@DBAcademyHelper.add_init
def app_config(self):
    # calculate default app name and add it to the display list
    self.app_name = ''.join(c for c in self.pseudonym.lower() if c in 'abcdefghijklmnopqrstuvwxyz0123456789-')
    self.display_config_add('app_name', 'App name')

    # display SQL warenouse name
    self.display_config_add('warehouse_name', 'SQL warehouse')

# COMMAND ----------

@DBAcademyHelper.add_init
def prune_apps(self):
    for a in filter(
        lambda x: x.creator == self.username and not x.name.startswith(self.app_name),
        self.workspace.apps.list()
    ):
        self.workspace.apps.delete(a.name)