import uuid
import os
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from PyPDF2 import PdfReader
import docx
from fastapi.responses import Response
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from groq import Groq

app = FastAPI()

# --- Groq setup ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
client = Groq(api_key=GROQ_API_KEY)
groq_model = "llama-3.1-8b-instant"

# In-memory storage
documents = {}
document_text = {}
document_chunks = {}
sessions = {}  # session_id -> conversation history


@app.get("/health")
def health_check():
    return {"status": "ok"}


def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    chunk_id = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk
        })
        chunk_id += 1
        start += chunk_size - overlap

    return chunks


def extract_text_and_chunk(document_id: str, file: UploadFile):
    try:
        content = ""

        if file.filename.endswith(".txt"):
            content = file.file.read().decode("utf-8")

        elif file.filename.endswith(".pdf"):
            reader = PdfReader(file.file)
            for page in reader.pages:
                content += page.extract_text() or ""

        elif file.filename.endswith(".docx"):
            doc = docx.Document(file.file)
            for para in doc.paragraphs:
                content += para.text + "\n"

        else:
            documents[document_id] = "failed"
            return

        document_text[document_id] = content
        document_chunks[document_id] = chunk_text(content)
        documents[document_id] = "completed"

    except Exception:
        documents[document_id] = "failed"


@app.post("/upload", status_code=202)
def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):

    if not file.filename.lower().endswith((".pdf", ".txt", ".docx")):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    document_id = str(uuid.uuid4())
    documents[document_id] = "processing"

    background_tasks.add_task(extract_text_and_chunk, document_id, file)

    return {
        "document_id": document_id,
        "filename": file.filename,
        "message": "Document accepted for processing."
    }


@app.get("/documents/{document_id}/status")
def get_document_status(document_id: str):

    if document_id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")

    return {
        "document_id": document_id,
        "status": documents[document_id]
    }


@app.get("/documents/{document_id}/chunks")
def get_document_chunks(document_id: str):

    if document_id not in document_chunks:
        raise HTTPException(status_code=404, detail="Chunks not found")

    return {
        "document_id": document_id,
        "chunks": document_chunks[document_id]
    }


@app.post("/ask")
def ask_question(payload: dict):

    session_id = payload.get("session_id") or str(uuid.uuid4())
    document_ids = payload.get("document_ids", [])
    question = payload.get("question")

    if not question or not document_ids:
        raise HTTPException(status_code=400, detail="Invalid request")

    # Initialize session
    if session_id not in sessions:
        sessions[session_id] = []

    # Save user message
    sessions[session_id].append({
        "role": "user",
        "content": question
    })

    # Retrieve first chunks
    source_chunks = []
    for doc_id in document_ids:
        chunks = document_chunks.get(doc_id, [])
        for chunk in chunks[:2]:
            source_chunks.append({
                "document_id": doc_id,
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"]
            })

    # Build prompt
    chunks_text = "\n\n".join(chunk["text"] for chunk in source_chunks)

    prompt = (
        "You are a helpful assistant. Answer the question only using the "
        "provided document text.\n\n"
        f"Document context:\n{chunks_text}\n\n"
        f"Question:\n{question}\n\n"
        "If the answer is not in the document, say you cannot find it."
    )

    # Call Groq API
    try:
        response = client.chat.completions.create(
            model=groq_model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024
        )

        answer = response.choices[0].message.content

    except Exception as e:
        print(f"[Groq Error] {type(e).__name__}: {e}")
        answer = "This is a mock answer generated from the document content."

    # Save assistant response
    sessions[session_id].append({
        "role": "assistant",
        "content": answer
    })

    return {
        "answer": answer,
        "session_id": session_id,
        "source_chunks": source_chunks,
        "batch_size": len(source_chunks)
    }


@app.get("/session/{session_id}")
def get_session_history(session_id: str):

    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": session_id,
        "history": sessions[session_id]
    }


@app.get("/session/{session_id}/export")
def export_session_pdf(session_id: str):

    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

    for msg in sessions[session_id]:
        role = msg["role"].capitalize()
        content = msg["content"]
        elements.append(Paragraph(f"<b>{role}:</b> {content}", styles["Normal"]))

    pdf.build(elements)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="session_{session_id}.pdf"'
        }
    )