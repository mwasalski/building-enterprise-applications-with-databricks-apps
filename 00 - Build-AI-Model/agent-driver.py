# Databricks notebook source
# MAGIC %md
# MAGIC # Develop the AI Agent for the Labs
# MAGIC
# MAGIC This notebook creates an AI agent using customer data. The agent will be deployed via a Model Serving endpoint.
# MAGIC
# MAGIC **🚨 Warning**: Do not run this notebook manually. It will be executed during workspace creation on Vocareum, and all resources should be prepared for use.

# COMMAND ----------

# MAGIC %pip install -U databricks-sdk==0.41.0 langchain-community==0.2.16 databricks-agents langchain-openai==0.1.19 mlflow==2.20.2 
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

import os
from databricks.sdk import WorkspaceClient

# Define catalog and schema variables
catalog_name = "shared_catalog"
schema_name = f"ws_{WorkspaceClient().get_workspace_id()}"

# Create shared catalog and grant permissions
spark.sql(f"CREATE CATALOG IF NOT EXISTS `{catalog_name}`")
spark.sql(f"GRANT USE CATALOG ON CATALOG `{catalog_name}` TO `account users`")
spark.sql(f"GRANT USE_SCHEMA, USE_CATALOG, EXECUTE ON CATALOG `{catalog_name}` TO `account users`")
spark.sql(f"USE CATALOG `{catalog_name}`")

# Create workspace scoped schema and setup permissions
spark.sql(f"CREATE SCHEMA IF NOT EXISTS `{schema_name}`;")
spark.sql(f"USE SCHEMA `{schema_name}`")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Tools for Agent

# COMMAND ----------

# MAGIC %md
# MAGIC ### Allow your LLM to retrieve the franchises for a given city

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Now we create our first function. This takes in a city name and returns a table of any franchises that are in that city.
# MAGIC -- Note that we've added a comment to the input parameter to help guide the agent later on.
# MAGIC CREATE FUNCTION IF NOT EXISTS cookies_franchise_by_city (
# MAGIC     city_name STRING COMMENT 'City to be searched'
# MAGIC )
# MAGIC RETURNS TABLE (
# MAGIC     franchiseID BIGINT,
# MAGIC     name STRING,
# MAGIC     size STRING
# MAGIC )
# MAGIC LANGUAGE SQL
# MAGIC -- Make sure to add a comment so that your AI understands what it does
# MAGIC COMMENT 'This function takes in a city name and returns a table of any franchises that are in that city.'
# MAGIC RETURN (
# MAGIC     SELECT franchiseID, name, size
# MAGIC     FROM `cookies`.`sales`.`franchises`
# MAGIC     WHERE lower(city) = lower(city_name)
# MAGIC     ORDER BY size DESC
# MAGIC );
# MAGIC

# COMMAND ----------

spark.sql(f"GRANT EXECUTE ON FUNCTION `{catalog_name}`.`{schema_name}`.`cookies_franchise_by_city` TO `account users`;")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Sum all the sales for a given franchise, grouping the result per product

# COMMAND ----------

# MAGIC %sql
# MAGIC -- This function takes an ID as input, and this time does an aggregate to return the sales for that franchise_id.
# MAGIC CREATE FUNCTION IF NOT EXISTS cookies_franchise_sales (
# MAGIC     franchise_id BIGINT COMMENT 'ID of the franchise to be searched'
# MAGIC )
# MAGIC RETURNS TABLE (
# MAGIC     total_sales BIGINT,
# MAGIC     total_quantity BIGINT,
# MAGIC     product STRING
# MAGIC )
# MAGIC LANGUAGE SQL
# MAGIC COMMENT 'This function takes an ID as input, and this time does an aggregate to return the sales for that franchise_id'
# MAGIC RETURN (
# MAGIC     SELECT 
# MAGIC         SUM(totalPrice) AS total_sales, 
# MAGIC         SUM(quantity) AS total_quantity, 
# MAGIC         product 
# MAGIC     FROM `cookies`.`sales`.`transactions` 
# MAGIC     WHERE franchiseID = franchise_id 
# MAGIC     GROUP BY product
# MAGIC );
# MAGIC

# COMMAND ----------

spark.sql(f"GRANT EXECUTE ON FUNCTION `{catalog_name}`.`{schema_name}`.`cookies_franchise_sales` TO `account users`;")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Get the best feedbacks for a given franchise

# COMMAND ----------

