def edit_prompt():
    import streamlit as st
    
    prompt = st.text_area(
        "Enter your prompt",
        placeholder="Enter prompt for image analysis",
        value='You are a data analyst extracting text from licenses. Extract all the text that can be found in the image including the location. A donor that has a red heart next to the text indicates that the individual is a donor. Use a "Y" for donor and "N" for nondonor. Do not add any additional information. Format the results in a visually appealing table for a demo.',
        height=100
    )
    
    return prompt
