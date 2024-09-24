import streamlit as st
import requests
import time

# Define the Flask backend URL
FLASK_BACKEND_URL = "http://localhost:8080"

# Function to send a query to the Flask backend
def send_query(query):
    data = {'query': query}
    response = requests.post(f"{FLASK_BACKEND_URL}/query", json=data)
    return response.json()

# Streamlit UI
st.title("Chatbot UI")

# Chat Interface
st.header("Chat with the RAG System")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# User input
user_query = st.text_input("You:")

if st.button("Send"):
    if user_query:
        # Add user query to chat history
        st.session_state.chat_history.append(("You", user_query))

        # Display user query in chat history
        st.write(f"You: {user_query}")

        # Simulate typing effect
        typing_placeholder = st.empty()
        typing_placeholder.text("Bot is typing...")

        # Send query to the backend and get the response
        response = send_query(user_query)
        if response.get('message'):
            # Remove typing effect
            typing_placeholder.empty()

            # Add bot response to chat history
            st.session_state.chat_history.append(("Bot", response['message']))

            # Display bot response in chat history
            st.write(f"Bot: {response['message']}")
        else:
            # Remove typing effect
            typing_placeholder.empty()
            st.error("Query processing failed.")
    else:
        st.warning("Please enter a query.")

# Display chat history
for sender, message in st.session_state.chat_history:
    st.write(f"{sender}: {message}")