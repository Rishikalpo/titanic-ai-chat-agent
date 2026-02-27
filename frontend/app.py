import streamlit as st
import requests
import base64

API_URL = "http://localhost:8000/chat"

st.set_page_config(page_title="Titanic AI Chatbot", layout="centered")

st.title("🚢 Titanic Dataset AI Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ask something about Titanic dataset...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

    with st.spinner("Thinking..."):
        response = requests.post(API_URL, json={"message": user_input})
        data = response.json()

    st.session_state.chat_history.append(("assistant", data))

for role, content in st.session_state.chat_history:
    if role == "user":
        st.chat_message("user").write(content)
    else:
        st.chat_message("assistant").write(content["answer"])
        if content["chart"]:
            image_bytes = base64.b64decode(content["chart"])
            st.image(image_bytes)