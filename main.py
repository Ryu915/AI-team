from loader.loader import ProjectLoader
from agents.understanding import UnderstandingAgent
from agents.router import router_node
from agents.planner import planner_node
from agents.retriever import RetrieverAgent
from human import human_approval_node 
from models.llm import get_llm
from state import State
from graph import build_graph

def get_project_path(loader):
    while True:
        project_path = input("\nEnter project path: ").strip()
    
        try:
            vector_store = loader.load(project_path)
            return project_path, vector_store

        except Exception as e:
            print(f"\nError: {e}")
            print("\nInvalid project directory\n")

def main():
    loader = ProjectLoader()
    #vector_store = loader.load("/Users/ishaan915/Me/projects/crypto")
    project_path, vector_store = get_project_path(loader)

    # Create LLM instance
    llm = get_llm()

    # Create the Understanding Agent
    understanding_agent = UnderstandingAgent(
        llm=llm,
        vector_store=vector_store
    )

    retriever_agent = RetrieverAgent(
        vector_store=vector_store
    )

    graph = build_graph(llm, vector_store, retriever_agent)

        # Initial state
    state: State = {
        "project_path": project_path,
        "project_understanding": None,

        "user_input": "",
        "next_agent": "",
        "router_response": "",
        "chat_history": [],
        "reflection": None,
        "reflection_iteration": 0
    }

        # Run the agent
    state = understanding_agent.run(state)

        # Print the result
    print("\n========== PROJECT UNDERSTANDING ==========\n")
    print(state["project_understanding"])

    while True:

        state["user_input"] = input("\nYou: ")
        state["reflection_iteration"] = 0

        # this is the main graph
        state = graph.invoke(state)

        # till here

        if state["next_agent"] == "end":
            break
    
if __name__ == "__main__":
    main()

    

