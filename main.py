from loader.loader import ProjectLoader
from agents.understanding import UnderstandingAgent
from models.llm import get_llm
from state import State

loader = ProjectLoader()
vector_store = loader.load("/Users/ishaan915/Me/projects/logo-processor")
print(loader.vector_store.peek())

    # Create the LLM
llm = get_llm()

    # Create the Understanding Agent
understanding_agent = UnderstandingAgent(
    llm=llm,
    vector_store=vector_store
)

    # Initial state
state: State = {
    "project_path": "/Users/ishaan915/Me/projects/logo-processor",
    "project_understanding": None
}

    # Run the agent
state = understanding_agent.run(state)

    # Print the result
print("\n========== PROJECT UNDERSTANDING ==========\n")
print(state["project_understanding"])
 
 