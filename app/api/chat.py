from pydantic import BaseModel
from fastapi import APIRouter ,Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db_session import get_db
from agent_core.orchestrator.agent_orchestrator import AgentOrchestrator


router = APIRouter()
class ChatInput(BaseModel):
    user_id: str
    message: str

@router.post("/chat")
async def chat(input: ChatInput, db:Session = Depends(get_db)):
    """Recevies the user input, and returns the response by the orchestrator"""
    try:
        orchestrator = AgentOrchestrator(db)
        response = await orchestrator.handle_interaction(
            user_id=input.user_id, #burasi farkli olmali
            user_input=input.message
        )

        return {"npc_id": "elara", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


