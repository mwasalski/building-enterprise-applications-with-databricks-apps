# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning">
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # Build a Data-Driven App

# COMMAND ----------

# MAGIC %md
# MAGIC ## Introduction
# MAGIC
# MAGIC In this example, we'll be using the Gradio framework to create a Databricks app that reads from a table. We'll create the app from the ground up rather than using any of the provided templates. Through this approach, you'll gain a full understanding of all the resources that go into building a Databricks app.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Prerequisites
# MAGIC
# MAGIC In this demo, you will reconfigure your existing app with changes to satisfy some new requirements. If you do not have an app created already, please follow the instructions in the [*01 - Build a Simple App* notebook]($../01 - Introduction to Databricks Apps/01 - Build a Simple App) first before proceeding.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup
# MAGIC
# MAGIC Before beginning, let's perform some preliminary setup. Since this notebook executes Python code, let's set up and configure serverless cluster. 
# MAGIC
# MAGIC 1. Configure the serverless environment.
# MAGIC    - Click the **Environment** icon to the right side of the notebook.
# MAGIC    - In the **Environment** panel that slides out, select **Environment version** *2*.
# MAGIC    - Click **Apply**.<br>
# MAGIC    ![Select serverless](../images/01 - Build a Simple App/serverless_version.png)
# MAGIC 1. Attach the notebook to a serverless cluster by clicking the compute menu at the top-right corner of the page, then select **Serverless**.<br>
# MAGIC ![Select serverless](../images/01 - Build a Simple App/select_serverless_compute.png)
# MAGIC 1. Once the cluster is connected, execute the following cell.

# COMMAND ----------

# MAGIC %run ../Includes/Classroom-Setup-02

# COMMAND ----------

