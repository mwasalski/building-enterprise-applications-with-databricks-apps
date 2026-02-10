import gradio as gr
import logging
from model_serving_utils import (
    endpoint_supports_feedback, 
    query_endpoint, 
    query_endpoint_stream, 
    _get_endpoint_task_type,
)
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure environment variable is set correctly
SERVING_ENDPOINT = os.getenv('SERVING_ENDPOINT')
assert SERVING_ENDPOINT,\
    ("Unable to determine serving endpoint to use for chatbot app. If developing locally, "
     "set the SERVING_ENDPOINT environment variable to the name of your serving endpoint. If "
     "deploying to a Databricks app, include a serving endpoint resource named "
     "'serving_endpoint' with CAN_QUERY permissions, as described in "
     "https://docs.databricks.com/aws/en/generative-ai/agent-framework/chat-app#deploy-the-databricks-app")

ENDPOINT_SUPPORTS_FEEDBACK = endpoint_supports_feedback(SERVING_ENDPOINT)

def query_llm(message, history):
    """
    Query the LLM with the given message and chat history.
    `message`: str - the latest user input.
    `history`: list of dicts - OpenAI-style messages.
    """
    if not message.strip():
        return "ERROR: The question should not be empty"

    # Convert from Gradio-style history to OpenAI-style messages
    message_history = []
    for user_msg, assistant_msg in history:
        message_history.append({"role": "user", "content": user_msg})
        message_history.append({"role": "assistant", "content": assistant_msg})

    # Add the latest user message
    message_history.append({"role": "user", "content": message})

    try:
        logger.info(f"Sending request to model endpoint: {SERVING_ENDPOINT}")
        messages, request_id = query_endpoint(
            endpoint_name=SERVING_ENDPOINT,
            messages=message_history,
            return_traces=ENDPOINT_SUPPORTS_FEEDBACK
        )
        return messages[-1]
    except Exception as e:
        logger.error(f"Error querying model: {str(e)}", exc_info=True)
        return f"Error: {str(e)}"

with gr.Blocks(
    title="BrixoCookies - Marketing Agent Dashboard",
    fill_height=True
) as demo:
    gr.Markdown("<center><h1>BrixoCookies - Marketing Agent Dashboard</h1></center>")
    with gr.Row(equal_height=True):
        with gr.Column():
            gr.ChatInterface(
                fn=query_llm,
                type="messages",
                title="Brixo Marketing Agent",
                description=(
                    "This agent helps you as a marketing agent."
                    "It can answer questions about our sales and stores."
                    "Also, you can ask the agent to generate custom marketing content based on sales and reviews."
                ),
                examples=[
                    "Write an Instagram message for the customers of my Seattle store.",
                    "Which cookies are best sellers in Seattle?",
                    "How many stores do we have in Seattle?"
                ]
            )

        with gr.Column(variant="panel"):
            gr.Markdown("### Sales Data")

if __name__ == "__main__":
    demo.launch()