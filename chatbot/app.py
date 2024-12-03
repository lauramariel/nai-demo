import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.base import BaseCallbackHandler
import os
from decouple import config
from tools import load_system_messages


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

system_messages = load_system_messages()

# Sidebar for user input
st.sidebar.header('Configuration')
api_endpoint = st.sidebar.text_input('API Endpoint URL', value=config('API_ENDPOINT', default='https://ai.nutanix.com/api/v1'))
model_name = st.sidebar.text_input('Model Name', value=config('MODEL_NAME', default='vllm-llama-3-1'))
api_key = st.sidebar.text_input('API Key', type='password', value=config('API_KEY', default=''))
temperature = st.sidebar.slider(
    "Select Temperature for Chatbot:",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1
)

option = st.sidebar.selectbox(
    "Choose a system mode:",
    list(system_messages.keys()),
    index=0
)

system_message = st.sidebar.text_area("System Message", value=system_messages.get(option))

# Clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Check if required fields are filled
required_fields_valid = bool(api_endpoint and model_name and api_key)

# Show warning if required fields are missing
if not required_fields_valid:
    st.warning("Please fill in all required fields (API Endpoint, Model Name, and API Key) in the sidebar to enable chat.")

# Main chat interface
st.title("AI Chatbot")

# logo
logo_path = './ntnx_logo.png'
if os.path.exists(logo_path):
    st.image(logo_path, width=200)
else:
    st.warning("Logo file not found. Please ensure 'ntnx_logo.png' is in the same directory as this script.")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input - only enable if required fields are valid
if required_fields_valid:
    if prompt := st.chat_input("You:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            # Initialize ChatOpenAI and memory
            llm = ChatOpenAI(
                openai_api_key=api_key,
                model_name=model_name,
                openai_api_base=api_endpoint,
                temperature=temperature,
                streaming=True
            )
            memory = ConversationBufferMemory(return_messages=True)

            # Generate AI response
            messages = [
                SystemMessage(content=system_message)
            ] + [HumanMessage(content=msg["content"]) if msg["role"] == "user" else AIMessage(content=msg["content"]) for msg in st.session_state.messages]
            with st.chat_message("assistant"):
                stream_handler = StreamHandler(st.empty())
                response = llm(messages, callbacks=[stream_handler])
                st.session_state.messages.append({"role": "assistant", "content": stream_handler.text})
        
        except Exception as e:
            st.error("An error occurred while connecting to the API. Please check your API endpoint and credentials.")
            # Optionally log the error for debugging purposes
            # print(e)

# Run the app: streamlit run chatbot_app.py