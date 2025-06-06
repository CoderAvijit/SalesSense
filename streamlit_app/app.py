import streamlit as st
from components.chatbot_ui import get_chat_response
from components.sales_suggestions import show_sales_suggestions
from components.recommendation_ui import show_recommendations
from utils.intent_detection import detect_intent
from components.chatbot_ui import show_message
from datetime import datetime
import speech_recognition as sr
from components.session import get_snowpark_session
session = get_snowpark_session()


# python UDF function for retrieving recent user-bot conversations to have past context linked to current user prompt
def get_recent_context(chat_history, n=2):
    return chat_history[-n:] if len(chat_history) >= n else chat_history

# ChatBot Title
st.title("❄️SalesSense",help="Next-gen AI-powered CRM assistant developed by SnowPals.")

# To keep a sidebar menu for -Clear chat history & save & download session chats
with st.sidebar:    
    if st.button("🗑 clear chat", help="Clear the chat history"):
        st.session_state.chat_history = []
    if st.button("💾 save chat"):
        chat_lines = []
        
        for entry in st.session_state.chat_history:
            role = "👤 User" if entry["role"] == "user" else "🤖 Bot"
            chat_lines.append(f"**{role}:** {entry['message']}")
        chat_md = "\n\n".join(chat_lines)
        
        # Write to file and trigger download
        st.download_button(
            label="Download",
            data=chat_md,
            file_name="sales_chat_history.txt",
            mime="text/plain"
        )
        
# Get the current active snowpark session/credentials

# keeping chat session history logic
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  

# Display existing chat history 
for entry in st.session_state.chat_history:
    with st.chat_message(entry["role"], avatar="❄️" if entry["role"] == "ai" else None):
        st.markdown(entry["message"])


# Initialize prompt in session state
if "prompt" not in st.session_state:
    st.session_state.prompt = None


# Handle text input from user
text_input = st.chat_input("Ask anything..")
if text_input:
    st.session_state.prompt = text_input

# Microphone input
if st.button("🎙️ Use Mic to Speak"):
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    try:
        with sr.Microphone() as source:
            st.info("🎤 Listening... Please speak clearly.")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        mic_input = recognizer.recognize_google(audio)
        st.success(f"🗣️ You said: {mic_input}")

        # ✅ Update session prompt with mic input
        st.session_state.prompt = mic_input

    except sr.UnknownValueError:
        st.error("❌ Could not understand audio.")
    except sr.RequestError as e:
        st.error(f"❌ Could not request results; {e}")
    except Exception as e:
        st.error(f"❌ Microphone error: {e}")

# Use prompt in downstream logic
prompt = st.session_state.prompt

# logic to handle when user enters chat prompt
if prompt:
        
    with st.chat_message("user"):
        st.write(f"{prompt}")
        safe_prompt = prompt.replace("'", "''")    #this line of code is for to remove any single quote issue entered by user
        st.session_state.chat_history.append({"role": "user", "message": prompt})

        recent_context = get_recent_context(st.session_state.chat_history, n=2)
        context_str = "\n".join([f"{entry['role']}: {entry['message']}" for entry in recent_context])

        # prompt engineering the LLM model to reply user's contextual questions.
        # Model - 'snowflake-arctic'
        model_response = session.sql(f"""
            SELECT snowflake.cortex.complete(
            'snowflake-arctic',$$ You are SalesSense, a friendly AI-powered CRM assistant.

            Recent conversation happend with you and user last:
            {context_str}

            User's latest message:
            "{safe_prompt}"

            Carefully follow these guidelines when replying:

            1. If the user has provided specific CRM-related details (e.g., lead name, contact, email, phone number, location),
            acknowledge the received details explicitly in short summarized way and confirm you are on it to udpate them. 
            Avoid asking again for the same details but no need to start with Hello! repeatedly,
            and at the end of your message, append: [ACTION: SQL_GENERATION_REQUIRED]

            2. If any provided information is unclear or incomplete, politely request just the missing or unclear details.

            3. For casual greetings or non-CRM tasks, reply naturally and concisely.
            4. Only greet (like "Hey" "Hello" or "Hi") if this is the very first interaction (hint : check from given past context {context_str} )or if the user explicitly greets you first.

            Respond now clearly and explicitly based on the above:
            $$)""").collect()

        model_response = model_response[0][0] # Bot model's responses captured in variable model_response
        
        if '[ACTION: SQL_GENERATION_REQUIRED]' in model_response:
            generate_sql=True
        else:
            generate_sql=False
            
        model_response=model_response.replace("[ACTION: SQL_GENERATION_REQUIRED]", "").strip()
        
        cortex_response=model_response

        if generate_sql: # if need to generate SQL then

            # Prompting model to generate SQL and execute
            sql_query_generated=session.sql(f"""
            SELECT snowflake.cortex.complete(
            'snowflake-arctic', 
            $$Act as an Snowflake SQL expert, convert this User's natuaral input prompt into a SQL statement.
            Note - When context is clear to you, then only give me the SQL statement to be executed as output.
            
            CRM database schema context given below for for generating SQL :
            
            - leads(lead_id, name, region, score)
            - deals(deal_id, lead_id, status, close_date)  
            sample deal status data - 'Closed-Won', 'Closed-lost', 
            'Proposal' etc., This is just an example  $$)""").collect()[0][0]

            st.session_state.chat_history.append({"role": "ai", "message": sql_query_generated})
            
            


    # Chatbot relpying back to user response
    with st.chat_message("ai",avatar="❄️"):
        
        st.write(f"{cortex_response}")
        st.session_state.chat_history.append({"role": "ai", "message":  cortex_response})

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

