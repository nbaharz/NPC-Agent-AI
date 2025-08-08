# api/memory.py
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session

from database.db_session import get_db
from memory.long_term import add_long_term_memory, search_long_term_memory

router = APIRouter()

class AddMemoryRequest(BaseModel):
    user_id: str = Field(..., description="Kullanıcı kimliği")
    npc_id: str = Field(..., description="NPC kimliği")
    text: str = Field(..., description="Kaydedilecek metin")
    tags: Optional[Dict[str, Any]] = Field(default_factory=dict)

class AddMemoryResponse(BaseModel):
    memory_id: str

class SearchMemoryResponseItem(BaseModel):
    id: str
    user_id: str
    npc_id: str
    text: str
    tags: Optional[Dict[str, Any]]
    created_at: Optional[str]
    score: float

@router.post("/add", response_model=AddMemoryResponse)
def add_memory(req: AddMemoryRequest, db: Session = Depends(get_db)):
    try:
        memory_id = add_long_term_memory(
            db,
            user_id=req.user_id,
            npc_id=req.npc_id,
            text=req.text,
            tags=req.tags
        )
        return AddMemoryResponse(memory_id=memory_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search", response_model=List[SearchMemoryResponseItem])
def search_memory(
    user_id: str = Query(...),
    npc_id: str = Query(...),
    q: str = Query(..., alias="query"),
    k: int = Query(5, ge=1, le=20),
    score_threshold: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):
    try:
        results = search_long_term_memory(
            db,
            user_id=user_id,
            npc_id=npc_id,
            query=q,
            k=k,
            score_threshold=score_threshold
        )
        return [SearchMemoryResponseItem(**r) for r in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
