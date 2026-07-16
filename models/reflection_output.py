from pydantic import BaseModel

class ReflectionOutput(BaseModel):
    approved: bool
    feedback: str
    issues: list[str]