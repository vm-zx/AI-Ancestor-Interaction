
#Basic Gradio App

# src/app/gradio_app.py

## Shell code to run the web app
# pip install -r requirements.txt
# python src/app/gradio_app.py
# python -m src.app.gradio_app.py  #run as a module

## Python code
import gradio as gr

# Import the RAG+LLM chatbot module
from src.rag.chatbot import generate_response

# Chat behaviour
def respond(message, history):
    history = history or []
    response = generate_response(message)
    history.append({"role": "user",
        "content": message})
    history.append({"role": "assistant",
        "content": response})
    return history, ""

# TTS AND STT Placeholders
def process_voice(audio):
    print("Voice input received.")
    return None

# Session Control Functions
def pause_session():
    return "⏸ Session Paused"

def help_session():
    return """
        Help

        1. Ask questions about memories.
        2. Use voice or text.
        3. View memory sources.
        4. End your visit when finished.
        """

def end_visit():
    return """
        Thank you for visiting.

        This interaction was generated from
        recorded memories and family history.

        We hope you learned something meaningful
        about this person's life.
        """
def logout_user():

    return (
        "✅ You have been logged out successfully.",

        gr.update(visible=False),  # home_group
        gr.update(visible=False),  # conversation_group
        gr.update(visible=False),  # avatar_group
        gr.update(visible=False),  # settings_group
        gr.update(visible=False),  # end_group

        gr.update(visible=True),   # home_status
        gr.update(visible=True),   # conversation_status
        gr.update(visible=True),   # avatar_status
        gr.update(visible=True),   # settings_status
        gr.update(visible=True),   # end_status

        "",                        # name
        None,                      # relationship
        "",                        # access_code
        False,                     # consent

        gr.update(selected="access")
        )

# New User Access Permission Page
VALID_ACCESS_CODE = "ANCESTOR2025"

def verify_access(name, relationship, access_code, consent):
    # Check consent
    if not consent:
        return (
            "❌ Please accept the consent form.",
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(visible=True),
            gr.update(visible=True),
            gr.update(visible=True),
            gr.update(visible=True),
            gr.Tabs(selected="access")
        )
    # Check access code
    if access_code != VALID_ACCESS_CODE:
        return (
            "❌ Access denied. Invalid access code.",
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(visible=True),
            gr.update(visible=True),
            gr.update(visible=True),
            gr.update(visible=True),
            gr.Tabs(selected="access")
        )

    return (f"""
        ✅ Access Approved

        Welcome {name} !

        Relationship: {relationship}

        Permission Level: Family Access

        You may now proceed to the AI Ancestor experience through the Home tab.
        """,
            gr.update(visible=True),   # home_group
            gr.update(visible=True),   # conversation_group
            gr.update(visible=True),   # avatar_group
            gr.update(visible=True),   # settings_group
            gr.update(visible=True),   # end_group

            gr.update(visible=False),  # home_status
            gr.update(visible=False),  # conversation_status
            gr.update(visible=False),  # avatar_status
            gr.update(visible=False),   # settings_status
            gr.update(visible=False),    # end_status

            gr.update(selected="welcome")  # tabs 
        )

# App Access Check
def check_access(access_granted):

    if access_granted:
        return "✅ Access Approved"

    return """
        ❌ Access Required

        Please complete verification on the
        Access & Consent page.
        """

# Custom CSS for Gradio App - Green and Beige Theme
#custom_css = """
    #.gradio-container {
        #background-color: #F7F3EE !important;
        #color: #2F3E2F !important;
    #}

    #/* Headings */
    #h1, h2, h3, h4 {
        #color: #4F5D4F !important;
    #}

    #/* Markdown text */
    #p, span, div {
        #color: #2F3E2F;
    #}

    #/* Buttons */
    #button {
        #background-color: #88A88A !important;
        #color: white !important;
    #}

    #/* #Textboxes */
    #textarea, input {
        #color: #2F3E2F !important;
        #background-color: #FFFDF9 !important;
    #}
    #"""

# Navigation Functions
def go_to_welcome():
    return gr.update(selected="welcome")

def go_to_conversation():
    return gr.update(selected="conversation")

