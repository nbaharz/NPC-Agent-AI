from fastapi import FastAPI
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from dotenv import load_dotenv
from tools import lore_search
from langchain.agents import initialize_agent, AgentType
import os
import promptTemplate

 # .env dosyasını yükle
load_dotenv()

# FastAPI uygulamasını başlat
app = FastAPI()

# Kullanıcıdan gelen veriyi tanımla
class ChatInput(BaseModel):
    message: str


memory= ConversationBufferMemory(memory_key="chat_history", input_key="input");

prompt= promptTemplate.prompt_template

llm = ChatOpenAI(
    temperature=0.7, #modelin cevaplarının rastgeleliğini ayarlar
    model_name="gpt-4",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
# Kısa süreli bellek
memory = ConversationBufferMemory(memory_key="chat_history")

# LLM zinciri
chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory
)

tools = [lore_search]

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory
)

# Chat endpoint
@app.post("/chat")
async def chat(input: ChatInput):
    response = agent_executor.run(input.message)
    return {"response": response}
