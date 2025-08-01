### agent_setup.py – Agent oluşturma fonksiyonu
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationSummaryMemory
from src.tools import lore_search, inventory_tool

load_dotenv()

def setup_agent():
    # LLM modeli
    llm = ChatOpenAI(
        temperature=0.7, #rastgelelik derecesi
        model_name="gpt-4",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    # Hafıza – konuşma özetleriyle birlikte
    memory = ConversationSummaryMemory(
        llm=llm,
        memory_key="chat_history",
        return_messages=True
    )

    if os.path.exists("src/text_files/elara_summary.txt"):
        with open("elara_summary.txt", "r", encoding="utf-8") as f:
         memory.buffer = f.read()

    # Prompt yükle
    with open("src/text_files/system_prompt.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # Araçları tanımla
    tools = [lore_search, inventory_tool]

    # Agent'i başlat
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

    return agent_executor, memory

