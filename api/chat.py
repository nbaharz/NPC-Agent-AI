from agent_setup import setup_agent
from pydantic import BaseModel
from fastapi import APIRouter


router = APIRouter()
class ChatInput(BaseModel):
    message: str  # gelen JSON şeması

# Agent ve kısa-özet hafıza yükle (modüler)
agent_executor, memory = setup_agent()

@router.post("")
async def chat(input: ChatInput):
    # Not: run senkron; yüksek trafikte ThreadPoolExecutor ya da asyncio uyumlu çağrı düşünebilirsin
    response = agent_executor.run(input.message)

    # Güncel hafıza özetini dışa aktar (istersen path'i /logs altına al)
    summary_text = getattr(memory, "buffer", "")
    with open("elara_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary_text or "")

    return {"response": response}