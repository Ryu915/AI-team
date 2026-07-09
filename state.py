from typing import TypedDict

from schemas.project import ProjectUnderstanding


class State(TypedDict):
    project_path: str
    project_understanding: ProjectUnderstanding | None