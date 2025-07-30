from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from tools import lore_search, inventory_tool

load_dotenv()

app = FastAPI()

class ChatInput(BaseModel):
    message: str

# LLM modeli
llm = ChatOpenAI(
    temperature=0.7,
    model_name="gpt-4",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Kısa süreli hafıza
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Tools (araçlar)
tools = [lore_search, inventory_tool]

# Okunacak sistem prompt dosyası
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

# AgentExecutor oluştur
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    memory=memory,
    verbose=True,
    agent_kwargs={
        "system_message": system_prompt
    }
)

# Chat endpoint
@app.post("/chat")
async def chat(input: ChatInput):
    response = agent_executor.run(input.message)
    return {"response": response}
