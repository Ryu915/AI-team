from langgraph.graph import START, END, StateGraph
from state import State

from agents.router import router_node
from agents.planner import planner_node
from human import human_approval_node
from agents.retriever import RetrieverAgent
from agents.coder import coder_node
from agents.reflection import reflection_node

def build_graph(understanding_agent, retriever_agent):

    def understanding_node(state: State):
        return understanding_agent.run(state)
    
    def retriever_node(state: State):
        return retriever_agent.run(state)
    
    # create graph
    graph = StateGraph(State)

    # add nodes
    graph.add_node("understanding", understanding_node)
    graph.add_node("router", router_node)
    graph.add_node("planner", planner_node)
    graph.add_node("human", human_approval_node)
    graph.add_node("retriever", retriever_node)
    graph.add_node("coder", coder_node)
    graph.add_node("reflection", reflection_node)

    # add edges
    graph.add_edge(START, "understanding")
    graph.add_edge("understanding", "router")
    graph.add_edge("planner", "human")
    graph.add_edge("retriever", "coder")
    graph.add_edge("coder", "reflection")

    # add conditional edges
    graph.add_conditional_edges(
        "router",
        lambda state: state["next_agent"],
        {
            "planner": "planner",
            "end": END
        }
    )

    graph.add_conditional_edges(
        "human",
        lambda state: state["approved"],
        {
            True: "retriever",
            False: "planner"
        }
    )

    def reflection_router(state: State):
        if state["reflection"].approved:
            return "approved"
        
        if state["reflection_iteration"] >= 3:
            return "max_attempts"
        
        return "retry"

    graph.add_conditional_edges(
        "reflection",
        reflection_router,
        {
            "approved" : END,
            "retry": "coder",
            "max_attempts" : END
        }
    )

    return graph.compile()
