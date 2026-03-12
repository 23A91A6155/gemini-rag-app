# 📄 Document Q&A System (RAG Powered)

A containerized document question-answering system that allows users to upload documents and ask questions about their content.

The system uses **Retrieval-Augmented Generation (RAG)** principles with efficient batching, conversational memory, and source attribution.

---

# 🚀 Features

- Upload documents (**PDF, TXT, DOCX**)
- Background document processing
- Text chunking for efficient retrieval
- Chat-based question answering
- Conversational session history
- Export conversation to **PDF**
- Fully containerized using **Docker & Docker Compose**
- Clean separation of **Backend (FastAPI)** and **Frontend (Streamlit)**
- LLM-powered answers using **Groq API**

---

# 🏗️ Architecture

Frontend (Streamlit)
|
| HTTP Requests
v
Backend (FastAPI)
|
| In-memory storage
v
Document Processing & Retrieval
|
| Context + Prompt
v
Groq LLM (Llama 3)


---

# 🧰 Tech Stack

**Backend**
- FastAPI
- Python

**Frontend**
- Streamlit

**LLM**
- Groq API (Llama 3)

**Containerization**
- Docker
- Docker Compose

**Document Processing**
- PyPDF2
- python-docx

**PDF Export**
- reportlab

---

# 📂 Project Structure


gemini-rag-app/
│
├── backend/
│ ├── main.py
│ ├── requirements.txt
│ └── Dockerfile
│
├── frontend/
│ ├── app.py
│ ├── requirements.txt
│ └── Dockerfile
│
├── docker-compose.yml
├── .env.example
└── README.md


---

# ▶️ How to Run

## 1️⃣ Create `.env` file

Create a `.env` file in the root directory.


GROQ_API_KEY=your_api_key_here
API_PORT=8000
UI_PORT=8501


---

## 2️⃣ Start the application

Run the following command from the project root:


docker-compose up --build


---

## 3️⃣ Open the application

Backend health check:


http://localhost:8000/health


Frontend UI:


http://localhost:8501


---

# 🧪 API Endpoints

| Endpoint | Method | Description |
|--------|--------|--------|
| `/health` | GET | API health check |
| `/upload` | POST | Upload document |
| `/documents/{id}/status` | GET | Document processing status |
| `/documents/{id}/chunks` | GET | Retrieve document chunks |
| `/ask` | POST | Ask question about documents |
| `/session/{id}` | GET | Conversation history |
| `/session/{id}/export` | GET | Export conversation as PDF |

---

# ⚙️ System Workflow

1. User uploads a document (PDF, TXT, DOCX)
2. Backend extracts text from the document
3. Text is split into **smaller chunks**
4. Relevant chunks are retrieved based on the question
5. Context + question are sent to the **Groq LLM**
6. LLM generates an answer
7. Conversation history is stored
8. Users can export the conversation as **PDF**

---

# 📌 Notes

- The system follows **RAG architecture** for document-based question answering.
- Document processing is done **asynchronously** in the background.
- The system stores conversation history **in memory** for each session.
- Groq LLM integration enables fast and cost-efficient inference.

---

# 👨‍💻 Author

**Paraselli Akhila**
