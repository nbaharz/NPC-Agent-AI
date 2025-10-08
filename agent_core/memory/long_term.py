# memory/long_term.py
import os
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.database.models import LongTermMemory
from agent_core.retrievers.embeddings import get_embedding_fn
from langchain_community.vectorstores import Chroma

#--- We should periodically clean the vector store to avoid excessive data growth and potential storage issues.---
VECTORSTORE_DIR = os.getenv("VECTORSTORE_DIR", "./vectorstore/memory")
COLLECTION_NAME = "long_term_memory"

def _get_vectorstore():
    embed = get_embedding_fn()
    vs = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embed,
        persist_directory=VECTORSTORE_DIR,
    )
    return vs

def add_long_term_memory(
    db: Session,
    *,
    user_id: str,
    npc_id: str,
    text: str,
    tags: Optional[Dict[str, Any]] = None
) -> str:
    """Metni SQLite'a yaz, vektörü Chroma'ya ekle. memory_id döndür."""
    row = LongTermMemory(user_id=user_id, npc_id=npc_id, text=text, tags=tags or {})
    db.add(row)
    db.commit()
    db.refresh(row)

    vs = _get_vectorstore()
    # metadata ile memory_id, user_id, npc_id yaz
    vs.add_texts(
        [text],
        metadatas=[{"memory_id": row.id, "user_id": user_id, "npc_id": npc_id, **(tags or {})}],
        ids=[row.id],
    )
    vs.persist()
    return row.id

def search_long_term_memory(
    db: Session,
    *,
    user_id: str,
    npc_id: str,
    query: str,
    k: int = 5,
    score_threshold: Optional[float] = None
) -> List[Dict[str, Any]]:
    vs = _get_vectorstore()

    # Chroma filter'ı $and ile yap
    filter_where = {
        "$and": [
            {"user_id": user_id},
            {"npc_id": npc_id}
        ]
    }
    docs_scores = vs.similarity_search_with_score(
        query,
        k=k,
        filter={"where": filter_where}  
    )
    results = []
    for doc, score in docs_scores:
        if score_threshold is not None and score > score_threshold:
            continue
        memory_id = doc.metadata.get("memory_id")
        row = db.query(LongTermMemory).filter(LongTermMemory.id == memory_id).first()
        if row:
            results.append({
                "id": row.id,
                "user_id": row.user_id,
                "npc_id": row.npc_id,
                "text": row.text,
                "tags": row.tags,
                "created_at": row.created_at.isoformat() if row.created_at else None,
                "score": float(score),
            })
    return results
