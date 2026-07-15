from loader.loader import ProjectLoader
from agents.understanding import UnderstandingAgent
from agents.router import router_node
from agents.planner import planner_node
from agents.retriever import RetrieverAgent
from human import human_approval_node 
from models.llm import get_llm
from state import State
from graph import build_graph

loader = ProjectLoader()
vector_store = loader.load("/Users/ishaan915/Me/projects/logo-processor")

    # Create the LLM
llm = get_llm()

    # Create the Understanding Agent
understanding_agent = UnderstandingAgent(
    llm=llm,
    vector_store=vector_store
)

retriever_agent = RetrieverAgent(
    vector_store=vector_store
)

graph = build_graph(understanding_agent, retriever_agent)

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

    # this is the main graph
    state = graph.invoke(state)
    print(state["next_agent"])
    print(state["router_response"])

    # till here

    """
    # this is for testing
    state = router_node(state)

    print(f"\nRoute: {state['next_agent']}")
    print(f"Router: {state['router_response']}")
    print(f"Touer: {state['chat_history']}")

    if state["next_agent"] == "planner":

        state = planner_node(state)

        state = human_approval_node(state)
    
    if state["next_agent"] == "retriever":

        retriever_agent = RetrieverAgent(vector_store)

        state = retriever_agent.run(state)
        print("\n==========Retriever===========")
        print(f"\n Retriever: {state['retrieved_context']}")

    #till  here
    """


    if state["next_agent"] == "end":
        break
  
