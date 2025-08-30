import gradio as gr
import os

def greet(name):
    return f"Hello {name}!"

iface = gr.Interface(fn=greet, inputs="text", outputs="text")
port = int(os.environ.get("PORT", 8080))
iface.launch(server_name="0.0.0.0", server_port=port)
