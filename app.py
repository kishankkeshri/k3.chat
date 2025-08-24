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

# Inject custom CSS for dark mode and background image
st.markdown(
    """
    <style>
    .background-container {
        min-height: 100vh;
        width: 100vw;
        position: fixed;
        top: 0; left: 0;
        z-index: -1;
        background-image: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1500&q=80');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        background-color: #181818 !important;
    }
    .stApp, .stChatMessage, .stTextInput, .stButton, .stMarkdown, .stTitle {
        background: rgba(24,24,24,0.92) !important;
        color: #f1f1f1 !important;
        box-shadow: none !important;
    }
    .stTextInput > div > input, .stTextInput > label {
        color: #f1f1f1 !important;
        background: #222 !important;
    }
    .stButton > button {
        background: #333 !important;
        color: #f1f1f1 !important;
    /* Remove overlays and effects */
    .animated-bg, .stApp[style*="box-shadow"] {
        background: none !important;
        box-shadow: none !important;
        animation: none !important;
    }
    .animated-bg, .element-container .stChatMessage, .stApp[style*="box-shadow"] {
        background: none !important;
        box-shadow: none !important;
        animation: none !important;
    }
    </style>
    <div class="background-container"></div>
    """,
    unsafe_allow_html=True
)

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
