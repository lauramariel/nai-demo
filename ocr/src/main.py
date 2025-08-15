import streamlit as st
from components.api_endpoint import create_api_endpoint_uploader
from components.image_uploader import upload_image
from components.prompt_editor import edit_prompt
from utils.api_handler import analyze_image
from utils.image_processor import preprocess_image
from urllib.parse import urlparse
from utils.text_effects import typing_effect
from decouple import config

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def main():
    # Configure page with custom styling
    st.set_page_config(layout="wide", page_title="Nutanix OCR Demo", page_icon="📄")
    
    # Add custom CSS for styling
    st.markdown("""
        <style>
        /* General page styling */
        .stApp {
            background-color: #1a1b1e;
            color: #ffffff;
        }

        /* Configuration section styling */
        .config-section {
            background-color: #2d2d2d;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
        }

        /* Results section styling */
        .results-section {
            background-color: #2d2d2d;
            border-radius: 10px;
            margin-top: 20px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
        }

        /* Button styling */
        .stButton > button {
            width: 100%;
            background-color: #7b61ff;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #5a45d6;
        }

        /* Input field styling */
        .stTextInput > div > div > input {
            background-color: #3a3b3d;
            color: white;
            border: 1px solid #7b61ff;
            border-radius: 5px;
            padding: 10px;
        }

        /* Subheader styling */
        .stMarkdown h2 {
            color: #7b61ff;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Nutanix Optical Character Recognition (OCR) Demo")

    # Create two columns for layout
    left_col, right_col = st.columns([1, 1.75])

    with left_col:
        # Start of configuration section
        with st.container():
            st.markdown('<div class="config-section">', unsafe_allow_html=True)
            
            st.subheader("API Configuration")
            base_url = "https://ai.nutanix.com/api/v1"
            api_url = st.text_input('API Endpoint URL', value=config('API_ENDPOINT', default='https://nai.tmelab.net/api/v1'))

            if api_url and not is_valid_url(api_url):
                st.error("Please enter a valid URL")
            
            model_name = st.text_input('Model Name', value=config('VISION_MODEL_NAME', default='llama-vision'))
            api_key = st.text_input('API Key', type='password', value=config('API_KEY', default=''))

            # Image Upload Section
            uploaded_image = upload_image()

            # Prompt Section
            st.subheader("Prompt Configuration")
            prompt = edit_prompt()

            # Submit Button
            submit_button = st.button("Analyze Image", use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="results-section">', unsafe_allow_html=True)
        st.subheader("Results")
        
        # Process and display results
        if submit_button and api_url and model_name and api_key and uploaded_image and prompt:
            with st.spinner('Processing image...'):
                processed_image = preprocess_image(uploaded_image)
                
                if processed_image is None:
                    st.error("Failed to process the image. Please try uploading again.")
                    return

                api_endpoint = {
                    "url": api_url,
                    "model_name": model_name,
                    "api_key": api_key
                }

                result = analyze_image(api_endpoint, processed_image, prompt)

                if "error" in result:
                    st.error(result["error"])
                else:
                    try:
                        content = result["choices"][0]["message"]["content"]
                        with st.container():
                            typing_effect(content)
                    except (KeyError, IndexError) as e:
                        st.error("Unexpected API response format")

        elif submit_button:
            st.warning("Please fill in all fields before submitting.")
            
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
