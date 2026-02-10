# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning">
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # LAB - Build and Deploy an AI Chat Application

# COMMAND ----------

# MAGIC %md
# MAGIC ## Lab Scenario
# MAGIC
# MAGIC In the previous lab, you deployed an app using a template and customized its layout. That app relied on a generic LLM, which struggled to accurately respond to queries about your organization’s data.
# MAGIC
# MAGIC In this lab, you’ll integrate a specialized agent—developed and fine-tuned on your internal data—into the existing app. You’ll also connect an SQL warehouse to query and visualize sales data, enhancing the app’s utility and relevance for business users.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Requirements
# MAGIC
# MAGIC Please review the following requirements before starting the lesson:
# MAGIC
# MAGIC * To run lab notebooks, you need to use the **`Serverless`**, which is enabled by default.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Lab Objectives
# MAGIC
# MAGIC - Remove the generic LLM resource from the existing app.
# MAGIC - Add the deployed data-specific agent as a new resource.
# MAGIC - Connect an SQL warehouse and query the `sales` table.
# MAGIC - Display results in both table and chart format.
# MAGIC
# MAGIC > **📌 Note:** This lab forms the foundation for upcoming labs. You must complete it before proceeding to the next exercises.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Lab Tasks
# MAGIC
# MAGIC * Reconfigure the app from the previous lab; connect it to a new agent and a SQL warehouse.
# MAGIC * Update the source code to query and display data.
# MAGIC * Deploy and test the updated app.
# MAGIC
# MAGIC **📌 Note:** This lab uses the app from the previous lab. Thus, you will need to complete the first lab before completing this one.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 1: Update App Resources
# MAGIC
# MAGIC Update the app resources:
# MAGIC
# MAGIC - Remove the model serving endpoint that was previously used as the app’s LLM resource and replace it with a new one: `cookie_sales_agent_endpoint`
# MAGIC - Add the `shared_warehouse` SQL warehouse for performing SQL queries
# MAGIC
# MAGIC > ⚠️ Note: Creating agents is outside the scope of this lab. This agent is created automatically. You can explore the [notebook]($../00 - Build-AI-Model/agent-driver) that creates it to gain a better understanding of how the agent was created and deployed using Model Serving.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 2: Update the App Code
# MAGIC
# MAGIC Update *app.yaml* as needed to accomodate the new resources. Enhance the app code to use the new agent instead of the previous LLM. Additionally, connect to the SQL warehouse and display a plot of cookie sales as a function of Country.
# MAGIC
# MAGIC - See below for some example code to incorporate, if desired, to assist with running the SQL queries
# MAGIC - The needed data can be found in:
# MAGIC    - `cookies.sales.transations`: facts table
# MAGIC    - `cookies.sales.franchises`: franchise dimension
# MAGIC
# MAGIC Once done, your app should look like this:
# MAGIC ![App Layout](../images/Labs/db-apps-lab-outline-2.png)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC If desired, use the following code snippet to get started integrating the SQL warehouse usage into your app:
# MAGIC
# MAGIC ```
# MAGIC # ensure environment variable is set correctly
# MAGIC assert os.getenv('DATABRICKS_WAREHOUSE_ID'), "DATABRICKS_WAREHOUSE_ID must be set in app.yaml."
# MAGIC
# MAGIC # general function to run SQL queries on a warehouse specified by DATABRICKS_WAREHOUSE_ID
# MAGIC def sql_query(query: str, request: gr.Request):
# MAGIC
# MAGIC     # initialize a connection to the workspace using app service principal credentials
# MAGIC     # (assumes DATABRICKS_CLIENT_ID, DATABRICKS_CLIENT_SECRET and DATABRICKS_HOST are set)
# MAGIC     wclient = WorkspaceClient(auth_type='oauth-m2m')
# MAGIC
# MAGIC     logger.info(f"processing query {query} as {wclient.current_user.me().display_name}")
# MAGIC
# MAGIC     response = wclient.statement_execution.execute_statement(
# MAGIC         statement=query,
# MAGIC         warehouse_id=os.getenv('DATABRICKS_WAREHOUSE_ID'),
# MAGIC         wait_timeout='50s'
# MAGIC     )
# MAGIC
# MAGIC     if response.status.state != StatementState.SUCCEEDED:
# MAGIC         # raise Gradio error if query did not succeed
# MAGIC         error_string = ' '. join(response.status.error.message.splitlines())
# MAGIC         logger.error(f"query failed: {error_string}")
# MAGIC         raise gr.Error(error_string, duration=10)
# MAGIC     else:
# MAGIC         logger.info(f"query returned {response.result.row_count} records")
# MAGIC
# MAGIC         if response.result.row_count > 0:
# MAGIC             return pd.DataFrame(
# MAGIC                 response.result.data_array,
# MAGIC                 columns = [ c.name for c in response.manifest.schema.columns]
# MAGIC             )
# MAGIC
# MAGIC         return pd.DataFrame()
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 3: Deploy and Test the Application
# MAGIC
# MAGIC Re-deploy the updated app from the UI and validate its functionality. Test the chatbot using the same prompts from earlier—do you observe improvements in accuracy or relevance?

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 4: Review Deployment Details
# MAGIC
# MAGIC Navigate to the **Apps** interface and inspect the deployment logs and resource configurations. This will help you troubleshoot and validate that all resources are correctly linked.
# MAGIC > **🚨 Important:** Do not delete this app! You’ll continue building on it in the next lab.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC &copy; 2025 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="blank">Apache Software Foundation</a>.<br/>
# MAGIC <br/><a href="https://databricks.com/privacy-policy" target="blank">Privacy Policy</a> | 
# MAGIC <a href="https://databricks.com/terms-of-use" target="blank">Terms of Use</a> | 
# MAGIC <a href="https://help.databricks.com/" target="blank">Support</a>