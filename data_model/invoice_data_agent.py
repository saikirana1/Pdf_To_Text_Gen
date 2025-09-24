from typing import Optional,List
from pydantic import BaseModel


class InvoiceAgent(BaseModel):
    agent: Optional[str] = None
    sql_query: Optional[str] = None
    sql_result: Optional[str] = None 
    final_result: Optional[str] = None 