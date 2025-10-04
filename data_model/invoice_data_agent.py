from typing import Optional, List, Any
from pydantic import BaseModel


class InvoiceAgent(BaseModel):
    agent: Optional[str] = None
    sql_query: Optional[str] = None
    sql_result: Optional[Any] = None
    final_result: Optional[str] = None
    rag_result: Optional[str] = None