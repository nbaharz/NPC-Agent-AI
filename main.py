# main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db_session import Base, engine
from database import models  # noqa: F401  # tabloların create_all için import olması yeterli
from api import memory as memory_api
from pydantic import BaseModel
from agent_setup import setup_agent  
from api import world_state as world_api



# --- DB tablolarını oluştur ---
Base.metadata.create_all(bind=engine)

# --- FastAPI app ---
app = FastAPI(title="FRP NPC Agent API")
 
app.include_router(world_api.router, prefix="/api", tags=["world"])

# --- CORS (gerekirse prod'da domain ile sınırla) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # TODO: prod'da ["https://my-domain.com"] yap
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers (hafıza arayüzü) ---
app.include_router(memory_api.router, prefix="/api/memory", tags=["memory"])

# --- Healthcheck ---
@app.get("/health")
def health():
    return {"status": "ok"}

# Chat endpoint 
class ChatInput(BaseModel):
    message: str  # gelen JSON şeması

# Agent ve kısa-özet hafıza yükle (modüler)
agent_executor, memory = setup_agent()

@app.post("/chat")
async def chat(input: ChatInput):
    # Not: run senkron; yüksek trafikte ThreadPoolExecutor ya da asyncio uyumlu çağrı düşünebilirsin
    response = agent_executor.run(input.message)

    # Güncel hafıza özetini dışa aktar (istersen path'i /logs altına al)
    summary_text = getattr(memory, "buffer", "")
    with open("elara_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary_text or "")

    return {"response": response}
