import streamlit as st
import requests

API_URL = "http://api:8000"

st.set_page_config(page_title="Gemini RAG App", layout="wide")
st.title("📄 Document Q&A System")

# Upload document
st.header("Upload Document")
uploaded_file = st.file_uploader("Upload PDF, TXT, or DOCX", type=["pdf", "txt", "docx"])

if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    res = requests.post(f"{API_URL}/upload", files=files)

    if res.status_code == 202:
        data = res.json()
        st.success("Document uploaded successfully!")
        st.session_state["document_id"] = data["document_id"]
    else:
        st.error("Upload failed")

# Ask question
if "document_id" in st.session_state:
    st.header("Ask a Question")
    question = st.text_input("Enter your question")

    if st.button("Ask"):
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

# Export PDF
if "session_id" in st.session_state:
    st.header("Export Conversation")
    if st.button("Download PDF"):
        pdf = requests.get(f"{API_URL}/session/{st.session_state['session_id']}/export")
        st.download_button(
            label="Download PDF",
            data=pdf.content,
            file_name="conversation.pdf",
            mime="application/pdf"
        )
