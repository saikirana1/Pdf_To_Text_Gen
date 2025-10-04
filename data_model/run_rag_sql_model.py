from pydantic import BaseModel
from typing import Optional, Any

class SqlRagaent(BaseModel):
    agent: Optional[str] = None
    sql_query: Optional[str] = None
    sql_result: Optional[Any] = None
    final_result: Optional[str] = None 

