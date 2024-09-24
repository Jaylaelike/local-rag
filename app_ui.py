import streamlit as st
import requests
import os

# Define the Flask backend URL
FLASK_BACKEND_URL = "http://localhost:8080"

# Function to upload a file to the Flask backend
def upload_file(file):
    files = {'file': file}
    response = requests.post(f"{FLASK_BACKEND_URL}/embed", files=files)
    return response.json()

# Function to send a query to the Flask backend
def send_query(query):
    data = {'query': query}
    response = requests.post(f"{FLASK_BACKEND_URL}/query", json=data)
    return response.json()

# Streamlit UI
st.title("Local RAG System")

# File Upload Section
st.header("Upload a PDF File")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.write("Uploading file...")
    response = upload_file(uploaded_file)
    if response.get('message') == "File embedded successfully":
        st.success("File uploaded and embedded successfully!")
    else:
        st.error("File upload failed.")

# Chat Section
st.header("Chat with the RAG System")
user_query = st.text_input("Enter your query")

if st.button("Send"):
    if user_query:
        st.write("Processing query...")
        response = send_query(user_query)
        if response.get('message'):
            st.write(f"Response: {response['message']}")
        else:
            st.error("Query processing failed.")
    else:
        st.warning("Please enter a query.")

# Delete Collection Section
st.header("Delete Collection")
if st.button("Delete Collection"):
    response = requests.delete(f"{FLASK_BACKEND_URL}/delete")
    if response.json().get('message') == "Collection deleted successfully":
        st.success("Collection deleted successfully!")
    else:
        st.error("Collection deletion failed.")