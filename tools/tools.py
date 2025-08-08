from langchain.tools import tool
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema.retriever import BaseRetriever
import os

# @tool
# def lore_search(query: str) -> str:
#     """
#     Oyun evrenine dair bilgileri döndürür.
#     Örnek: 'Yasaklı Tapınak hakkında bilgi ver' gibi sorular için kullanılır.
#     """
#     embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
#     vectorstore = FAISS.load_local("lore_index", embeddings, allow_dangerous_deserialization=True)
#     retriever = vectorstore.as_retriever()
#     docs = retriever.get_relevant_documents(query)
#     return "\n".join(doc.page_content for doc in docs)

@tool
def inventory_tool(query: str) -> str:
    """
    Elara'nın mevcut envanterini döndürür.
    Kullanıcı envanter hakkında soru sorarsa bu araç tetiklenir.
    """
    inventory = [
        "⛓️ Gümüş zincirli kadim bir kolye",
        "📜 Büyülü yazıtlarla dolu bir parşömen",
        "🌿 Şifa otlarından yapılmış iksir",
        "🗡️ Gölge Çeliği'nden yapılmış eski bir hançer"
    ]
    return "\n".join(inventory)
