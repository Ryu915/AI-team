from typing import Literal
from pydantic import BaseModel

class RouterOutput(BaseModel):
    """
    structured output returned by router LLM.
    """
    next_agent: Literal[
        "planner",
        "retriever",

        "end"
    ]

    message: str