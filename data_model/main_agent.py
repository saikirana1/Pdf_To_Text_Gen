from pydantic import BaseModel
from typing import Optional,List,Tuple,Any


class MainAgent(BaseModel):
    sql_query:Optional[str]=None
    sql_result:Optional[Any]=None
    parent_agent:Optional[str]=None
    child_agent:Optional[str]=None
    final_result:Optional[str]=None
    rag_result: Optional[str] = None
class InvoiceAgent(BaseModel):
    sql_query:Optional[str]=None
    sql_result:Optional[str]=None
    parent_agent:Optional[str]=None
    child_agent:Optional[str]=None
    final_result:Optional[str]=None

class DocumentAGENT(BaseModel):
    final_result:Optional[str]=None
    parent_agent:Optional[str]=None
    child_agent:Optional[str]=None
class ReturnData(BaseModel):
    bank_agent: List[MainAgent]
    invoice_agent: List[InvoiceAgent]
    document_agent: List[DocumentAGENT]

