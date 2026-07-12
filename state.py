from typing import TypedDict
from langchain_core.messages import AnyMessage
from schemas.project import ProjectUnderstanding



class State(TypedDict):
    project_path: str
    project_understanding: ProjectUnderstanding | None

    # router
    user_input: str
    next_agent: str
    router_response: str
    chat_history: list[AnyMessage]

    approved: bool # for human approval
    review_status: str # same
