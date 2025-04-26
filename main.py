# Import necessary libraries
import streamlit as st
import google.generativeai as genai
import os

# --- Configuration ---

# Set page configuration for the Streamlit app
st.set_page_config(
    page_title="Gemini Chatbot",
    page_icon="✨",
    layout="wide"
)

# Set the title of the Streamlit app
st.title("💬 Gemini Chatbot")
st.caption("🚀 A Streamlit chatbot powered by Google's Gemini API")

# --- API Key Handling ---

# Try to get the API key from Streamlit secrets
api_key = "AIzaSyCRlWjfBnfPVWWEoXas11fME8foyk4Hppo"

# If the API key is not found in secrets, prompt the user
if not api_key:
    api_key = st.text_input("Enter your Google AI API Key:", type="password", key="api_key_input")
    if api_key:
        st.success("API Key entered successfully!", icon="✅")
    else:
        st.warning("Please enter your Google AI API Key to proceed.", icon="⚠️")
        st.stop() # Stop execution if no API key is provided

# Configure the generative AI library with the API key
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Error configuring Google AI SDK: {e}")
    st.stop()

# --- Model Selection ---

# Allow user to select the Gemini model
# Update this list based on available models from Google AI
available_models = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"]
selected_model = st.sidebar.selectbox("Select Gemini Model", available_models, index=0) # Default to flash

# --- Initialize Model and Chat ---

# Create the generative model instance
try:
    model = genai.GenerativeModel(
        model_name=selected_model,
        # Optional: Add safety settings and generation config if needed
        # safety_settings=[...],
        # generation_config=genai.types.GenerationConfig(...)
    )
except Exception as e:
    st.error(f"Error initializing the generative model: {e}")
    st.stop()

# Initialize chat history in session state if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    # Start a chat session using the model (maintains context)
    st.session_state.chat_session = model.start_chat(history=[])

# --- Display Chat History ---

# Display existing messages from history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Handle User Input and Model Response ---

# Get user input using Streamlit's chat input widget
user_prompt = st.chat_input("Ask FinAI...")

if user_prompt:
    # Add user message to chat history and display it
    #user_prompt = "Sen bir finans asistanısın! Sana verdiğim mesaja göre bana, finans danışmanlığı yap. " + user_prompt
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Send the user's message to the Gemini model and get the response
    try:
        # Use the chat session to send the message
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Add model's response to chat history and display it
        response_text = gemini_response.text # Access the text part of the response
        st.session_state.chat_history.append({"role": "Sen bir finans asistanısın! Sana verdiğim mesaja göre bana, finans danışmanlığı yap.", "content": response_text})
        with st.chat_message("model"):
            st.markdown(response_text)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        # Optionally remove the user message if the API call failed
        # st.session_state.chat_history.pop()


# --- Sidebar for Clearing Chat ---
st.sidebar.header("Chat Controls")
if st.sidebar.button("Clear Chat History"):
    st.session_state.chat_history = []
    # Restart the chat session to clear context
    st.session_state.chat_session = model.start_chat(history=[])
    st.rerun() # Rerun the app to reflect the cleared state