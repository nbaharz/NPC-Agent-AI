from fastapi import FastAPI
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from dotenv import load_dotenv
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

# Chat endpoint
@app.post("/chat")
async def chat(input: ChatInput):
    response = chain.invoke({
        "input": input.message
    })
    return {"response": response}
#new comment line