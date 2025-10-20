from agent_core.agent_setup import setup_agent
from pydantic import BaseModel
from fastapi import APIRouter
from app.database.models import ChatMessage
from app.database.db_session import SessionLocal
from agent_core.memory.long_term import add_long_term_memory


router = APIRouter()
class ChatInput(BaseModel):
    message: str  # gelen JSON şeması

# Agent ve kısa-özet hafıza yükle (modüler)
agent_executor, memory = setup_agent()

@router.post("/chat")
async def chat(input: ChatInput):
    # Not: run senkron; yüksek trafikte ThreadPoolExecutor ya da asyncio uyumlu çağrı düşünebilirsin
    response = agent_executor.run(input.message)

    # Güncel hafıza özetini dışa aktar (istersen path'i /logs altına al)
    summary_text = getattr(memory, "buffer", "")
    with open("elara_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary_text or "")

    return {"response": response}

def chat_endpoint(user_id: str, user_input: str):
    db = SessionLocal()
    agent, memory = setup_agent(user_id=user_id, db=db)

    # NPC yanıtı üret
    response = agent.run(user_input)

    # ChatMessage tablosuna kaydet
    db.add(ChatMessage(user_id=user_id, npc_id="elara", role="user", content=user_input))
    db.add(ChatMessage(user_id=user_id, npc_id="elara", role="npc", content=response))
    db.commit()

    # 🔹 1️⃣ uzun vadeli hafızaya ekle
    add_long_term_memory(
        db=db,
        user_id=user_id,
        npc_id="elara",
        text=f"USER: {user_input}",
        tags={"role": "user"}
    )
    add_long_term_memory(
        db=db,
        user_id=user_id,
        npc_id="elara",
        text=f"NPC: {response}",
        tags={"role": "npc"}
    )

    return response