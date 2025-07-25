from pydantic import BaseModel
import time
# ---------------------------
# Pydantic Schemas (Optimized)
# ---------------------------
class Triple(BaseModel):
    subject: str
    predicate: str
    object: str
    context: str | None = None

class InteractionLog(BaseModel):
    event: str
    details: str
    timestamp: float = time.time()

class Workflow(BaseModel):
    name: str
    steps: list[str]
    completed: bool = False
    last_updated: float = time.time()

class UserInfo(BaseModel):
    username: str 
    
