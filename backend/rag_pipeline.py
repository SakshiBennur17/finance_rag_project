import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# Load environment variables (like OpenAI API key)
load_dotenv()

# -----------------------------
# STEP 1: LOAD DOCUMENT
# -----------------------------
def load_document(file_path):
    """Loads PDF and returns it as a list of Documents."""
    loader = PyPDFLoader(file_path)
    return loader.load()

# -----------------------------
# STEP 2: SPLIT INTO CHUNKS
# -----------------------------
def chunk_documents(documents):
    """Splits documents into smaller chunks (for better retrieval)."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(documents)

# -----------------------------
# STEP 3: CREATE VECTOR STORE
# -----------------------------
def create_vectorstore(chunks):
    """Converts text chunks into embeddings and stores them in Chroma DB."""
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    vectorstore = Chroma.from_documents(chunks, embedding=embeddings)
    return vectorstore

# -----------------------------
# STEP 4: CREATE RETRIEVER
# -----------------------------
def get_retriever(vectorstore):
    """Creates a retriever (search engine) from vectorstore."""
    return vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# -----------------------------
# STEP 5: BUILD QA CHAIN
# -----------------------------
def build_qa_chain(retriever):
    """Creates a Question-Answer pipeline using GPT + retriever."""
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )
    return qa_chain
