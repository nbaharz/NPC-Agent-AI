# agent_setup.py – Agent oluşturma fonksiyonu
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationSummaryMemory
from agent_core.tools.lore_search import lore_search_tool
from agent_core.tools.world_state_tool import get_world_state_tool, set_world_state_tool, reputation_change_tool
from agent_core.tools.inventory_tool import inventory_add_tool, inventory_remove_tool
from agent_core.prompts.promptTemplate import elara_prompt 

load_dotenv()

def setup_agent():
    # LLM model
    llm = ChatOpenAI(
        temperature=0.7,
        model_name="gpt-4",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    # Memory (can be deleted later)
    memory = ConversationSummaryMemory(
        llm=llm,
        memory_key="chat_history",
        return_messages=True
    )

    if os.path.exists("prompts/elara_summary.txt"):
        with open("elara_summary.txt", "r", encoding="utf-8") as f:
            memory.buffer = f.read()

    
    tools = [
        lore_search_tool,
        get_world_state_tool, set_world_state_tool,
        inventory_add_tool, inventory_remove_tool,
        reputation_change_tool
    ]

    # Initilaizing the agent
    agent_executor = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        memory=memory,
        verbose=True,
        agent_kwargs={
            "system_message": elara_prompt.format(chat_history="{chat_history}", input="{input}")
        }
    )

    return agent_executor, memory
