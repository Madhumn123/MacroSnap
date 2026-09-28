from google import genai
from google.genai import types
import streamlit as st

from promat import SYSTEM_PROMPT, WELCOME_MESSAGE, WHATSAPP_SUMMARY_PROMPT 

# Securely grab the API key from Streamlit secrets
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)

gemini_client = get_gemini_client()
# Using the stable production-ready Flash model name
model = "gemini-2.5-flash"  

# --- Dummy helper functions for WhatsApp integration ---
def ask_gemini(prompt_list):
    """Generates content using the official Google GenAI SDK syntax."""
    response = gemini_client.models.generate_content(
        model=model,
        contents=prompt_list,
    )
    return response.text

def send_whatsapp(number, text_content):
    """
    Placeholder for your WhatsApp sending utility.
    Replace this with your actual Twilio / Vonage API logic.
    """
    if number and text_content:
        return True, "Success"
    return False, "Invalid number or empty content"


# --- Step 1: Onboarding (Username and WhatsApp Number) ---

if 'onboared' not in st.session_state:
    st.title("MacroSnap - Food and Fitness Assistant")
    st.caption("Your friendly AI assistant for nutrition, meal planning, and fitness guidance.")

    with st.form("onboarding-form"):
        name = st.text_input("Your Name")
        whatsApp_Number = st.text_input(
            "WhatsApp number (with country code)",
            placeholder="+91XXXXXXXXXX",
            help="This is the number MacroSnap will text your summaries to"
        )
        submitted = st.form_submit_button("Let's go")
        
    if submitted:
        if not name.strip() or not whatsApp_Number.strip():
            st.error("Please fill in both fields.")
        else:
            st.session_state.name = name
            st.session_state.whatsApp_Number = whatsApp_Number

            # Activate Chat Session using the correct variable and system instructions
            st.session_state.chat = gemini_client.chats.create(
               model=model,
               config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
            )
            st.session_state.message = []
            st.session_state.onboared = True
            st.rerun()
        
    st.stop()   


# --- Step 2: Chat Interface ---

header_col, button_col = st.columns([5, 2], vertical_alignment="center")

with header_col:
    st.title("MacroSnap - Food and Fitness Assistant")
    st.caption(f"Welcome back, {st.session_state.name}! Your friendly AI assistant for nutrition, meal planning, and fitness guidance.")


st.caption(f"logged in as: {st.session_state.name} | WhatsApp: {st.session_state.whatsApp_Number}")