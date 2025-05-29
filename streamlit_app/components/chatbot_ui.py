import os
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

load_dotenv()  # loads environment variables from .env file if present

# Initialize OpenAI client with API key from environment variable
# Initialize OpenAI client (make sure OPENAI_API_KEY is set in your env)
client = OpenAI()

def get_chat_response(prompt, chat_history=None):
    if chat_history is None:
        chat_history = []

    messages = chat_history + [{"role": "user", "content": prompt}]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=300,
        )
        reply = response.choices[0].message.content
        return reply

    except Exception as e:
        # Print full error details for debugging
        import traceback
        traceback.print_exc()
        print(f"Error getting chat response: {e}")
        return f"Sorry, I couldn't process your request right now. Please try again later."
    
def show_message(role, content):
    # Define CSS for left/right chat bubbles
    st.markdown("""
    <style>
    .chat-bubble {
        # padding: 12px 16px;
        margin: 6px 0;
        border-radius: 12px;
        max-width: 75%;
        font-size: 16px;
        word-wrap: break-word;
    }
    .left {
        # background-color: rgba(220, 248, 198, 0.9);
        margin-right: auto;
        margin-left: 0;
        text-align: left;
    }
    .right {
        # background-color: rgba(230, 230, 230, 0.9);
        margin-left: auto;
        margin-right: 0;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

    align_class = "right" if role == "user" else "left"

    with st.chat_message(role):
        st.markdown(f"<div class='chat-bubble {align_class}'>{content}</div>", unsafe_allow_html=True)