# MAGIC %md
# MAGIC ## Reconfiguring the App
# MAGIC
# MAGIC In this section, we reconfigure the existing app, updating it so that it will be able to access a SQL warehouse to run queries on.
# MAGIC
# MAGIC 1. In the [Apps page](/compute/apps) (opens in a new tab), locate and select your app (the app named in the cell output from above).
# MAGIC 1. Click **Edit**.
# MAGIC 1. Click **Next** to advance to the resource configuration.
# MAGIC 1. Let's share access to a SQL warehouse for the app to execute SQL queries on.
# MAGIC    - Click **Add resource** and select **SQL warehouse**.
# MAGIC    - In the **SQL warehouse** dropdown, select *shared_warehouse* (this SQL warehouse is created automatically as part of the learning environment).
# MAGIC    - Leave **Permission** set to *Can use*.
# MAGIC    - Change **Resource key** to **sql_warehouse**.
# MAGIC 1. Click **Save**.
# MAGIC
# MAGIC Now that the app has access to a SQL warehouse, let's explore how to use it in the app code.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exploring the code
# MAGIC
# MAGIC Before deploying updated code, let's examine the files that make up a simple data-driven app. This app is a simple table viewer, which accepts the following input from the user:
# MAGIC
# MAGIC - Catalog
# MAGIC - Schema
# MAGIC - Relation name (table or view)
# MAGIC
# MAGIC In response it will display a sample of data from the specified table or view. It's a simple example, but it illustrates the basic mechanics of how to interact with any data object in the context of a Databricks app.
# MAGIC
# MAGIC Use the workspace navigator to locate the *app_code* folder, or use [this link]($./app_code) (opens in a new tab) to get there.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Source code
# MAGIC
# MAGIC Open the *data_app.py* file. The code is generously commented, but we'll walk through it now, section by section. We won't get into too much detail on how Gradio works, since this topic is covered in great detail by the [Gradio documentation](https://www.gradio.app/docs). But we'll provide a quick overview here.
# MAGIC ___
# MAGIC ```
# MAGIC from databricks.sdk import WorkspaceClient
# MAGIC from databricks.sdk.service.sql import StatementParameterListItem, StatementState
# MAGIC import gradio as gr
# MAGIC import logging
# MAGIC import os
# MAGIC import sys
# MAGIC from typing import Dict, List
# MAGIC ```
# MAGIC These lines import the various modules that we'll use through the code:
# MAGIC - Various objects from the Databricks SDK, primarily for interacting with the SQL warehouse
# MAGIC - core Gradio functionality, making it accessible through the shorter alias, `gr` (his is a widely adopted convention for better readability of code)
# MAGIC - logging for emitting messages from the app, to facilitate troubleshooting and gaining insight into app behaviour
# MAGIC - miscellaneous utility modules
# MAGIC ___
# MAGIC ```
# MAGIC assert os.getenv('DATABRICKS_WAREHOUSE_ID'), "DATABRICKS_WAREHOUSE_ID must be set in app.
# MAGIC ```
# MAGIC This line will trigger an immediate failure if a SQL warehouse is not configured. This configuration is effected through the app configuration (which we saw in the previous section) and a manifest in the  *app.yaml* file, which we will see shortly.
# MAGIC ___
# MAGIC ```
# MAGIC wclient = WorkspaceClient(auth_type='oauth-m2m')
# MAGIC ```
# MAGIC This establishes a connection to the workspace so that we can invoke SDK functionality (here, primarily for interacting with the SQL warehouse). The specified `auth_type` (*oauth-m2m*) will authenticate as the app service principal, using the values specified in the `DATABRICKS_CLIENT_ID`, `DATABRICKS_CLIENT_SECRET` and `DATABRICKS_HOST` environment variables. You can validate that these are set in the **Environment** configuration tab.
# MAGIC
# MAGIC For more details on authentication, or the SDK in general, please refer to the [Databricks documentation](https://docs.databricks.com/aws/en/dev-tools/sdk-python) and the [external SDK documentation](https://databricks-sdk-py.readthedocs.io/en/latest/).
# MAGIC ___
# MAGIC ```
# MAGIC def sql_query(
# MAGIC     query: str,
# MAGIC     catalog: str=None,
# MAGIC     schema: str=None,
# MAGIC     parameters: List[Dict]=None
# MAGIC ) -> Dict...
# MAGIC ```
# MAGIC The `sql_query()` helper function runs the specified query on the SQL warehouse through the SDK connection established on startup (`wclient`).
# MAGIC
# MAGIC NOTE: it's possible to execute SQL queries using the [Databricks SQL connector](https://docs.databricks.com/aws/en/dev-tools/python-sql-connector), which some of the templates and documentation examples do. That library provides slightly different functionality though, and the SDK fits this use case better.
# MAGIC ___
# MAGIC ```
# MAGIC def display_table(catalog, schema, table)...
# MAGIC ```
# MAGIC Gradio's **Interface** class is designed for mocking up demos quickly. It works by wrapping a user interface containing interactive input elements around a function that accepts one or more inputs, and returns one or more outputs. This basic pattern makes it useful for interactively exploring functional behaviour, such as the response of a machine learning model to various inputs.
# MAGIC
# MAGIC In this demo, the `display_table()` function returns a table (that is, a dictionary that references lists) providing header info as well as the data records. It takes three inputs that specify the catalog, schema, and name of the relation to read.
# MAGIC ___
# MAGIC ```
# MAGIC gradio_app = gr.Interface(
# MAGIC     fn=display_table,
# MAGIC     inputs=["text", "text", "text"],
# MAGIC     outputs=["dataframe"]
# MAGIC ```
# MAGIC Here, we instantiate an **Interface** object. We initialize the object with three parameters:
# MAGIC 1. Our previously defined function.
# MAGIC 1. A list of input components to create, which wil generate the input parameters to the function: three **text** components that will generate inputs to the function
# MAGIC 1. A list of output components to populate with the function output. In this case, a single dataframe component will display the tabular output returned by the function.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Configuration file
# MAGIC
# MAGIC Open the *app.yaml* file, which provides configuration information for deploying the app. Now let's walk through this simple file that currently only consists of one section.
# MAGIC ___
# MAGIC ```
# MAGIC command: [
# MAGIC   "python", 
# MAGIC   "data_app.py"
# MAGIC ]
# MAGIC ```
# MAGIC This line specifies the command to run the app. In this case, we're running *data_app.py* using the Python interpreter.
# MAGIC ___
# MAGIC ```
# MAGIC env:
# MAGIC   - name: "DATABRICKS_WAREHOUSE_ID"
# MAGIC     valueFrom: "sql_warehouse"
# MAGIC ```
# MAGIC This line establishes a variable named `DATABRICKS_WAREHOUSE_ID` in the app environment. The value for this variable is derived from the SQL warehouse resource we added when creating the app. This is the element that translates that setting into something the code can access.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Deploying and Using the App
# MAGIC
# MAGIC Once the resources are provisioned, we can deploy the app. In this context, "deploying the app" means capturing the source and starting the app.
# MAGIC
# MAGIC 1. Returning to the app page. Click the chevron to the right of the **Deploy** button, and select **Deploy using different source code path**.
# MAGIC 1. In the **Create deployment** dialog, specify the folder containing the app source:
# MAGIC    - Click the folder icon.
# MAGIC    - Click **All**.
# MAGIC    - Navigate to your home folder
# MAGIC    - From there, navigate to the *02 - Building and Deploying Data-Driven Applications/app_code* folder
# MAGIC    - Click **Select**
# MAGIC    - Finally, click **Deploy**
# MAGIC
# MAGIC The app takes a moment to deploy, and once complete, you can view and interact with the app.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Reading a Public Table
# MAGIC
# MAGIC Let's test the functionality of the app once it's deployed. Once complete, the status near the top of the page will switch to **Running**.
# MAGIC
# MAGIC 1. Use the link to the right to open your app in a separate tab.
# MAGIC 1. Enter the following values to read a publicly accessible table in the *samples* catalog:
# MAGIC    - **catalog**: *samples*
# MAGIC    - **schema**: *tpch*
# MAGIC    - **table**: *customer*
# MAGIC 1. Click **Submit**.
# MAGIC
# MAGIC A sample of the table data appears in the output.
# MAGIC ![](../images/02 - Building and Deploying Data-Driven Applications/data_app_displayed.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Reading a Private Table
# MAGIC
# MAGIC As part of the setup, a private table named *trips* has been created in your personal schema. Let's validate its existence by running the following query.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM trips LIMIT 10

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC Now let's try reading this table using the app.
# MAGIC
# MAGIC 1. Use the link to the right to open your app in a separate tab.
# MAGIC 1. Enter the following values to read a publicly accessible table in the *samples* catalog:
# MAGIC    - **catalog**: use the value displayed in the setup cell output above (typically *dbacademy*)
# MAGIC    - **schema**: use the value displayed in the setup cell output above 
# MAGIC    - **table**: *trips*
# MAGIC 1. Click **Submit**.
# MAGIC
# MAGIC ![](../images/02 - Building and Deploying Data-Driven Applications/data_app_failure.png)
# MAGIC
# MAGIC This time, the output is not displayed. Instead, we get a permission error. What went wrong?

