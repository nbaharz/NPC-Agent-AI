# retrievers/embeddings.py
import os
from langchain_openai import OpenAIEmbeddings

def get_embedding_fn():
    # Gerekirse burada model_adi ayarlayabilirsin: text-embedding-3-small / large
    return OpenAIEmbeddings(model="text-embedding-3-small", api_key=os.getenv("OPENAI_API_KEY"))
