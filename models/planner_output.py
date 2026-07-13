from pydantic import BaseModel, Field

class PlanStep(BaseModel):
    step_no: int
    description: str

class PlanOutput(BaseModel):
    """
    Structured output returned by the Planner Agent.
    """
    goal: str
    steps: list[PlanStep]

    files_to_modify: list[str] = Field(default_factory=list)
    new_files: list[str] = Field(default_factory=list)
    retrieval_targets : list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
