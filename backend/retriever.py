from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

CHROMA_DIR = "chroma_db"

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)

def retrieve(query: str, k: int = 3) -> list[str]:
    results = vectorstore.similarity_search(query, k=k)
    return [doc.page_content for doc in results]

if __name__ == "__main__":
    test_query = "What is RAG?"
    chunks = retrieve(test_query)
    for i, chunk in enumerate(chunks, 1):
        print(f"--- Result {i} ---")
        print(chunk)
        print()