def create_api_endpoint_uploader():
    import streamlit as st

    st.header("API Endpoint Uploader")
    api_endpoint = st.text_input("Enter your API endpoint:")
    
    if st.button("Submit API Endpoint"):
        if api_endpoint:
            st.success(f"API Endpoint '{api_endpoint}' submitted successfully!")
        else:
            st.error("Please enter a valid API endpoint.")