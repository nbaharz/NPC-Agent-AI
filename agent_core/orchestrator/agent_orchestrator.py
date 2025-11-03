import traceback
from datetime import datetime
from sqlalchemy.orm import Session
from app.database.models import ChatMessage
from agent_core.agent_setup import setup_agent
from agent_core.memory.long_term import add_long_term_memory
from app.repositories.chat_repository import add_message

class AgentOrchestrator:
    def __init__(self, db:Session):
        self.db = db
        self.active_sessions = {} #dict
    
    def _get_or_create_session(self, user_id:str):
        """Creates an active session for each user"""
        if user_id not in self.active_sessions:
            self.active_sessions[user_id] = {"session_start": datetime.utcnow()}
        return self.active_sessions[user_id]  

    async def _generate_response(self, agent, user_input:str):
        """Generates the response of LLM"""
        try:
            response = await agent.ainvoke({"input":user_input})
            if isinstance(response,dict):
                return response.get("output","")
            return str(response)
        except Exception as e :
            print(f"Response error {e}")
            return "Cannot process your request right now."
    
    async def handle_interaction(self, user_id:str, user_input:str, context=None):
        """Main interaction process"""
        try:
            session_context = self._get_or_create_session(user_id)
            agent, memory = setup_agent(user_id= user_id, db= self.db)
            response_text = self.generate_response

            # Add messages to ChatMessage table
            add_message(self.db, user_id,"elara", "user", user_input)
            add_message(self.db, user_id,"elara", "npc", response_text)
          
            # Add long term memory
            add_long_term_memory(
                db=self.db,
                user_id=user_id,
                npc_id="elara",
                text=f"USER: {user_input}\nNPC: {response_text}",
                metadata={"type": "interaction", "timestamp": str(datetime.utcnow())}
            )

            # 6️⃣ Yanıtı döndür
            return response_text
        
        except Exception as e:
            print(f"[Agent Error] {e}")
            traceback.print_exc()
            return "Something went wrong during the interaction."
        


'''
Flow
Frontend → POST /api/agent/chat
↓
AgentOrchestrator.handle_interaction()
↓
setup_agent() → agent.ainvoke()
↓
add_message() (repository)
↓
add_long_term_memory()
↓
Return the response to frontend


'''