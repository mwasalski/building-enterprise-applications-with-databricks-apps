import gradio as gr
import logging
import sys

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
    )
    logger.addHandler(handler)

def greet(name, intensity):
    logger.info(f"received inputs {name} and {intensity}")
    return "Hello, " + name + "!" * int(intensity)

gradio_app = gr.Interface(
    fn=greet,
    inputs=["text", "slider"],
    outputs=["text"],
)

if __name__ == '__main__':
    gradio_app.launch()