# MAGIC %sql
# MAGIC -- This function takes an ID as input, and this time does an aggregate to return the sales for that franchise_id.
# MAGIC CREATE FUNCTION IF NOT EXISTS cookies_summarize_best_sellers_feedback (
# MAGIC     franchise_id BIGINT COMMENT 'ID of the franchise to be searched'
# MAGIC )
# MAGIC RETURNS STRING
# MAGIC LANGUAGE SQL
# MAGIC COMMENT 'This function will fetch the best feedback from a product and summarize them'
# MAGIC RETURN (
# MAGIC     SELECT 
# MAGIC         AI_GEN(
# MAGIC             SUBSTRING(
# MAGIC                 'Extract the top 3 reason people like the cookies based on this list of review:' || 
# MAGIC                 ARRAY_JOIN(COLLECT_LIST(review), ' - '), 
# MAGIC                 1, 
# MAGIC                 80000
# MAGIC             )
# MAGIC         ) AS all_reviews
# MAGIC     FROM 
# MAGIC         `cookies`.`media`.`customer_reviews`
# MAGIC     WHERE 
# MAGIC         franchiseID = franchise_id
# MAGIC );
# MAGIC

# COMMAND ----------

spark.sql(f"GRANT EXECUTE ON FUNCTION `{catalog_name}`.`{schema_name}`.`cookies_summarize_best_sellers_feedback` TO `account users`;")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Build Agent

# COMMAND ----------

