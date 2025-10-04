from pydantic import BaseModel
from typing import Optional
class DataDecision(BaseModel):
    agent:Optional[str]=None