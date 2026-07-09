from langchain_core.messages import SystemMessage, HumanMessage

from prompts.understanding import UNDERSTANDING_SYSTEM_PROMPT
from schemas.project import ProjectUnderstanding

class UnderstandingAgent:

    def __init__(self, llm , vector_store):
        self.llm = llm
        self.vector_store = vector_store # retrieves from chromaDb
        self.structured_llm = self.llm.with_structured_output(ProjectUnderstanding)

    def run(self, state):
        context = self._retrieve_context()

        understanding = self._invoke_llm(context)

        state["project_understanding"] = understanding

        return state
    
    def _retrieve_context(self):
        query = """
Understand this software project.
Find the project purpose, architecture,
important modules, technologies,
entry points and execution flow.
"""

        context = self.vector_store.search(query)

        return context

    def _invoke_llm(self, context: str) -> ProjectUnderstanding:
        
        

        messeges = [
            SystemMessage(content = UNDERSTANDING_SYSTEM_PROMPT),
            HumanMessage(
                content = f"""
Project Context: 
{context}
Analyse the project and return the project understanding.

"""
            ),
        ]

        understanding = self.structured_llm.invoke(messeges)

        return understanding

