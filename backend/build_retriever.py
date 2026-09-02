import os
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

UPLOADS_DIR = "uploads"
CHROMA_DIR = "chroma_db"

def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def load_all_documents():
    docs = []
    for filename in os.listdir(UPLOADS_DIR):
        if filename.endswith(".pdf"):
            filepath = os.path.join(UPLOADS_DIR, filename)
            print(f"Extracting: {filename}")
            text = extract_text_from_pdf(filepath)
            docs.append(Document(page_content=text, metadata={"source": filename}))
    return docs

def build_vector_store():
    raw_docs = load_all_documents()
    print(f"Loaded {len(raw_docs)} documents")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(raw_docs)
    print(f"Split into {len(chunks)} chunks")

    print("Loading embedding model (first run downloads it, may take a minute)...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print("Building Chroma vector store...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    print(f"Done. Vector store saved to {CHROMA_DIR}/")
    return vectorstore

if __name__ == "__main__":
    build_vector_store()