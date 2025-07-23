from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_pipeline import load_document, chunk_documents, create_vectorstore, get_retriever, build_qa_chain

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (frontend)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],  # Allow all headers
)


class Query(BaseModel):
    question: str

# Load the finance document and prepare retriever once when the server starts
pdf_path = "data/personal-finance-guide.pdf"  # Ensure this path is correct
documents = load_document(pdf_path)
chunks = chunk_documents(documents)
vectorstore = create_vectorstore(chunks)
retriever = get_retriever(vectorstore)
qa_chain = build_qa_chain(retriever)

@app.get("/")
def home():
    return {"message": "Finance RAG API is running with real data!"}

@app.post("/ask")
def ask(query: Query):
    answer = qa_chain.run(query.question)
    return {"answer": answer}
