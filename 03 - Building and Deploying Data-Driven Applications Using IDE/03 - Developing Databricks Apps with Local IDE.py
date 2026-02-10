# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning">
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # Developing Databricks Apps with Local IDE

# COMMAND ----------

# MAGIC %md
# MAGIC ## Introduction
# MAGIC
# MAGIC In this example, we'll be using the building a simple data-driven app using the Gradio framework. This app was covered in the [Build a Data-Driven App demo]($../02 - Building and Deploying Data-Driven Applications/02 - Build a Data-Driven App), but in this demo we'll see how to set up development in a local IDE. The ability to connect an IDE to Databricks provides an alternate development experience that may be beneficial to some organizations.

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

# MAGIC %run ../Includes/Classroom-Setup-03

# COMMAND ----------

# MAGIC %md
# MAGIC ### Obtaining Workspace Credentials
# MAGIC
# MAGIC In order to connect to the workspace, we need a host address and a token. A token can be created from the workspace, although as a shortcut we have provided a method to display the host and token in text fields at the top of the notebook.
# MAGIC
# MAGIC 1. Run the following cell.
# MAGIC 2. Note the values displayed in the **host** and **token** fields, which will be needed in the next section.

# COMMAND ----------

DA.display_credentials()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Accessing the IDE
# MAGIC
# MAGIC In order to run through this demo, an IDE (integrated development environment) is needed. Popular examples include VSCode and PyCharm. Exact procedures for developing and deploying apps vary by IDE, but the general workflow is consistent across most platforms.
# MAGIC
# MAGIC In this demo, we provide a preconfigured VSCode environment, so the instructions provided will be specific to this environment. Let's access this now.
# MAGIC
# MAGIC If you have the **Databricks Workspace** menu (as shown below) in the top-left corner of the page:
# MAGIC
# MAGIC 1. Click the **Databricks Workspace** menu item to open it.
# MAGIC 1. Open the **VSCode** item in a new tab (right-click in most browser environments) so that you will have access to the workspace and the IDE simultaneously.<br>
# MAGIC ![](../images/03 - Building and Deploying Data-Driven Applications Using IDE/workspace_menu.png)
# MAGIC
# MAGIC If you do not see this menu item, please refer back to the system from which you launched this lab environment for a link to the VSCode environment, or consult with your facilitator.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Preparing the Development Environment
# MAGIC
# MAGIC Prior to developing and debugging an app, there are some preliminary steps involved in setting up the environment. While the procedures presented here are specific to VSCode (and in some cases the unique properties of this learning environment) most of the steps presented are generally applicable independent of the IDE you're using.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Setting Up a Workspace
# MAGIC
# MAGIC Let's set up a new VSCode workspace in the */voc/work* folder, since this allows for read-write access in the learning environment.
# MAGIC
# MAGIC 1. From the kebab menu in the top-left corner of the VSCode interface, select **File > Open Folder...**.<br>
# MAGIC ![](../images/03 - Building and Deploying Data-Driven Applications Using IDE/open_folder.png)
# MAGIC 1. In the **Open Folder** dialog, navigate to the */voc/work* folder and click **OK**.<br>
# MAGIC ![](../images/03 - Building and Deploying Data-Driven Applications Using IDE/navigate_voc_work.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Creating a Virtual Environment
# MAGIC
# MAGIC A Python *venv* (virtual environment) is a self-contained folder that houses its own Python interpreter, as well as a separate set of installed packages. The venv decouples your development environment from your host system and other projects.
# MAGIC
# MAGIC 1. From the kebab menu, select **View > Command Palette...**.<br>
# MAGIC ![](../images/03 - Building and Deploying Data-Driven Applications Using IDE/open_command_palette.png)
# MAGIC 1. In the text field, type *python* to narrow the tool search, then select **Python Create Environment...**<br>
# MAGIC ![](../images/03 - Building and Deploying Data-Driven Applications Using IDE/python_create_environment.png)
# MAGIC 1. Choose the **Venv** option.<br>
# MAGIC ![](../images/03 - Building and Deploying Data-Driven Applications Using IDE/python_create_venv.png)
# MAGIC 1. Select the Python version to use as a base. Since Databricks apps require Python version 3.11 or above, let's chose 3.12 in this case. Note that this will take a moment to complete.<br>
# MAGIC ![](../images/03 - Building and Deploying Data-Driven Applications Using IDE/python_select_version.png)
# MAGIC 1. Now let's add some packages our app will need to the venv, using the `pip` package manager from the command-line. From the kebab menu, select **Terminal > New Terminal**.<br>
# MAGIC ![](../images/03 - Building and Deploying Data-Driven Applications Using IDE/new_terminal.png)
# MAGIC 1. In the terminal, run the following command to install the packages:
# MAGIC    ```
# MAGIC    pip install databricks-sdk gradio
# MAGIC    ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### Installing the Databricks CLI
# MAGIC
# MAGIC Let's install a recent version of the Databricks CLI. Follow these steps in the VSCode termina.
# MAGIC
# MAGIC 1. Ensure any previous version of the Databricks CLI is removed by running the following command:
# MAGIC    ```
# MAGIC    sudo rm -f /usr/local/bin/databricks
# MAGIC    ```
# MAGIC 1. Run the following command to install a recent version of the Databricks CLI: 
# MAGIC    ```
# MAGIC    curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/refs/tags/v0.252.0/install.sh | sudo sh
# MAGIC    ```
# MAGIC    Note: for stability in the training environment, we're specifying a specific version to install. In your own environment, you can install the latest stable version by replacing the URL above with *https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh*.
# MAGIC 1. Validate the install by running the following command:
# MAGIC    ```
# MAGIC    databricks -v
# MAGIC    ```
# MAGIC    The output should correspond the version we installed; that is, *Databricks CLI v0.252.0*.

