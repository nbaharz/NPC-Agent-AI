# main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.db_session import Base, engine
from app.api import memory as memory_api
from pydantic import BaseModel
from agent_core.agent_setup import setup_agent  
from app.api import chat as chat_api
from app.api import world_state as world_api
from app.api import inventory as inventory_api


# --- Create DB Tables ---
Base.metadata.create_all(bind=engine)

# --- FastAPI app ---
app = FastAPI(title="FRP NPC Agent API")

#--- Allowed Origins ---
origins = [
    "http://localhost:3000",  # Next.js dev server
    "http://127.0.0.1:3000",
    
]

# --- CORS (gerekirse prod'da domain ile sınırla) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
app.include_router(world_api.router, prefix="/api", tags=["world"])
app.include_router(inventory_api.router, prefix="/api", tags=["inventory"])
app.include_router(memory_api.router, prefix="/api/memory", tags=["memory"])
app.include_router(chat_api.router,  prefix="/api", tags=["chat"] )