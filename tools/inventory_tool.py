from langchain.tools import tool
from sqlalchemy.orm import Session
from database.models import WorldState, Inventory, Reputation
from database.db_session import SessionLocal
import uuid

@tool("inventory_add", return_direct=False)
def inventory_add_tool(user_id: str, item_id: str, qty: int = 1, meta: dict = None) -> str:
    """Envantere eşya ekle veya miktarı arttır."""
    user_id = "u1"
    db = SessionLocal()
    row = db.query(Inventory).filter(Inventory.user_id == user_id, Inventory.item_id == item_id).first()
    if row:
        row.qty += qty
    else:
        row = Inventory(id=str(uuid.uuid4()), user_id=user_id, item_id=item_id, qty=qty, meta=meta or {})
        db.add(row)
    db.commit()
    db.close()
    return f"{qty} adet {item_id} eklendi."


@tool("inventory_remove", return_direct=False)
def inventory_remove_tool(user_id: str, item_id: str, qty: int = 1) -> str:
    """Envanterden eşya çıkar."""
    db = SessionLocal()
    row = db.query(Inventory).filter(Inventory.user_id == user_id, Inventory.item_id == item_id).first()
    if not row:
        db.close()
        return "Eşya bulunamadı."
    if row.qty <= qty:
        db.delete(row)
    else:
        row.qty -= qty
    db.commit()
    db.close()
    return f"{qty} adet {item_id} çıkarıldı."
