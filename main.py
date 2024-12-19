import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
if not load_dotenv("api.env"):
    st.error("Failed to load environment variables. Ensure 'api.env' exists and is configured correctly.")
    st.stop()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with AbdiCheats!",
    page_icon=":matrix:",  # Favicon emoji
    layout="centered",  # Page layout option
)

# API Key Setup
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY not found. Please check your .env file or environment settings.")
    st.stop()

# Set up Google Generative AI configuration
try:
    gen_ai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error(f"Failed to configure Google Generative AI: {e}")
    st.stop()

# Translate roles for Streamlit
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session in Streamlit
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ChatBot Title
st.title("🤖 Abdi - ChatBot")

# Display Chat History
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# Input Field
user_prompt = st.chat_input("Ask Me Anything, (human(s))...")
if user_prompt:
    user_prompt = user_prompt.strip()
    if user_prompt == "":
        st.warning("Input cannot be empty. Please ask a question.")
    else:
        # Display User Message
        st.chat_message("user").markdown(user_prompt)
        st.session_state.chat_history.append({"role": "user", "text": user_prompt})
        
        try:
            # Generate Assistant Response
            gemini_response = gen_ai.generate_text(prompt=user_prompt)
            response_text = gemini_response["candidates"][0]["output"]
            
            # Append and Display Response
            st.session_state.chat_history.append({"role": "assistant", "text": response_text})
            with st.chat_message("assistant"):
                st.markdown(response_text[:3000])  # Handle large responses
        except Exception as e:
            st.error(f"An error occurred while processing your message: {e}")
