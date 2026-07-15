from pydantic import BaseModel
from typing import Literal

class CodeChange(BaseModel):
    file_path: str
    action: Literal["create", "update", "delete"] # create / update / delete
    code: str
    description: str

class CoderOutput(BaseModel):
    changes: list[CodeChange]
    explanation: str