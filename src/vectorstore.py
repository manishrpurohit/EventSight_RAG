from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from src.config import BUSINESS_REPORT, OPERATIONS_REPORT, FAISS_INDEX_DIR, EMBEDDING_MODEL_NAME

def get_embeddings_model():
    """Load and return HuggingFace Embedding model."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

def init_vectorstore(force_rebuild: bool = False):
    """
    Initializes or loads FAISS Vectorstore from local files.
    """
    embeddings = get_embeddings_model()

    # Load existing if available and not forcing rebuild
    if FAISS_INDEX_DIR.exists() and (FAISS_INDEX_DIR / "index.faiss").exists() and not force_rebuild:
        try:
            vector_db = FAISS.load_local(
                str(FAISS_INDEX_DIR),
                embeddings,
                allow_dangerous_deserialization=True
            )
            return vector_db
        except Exception as e:
            print(f"Error loading existing FAISS index ({e}). Rebuilding...")

    pdf_files = [BUSINESS_REPORT, OPERATIONS_REPORT]
    all_documents = []

    for pdf_file in pdf_files:
        if pdf_file.exists():
            loader = PyPDFLoader(str(pdf_file))
            all_documents.extend(loader.load())
        else:
            print(f"Warning: PDF file not found at {pdf_file}")

    if not all_documents:
        raise FileNotFoundError("No PDF documents found to index into FAISS.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    chunks = text_splitter.split_documents(all_documents)

    vector_db = FAISS.from_documents(chunks, embeddings)
    FAISS_INDEX_DIR.mkdir(parents=True, exist_ok=True)
    vector_db.save_local(str(FAISS_INDEX_DIR))
    return vector_db

def retrieve_documents(question: str, k: int = 4) -> List:
    """
    Retrieve top-k relevant document chunks for a question.
    """
    vector_db = init_vectorstore()
    return vector_db.similarity_search(question, k=k)

def create_context(docs: List) -> str:
    """
    Formats document chunks into structured LLM context string.
    """
    context_parts = []
    for doc in docs:
        source = Path(doc.metadata.get("source", "Unknown")).name
        page = doc.metadata.get("page", 0) + 1
        context_parts.append(
            f"SOURCE: {source}\nPAGE: {page}\nCONTENT:\n{doc.page_content}"
        )
    return "\n\n".join(context_parts)

def format_sources(docs: List) -> str:
    """
    Formats document chunks into readable source citation list.
    """
    sources = []
    for doc in docs:
        source = Path(doc.metadata.get("source", "Unknown")).name
        page = doc.metadata.get("page", 0) + 1
        source_text = f"📄 **{source}** — Page {page}"
        if source_text not in sources:
            sources.append(source_text)
    return "\n\n".join(sources)
