import streamlit as st
from agent import ask

st.set_page_config(page_title="Placement Prep Copilot")

st.title("🎓 Placement Prep Copilot")

# session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "1"

# sidebar
with st.sidebar:
    st.header("About")
    st.write("AI assistant for placement preparation.")
    
    if st.button("New Conversation"):
        st.session_state.messages = []
        st.session_state.thread_id = str(int(st.session_state.thread_id) + 1)

# display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# input
user_input = st.chat_input("Ask your question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    response = ask(user_input, st.session_state.thread_id)

    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})