# COMMAND ----------

# MAGIC %md
# MAGIC #### Configuring CLI Authentication
# MAGIC
# MAGIC 1. Issue the following command to configure the Databricks CLI:
# MAGIC    ```
# MAGIC    databricks configure
# MAGIC    ```
# MAGIC    - When prompted for a **Databricks host**, copy and paste the value from **host** field at the top of this notebook (note, if using a Mac, use **COMMAND+SHIFT+V**).
# MAGIC    - When prompted for a **Personal access token**, copy the value from the **token** field of this notebook.
# MAGIC 1. Test CLI connectivity with the following command:
# MAGIC    ```
# MAGIC    databricks workspace list /
# MAGIC    ```
# MAGIC
# MAGIC Assuming this command succeeded, we have established a development environment outside the Databricks workspace, with a connection to the target workspace.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Developing the App
# MAGIC
# MAGIC In this section, we'll set up the code and other support files to develop our app in the IDE.
# MAGIC
# MAGIC The app structure will look like this:
# MAGIC
# MAGIC ```
# MAGIC work/
# MAGIC ├── app/
# MAGIC │   ├── app.py
# MAGIC │   └── app.yaml
# MAGIC └── app.json
# MAGIC ```
# MAGIC Where:
# MAGIC - *app/* is a project folder containing the files needed to run and deploy the app
# MAGIC - *app.py* contains the app source
# MAGIC - *app.yaml* contains metadata that describes how to deploy the app
# MAGIC - *app.json*, outside the project folder, will be used as input to the Databricks CLI when creating the Databricks App

# COMMAND ----------

# MAGIC %md
# MAGIC ### Creating the Structure
# MAGIC
# MAGIC Let's create a basic structure for our app, consisting of a project folder and some files that will contribute to app functionality.
# MAGIC
# MAGIC 1. Notice the **New File** and **New Folder** buttons that appear in the **Explorer** view when it is selected. If a folder is already selected, these also allow you to nest new folders and files. Without any existing folders selected, click the **New File** button to create a new file named *app.json*.<br>
# MAGIC    ![](../images/03 - Building and Deploying Data-Driven Applications Using IDE/create_files_folders.png)
# MAGIC 1. Use the **New Folder** button to create a new folder named *app*.
# MAGIC 1. With the new folder selected, create new files for the app source and metadata: *app.py* and *app.yaml*.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Populating the Files
# MAGIC
# MAGIC Now, let's populate the files we created in the previous section with contents, briefly exploring them as we go.

# COMMAND ----------

# MAGIC %md
# MAGIC #### App Source Code
# MAGIC
# MAGIC Let's populate *app.py*. This simple example will be implemented in this single source file, although more complicated projects will likely span multiple files and potentially even be divided into folders and modules.
# MAGIC
# MAGIC The source code implements the same data-driven application that we covered in [Build a Data-Driven App demo]($../02 - Building and Deploying Data-Driven Applications/02 - Build a Data-Driven App), so please refer to that demo for a more thorough explanation of the source.
# MAGIC
# MAGIC Follow this link to [app.py]($./app_code/app.py) (opens in a new tab). Copy the contents and paste them into the *app.py* file in your IDE project.

# COMMAND ----------

