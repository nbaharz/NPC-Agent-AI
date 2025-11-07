from pydantic import BaseModel
from fastapi import APIRouter ,Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db_session import get_db
from app.services.token_service import get_current_user
from agent_core.core.orchestrator.agent_orchestrator import AgentOrchestrator


router = APIRouter()
class ChatInput(BaseModel):
    message: str

@router.post("/chat")
async def chat(input: ChatInput, db:Session = Depends(get_db),
               current_user= Depends(get_current_user)):
    """Recevies the user input, and returns the response by the orchestrator"""
    try:
        orchestrator = AgentOrchestrator(db)
        response = await orchestrator.handle_interaction(
            user_id = current_user.id,
            user_input=input.message
        )

        return {"npc_id": "elara", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/end-session")
async def end_session(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Ends the user's active chat session, generates a session summary,
    and stores it in long-term memory.
    """
    try:
        orchestrator = AgentOrchestrator(db)

        summary = await orchestrator.end_session(user_id=current_user.id)

        return {
            "message": "Session ended and summarized successfully.",
            "summary": summary
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to end session: {e}")

#NOT: Depends() fonksiyonu => Bu endpoint şu fonksiyona bağımlı, önce onu çalıştır, sonucunu bana ver.