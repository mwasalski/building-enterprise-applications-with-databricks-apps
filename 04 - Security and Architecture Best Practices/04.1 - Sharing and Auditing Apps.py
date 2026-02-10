# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning">
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC #  Sharing and Auditing Apps

# COMMAND ----------

# MAGIC %md
# MAGIC ## Introduction
# MAGIC
# MAGIC In this example, we'll highlight some workflows for sharing/publishing apps with other users in the workspace, as well as auditing app usage.

# COMMAND ----------

# MAGIC %md
# MAGIC ## App Permissions and Sharing
# MAGIC
# MAGIC By default, apps are private. Only you, the principal who created the app, can access or administer it. Sharing the app with other workspace users is easy as we'll see here.
# MAGIC
# MAGIC 1. In the [Apps page](/compute/apps), locate your app (the one named in the cell output above) and select it.
# MAGIC 1. Click **Permissions** in the top-right corner.
# MAGIC 1. If you simple want to allow everyone in the workspace to access the app, then specify *Anyone in my organization can use* for **Organization permissions**. If you prefer finer gained control, then add users, service principals or groups individually with one of the following permissions:
# MAGIC    - `CAN USE`: provides ability for principal to use the deployed app (similar to the organization permissions mentioned before, only specific to the named principal)
# MAGIC    - `CAN MANAGE`: provides ability to deploy, update and delete the app
# MAGIC 1. Click **Save**.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Auditing App Usage with System Tables
# MAGIC
# MAGIC System tables serve as an analytical store of operational data, facilitating historical observability across account activities. They are critical for monitoring and analytics related to costs, usage, and performance. Since system tables are simple SQL relations, SQL queries (or dashboards) can be constructed to audit various aspects related to your apps. A simple example is provided here, but for more examples, please refer to the [Databricks documentation](https://docs.databricks.com/aws/en/admin/system-tables/audit-logs).

# COMMAND ----------

# MAGIC %md
# MAGIC ### Prerequisites
# MAGIC
# MAGIC Systems tables is a collective term that refers to a variety of tables spread across various function-based schemas, all situated within the *system* catalog. Most of these system schemas are not enabled, and hence not visible by default.
# MAGIC
# MAGIC This demo requires the *access* system schema. This must be enabled by a metastore admin, through the Databricks CLI, SDK or APIs. This has already been taken care of in this provided learning environment.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Most recently created Apps
# MAGIC
# MAGIC This example illustrates how to query the *audit* table to identify App creation events, providing a summary of when the app was created and who created it.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   event_time,
# MAGIC   user_identity.email AS email,
# MAGIC   action_name,
# MAGIC   get_json_object(request_params.app, '$.name') AS app_name
# MAGIC FROM
# MAGIC   system.access.audit
# MAGIC WHERE
# MAGIC   action_name == "createApp"
# MAGIC ORDER BY
# MAGIC   event_time DESC

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC &copy; 2025 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="blank">Apache Software Foundation</a>.<br/>
# MAGIC <br/><a href="https://databricks.com/privacy-policy" target="blank">Privacy Policy</a> | 
# MAGIC <a href="https://databricks.com/terms-of-use" target="blank">Terms of Use</a> | 
# MAGIC <a href="https://help.databricks.com/" target="blank">Support</a>