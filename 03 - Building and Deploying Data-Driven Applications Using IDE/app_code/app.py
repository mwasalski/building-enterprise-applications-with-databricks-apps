from databricks.sdk import WorkspaceClient
from databricks.sdk.service.sql import StatementParameterListItem, StatementState
import gradio as gr
import logging
import os
import sys
from typing import Dict, List

# ensure environment variable is set correctly
assert os.getenv('DATABRICKS_WAREHOUSE_ID'), "DATABRICKS_WAREHOUSE_ID must be set in app.yaml."

# set up logging to stdout so output shows in Logs tab (stderr works too)
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
    )
    logger.addHandler(handler)

# initialize a connection to the workspace
try:
    # attempt to use app service principal credentials (works only in a Databricks App env,
    # where DATABRICKS_CLIENT_ID, DATABRICKS_CLIENT_SECRET and DATABRICKS_HOST are set)
    wclient = WorkspaceClient(auth_type='oauth-m2m')
except:
    # fall back to default PAT authentication (helps when developing locally)
    wclient = WorkspaceClient()

logger.info(f"logged in to {wclient.config.host} as {wclient.current_user.me().user_name}")

# general function to run SQL queries on a warehouse specified by DATABRICKS_WAREHOUSE_ID
# uses the statement execution API to safely handle catalog, schema, and query parameters
# returns dict with headers and data as per https://www.gradio.app/docs/gradio/dataframe
def sql_query(
    query: str,
    catalog: str=None,
    schema: str=None,
    parameters: List[Dict]=None
) -> Dict:

    logger.info(f"processing query {query}")

    response = wclient.statement_execution.execute_statement(
        statement=query,
        catalog=catalog,
        schema=schema,
        parameters=[
            StatementParameterListItem(
                name=p['key'],
                value=p['value']
            ) for p in parameters
        ] if parameters else None,
        warehouse_id=os.getenv('DATABRICKS_WAREHOUSE_ID'),
        wait_timeout='50s'
    )

    if response.status.state != StatementState.SUCCEEDED:
        # raise Gradio error if query did not succeed
        error_string = ' '. join(response.status.error.message.splitlines())
        logger.error(f"query failed: {error_string}")
        raise gr.Error(error_string, duration=10)
    else:
        logger.info(f"query returned {response.result.row_count} records")

        if response.result.row_count > 0:
            return {
                'headers': [ c.name for c in response.manifest.schema.columns],
                'data': response.result.data_array
            }

        return {
            'headers': [],
            'data': []
        }

# inputs: catalog, schema, table
# output: table (formatted like a dict as per https://www.gradio.app/docs/gradio/dataframe)
def display_table(catalog, schema, table):

    # use query parameter for table name. Parametrized queries are generally more reusable and
    # also less prone to injection attacks
    return sql_query(
        "SELECT * FROM IDENTIFIER(:table) LIMIT 10",
        catalog=catalog,
        schema=schema,
        parameters=[
            {
                'key': 'table',
                'value': table
            }
        ]
    )

gradio_app = gr.Interface(
    fn=display_table,
    inputs=["text", "text", "text"],
    outputs=["dataframe"]
)

if __name__ == '__main__':
    # use public app hosting for local dev
    gradio_app.launch(share=True)
