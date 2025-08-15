import streamlit as st
import time

def typing_effect(text, speed=0.0001):
    """
    Display text with a typing effect in Streamlit
    Args:
        text (str): The text to display
        speed (float): Delay between each character in seconds
    """
    placeholder = st.empty()
    displayed_text = ""
    
    for char in text:
        displayed_text += char
        placeholder.markdown(f">{displayed_text}▌")
        time.sleep(speed)
    
    # Final display without cursor
    placeholder.markdown(f">{displayed_text}")