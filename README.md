📄 Gemini RAG Document Q&A System

A containerized document question-answering system that allows users to upload documents and ask questions about their content.
The system uses Retrieval-Augmented Generation (RAG) principles with efficient batching, conversational memory, and source attribution.

🚀 Features

Upload documents (PDF, TXT, DOCX)

Background document processing

Text chunking for retrieval

Chat-based question answering

Conversational session history

Export conversation to PDF

Fully containerized using Docker & Docker Compose

Clean separation of Backend (FastAPI) and Frontend (Streamlit)

🏗️ Architecture
Frontend (Streamlit)
        |
        | HTTP Requests
        v
Backend (FastAPI)
        |
        | In-memory storage
        v
Document Processing & Retrieval

🧰 Tech Stack

Backend: FastAPI (Python)

Frontend: Streamlit

Containerization: Docker, Docker Compose

Document Parsing: PyPDF2, python-docx

PDF Export: reportlab

📂 Project Structure
gemini-rag-app/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
├── .env.example
└── README.md

▶️ How to Run
1️⃣ Create .env file
GEMINI_API_KEY=dummy_key
API_PORT=8000
UI_PORT=8501

2️⃣ Start the application
docker-compose up --build

3️⃣ Open the app

Backend health: http://localhost:8000/health

Frontend UI: http://localhost:8501

🧪 API Endpoints
Endpoint	Method	Description
/health	GET	API health check
/upload	POST	Upload document
/documents/{id}/status	GET	Processing status
/documents/{id}/chunks	GET	Retrieve chunks
/ask	POST	Ask questions
/session/{id}	GET	Conversation history
/session/{id}/export	GET	Export session PDF
📌 Notes

Gemini API is pluggable and can be integrated later.

Mock responses are used for demonstration without API keys.

Designed for scalability and cost-efficiency.

👨‍💻 Author

Paraselli Akhila