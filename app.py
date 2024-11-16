import streamlit as st
from src import utils
from src.llm import EmotionalChatbot
from src.log import logger

# Streamlit UI Setup
st.set_page_config(
    page_title="Emotional Intelligence Bot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

try:
    # Initialize the chatbot
    chatbot = EmotionalChatbot(chat_history=st.session_state.chat_history)
except Exception as e:
    logger.critical("Failed to initialize the chatbot", exc_info=True)
    st.error("Unable to initialize the bot. Check logs for more details.")

st.markdown(utils.styles(), unsafe_allow_html=True)

st.header(":rainbow[Lumina] - :blue[EI Bot] 🤗")

st.sidebar.markdown(utils.sidebar_markdown())

# Display chat history
for message in st.session_state.chat_history:
    for role, content in message.items():
        with st.chat_message(role):
            st.write(content)

# User input
user_input = st.chat_input("Chat With Lumina...")
if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    # Process the user input and generate bot response
    try:
        with st.spinner("Thinking..."):
            response = chatbot.generate_response(user_input)
            message = {'human':user_input, 'AI':response}
            st.session_state.chat_history.append(message)
            with st.chat_message("assistant"):
                st.write(response)
    except Exception as e:
        logger.error(f"Error generating bot response: {e}")
        st.error("An error occurred. Check logs for more details.")
