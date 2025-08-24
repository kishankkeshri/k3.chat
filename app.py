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

# Inject custom CSS for background and animations
st.markdown(
    """
    <style>
    body {
        background-image: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1500&q=80');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }
    .stApp {
        background: rgba(255,255,255,0.85);
        border-radius: 16px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        padding: 2rem;
        margin-top: 2rem;
        animation: fadeInApp 1.2s;
    }
    @keyframes fadeInApp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .element-container .stChatMessage {
        animation: fadeInMsg 0.8s;
    }
    @keyframes fadeInMsg {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animated-bg {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1;
        pointer-events: none;
        background: radial-gradient(circle at 20% 30%, #a1c4fd55 0%, transparent 70%),
                    radial-gradient(circle at 80% 70%, #c2e9fb55 0%, transparent 70%);
        animation: moveBg 10s infinite alternate;
    }
    @keyframes moveBg {
        0% { background-position: 20% 30%, 80% 70%; }
        100% { background-position: 25% 35%, 75% 65%; }
    }
    </style>
    <div class="animated-bg"></div>
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