with open("agent.py", "w") as fd:
    fd.write(f"""
# Imports
import mlflow
from operator import itemgetter
from databricks.sdk import WorkspaceClient
from langchain_community.tools.databricks import UCFunctionToolkit
from langchain_community.chat_models.databricks import ChatDatabricks
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.schema.runnable import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

def get_shared_warehouse(name=None):
    w = WorkspaceClient()
    warehouses = w.warehouses.list()

    # Check for warehouse by exact name (if provided)
    if name:
        for wh in warehouses:
            if wh.name == name:
                return wh

    # Define fallback priorities
    fallback_priorities = [
        lambda wh: wh.name.lower() == "serverless starter warehouse",
        lambda wh: wh.name.lower() == "shared endpoint",
        lambda wh: wh.name.lower() == "dbdemos-shared-endpoint",
        lambda wh: "shared" in wh.name.lower(),
        lambda wh: "dbdemos" in wh.name.lower(),
        lambda wh: wh.num_clusters > 0,
    ]

    # Try each fallback condition in order
    for condition in fallback_priorities:
        for wh in warehouses:
            if condition(wh):
                return wh

    # If non of above conditions are met, use the first one
    if(len(warehouses) > 0):
        return warehouses[0]

    # Raise an exception if no warehouse is found
    raise Exception(
        "Couldn't find any Warehouse to use. Please create one first or pass "
        "a specific name as a parameter to the get_shared_warehouse(name='xxx') function."
    )

# Initialize Warehouse
wh = get_shared_warehouse(name="shared_warehouse") 
print(f'This demo will be using the {{wh.name}} to execute the functions')

# Define Tools
def get_tools():
    return (
         UCFunctionToolkit(warehouse_id=wh.id)
        .include("{catalog_name}.{schema_name}.cookies_franchise_by_city", 
                 "{catalog_name}.{schema_name}.cookies_franchise_sales", 
                 "{catalog_name}.{schema_name}.cookies_summarize_best_sellers_feedback")
        .get_tools())

# Initialize LLM
llm = ChatDatabricks(
    endpoint="databricks-claude-3-7-sonnet",
    temperature=0.0,
    streaming=False
)

# Define Prompt
def get_prompt(history=[], prompt=None):
    if not prompt:
        prompt = \"\"\"You are a helpful assistant for a global company that oversees cookie stores. Your task is to help store owners understand more about their products and sales metrics. You have the ability to execute functions as follows: 

        Use the franchise_by_city function to retrieve the franchiseID for a given city name.

        Use the franchise_sales function to retrieve the cookie sales for a given franchiseID.

        Use the cookies_summarize_best_sellers_feedback function to understand what customers like the most.

        Make sure to call the function for each step and provide a coherent response to the user. Don't mention tools to your users. Don't skip to the next step without ensuring the function was called and a result was retrieved. Only answer what the user is asking for. If a user ask to generate instagram posts, make sure you know what customers like the most to make the post relevant.\"\"\"
    return ChatPromptTemplate.from_messages([
        ("system", prompt),
        ("human", "{{messages}}"),
        ("placeholder", "{{agent_scratchpad}}"),
    ])

# Create Agent
prompt = get_prompt()
tools = get_tools()
agent = create_openai_tools_agent(llm, tools, prompt)

# Create Agent Executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Create chain
chain = ({{ "messages": itemgetter("messages")}} | agent_executor | itemgetter("output") | StrOutputParser())

mlflow.models.set_model(chain)
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Register the Agent If Not Exists

# COMMAND ----------

import agent
import mlflow
from mlflow.tracking import MlflowClient
from mlflow.models.signature import infer_signature

mlflow.set_registry_uri("databricks-uc")
UC_MODEL_NAME = f"{catalog_name}.{schema_name}.cookie_sales_agent"

def register_new_agent():
    # Very basic chain that allows us to pass the input (messages) into the Agent and collect the (output) as a string
    input = {
        "messages": [
            {
                "role": "user",
                "content": "Help me write an instagram message for the customers of my Seattle store, we want to increase our sales for the top 1 cookie only."
            }
        ]
    }

    answer = agent.chain.invoke(input)
    print(answer)

    # Define an input example for signature inference
    input_example = {
        "messages": [
            {
                "role": "user",
                "content": "Which cookies are best sellers in New York?"
            }
        ]
    }

    signature = infer_signature(input_example, answer)

    # Log and register the model
    with mlflow.start_run():
        logged_model_info = mlflow.langchain.log_model(
            lc_model="agent.py",
            artifact_path="cookie_agent",
            registered_model_name=UC_MODEL_NAME,
            input_example=input_example,
            signature=signature,
            pip_requirements=[
                "databricks-sdk==0.41.0",
                "langchain-community==0.2.16",
                "databricks-agents",
                "langchain-openai==0.1.19",
                "mlflow==2.20.2"
            ]
        )

    print(f"Model registered as: {logged_model_info.model_uri}")


# Check if model already registered or not
client = MlflowClient()
models = [m.name for m in client.search_registered_models()]
model_exists = UC_MODEL_NAME in models

if model_exists:
    print("Model already exists. Skip registering the new model.")
else:
    print("Registering new model.")
    register_new_agent()

# COMMAND ----------

spark.sql(f"GRANT EXECUTE ON FUNCTION `{catalog_name}`.`{schema_name}`.`cookie_sales_agent` TO `account users`;")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Deploy the Agent

# COMMAND ----------

import time
import json
import requests
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import EndpointStateReady, EndpointStateConfigUpdate
from databricks import agents
from mlflow.deployments import get_deploy_client

# Initialize MLflow clients
mlflow_client = MlflowClient()
model_serving_client = get_deploy_client("databricks")

# Define the serving endpoint name
endpoint_name = "cookie_sales_agent_endpoint"

def deploy_agent():
    # Deploy the model using agent framework
    deployment_info = agents.deploy(
        model_name=UC_MODEL_NAME,
        model_version=1,            # always deploy the v1 of the model to prevent multiple models being deployed
        scale_to_zero=True,
        endpoint_name=endpoint_name,
        
    )

    # Wait for endpoint to become ready
    w = WorkspaceClient()
    print("\nWaiting for endpoint to deploy. This can take 15 - 20 minutes.", end="")

    while True:
        state = w.serving_endpoints.get(deployment_info.endpoint_name).state
        if state.ready == EndpointStateReady.READY and state.config_update == EndpointStateConfigUpdate.NOT_UPDATING:
            break
        print(".", end="", flush=True)
        time.sleep(30)

    print("\nThe endpoint is ready!")

def set_endpoint_permissions():
    # Get endpoint ID (Databricks REST API expects endpoint name, not ID here — fixed below)
    DATABRICKS_INSTANCE = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiUrl().get()
    TOKEN = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()

    # API endpoint for setting permissions (use name directly, not ID)
    endpoint_id = model_serving_client.get_endpoint(endpoint=endpoint_name).id
    url = f"{DATABRICKS_INSTANCE}/api/2.0/permissions/serving-endpoints/{endpoint_id}"

    # Define the permission payload
    payload = {
        "access_control_list": [
            {
                "group_name": "users",
                "permission_level": "CAN_QUERY"
            }
        ]
    }

    # Headers for the request
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    # Send PATCH request to update permissions
    response = requests.patch(url, headers=headers, data=json.dumps(payload))

    # Handle response
    if response.status_code == 200:
        print(f"✅ Permissions successfully updated on endpoint '{endpoint_name}'.")
    else:
        print(f"❌ Failed to update permissions. Status: {response.status_code}, Response: {response.text}")

    print("ℹ️ Model serving endpoint is being created. Please wait a few minutes for it to be ready.")

# COMMAND ----------

# existing_agents = agents.get_deployments(model_name=UC_MODEL_NAME, model_version=1) # BUG: Agents framework keeps the endpoint info even after deleting it
endpoint_exists = False
try:
    w.serving_endpoints.get(endpoint_name)
    endpoint_exists = True
except:
    pass

if endpoint_exists:
    print("Agent already deployed. Skipping agent deployment.")
else:
    deploy_agent()
    set_endpoint_permissions()