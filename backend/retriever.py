from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

CHROMA_DIR = "chroma_db"

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)

def retrieve(query: str, k: int = 3) -> list[str]:
    results = vectorstore.similarity_search(query, k=k)
    return [doc.page_content for doc in results]

def add_document_to_index(filepath: str, filename: str):
    """Extract, chunk, and embed a single PDF into the existing Chroma index."""
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    doc = Document(page_content=text, metadata={"source": filename})
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents([doc])

    vectorstore.add_documents(chunks)
    return len(chunks)

if __name__ == "__main__":
    test_query = "What is RAG?"
    chunks = retrieve(test_query)
    for i, chunk in enumerate(chunks, 1):
        print(f"--- Result {i} ---")
        print(chunk)
        print()