# MAGIC %md
# MAGIC #### App Metadata
# MAGIC
# MAGIC The *app.yaml* file provides metadata describing how to deploy the app. The key elements of this file describe how to run the app, and also how to map a SQL warehouse resource into the app environment. Again, please refer to [Build a Data-Driven App demo]($../02 - Building and Deploying Data-Driven Applications/02 - Build a Data-Driven App) for more details.
# MAGIC
# MAGIC Follow this link to [app.yaml]($./app_code/app.yaml) (opens in a new tab). Copy the contents and paste them into the *app.yaml* file in your IDE project.

# COMMAND ----------

# MAGIC %md
# MAGIC #### CLI Metadata
# MAGIC
# MAGIC Finally, let's populate *app.json*. This file isn't actually a real part of the app. This file just simplifies the process of creating a Databricks App through the Databricks CLI, by specifying advanced parameters in the JSON file format. Specifically, this provides additional parameters describing a SQL warehouse resource.
# MAGIC
# MAGIC Follow this link to [app.json]($./app_code/app.json) (opens in a new tab). Copy the contents and paste them into the *app.json* file in your IDE project. But, the file needs the following modifications before going any further:
# MAGIC
# MAGIC 1. Replace `<app-name>` with the app name from the setup cell output from earlier.
# MAGIC 1. Replace `<warehouse-id>` with the ID of your SQL warehouse. To obtain this information:
# MAGIC    - Go to the [SQL warehouses page](/compute/sql-warehouses) (opens in a new tab).
# MAGIC    - Select the *shared_warehouse* entry.
# MAGIC    - Copy the ID string (to the right of the name).<br>
# MAGIC    ![](../images/03 - Building and Deploying Data-Driven Applications Using IDE/shared_warehouse.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Locally Running and Debugging the App
# MAGIC
# MAGIC With all the pieces in place, let's prepare to run and debug the app locally; that is, on the same compute host as the IDE.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Creating a Debug Configuration
# MAGIC
# MAGIC VSCode collects the information needed to launch a program for running or debugging in a JSON file. Let's set one up now to launch our Python web app in the debugger.
# MAGIC
# MAGIC 1. From the kebab menu, **Run > Add Configuration...**<br>
# MAGIC    ![](../images/03 - Building and Deploying Data-Driven Applications Using IDE/new_launch.png)
# MAGIC 1. Choose **Python Debugger**.<br>
# MAGIC    ![](../images/03 - Building and Deploying Data-Driven Applications Using IDE/python_debugger.png)
# MAGIC 1. From the sub-options presented, choose **Debug the currently active Python file**.<br>
# MAGIC    ![](../images/03 - Building and Deploying Data-Driven Applications Using IDE/python_current_file.png)
# MAGIC 1. A file called *launch.json* is generated in response, although we'll need to configure the environment variable `DATABRICKS_WAREHOUSE_ID`, which the app is expecting to be set.
# MAGIC    - Add the following element to the inner block of the configuration:
# MAGIC      ```
# MAGIC      "env": {
# MAGIC        "DATABRICKS_WAREHOUSE_ID": "<warehouse-id>"
# MAGIC       }
# MAGIC       ```
# MAGIC    - Replace `<warehouse-id>` with the actual ID of the shared warehouse (this was the same value you transferred to the *app.json* file earlier).
# MAGIC 1. In launch.json, update the field ``` "program":"${workspaceFolder}/app/app.py" ``` to specify the path to your app.py file.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Debugging the App
# MAGIC
# MAGIC With the *app.py* file tab selected, let's launch the app in the debugger.
# MAGIC
# MAGIC 1. Before launching, plant a breakpoint in the first line of the display function by clicking in the trough. This code is executed when the user submits input.<br>
# MAGIC    ![](../images/03 - Building and Deploying Data-Driven Applications Using IDE/add_breakpoint.png)
# MAGIC 1. Launch the app. From the kebab menu, select **Run > Start Debugging**.<br>
# MAGIC    ![](../images/03 - Building and Deploying Data-Driven Applications Using IDE/start_debugging.png)
# MAGIC 1. Note the terminal output, which will resemble the following:
# MAGIC    ```
# MAGIC    [2025-05-27 03:50:20,210] [app] [INFO] logged in to https://dbc-[REDACTED].cloud.databricks.com as [REDACTED]
# MAGIC    * Running on local URL:  http://127.0.0.1:7860
# MAGIC    * Running on public URL: https://[REDACTED].gradio.live
# MAGIC    ```
# MAGIC    Due to firewall restrictions in the learning environment, using the local URL will not work. But leveraging Gradio's app sharing capability, we can use the public URL provided. Copy the public URL into a new tab.
# MAGIC 1. Enter the following values into the app fields. When done, click **Submit**.
# MAGIC    - **catalog**: *samples*
# MAGIC    - **schema**: *tpch*
# MAGIC    - **table**: *customer*
# MAGIC 1. The app will stop on the breakpoint, allowing you to fully inspect the execution context.
# MAGIC
# MAGIC When done, feel free to terminate the running app and close the tab in preparation for the next section.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Creating a Databricks App
# MAGIC
# MAGIC In order to deliver app code to Databricks, we will need to create a Databricks App in the target workspace. In this section, we'll remotely provision a Databricks App using the Databricks CLI in the IDE terminal.
# MAGIC
# MAGIC 1. Run the following command in the command-line terminal to create a Databricks App. Because we're configuring more advanced options (the SQL warehouse resource) we're leveraging the `--json` option to supply parameter input from the *app.json* file we created earlier.
# MAGIC    ```
# MAGIC    databricks apps create  --json @app.json
# MAGIC    
# MAGIC    ```
# MAGIC 1. The command will wait til the App is provisioned. This will take a few minutes. Ultimately, output will be displayed that includes the app URL. Copy this value and visit it in a new tab.
# MAGIC
# MAGIC Notice that nothing will be displayed yet when visiting the app URL, since the app has not been deployed yet.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Synchronizing the App Code
# MAGIC
# MAGIC In this section, we'll set up synchronization between the IDE source and a provisioned Databricks App via the CLI.
# MAGIC
# MAGIC 1. Visit the [Apps page](/compute/apps) (opens in a new tab). Identify your App and select it.
# MAGIC 1. In the **Overview** tab, locate the section entitled **Edit in your IDE**. Locate the field containing the sync command.<br>
# MAGIC    ![](../images/03 - Building and Deploying Data-Driven Applications Using IDE/sync_files.png)
# MAGIC 1. In the command-line terminal of the IDE, execute the following command to change into your app folder:
# MAGIC    ```
# MAGIC    cd app
# MAGIC    ```
# MAGIC 1. Copy the command from the earlier step, adding the parameter `--exclude app.json` to the end before running it. This syncs all the files in the current folder to the app directory in the Databricks workspace (except for the *app.json* file, which is not needed there). Once the initial file transfer completes, the command will continue to run indefinitely, monitoring and uploading changes as they occur.
# MAGIC 1. Because the terminal will be occupied by the sync command, let's open a new working terminal view like we did previously before continuing into the next section.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Deploying the App Code
# MAGIC
# MAGIC Whenever you want to test the app code, you'll need to deploy it, which transfers a snapshot of the app code in the workspace to the app server and restarts the app. Let's do that in this section.
# MAGIC
# MAGIC 1. Back in the **Overview** tab for your App, further down in the **Edit in your IDE** section, locate the deploy command.<br>
# MAGIC    ![](../images/03 - Building and Deploying Data-Driven Applications Using IDE/deploy_app.png)
# MAGIC 1. Copy the command from the previous step into the new command-line terminal in the IDE, and run it.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Testing the App
# MAGIC
# MAGIC Let's test the functionality of the app now that it's deployed. Back the the app tab you opened previously, reload the page content. If you closed the tab, you can get the URL again from the first terminal view in the IDE, or from your app's **Overview** tab in the workspace.
# MAGIC
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
# MAGIC ## Deploying Changes
# MAGIC
# MAGIC Like any software, app development is an iterative process that will require updates as you make changes. To illustrate the process, let's make a superficial change to *app.py*, deploy, and test it.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Modifying the Source
# MAGIC
# MAGIC In the *app.py* file in the IDE, locate the section of code that declares the `Interface`. Add a line specifying a title for the app. When done, this code should read as follows:
# MAGIC ```
# MAGIC gradio_app = gr.Interface(
# MAGIC     fn=display_table,
# MAGIC     inputs=["text", "text", "text"],
# MAGIC     outputs=["dataframe"],
# MAGIC     title="My Test App"
# MAGIC )
# MAGIC ```
# MAGIC By virtue of the `databricks sync` command that runs continuously, the changes will be automatically uploaded to the workspace as you make them (the output from the first terminal view reflects this).

# COMMAND ----------

# MAGIC %md
# MAGIC ### Deploying the Updated Source
# MAGIC
# MAGIC Once the changes are complete, re-run the deploy command from earlier in the second terminal view. Once it completes, reload the app to test the changes.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC &copy; 2025 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="blank">Apache Software Foundation</a>.<br/>
# MAGIC <br/><a href="https://databricks.com/privacy-policy" target="blank">Privacy Policy</a> | 
# MAGIC <a href="https://databricks.com/terms-of-use" target="blank">Terms of Use</a> | 
# MAGIC <a href="https://help.databricks.com/" target="blank">Support</a>