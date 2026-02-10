# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning">
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # Build a Simple App

# COMMAND ----------

# MAGIC %md
# MAGIC ## Introduction
# MAGIC
# MAGIC Databricks Apps is a framework that allows developers to create, deploy, and share secure data and AI applications directly within a Databricks workspace. This feature simplifies app development by integrating Databricks services and capabilities, enabling developers to focus application functionality rather than infrastructure.
# MAGIC
# MAGIC This demo will walk through the process of setting up a new Databricks app. The code implements a simple interactive user interface, and is based on an example provided in the [Gradio Quickstart](https://www.gradio.app/guides/quickstart).
# MAGIC
# MAGIC Databricks provides several starter templates to help get you started in a variety of Python-based web application frameworks, including:
# MAGIC - **Dash:** well suited for data visualization dashboards
# MAGIC - **Flask:** minimal and highly extensible framework for a variety of use cases
# MAGIC - **Gradio:** well suited for machine learning model interaction
# MAGIC - **Shiny:** popular frame work with a strong R-based heritage
# MAGIC - **Streamlit:** minimal code required to turn Python scripts into slick apps
# MAGIC
# MAGIC In this example, we'll be using the Gradio framework, but we'll create the app from the ground up rather than using any of the provided templates. Through this approach, you'll gain a full understanding of all the resources that go into building a Databricks app.

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

# MAGIC %run ../Includes/Classroom-Setup-01

# COMMAND ----------

