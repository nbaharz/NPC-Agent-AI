from langchain.tools import tool
from sqlalchemy.orm import Session
from database.models import WorldState, Inventory, Reputation
from database.db_session import SessionLocal
import uuid

# DB session helper
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@tool("get_world_state", return_direct=False)
def get_world_state_tool(key: str) -> str:
    """Dünya durumundan belirli bir değeri getir."""
    db = SessionLocal()
    row = db.query(WorldState).filter(WorldState.key == key).first()
    db.close()
    return str(row.value) if row else "Bulunamadı"

@tool("set_world_state", return_direct=False)
def set_world_state_tool(key: str, value: dict) -> str:
    """Dünya durumunda belirli bir anahtarı ayarla."""
    db = SessionLocal()
    row = db.query(WorldState).filter(WorldState.key == key).first()
    if row:
        row.value = value
    else:
        row = WorldState(key=key, value=value)
        db.add(row)
    db.commit()
    db.close()
    return f"{key} ayarlandı."

@tool("reputation_change", return_direct=False)
def reputation_change_tool(user_id: str, faction_id: str, delta: float) -> str:
    """Fraksiyon itibarını değiştir."""
    db = SessionLocal()
    row = db.query(Reputation).filter(Reputation.user_id == user_id, Reputation.faction_id == faction_id).first()
    if row:
        row.score += delta
    else:
        row = Reputation(id=str(uuid.uuid4()), user_id=user_id, faction_id=faction_id, score=delta)
        db.add(row)
    db.commit()
    db.close()
    return f"{faction_id} itibarı {delta} değişti."
