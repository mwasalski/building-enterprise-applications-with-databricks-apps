# Databricks notebook source
# MAGIC %run ./Classroom-Setup-Common

# COMMAND ----------

DA = DBAcademyHelper()

# COMMAND ----------

from databricks.sdk.errors import NotFound

@DBAcademyHelper.add_init
def delete_demo_app():
    try:
        app = DA.workspace.apps.get(DA.app_name)
        DA.workspace.apps.delete(app.name)
        print(f"Deleted app: {app.name}")
    except NotFound:
        print("App not found")
    except Exception as e:
        print(f"Failed to delete app: {e}")

# COMMAND ----------

# Deleting the app created in the previous module
delete_demo_app()

# COMMAND ----------

# create and display PAT credentials on demand
@DBAcademyHelper.add_method
def display_credentials(self):
    token = self.workspace.tokens.create(comment=self.username)
    self.workspace.dbutils.widgets.removeAll()
    self.workspace.dbutils.widgets.text(name='token', defaultValue=token.token_value)
    self.workspace.dbutils.widgets.text(name='host', defaultValue=self.workspace.config.host)