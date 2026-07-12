from loader.loader import ProjectLoader
from agents.understanding import UnderstandingAgent
from agents.router import router_node
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
    "project_understanding": None,

    "user_input": "",
    "next_agent": "",
    "router_response": "",
    "chat_history": []
}

    # Run the agent
state = understanding_agent.run(state)

    # Print the result
print("\n========== PROJECT UNDERSTANDING ==========\n")
print(state["project_understanding"])

while True:

    state["user_input"] = input("\nYou: ")

    state = router_node(state)

    print(f"\nRoute: {state['next_agent']}")
    print(f"Router: {state['router_response']}")

    if state["next_agent"] == "end":
        break
 