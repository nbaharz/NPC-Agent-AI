from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from dotenv import load_dotenv
import os

load_dotenv()

# lore.txt'yi yükle
def load_lore_documents(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    return [Document(page_content=line) for line in lines]

# Belgeleri vektör veritabanına ekle
def create_vectorstore():
    documents = load_lore_documents("lore.txt")
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local("lore_index")

if __name__ == "__main__":
    create_vectorstore()