# COMMAND ----------

# MAGIC %md
# MAGIC ### Understanding the Authorization Model
# MAGIC
# MAGIC When you create an app, Databricks automatically creates a service principal for the app. The service principal only has access to the workspace in which the app is created and is used to authenticate and authorize access to resources in the workspace. Such resources can include SQL warehouses or model serving endpoints, as well as data and AI object like tables and models. 
# MAGIC
# MAGIC The way the app code is currently written, it executes queries as the app service principal. This means that the app can only display tables to which that service principal has access. So the failure seen above is actually an issue related to data governance and the limitations imposed by this authorization model: the private table we attempted to access is only accessible by its owner; the app service principal cannot access it.
# MAGIC
# MAGIC How do we fix a problem like this? Generally speaking, there are two ways:
# MAGIC
# MAGIC 1. Architect your app and data access rules such that all required data objects are accessible by the app service principal
# MAGIC 1. Design your app to authenticate *as the user making the request* (rather than the app service principal)
# MAGIC
# MAGIC The second option is the choice generally recommended by Databricks, since it ensures that your app is not violating or circumventing any of your data access rules; no user will be able to access data through the app to which they would otherwise not be able to access.
# MAGIC
# MAGIC We will dive into this further in a separate demo.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC &copy; 2025 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="blank">Apache Software Foundation</a>.<br/>
# MAGIC <br/><a href="https://databricks.com/privacy-policy" target="blank">Privacy Policy</a> | 
# MAGIC <a href="https://databricks.com/terms-of-use" target="blank">Terms of Use</a> | 
# MAGIC <a href="https://help.databricks.com/" target="blank">Support</a>