import streamlit as st
import os
import google.generativeai as genai

# Set Streamlit page config
st.set_page_config(layout="centered", page_title="K3 Personal Chatbot")

# Helper: Load personal data
@st.cache_data
def load_personal_data():
    try:
        with open("my_data.txt", "r", encoding="utf-8") as f:
            data = f.read().strip()
            if not data:
                raise ValueError("Personal data file is empty.")
            return data
    except FileNotFoundError:
        st.error("Personal data file 'my_data.txt' not found. Please add it to the app directory.")
        st.stop()
    except ValueError as ve:
        st.error(str(ve))
        st.stop()

# Helper: Get Gemini API key
@st.cache_data
def get_api_key():
    try:
        return st.secrets["GOOGLE_API_KEY"]
    except Exception:
        st.error("Google Gemini API key not configured. Please add 'GOOGLE_API_KEY' to Streamlit secrets.")
        st.stop()

# Helper: Generate AI response
@st.cache_data(show_spinner=False)
def get_gemini_response(prompt, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

# Load data and API key
personal_data = load_personal_data()
api_key = get_api_key()

# Session state for chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hello! I'm your personal assistant. Ask me anything about you!"}
    ]

# Chat UI
st.title("K3 Personal Chatbot")
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Ask me anything about yourself...")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        prompt = f"""
You are a helpful AI assistant. Answer as if you are the user, using the following personal data:

{personal_data}

User's question: {user_input}
"""
        try:
            ai_response = get_gemini_response(prompt, api_key)
        except Exception as e:
            st.error(f"Error from Gemini API: {e}")
            st.stop()
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        st.chat_message("assistant").write(ai_response)
