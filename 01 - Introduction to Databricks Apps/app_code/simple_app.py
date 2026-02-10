import gradio as gr

def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)

gradio_app = gr.Interface(
    fn=greet,
    inputs=["text", "slider"],
    outputs=["text"],
)

if __name__ == '__main__':
    gradio_app.launch()
