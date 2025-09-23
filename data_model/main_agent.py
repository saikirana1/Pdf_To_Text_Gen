from pydantic import BaseModel
from typing import Optional,List,Tuple


class BankAgent(BaseModel):
    sql_query:Optional[str]=None
    sql_result:Optional[str]=None
    parent_agent:Optional[str]=None
    child_agent:Optional[str]=None

class InvoiceAgent(BaseModel):
    sql_query:Optional[str]=None
    sql_result:Optional[str]=None
    parent_agent:Optional[str]=None
    child_agent:Optional[str]=None

class DocumentAGENT(BaseModel):
    final_result:Optional[str]=None
    parent_agent:Optional[str]=None
    child_agent:Optional[str]=None

class ReturnData(BaseModel):
  bank_agent=List[BankAgent]
  invoice_agent=List[InvoiceAgent]
  document_agent=List[DocumentAGENT]