# MAGIC %md
# MAGIC ## Creating an App
# MAGIC
# MAGIC In this section, we will create a new, blank app that we will populate with code. Databricks provides templates to get you started in a variety of web application frameworks, but for this example we will start from scratch.
# MAGIC
# MAGIC 1. Follow [this link](/apps/create) (opens in a new tab) to create a new app. Alternatively, select the **New > App** from the left sidebar.
# MAGIC 1. We'll be using Gradio for this example, but we will populate the app with our own code rather than starting with a template. So:
# MAGIC    - Select **Create a custom app**.
# MAGIC    - Click **Next**.
# MAGIC 1. Specify the app name, using the value from the setup cell output above.
# MAGIC 1. Click **Create app**.
# MAGIC
# MAGIC This will provision the resources required to support the app:
# MAGIC * A service principal, which represents the identity under which the app runs
# MAGIC * Compute resources that actually service requests and execute your app code
# MAGIC
# MAGIC This provisioning process will take a few minutes. We can deploy the app source code once the provisioning process is complete, but in the meantime let's familiarize ourselves with the app code and structure.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exploring the code
# MAGIC
# MAGIC Before deploying the code for the web app, let's examine the files that make up a typical web app. Use the workspace navigator to locate the *app_code* folder, or use [this link]($./app_code) (opens in a new tab) to get there.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Source code
# MAGIC
# MAGIC Open the *simple_app.py* file. Now let's walk through the code, section by section. We won't get into too much detail on how Gradio works, since this topic is covered in great detail by the [Gradio documentation](https://www.gradio.app/docs). But we'll provide a quick overview here.
# MAGIC ___
# MAGIC ```
# MAGIC import gradio as gr
# MAGIC ```
# MAGIC This line imports the core Gradio functionality, making it accessible through the shorter alias, `gr`. This is a widely adopted convention for better readability of code.
# MAGIC ___
# MAGIC ```
# MAGIC def greet(name, intensity):
# MAGIC     return "Hello, " + name + "!" * int(intensity)
# MAGIC ```
# MAGIC Gradio's **Interface** class is designed for mocking up demos quickly. It works by wrapping a user interface containing interactive input elements around a function that accepts one or more inputs, and returns one or more outputs. This basic pattern makes it useful for interactively exploring functional behaviour, such as the response of a machine learning model to various inputs.
# MAGIC
# MAGIC In this simple demo, the `greet()` function returns a single string output based on two inputs, `name` and `intensity`.
# MAGIC ___
# MAGIC ```
# MAGIC gradio_app = gr.Interface(
# MAGIC     fn=greet,
# MAGIC     inputs=["text", "slider"],
# MAGIC     outputs=["text"],
# MAGIC )
# MAGIC ```
# MAGIC Here, we instantiate an **Interface** object. We initialize the object with three parameters:
# MAGIC 1. Our previously defined function.
# MAGIC 1. A list of input components to create, which will generate the input parameters to the function:
# MAGIC    * **text** will establish an interactive Gradio text component that will generate string input to the function
# MAGIC    * **slider** will establish a slider component that will generate numeric input to the function
# MAGIC 1. A list of output components to populate with the function output. In this case, a single text component will display the string returned by the function.
# MAGIC ___
# MAGIC ```
# MAGIC if __name__ == '__main__':
# MAGIC     gradio_app.launch()
# MAGIC ```
# MAGIC
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
# MAGIC   "simple_app.py"
# MAGIC ]
# MAGIC ```
# MAGIC This line specifies the command to run the app. In this case, we're running *simple_app.py* using the Python interpreter.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Deploying the App
# MAGIC
# MAGIC Once the resources are provisioned, we can deploy the app. In this context, "deploying the app" means capturing the source and starting the app.
# MAGIC
# MAGIC 1. Returning to the page from which you created the app earlier, click **Deploy**.
# MAGIC 1. Use the navigator dialog to specify the folder containing the app source:
# MAGIC    - Navigate to your home folder
# MAGIC    - From there, navigate to the *01 - Introduction to Databricks Apps/app_code* folder
# MAGIC    - Click **Select**
# MAGIC    - Finally, click **Deploy**
# MAGIC
# MAGIC The app takes a few moments to deploy. Once deployment is complete, you can view and interact with the app.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Testing the app
# MAGIC
# MAGIC Once the app deploys, the status near the top of the page will switch to **Running**. Use the link to the right to open your app in a separate tab.<br>
# MAGIC ![](../images/01 - Build a Simple App/simple_app_displayed.png)
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Additional Tools
# MAGIC
# MAGIC In developing your app, there are a few additional useful features provided. Let's explore these one by one:
# MAGIC - The **Authorization** tab provides documentation on the various credentials for interacting with Databricks services, either as the app itself or as the user using the app. We'll get into these distinctions in more detail in a separate demo.
# MAGIC - The **Deployments** tab maintains a history of the app deployment events.
# MAGIC - The **Logs** tab captures log output from the deployment process and the application code.
# MAGIC - The **Environment** tab captures information about the app execution environment, including environment variables and packages.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Logging from Application Code
# MAGIC
# MAGIC Instrumenting code with log messages can be extremely useful for the optimization and debugging of any piece of software. In the context of a Databricks app, you can configure logging to go to a file or some other persistent storage, although you might wish to have the ability to view log messages directly from the Databricks UI. In order for this to happen, you'll need to ensure that the log messages are emitted to `stdout` or `stderr`.
# MAGIC
# MAGIC In this section, we'll explore a simple approach to logging messages using Python's inbuilt `logging` facility. The principles shown here apply to any Python code, regardless of the web app framework you choose.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Exploring the Changes
# MAGIC
# MAGIC Open the [*simple_app_logging.py*]($./app_code/simple_app_logging.py) file, found in the same folder as the app code we've been exploring so far. This file contains the same app code, with a few additional lines to configure logging.
# MAGIC
# MAGIC Let's walk through the changes to gain an understanding of how to implement logging in app code.
# MAGIC ___
# MAGIC ```
# MAGIC import logging
# MAGIC import sys
# MAGIC ```
# MAGIC This line imports the Python **logging** and **sys** modules.
# MAGIC ___
# MAGIC ```
# MAGIC logger = logging.getLogger("app")
# MAGIC logger.setLevel(logging.INFO)
# MAGIC
# MAGIC if not logger.handlers:
# MAGIC     handler = logging.StreamHandler(sys.stdout)
# MAGIC     handler.setFormatter(
# MAGIC         logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
# MAGIC     )
# MAGIC     logger.addHandler(handler)
# MAGIC ```
# MAGIC This code block configures a logger object (named *app*) to log to `stdout`. Feel free to adjust the name or logging level as needed.
# MAGIC ```
# MAGIC def greet(name, intensity):
# MAGIC     logger.info(f"received inputs {name} and {intensity}")
# MAGIC     return "Hello, " + name + "!" * int(intensity)
# MAGIC ```
# MAGIC The addition of `logger.info()` to the function body emits an informational message that captures the function inputs. When logging, you can use different functions depending on the severity of the what is is that you're logging. Here are some general guidelines:
# MAGIC - `debug()` diagnostic details useful during development (typically disabled for production)
# MAGIC - `info()` general events useful for confirming that things are working as expected
# MAGIC - `warning()` unexpected but noncritical situations that could become serious issues
# MAGIC - `error()` serious problems that caused part of the program to fail
# MAGIC - `critical()` severe errors signaling the program itself may not continue running
# MAGIC - `exception()` logs an error and includes a traceback; useful inside an `except` block

# COMMAND ----------

# MAGIC %md
# MAGIC ### Updating and Re-deploying the App
# MAGIC
# MAGIC Let's update the app to incorporate logging and observe the changes.
# MAGIC
# MAGIC 1. Open the [*app.yaml*]($./app_code/app.yaml) file. In the `command` block, replace *simple_app.py* with *simple_app_logging.py*.
# MAGIC 1. Return to the page from which you created the app earlier, and click **Deploy** to re-deploy the changes.
# MAGIC 1. Use the link in the **Overview** tab to open the app, if it isn't open already, and submit some input.
# MAGIC 1. Notice the log output in the **Logs** tab.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC &copy; 2025 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="blank">Apache Software Foundation</a>.<br/>
# MAGIC <br/><a href="https://databricks.com/privacy-policy" target="blank">Privacy Policy</a> | 
# MAGIC <a href="https://databricks.com/terms-of-use" target="blank">Terms of Use</a> | 
# MAGIC <a href="https://help.databricks.com/" target="blank">Support</a>