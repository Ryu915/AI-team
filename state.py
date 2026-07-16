from typing import TypedDict
from langchain_core.messages import AnyMessage
from schemas.project import ProjectUnderstanding
from models.reflection_output import ReflectionOutput



class State(TypedDict):
    project_path: str
    project_understanding: ProjectUnderstanding | None

    # router
    user_input: str
    next_agent: str
    router_response: str
    chat_history: list[AnyMessage]

    # planner
    plan: list[str]

    # human approval
    approved: bool 
    human_feedback: str 

    # retriever
    retrieved_context: list[str]

    # coder
    code_output: list[str]

    # reflection
    reflection: ReflectionOutput | None
    reflection_iteration: int