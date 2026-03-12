import streamlit as st
import requests
import time

API_URL = "http://api:8000"

st.set_page_config(page_title="Groq RAG App", layout="wide")
st.title("📄 Document Q&A System (Powered by Groq)")

# Initialize session state
if "document_id" not in st.session_state:
    st.session_state["document_id"] = None

if "session_id" not in st.session_state:
    st.session_state["session_id"] = None


# -----------------------------
# Upload Document
# -----------------------------
st.header("Upload Document")

uploaded_file = st.file_uploader(
    "Upload PDF, TXT, or DOCX",
    type=["pdf", "txt", "docx"]
)

if uploaded_file and st.session_state["document_id"] is None:

    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}

    res = requests.post(f"{API_URL}/upload", files=files)

    if res.status_code == 202:
        data = res.json()

        st.session_state["document_id"] = data["document_id"]

        st.success("Document uploaded successfully!")

        # Wait for document processing
        with st.spinner("Processing document..."):
            for _ in range(10):
                status_res = requests.get(
                    f"{API_URL}/documents/{st.session_state['document_id']}/status"
                )
                status_data = status_res.json()

                if status_data["status"] == "completed":
                    st.success("Document processed and ready!")
                    break

                time.sleep(1)

    else:
        st.error("Upload failed")


# -----------------------------
# Ask Question
# -----------------------------
if st.session_state["document_id"]:

    st.header("Ask a Question")

    question = st.text_input("Enter your question")

    if st.button("Ask") and question:

        payload = {
            "document_ids": [st.session_state["document_id"]],
            "question": question
        }

        res = requests.post(f"{API_URL}/ask", json=payload)

        if res.status_code == 200:

            data = res.json()

            st.session_state["session_id"] = data["session_id"]

            st.write("### Answer")
            st.write(data["answer"])

        else:
            st.error("Failed to get answer")


# -----------------------------
# Export Conversation
# -----------------------------
if st.session_state["session_id"]:

    st.header("Export Conversation")

    if st.button("Download PDF"):

        pdf = requests.get(
            f"{API_URL}/session/{st.session_state['session_id']}/export"
        )

        st.download_button(
            label="Download PDF",
            data=pdf.content,
            file_name="conversation.pdf",
            mime="application/pdf"
        )