import streamlit as st
from components.chatbot_ui import get_chat_response
from components.sales_suggestions import show_sales_suggestions
from components.recommendation_ui import show_recommendations
from utils.intent_detection import detect_intent
from components.chatbot_ui import show_message
from datetime import datetime


# --- Page Config ---
st.set_page_config(page_title="❄️ SalesSense", layout="centered")
st.title("❄️ SalesSense")
st.header("Sales AI Assistant : Powered by SnowPals")

# --- Session State for Chat History ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Chat UI Renderer ---
def show_chat():
    for message in st.session_state.chat_history:
        show_message(message["role"], message["content"])

def get_time_of_day():
    current_hour = datetime.now().hour
    
    if 5 <= current_hour < 12:
        return "morning"
    elif 12 <= current_hour < 17:
        return "afternoon"
    elif 17 <= current_hour < 21:
        return "evening"
    else:
        return "night"


def greetings_message():
    # Get time_of_day from session state, default to 'day'
    time_of_day = get_time_of_day()

    if time_of_day == "morning":
        greeting = "Good morning! ☀️"
    elif time_of_day == "afternoon":
        greeting = "Good afternoon! 🌞"
    elif time_of_day == "evening":
        greeting = "Good evening! 🌆"
    else:
        greeting = "Hello! 😊"
    
    return f"{greeting} How can I assist you today? You can ask me about pricing, features, or recommendations!"



# --- Chat Input ---
user_input = st.chat_input("Ask me about pricing, features, or recommendations...")

if user_input:
    intent = detect_intent(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    if intent == "support_request":
        reply = get_chat_response(user_input, st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

    elif intent == "sales_inquiry":
        show_sales_suggestions = show_sales_suggestions(user_input)
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "Here are a few sales tips and suggestions I found for you! 😊" 
        })

    elif intent == "greeting":
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": greetings_message()
        })

        # for message in st.session_state.chat_history:
        #     with st.chat_message(message["role"]):
        #         st.write(message["content"])


    elif intent == "recommendation":
        show_recommendations(user_id="u1")
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "Based on your preferences, here are some product recommendations! 📦"
        })

    else:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "🤔 I'm not quite sure how to help with that. You can ask me about pricing, features, or recommendations!"
        })

# --- Show All Messages ---
show_chat()

# --- Background Styling ---
def set_bg_hack_url(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-attachment: fixed;
            background-size: cover;
            background-repeat: no-repeat;
        }}
         /* Default markdown text and buttons */
        .stMarkdown, .stButton > button, .stChatInput > div > textarea {{
            color: black !important;
        }}

        /* Title (h1) and header (h2) custom style */
        h1 {{
            color: white !important;
            font-size: 50px !important;
        }}
        h2 {{
            color: white !important;
            font-size: 26px !important;
        }}
        .st-emotion-cache-1f1nna7 {{
            background-color: rgba(220, 248, 198, 0.9) !important;
            border-radius: 10px !important;
            padding: 10px !important;
            color: black !important;
        }}
        .st-emotion-cache-4oy321 {{
            background-color: rgba(230, 230, 230, 0.9) !important;
            border-radius: 10px !important;
            padding: 10px !important;
            color: black !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set background image
set_bg_hack_url("https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1350&q=80")

