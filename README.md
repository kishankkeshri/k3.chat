# K3 Personal Chatbot

This is a Streamlit-based personal chatbot app that uses Google's Gemini 1.5 Flash model to answer questions about you, based on your personal data (e.g., social media profiles, resumes).

## Features
- Reads your personal data from `my_data.txt` (must be in the app directory).
- Securely uses your Google Gemini API key via Streamlit secrets.
- Clean, centered chat UI with session-based history.
- Robust error handling for missing/empty data or missing API key.

## Setup
1. **Install dependencies:**
   ```sh
   pip install streamlit google-generativeai
   ```
2. **Add your personal data:**
   - Create a file named `my_data.txt` in the app directory and paste your personal info (social media, resume, etc).
3. **Configure API key:**
   - In `.streamlit/secrets.toml`, add:
     ```toml
     GOOGLE_API_KEY = "your-gemini-api-key"
     ```
4. **Run the app:**
   ```sh
   streamlit run app.py
   ```

## Usage
- Ask questions about yourself in the chat window.
- The assistant will answer using your personal data as context.

---

*Built with Streamlit and Google Gemini.*
