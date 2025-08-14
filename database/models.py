# database/models.py
from sqlalchemy import Column, String, DateTime, Text, Integer, Float
from sqlalchemy.sql import func
from sqlalchemy.dialects.sqlite import JSON as SQLITE_JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import TypeDecorator
from .db_session import Base
import json
import uuid
import os

# SQLite'ta JSON için basit bir wrapper 
class JSONType(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value, ensure_ascii=False)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return json.loads(value)

def json_column():
    # Postgres ise JSONB; değilse custom JSON
    if os.getenv("DATABASE_URL", "").startswith("postgres"):
        return Column(JSONB)
    return Column(JSONType)

class LongTermMemory(Base):
    __tablename__ = "long_term_memory"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True, nullable=False)
    npc_id  = Column(String, index=True, nullable=False)
    text    = Column(Text, nullable=False)
    tags    = json_column()
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class WorldState(Base):
    __tablename__ = "world_state"
    key = Column(String, primary_key=True)
    value = json_column()
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    item_id = Column(String, index=True)
    qty = Column(Integer, default=1)
    meta = json_column()
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Reputation(Base):
    __tablename__ = "reputation"
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    faction_id = Column(String, index=True)
    score = Column(Float, default=0.0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())