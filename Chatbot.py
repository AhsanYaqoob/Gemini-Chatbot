import streamlit as st
import google.generativeai as genai
import os

# ---------------------------
# API Key Setup
# ---------------------------
# Expect the key in environment variables (safe for GitHub / Streamlit secrets)
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ No API key found! Please set GEMINI_API_KEY in your environment or Streamlit secrets.")
else:
    genai.configure(api_key=api_key)

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.title("💬 Google Gemini Chatbot")

# Model selection dropdown
model_name = st.selectbox(
    "Choose a Gemini model:",
    ["gemini-2.5-flash", "gemini-2.5-pro"],
    index=0
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Show chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input box
if prompt := st.chat_input("Type your message here..."):
    # Append user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gemini response
    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            reply = response.text.strip() if response and response.text else "No response received."
        except Exception as e:
            reply = f"Error: {str(e)}"

        st.markdown(reply)

    # Save response to history
    st.session_state["messages"].append({"role": "assistant", "content": reply})