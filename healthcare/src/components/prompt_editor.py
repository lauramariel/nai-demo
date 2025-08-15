def edit_prompt():
    import streamlit as st
    
    prompt = st.text_area(
        "Enter your prompt",
        placeholder="Enter instructions for analyzing the healthcare document",
        height=150
    )
    
    # Add a help text explaining the prompt
    st.markdown("""
    <div style="font-size: 0.8em; color: #666;">
    <p><strong>Tip:</strong> The default prompt is configured for healthcare document analysis. 
    You can customize it to focus on specific medical information you need to extract.</p>
    </div>
    """, unsafe_allow_html=True)
    
    return prompt
