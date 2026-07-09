from pydantic import BaseModel


class ProjectUnderstanding(BaseModel):

    summary: str

    architecture: str

    technologies: list[str]

    entry_points: list[str]

    important_modules: dict[str, str]

    execution_flow: str