def go_to_avatar():
    return gr.update(selected="avatar")

def go_to_end():
    return gr.update(selected="end_visit")


# Defining Page Blocks
with gr.Blocks() as demo:
#with gr.Blocks(css=custom_css) as demo:
    #Limiit access to the app until verification is successful
    access_granted = gr.State(False)

    gr.Markdown("""# AI Ancestor Interaction 
        
        Speak with your ancestor's AI Persona.
        """
        )
    gr.Markdown("""
        ### Memorial Identity Disclosure

        This system is an AI-generated memorial representation
        created from recorded memories, stories, and family history.

        It is not the actual individual and does not possess
        their consciousness, emotions, or personal awareness.
        """)

    with gr.Tabs(selected="access") as tabs:
    # Screen 0 - Access and Consent
        with gr.Tab("Access & Consent", id="access"):

            gr.Markdown("""
                # Welcome to AI Ancestor Interaction

                Before accessing the memorial system, identity
                verification and consent are required.
                """)

            # User verification form
            name = gr.Textbox(
                label="Full Name"
            )

            relationship = gr.Dropdown(
                choices=[
                    "Grandchild",
                    "Child",
                    "Spouse",
                    "Sibling",
                    "Family Friend",
                    "Co-Worker"
                ],
                label="Relationship"
            )

            access_code = gr.Textbox(
                label="Access Code"
            )

            # Consent checkbox 
            consent = gr.Checkbox(
                label="""
                I understand this is an AI memorial
                representation and I have permission
                to access these memories.

                I accept the terms and conditions.
                """
            )
            # verification button and status output
            verify_button = gr.Button("Verify Access")
            access_status = gr.Markdown(
                label="Awaiting Verification ..."
            )

            

        # Screen 1 - Home/Visitor Welcome Page
        with gr.Tab("Home", id="welcome"):
            # Protected content - only accessible after verification
            home_group = gr.Group(visible=False)
            home_status = gr.Markdown("""
                🔒 Restricted Area

                Access approval required before interacting
                with the AI Ancestor.
                """)

            
            # Invisible group for home content, only visible after access granted
            with home_group:
                gr.Markdown("## Welcome")
                gr.Markdown(
                    """
                    This experience allows authorised visitors to
                    explore approved memories and stories.
                    """
                )
                gr.Markdown("""
                    ## You may interact using text, speech, or
                    the digital avatar experience.

                    Select how you would like to interact with the AI Ancestor.
                    """)

                with gr.Row():

                    chat_button = gr.Button(
                        "💬 Begin Conversation with AI Ancestor",
                        variant="primary"
                    )
                    chat_button.click(
                        go_to_conversation,
                        outputs=tabs
                    )

                    avatar_button = gr.Button(
                        "🧓 Visit AI Avatar Ancestor",
                        variant="secondary"
                    )
                    avatar_button.click(
                        go_to_avatar,
                        outputs=tabs
                    )

                # Information and Instructions for Visitors
                with gr.Row():
                    gr.Markdown("""
                        ### Choose an Experience

                        **Chat with AI Ancestor**
                        - Text-based interaction
                        - Ask questions about memories and life experiences
                        - Fast responses

                        **AI Avatar Ancestor**
                        - Voice-enabled interaction
                        - Digital avatar representation
                        - Audio and visual responses
                        """)
                
                    gr.Markdown("""
                        ### Important Notice

                        This system is an AI memorial representation and
                        not the actual individual.


                        ### Privacy Notice

                        Please review the Settings tab before using the system.
                        """)
                
            
        # Screen 2 - Chat Coversation Interface
        with gr.Tab("Conversation", id="conversation"):
            # Protected content - only accessible after verification
            conversation_group = gr.Group(visible=False)
            conversation_status = gr.Markdown("""
                🔒 Restricted Area

                Access approval required before interacting
                with the AI Ancestor.
                """) 
            
        # Invisible group for conversation content, only visible after access granted
            with conversation_group:
                gr.Markdown("""
                    ## Text Conversation

                    Ask about life experiences, stories, advice,
                    and family memories.
                    """)
                gr.Markdown("""
                    ⚠️ This chat is an AI persona representation and
                    not the actual person.
                    """)
                
                chatbot = gr.Chatbot(height=200, label="AI Ancestor Chatbot")
                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="Ask a question...",
                        label="Message"
                        )
                    
                    send = gr.Button("Send", scale=1)

                send.click(respond,
                    [msg, chatbot],
                    [chatbot, msg]
                )

            # Clear Chat Button
                clear = gr.Button("Clear Chat")
                
                clear.click(
                    lambda: [],
                    outputs=chatbot 
                )   

                # Session Control Buttons - Pause, End Visit, Help
                with gr.Row():
        
                    pause_button = gr.Button("⏸Pause")
        
                    end_button = gr.Button("End Visit",
                        variant="stop"
                    )
        
                    help_button = gr.Button("Help") 

                # Session Control Message Output
                session_message = gr.Markdown()
                pause_button.click(pause_session,
                    outputs=session_message
                )

                help_button.click(help_session,
                    outputs=session_message
                )

                end_button.click(go_to_end,
                    outputs=tabs
                )
                with gr.Row():
                    gr.Markdown("""
                        ## Example Questions

                        • Tell me about your childhood

                        • What was family life like growing up?

                        • What was your favourite memory?

                        • What advice would you give me?
                        """
                    )

                    gr.Markdown("""
                    If a memory cannot be verified from the
                    available records, the AI ancestor will
                    say it does not have that memory.
                    """)

            # Audio Input (Microphone)
                audio_input = gr.Audio(
                    sources=["microphone"],
                    type="filepath",
                    label="Record your question"
                )
            
            # Audio Output (Speaker)
                audio_output = gr.Audio(
                    label="Listen to the AI Ancestor's response"
                )
            
            #Voice Submit Button
                voice_button = gr.Button(
                "Submit Voice Question"
                )
            
                voice_button.click(
                    process_voice,
                    inputs=audio_input,
                    outputs=audio_output
                )

                # Memory Source Display
                source_box = gr.Textbox(
                    label="Memory Source",
                    interactive=False
                    )

                view_source = gr.Button(
                    "View Source"
                    )
            
        # Screen 3 - Avatar Screen
        with gr.Tab("Avatar", id="avatar"):
            # Protected content - only accessible after verification
            avatar_group = gr.Group(visible=False)
            avatar_status = gr.Markdown("""
                🔒 Restricted Area

                Access approval required before interacting
                with the AI Ancestor.
                """)


            # Invisible group for avatar content, only visible after access granted
            with avatar_group:

                gr.Markdown("## Digital Ancestor Avatar")

                # Avatar Placeholder Image
                gr.Image(
                    value="https://via.placeholder.com/400x400.png?text=AI+Avatar",
                    label="Prototype Avatar"
                )
                gr.Markdown(
                    """
                    🧓 Avatar Placeholder

                    Future AI Avatar will appear here.

                    Status: Prototype Mode
                    """
                )
                gr.Markdown(
                    """
                    In the final system, this screen will display
                    the digital representation of the principal.
                    """
                )

                play_button = gr.Button("Play Sample Response")

                gr.Markdown("""
                ### Voice Interaction

                Speak to the AI ancestor and listen to responses.
                """)

                # Audio Input (Microphone)
                avatar_audio_input = gr.Audio(
                    sources=["microphone"],
                    type="filepath",
                    label="Ask the AI Ancestor a Question"
                )

                # Audio Output (Speaker)
                avatar_audio_output = gr.Audio(
                    label="AI Ancestor Response"
                )

                # Voice Submit Button
                avatar_voice_button = gr.Button(
                    "Submit Voice Question"
                )

                avatar_voice_button.click(
                    process_voice,
                    inputs=avatar_audio_input,
                    outputs=avatar_audio_output
                )

                # Avatar Interaction Buttons - Open Conversation, End Visit
                with gr.Row():
                    avatar_chat = gr.Button(
                        "💬 Open Conversation"
                    )

                    avatar_end = gr.Button(
                        "🛑 End Visit"
                    )

                avatar_chat.click(
                    go_to_conversation,
                    outputs=tabs
                    )

                avatar_end.click(
                    go_to_end,
                    outputs=tabs
                    )

                gr.Markdown("""
                    ⚠️ This avatar is an AI representation and
                    not the actual person.
                    """)

        # Screen 4 - Settings & Privacy
        with gr.Tab("Settings", id="settings"):
            # Protected content - only accessible after verification
            settings_group = gr.Group(visible=False)
            settings_status = gr.Markdown("""
                🔒 Restricted Area

                Access approval required before interacting
                with the AI Ancestor.
                """)


            # Invisible group for settings content, only visible after access granted
            with settings_group:
                gr.Markdown("## Account")
                username = gr.Textbox(label="Username")

                password = gr.Textbox(
                    label="Password",
                    type="password"
                )

                gr.Markdown("## Privacy & Consent")
                privacy = gr.Checkbox(
                    label="I understand this is an AI  representation."
                )

                login = gr.Button("Login")
                
                gr.Markdown(
                    """
                    ### Data Protection and Privacy Settings
                    ✓ Personal memories protected

                    ✓ Authentication required

                    ✓ Approved family access only

                    ✓ Identity verification required

                    ✓ Consent acknowledgement required

                    ✓ Sensitive memories protected

                    ✓ Memorial identity disclosure
                    
                    ✓ Future secure cloud storage planned

                    ✓ Access logging planned
                    """
                )

                # Visitor Permissions and Access Level
                gr.Markdown("""
                    ## Visitor Permissions

                    Current Access Level:
                    Family Access

                    Relationship Verified:
                    Approved

                    Consent Status:
                    Accepted
                    """)

                # Data Handling and Security
                gr.Markdown("""
                    ## Data Handling

                    ✓ Approved access only

                    ✓ Session protected

                    ✓ Source-grounded responses

                    ✓ Memorial identity disclosure active

                    ✓ Access logging planned
                    """)
                                
            # Screen 5 - End Visit
        with gr.Tab("End Visit", id="end_visit"):
            # Protected content - only accessible after verification
            end_group = gr.Group(visible=False)
            end_status = gr.Markdown("""
                🔒 Restricted Area

                Access approval required before interacting
                with the AI Ancestor.
                """)
            # Invisible group for end visit content, only visible after access granted
            with end_group:
                gr.Markdown("""
                    # Thank You For Visiting

                    This interaction was generated from
                    approved recorded stories, memories and family history.

                    The responses generated during this
                    session do not represent the thoughts
                    or consciousness of the actual person.

                    We hope you learned something meaningful
                    about this person and their life.

                    You may close the session OR start a new authorised visit.
                    """)
            
                close_button = gr.Button("Close Session", 
                    variant="stop")
                
                close_button.click(
                    logout_user,
                    outputs=[
                        access_status,

                        home_group,
                        conversation_group,
                        avatar_group,
                        settings_group,
                        end_group,

                        home_status,
                        conversation_status,
                        avatar_status,
                        settings_status,
                        end_status,

                        name,
                        relationship,
                        access_code,
                        consent,

                        tabs
                    ]
                )

                restart_button = gr.Button("Start New Visit")

                restart_button.click(go_to_welcome,
                    outputs=tabs
                )


            verify_button.click(verify_access,
                inputs=[name,relationship,
                    access_code,consent],
                outputs=[access_status,
                          
                        home_group,conversation_group,
                        avatar_group, settings_group,
                        end_group,

                        home_status, conversation_status,
                        avatar_status, settings_status, 
                        end_status,

                        tabs]
            )


# AI Ancestor Identity Disclosure
gr.Markdown("""
    
    # Memorial Identity Disclosure
    
    This system is an AI-generated memorial representation
    created from stories, memories and family records.
    
    It is not the actual individual and does not possess
    consciousness or emotions.
    """)
    
#gr.HTML("""
    #<div class="warning">
    #<h3> Memorial Identity Disclosure</h3>
    #<p>
    
    #This system is an AI-generated memorial representation
    #created from stories, memories and family records.
    #</p>
    #<p>
    
    #It is not the actual individual and does not possess
    #consciousness or emotions.
    #</p>
    #</div>
    #""")


demo.launch(server_name="0.0.0.0",
    server_port=7860)

# Shell code to save to Github
# git add .
#git commit -m "Create Gradio front-end skeleton"
# git push