"""
app.py - the web page for the chat assistant (built with Streamlit).

Run it with:   streamlit run app.py

All the AI logic lives in chat_logic.py; this file only handles the screen.
"""

import streamlit as st

from chat_logic import (
    MissingAPIKeyError,
    friendly_error_message,
    get_answer,
    load_settings,
)

# --- Page setup -------------------------------------------------------------
st.set_page_config(page_title="AI chat assistant", page_icon=":material/forum:")

settings = load_settings()

# --- Memory: one list of messages per browser tab, kept between reruns ------
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar: New Chat button and info --------------------------------------
with st.sidebar:
    st.header("Chat options")
    if st.button("New chat", icon=":material/add_comment:", width="stretch"):
        st.session_state.messages = []
        st.rerun()

    st.caption(f"Model: `{settings.model}`")
    st.caption(f"Memory: the last {settings.max_history} messages")

# --- Title and description --------------------------------------------------
st.title(":material/forum: AI chat assistant")
st.caption(
    "Ask me anything! I remember the recent conversation, so you can ask "
    "follow-up questions. Click **New chat** in the sidebar to start fresh."
)

if not settings.api_key:
    st.warning(friendly_error_message(MissingAPIKeyError()), title="Setup needed")

# --- Show the conversation so far -------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Handle a new question --------------------------------------------------
question = st.chat_input("Type your message...", submit_mode="disable")

if question:
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                answer = get_answer(question, st.session_state.messages, settings)
        except Exception as error:
            # Show a friendly message only - never the raw error (it could contain secrets).
            st.error(friendly_error_message(error), title="Couldn't get an answer")
        else:
            st.markdown(answer)
            # Save both sides only when it worked, so errors never enter the memory.
            st.session_state.messages.append({"role": "user", "content": question})
            st.session_state.messages.append({"role": "assistant", "content": answer})
