
#Basic Gradio App

# src/app/gradio_app.py

## Shell code
# pip install -r requirements.txt
# python src/app/gradio_app.py


## Python code
import gradio as gr

def respond(message, history):
    history = history or []
    history.append((message, f"Echo: {message}"))
    return history

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""# AI Ancestor Interaction 
                
                Speak with your ancestor's AI Persona.
                """
                )

    chatbot = gr.Chatbot(height=500)

    msg = gr.Textbox(
        placeholder="Ask a question...",
        label="Message"
    )

    send = gr.Button("Send", scale=1)

    send.click(
        respond,
        [msg, chatbot],
        chatbot
    )

demo.launch(server_name="0.0.0.0",
    server_port=7860)