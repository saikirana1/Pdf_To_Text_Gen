from pydantic import BaseModel
from typing import List, Tuple

class Student(BaseModel):
    name: str
    age: int

class DataResponse(BaseModel):
    students: List[Student]
    position: Tuple[float, float]
