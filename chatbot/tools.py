import json
import requests
import streamlit as st
import logging
import re
from decouple import config


logging.basicConfig(level=config('LOG_LEVEL', default='INFO'))
logger = logging.getLogger(__name__)


def fetch_available_models(api_endpoint, api_key):
    """Fetch available models from the OpenAI endpoint"""
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Construct the models endpoint URL
        if api_endpoint.endswith('/'):
            models_url = f"{api_endpoint}models"
        else:
            models_url = f"{api_endpoint}/models"
        
        response = requests.get(models_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            models = [model['id'] for model in data.get('data', [])]
            # Sort models alphabetically for better UX
            models.sort()
            return models
        elif response.status_code == 401:
            st.error("Authentication failed. Please check your API key.")
            return []
        elif response.status_code == 404:
            st.error("Models endpoint not found. Please check your API endpoint URL.")
            return []
        else:
            st.error(f"Failed to fetch models: {response.status_code} - {response.text}")
            return []
            
    except requests.exceptions.ConnectionError:
        st.error("Connection failed. Please check your API endpoint URL and internet connection.")
        return []
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []
    except json.JSONDecodeError as e:
        st.error(f"Error parsing response: {str(e)}")
        return []
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return []


def load_file_text(filename):
    content = None
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        logger.error(f'The file {filename} does not exist.')
    except IOError:
        logger.error(f'An I/O error occurred while trying to read {filename}.')

def process_text_with_context(text):
    
    if not text:
        return text
        
    # Pattern to match {{context:filename.txt}} tags, ensuring filename ends with .txt
    pattern = r'\{\{context:(.*?\.txt)\}\}'
    
    def replace_with_content(match):
        filename = match.group(1)
        if not filename.endswith('.txt'):
            logger.warning(f'Skipping {filename} - not a .txt file')
            return match.group(0)
        content = load_file_text(filename)
        if content is None:
            logger.warning(f'Could not load content from {filename}')
            return ''
        return content
        
    # Replace all matches with their file contents
    processed_text = re.sub(pattern, replace_with_content, text)
    
    return processed_text



@st.cache_data
def load_system_messages(system_messages_json='system_messages.json'):
    with open(system_messages_json, 'r') as file:
        data = json.load(file)
    
    system_messages = {}
    for item in data:
        system_messages[item['name']] = process_text_with_context(item['message'])

    return system_messages