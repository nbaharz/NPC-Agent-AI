from langchain.tools import tool
from sqlalchemy.orm import Session
from database.models import WorldState, Inventory, Reputation
from database.db_session import SessionLocal
import uuid

# DB session helper
def get_db():
    """Veritabani oturumu baslatir ve kapatir."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@tool("get_world_state", return_direct=False)
def get_world_state_tool(key: str) -> str:
    """
    Dunya durumundan belirli bir anahtara ait degeri getirir.

    Args:
        key (str): Dunya durumu anahtari (or. 'weather', 'castle_gate_status').

    Returns:
        str: Anahtarin degeri string olarak.
             Anahtar bulunamazsa "Bulunamadi" doner.

    Ornek:
        "weather" -> "Gunesli"
    """
    db = SessionLocal()
    row = db.query(WorldState).filter(WorldState.key == key).first()
    db.close()
    return str(row.value) if row else "Bulunamadi"


@tool("set_world_state", return_direct=False)
def set_world_state_tool(key: str, value: str) -> str:
    """
    Dunya durumunda belirli bir anahtari ayarlar veya gunceller.

    Args:
        key (str): Ayarlanacak dunya durumu anahtari.
        value (str): Yeni deger (string formatinda tutulmasi onerilir).

    Returns:
        str: Ayar yapilan anahtari belirten mesaj.

    Ornek:
        ("weather", "Yagmurlu") -> "weather ayarlandi."
    """
    db = SessionLocal()
    row = db.query(WorldState).filter(WorldState.key == key).first()
    if row:
        row.value = value
    else:
        row = WorldState(key=key, value=value)
        db.add(row)
    db.commit()
    db.close()
    return f"{key} ayarlandi."


@tool("reputation_change", return_direct=False)
def reputation_change_tool(user_id: str, faction_id: str, delta: float) -> str:
    """
    Belirtilen oyuncunun belirli bir fraksiyon ile itibarini degistirir.

    Args:
        user_id (str): Oyuncunun kimligi.
        faction_id (str): Fraksiyon kimligi.
        delta (float): Eklenecek veya cikarilacak itibar degeri.

    Returns:
        str: Degisiklik miktarini belirten mesaj.

    Ornek:
        ("u1", "guild_mages", 5) -> "guild_mages itibari 5 degisti."
    """
    db = SessionLocal()
    row = db.query(Reputation).filter(
        Reputation.user_id == user_id,
        Reputation.faction_id == faction_id
    ).first()

    if row:
        row.score += delta
    else:
        row = Reputation(
            id=str(uuid.uuid4()),
            user_id=user_id,
            faction_id=faction_id,
            score=delta
        )
        db.add(row)
    db.commit()
    db.close()
    return f"{faction_id} itibari {delta} degisti."
