from fastapi import FastAPI
from pydantic import BaseModel
from src.agent_setup import setup_agent

app = FastAPI()

class ChatInput(BaseModel):
    message: str # Bu model, gelen JSON verisinin nasıl bir yapıya sahip olacağını belirler

# Agent ve hafıza yükle (modüler)
agent_executor, memory = setup_agent()

# Chat endpoint
@app.post("/chat")
async def chat(input: ChatInput):
    response = agent_executor.run(input.message)

    # Güncel hafıza özetini dışa aktar
    summary_text = memory.buffer
    with open("elara_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary_text)

    return {"response": response}