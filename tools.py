
from langchain.tools import tool
from langchain.schema import Document
from langchain.schema.retriever import BaseRetriever
from typing import List

# Sahte retriever – test amaçlı
class FakeRetriever(BaseRetriever):
    def _get_relevant_documents(self, query: str) -> List[Document]:
        return [
            Document(page_content="Yasaklı Tapınak, Gölgeler Savaşı’ndan sonra inşa edilmiştir."),
            Document(page_content="Rüya Krallığı’nın kralı Elenion’dur."),
        ]

    async def _aget_relevant_documents(self, query: str) -> List[Document]:
        return self._get_relevant_documents(query)


@tool
def lore_search(query: str) -> str:
    """
    Oyun evrenine dair bilgileri döndürür.
    Örnek: 'Yasaklı Tapınak hakkında bilgi ver' gibi sorular için kullanılır.
    """
    retriever = FakeRetriever()
    docs = retriever.get_relevant_documents(query)
    return "\n".join(doc.page_content for doc in docs)

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
