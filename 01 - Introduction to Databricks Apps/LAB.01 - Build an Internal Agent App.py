# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning">
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # LAB - Build an Internal Agent App with Databricks Apps

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Lab Scenario
# MAGIC
# MAGIC In this **lab series**, you will take on the role of a Generative AI Engineer responsible for **building an internal application for a network of cookie stores**. The purpose of the app is to help marketing teams quickly **generate personalized promotional content by leveraging customer reviews and purchase data**.
# MAGIC
# MAGIC The first lab focuses on **building a chatbot interface that exposes a Large Language Model (LLM) to end-users**, laying the foundation for intelligent, context-aware content generation.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Requirements
# MAGIC
# MAGIC Please review the following requirements before starting the lesson:
# MAGIC
# MAGIC * To run lab notebooks, you need to use the **`Serverless`**, which is enabled by default.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ##Lab Tasks
# MAGIC
# MAGIC * Create a **Chatbot app** using existing template.
# MAGIC * Update the code to customize the app.
# MAGIC * Deploy and test the app.
# MAGIC
# MAGIC **📌 Note:** This lab is just a first step and you will develop it as progressing to the next labs. Following labs will be based on this lab. Thus, you will need to complete this lab before moving to next labs.

# COMMAND ----------

# MAGIC %run ../Includes/Lab-Setup-01

# COMMAND ----------

# MAGIC %md
# MAGIC ###Task 1: Create a Gradio App
# MAGIC
# MAGIC Build the core of your chat application. Create a Databricks app that has the following properties:
# MAGIC
# MAGIC - Use a custom app based on the source template shown above, in the **App code template** output. This prototype will simulate how employees will interact with your internal data agent in future iterations.
# MAGIC - Add a **serving endpoint** resource serving the `databricks-claude-3-7-sonnet` LLMagent.
# MAGIC - Specify an app name as shown above.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 2: Update the Code
# MAGIC
# MAGIC Update the application code as follows:
# MAGIC
# MAGIC - Update the template's layout as shown in this diagram.
# MAGIC - Update Chatbot's example questions.
# MAGIC - Ensure the YAML configuration metches the resource key
# MAGIC - View the code and log messages when the app starts and queries the LLM.
# MAGIC
# MAGIC ![App Layout](../images/Labs/db-apps-lab-outline-1.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 3: Deploy and Test the Application
# MAGIC
# MAGIC Deploy your newly created app and validate its functionality by launching the interface directly in your browser. This is your chance to see the employee-facing application in action and confirm that it integrates well within the Databricks environment.
# MAGIC
# MAGIC Some of the questions you can ask to the agent;
# MAGIC - Generate an Instagram ad message for our Seattle store.
# MAGIC - How many stores do we have in Seattle?
# MAGIC
# MAGIC 💡 What do you think about the responses? Ok! We will improve it in the following labs.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 4: View Deployment Details
# MAGIC
# MAGIC Review the details of the deployed app. Check the following settings;
# MAGIC - What service principal is used? 
# MAGIC - Which libraries are installed?
# MAGIC - Are there any errors when deploying the app? Do you see your logs for the app?
# MAGIC
# MAGIC **🚨 Important**: Don't delete the app! You will need it in the next lab.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC &copy; 2025 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="blank">Apache Software Foundation</a>.<br/>
# MAGIC <br/><a href="https://databricks.com/privacy-policy" target="blank">Privacy Policy</a> | 
# MAGIC <a href="https://databricks.com/terms-of-use" target="blank">Terms of Use</a> | 
# MAGIC <a href="https://help.databricks.com/" target="blank">Support</a>