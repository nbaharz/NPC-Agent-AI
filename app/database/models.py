# app/database/models.py
from sqlalchemy import Column, String, DateTime, Text, Integer, Float, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import TypeDecorator
from .db_session import Base
import json
import enum
import os
import uuid

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
    # PostgreSQL ise JSONB kullan, değilse custom JSON type
    if os.getenv("DATABASE_URL", "").startswith("postgres"):
        return Column(JSONB)
    return Column(JSONType)


class LongTermMemory(Base):
    __tablename__ = "long_term_memory"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, index=True, nullable=False)
    npc_id  = Column(String, index=True, nullable=False)
    text    = Column(Text, nullable=False)
    tags    = json_column()
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class WorldState(Base):
    __tablename__ = "world_state"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    key = Column(String, unique=True, index=True)
    value = json_column()
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, index=True)
    item_name = Column(String, index=True)
    qty = Column(Integer, default=1)
    meta = json_column()
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Reputation(Base):
    __tablename__ = "reputation"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, index=True)
    faction_id = Column(String, index=True)
    score = Column(Float, default=0.0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


# QUEST SYSTEM
class QuestStatus(str, enum.Enum):
    locked = "locked"
    active = "active"
    completed = "completed"
    failed = "failed"

class Quest(Base):
    __tablename__ = "quests"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, index=True)
    title = Column(String, nullable=False)
    summary = Column(String, nullable=True)
    status = Column(Enum(QuestStatus), default=QuestStatus.locked, nullable=False)
    meta_json = Column(JSON, default=dict)

    steps = relationship("QuestStep", back_populates="quest", order_by="QuestStep.order")

class StepStatus(str, enum.Enum):
    locked = "locked"
    active = "active"
    completed = "completed"
    failed = "failed"

class QuestStep(Base):
    __tablename__ = "quest_steps"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    quest_id = Column(String, ForeignKey("quests.id"), nullable=False, index=True)
    order = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    status = Column(Enum(StepStatus), default=StepStatus.locked, nullable=False)
    conditions_json = Column(JSON, default=list)
    rewards_json = Column(JSON, default=list)

    quest = relationship("Quest", back_populates="steps")
