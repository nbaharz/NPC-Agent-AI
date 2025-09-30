# main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db_session import Base, engine
from database import models  # noqa: F401  # tabloların create_all için import olması yeterli
from api import memory as memory_api
from pydantic import BaseModel
from agent_setup import setup_agent  
from api import chat as chat_api
from api import world_state as world_api


# --- DB tablolarını oluştur ---
Base.metadata.create_all(bind=engine)

# --- FastAPI app ---
app = FastAPI(title="FRP NPC Agent API")
 
app.include_router(world_api.router, prefix="/api", tags=["world"])

# --- CORS (gerekirse prod'da domain ile sınırla) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # TODO: prod'da ["https://my-domain.com"] yap
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers (hafıza arayüzü) ---
app.include_router(memory_api.router, prefix="/api/memory", tags=["memory"])

app.include_router(chat_api.router,  prefix="/api/chat", tags=["chat"] )