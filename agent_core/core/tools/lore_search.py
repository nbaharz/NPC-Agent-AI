# tools/lore_search.py
from langchain.tools import tool
from agent_core.core.retrievers.lore_retriever import search_lore

@tool("lore_search", return_direct=False)
def lore_search_tool(query: str) -> str:
    """
    Evren bilgisinden (lore) arama yapar.
    query: Aranacak kelime veya cümle.
    Sonuçları kaynak bilgisiyle döndürür.
    """
    results = search_lore(query)
    if not results:
        return "Evren bilgisinde ilgili bilgi bulunamadı."
    
    output_lines = []
    for r in results:
        meta = r["metadata"]
        output_lines.append(
            f"[{meta.get('category')}] {meta.get('filename')}: {r['text'][:200]}..."
        )
    return "\n".join(output_lines)
