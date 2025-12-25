from typing import Optional
from pydantic import BaseModel

#inputs
class AgentInput(BaseModel):
    value: float
    value2: Optional[float] = None
    percentage: Optional[float] = None
    operation: Optional[str] = None

#outputs
class AgentOutput(BaseModel):
    value: float
    agent: str
    status: str
    details: str
