import os
from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from embeddings import get_embedding_fn
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VECTORSTORE_DIR = os.getenv("LORE_VECTORSTORE_DIR", "./vectorstore/lore")
COLLECTION_NAME = "lore_entries"


def build_lore_vectorstore(lore_dir: str = "./data/lore"):
    """Lore dosyalarini yükle, temizle, chunk'la ve Chroma'ya ekle."""
    embed_fn = get_embedding_fn()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)

    texts = []
    metadatas = []

    lore_path = Path(lore_dir)
    for file_path in lore_path.rglob("*.md"):
        category = file_path.parent.name  # örn. characters, locations
        content = file_path.read_text(encoding="utf-8").strip()
        chunks = splitter.split_text(content)
        for chunk in chunks:
            texts.append(chunk)
            metadatas.append({
                "source_file": str(file_path),
                "category": category,
                "filename": file_path.name
            })

    vs = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embed_fn,
        persist_directory=VECTORSTORE_DIR
    )

    if texts:
        vs.add_texts(texts=texts, metadatas=metadatas)
        vs.persist()
        print(f"[Lore Pipeline] {len(texts)} chunks indexed into {VECTORSTORE_DIR}")
    else:
        print("[Lore Pipeline] No lore files found.")

def get_lore_vectorstore():
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embedding_fn(),
        persist_directory=VECTORSTORE_DIR
    )

def search_lore(query: str, k: int = 5, category: str = None, threshold: float = 0.75):
    vs = get_lore_vectorstore()

    filter_arg = None
    if category:
        filter_arg = {"where": {"category": category}}

    docs_scores = vs.similarity_search_with_score(query, k=k, filter=filter_arg)

    results = []
    for doc, score in docs_scores:
        if float(score) <= threshold:   
         results.append(...)


    return results

if __name__ == "__main__":
    build_lore_vectorstore()