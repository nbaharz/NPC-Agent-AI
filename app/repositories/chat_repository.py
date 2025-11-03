from app.database.models import ChatMessage

class ChatRepository:
    def __init__(self, db):
        self.db = db

    def add_message(self, user_id, npc_id, role, content):
        message = ChatMessage(
            user_id=user_id,
            npc_id=npc_id,
            role=role,
            content=content,
        )
        self.db.add(message)
        self.db.commit()
        return message
