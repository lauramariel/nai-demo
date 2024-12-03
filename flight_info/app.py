import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from typing import List, Dict
import json
from langchain.prompts import MessagesPlaceholder
import requests
import os
from datetime import datetime
from time import sleep
from decouple import config



class StreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self, container, debug_container):
        super().__init__()
        self.container = container
        self.debug_container = debug_container
        self.text = ""
        self.debug_text = ""

    def on_llm_start(self, serialized, prompts, **kwargs):
        self.text += "Starting LLM...\n"
        self.container.markdown(self.text)

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

    def on_llm_end(self, response, **kwargs) -> None:
        self.text += "\nLLM finished.\n"
        self.container.markdown(self.text)

    def on_llm_error(self, error, **kwargs) -> None:
        self.text += f"Error: {str(error)}\n"
        self.container.markdown(self.text)
    
    def __init__(self, container, debug_container):
        super().__init__()
        self.container = container
        self.debug_container = debug_container
        self.text = ""
        self.debug_text = ""

    def on_llm_start(self, serialized, prompts, **kwargs):
        print("Starting LLM...")
        self.text += "Starting LLM...\n"
        self.container.markdown(self.text)

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.debug_text += token
        if self.debug_container:
            self.debug_container.text(self.debug_text)
        self.text += token
        self.container.markdown(self.text)

    def on_tool_start(self, serialized, input_str, **kwargs):
        print("Tool start:", serialized, input_str)
        self.text += f"\nUsing tool: {serialized['name']}\n"
        self.container.markdown(self.text)

    def on_tool_end(self, output: str, **kwargs) -> None:
        print("Tool end:", output)
        self.text += f"Tool output: {output}\n"
        self.container.markdown(self.text)

    def on_chain_end(self, outputs, **kwargs):
        print("Chain end:", outputs)
        if outputs and isinstance(outputs, dict):
            self.text += f"\nFinal output: {outputs.get('output', '')}\n"
            self.container.markdown(self.text)

    def on_chain_error(self, error: Exception, **kwargs) -> None:
        print("Chain error:", error)
        self.text += f"\nError: {str(error)}\n"
        self.container.markdown(self.text)

def get_flight_info(query: str) -> str:
    """Function to return Qatar Airways flight information between specified airports"""
    try:
        departure, arrival = query.split(',')
        departure = departure.strip().upper()
        arrival = arrival.strip().upper()
    except ValueError:
        return "Error: Please provide both departure and arrival airport codes separated by a comma (e.g., 'DOH,DXB')."


    qa_url = 'https://qoreservices.qatarairways.com/fltstatus-services/flight/getStatus'
    params = {
        "departureStation": departure,
        "arrivalStation": arrival,
        "scheduledDate": datetime.now().strftime("%Y-%m-%d"),
        "appLocale": "en"
    }
    response = requests.post(qa_url, json=params)
    flights = response.json().get('flights', [])
    text_flights = f'Flights from {departure} to {arrival} on {datetime.now().strftime("%d-%B-%Y")}:\n'
    counter = 1
    for flight in flights:
        record = f"({counter}) Flight: QR{flight['flightNumber']}, Departure Time: {flight['departureDateScheduled']}, Arrival Time: {flight['arrivalDateScheduled']}, Status: {flight['flightStatus']}\n"
        text_flights += record
        counter += 1

    return text_flights


# Sidebar for user input
st.sidebar.header("Configuration")
api_endpoint = st.sidebar.text_input('API Endpoint URL', value=config('API_ENDPOINT', default='https://ai.nutanix.com/api/v1'))
model_name = st.sidebar.text_input('Model Name', value=config('MODEL_NAME', default='vllm-llama-3-1'))
api_key = st.sidebar.text_input('API Key', type='password', value=config('API_KEY', default=''))
debug_mode = False

# Check if all required fields are filled
required_fields_filled = bool(api_endpoint and model_name and api_key)

# If any field is empty, show warning
if not required_fields_filled:
    st.warning("Please fill in all required fields in the sidebar (API Endpoint, Model Name, and API Key)")

# Clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Main chat interface
# Display Qatar Airways logo
logo_path = './logo.png'
if os.path.exists(logo_path):
    st.image(logo_path, width=200)
else:
    st.warning("Logo file not found. Please ensure 'logo.png' is in the same directory as this script.")

st.title("Qatar Airways Flight Information Chatbot")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input - now conditional
if required_fields_filled:
    if prompt := st.chat_input("You:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Initialize ChatOpenAI and memory
        llm = ChatOpenAI(
            openai_api_key=api_key,
            model_name=model_name,
            openai_api_base=api_endpoint,
            streaming=True
        )
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # Create the flight info tool
        flight_tool = Tool(
            name="Flight Information",
            func=get_flight_info,
            description="Use this tool to get Qatar Airways flight information between two airports. Input should be two airport codes separated by a comma (e.g., 'DOH,DXB' for flights from Doha to Dubai)."
        )

        # Define the system message to control the chatbot's behavior
        system_message = f"""You are an AI assistant specializing in Qatar Airways flights, with a focus on flights to and from Doha Hamad International Airport (DOH). 
        Your primary function is to provide information about Qatar Airways flights, their schedules, and general information about traveling with Qatar Airways.
        When using the Flight Information tool, always provide both the departure and arrival airport codes, separated by a comma.
        Only use the provided flight information tool when specific flight details are requested.
        If asked about flights from other airlines, politely explain that you can only provide information about Qatar Airways flights.
        Be helpful, concise, and friendly in your responses.
        
        Today's date is {datetime.now().strftime("%d-%B-%Y")}.
        """

        # Initialize the agent with the tool and the system message
        agent = initialize_agent(
            tools=[flight_tool],
            llm=llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            memory=memory,
            handle_parsing_errors=True,
            agent_kwargs={
                "system_message": system_message,
                "extra_prompt_messages": [MessagesPlaceholder(variable_name="chat_history")]
            }
        )

        # Generate AI response
        with st.chat_message("assistant"):
            response_container = st.empty()
            debug_container = st.empty() if debug_mode else None
            stream_handler = StreamHandler(response_container, debug_container)
            try:
                response = agent.run(
                    input=prompt,
                    callbacks=[stream_handler]
                )
                st.session_state.messages.append({"role": "assistant", "content": response})
                response_container.markdown(response)
                sleep(5)
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
                response_container.error(error_message)
                if debug_mode:
                    st.exception(e)

        # Display debug information if debug mode is on
        if debug_mode:
            with st.expander("Debug Information"):
                st.text(stream_handler.debug_text)
else:
    # Disabled chat input
    st.chat_input("You:", disabled=True)

# Run the app: streamlit run chatbot_app.py