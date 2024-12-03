import json
import streamlit as st
import logging
import re
from decouple import config


logging.basicConfig(level=config('LOG_LEVEL', default='INFO'))
logger = logging.getLogger(__name__)


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