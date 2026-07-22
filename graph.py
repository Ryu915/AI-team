from langgraph.graph import START, END, StateGraph
from state import State

from agents.router import router_node
from agents.planner import planner_node
from human import human_approval_node
from agents.coder import coder_node
from agents.reflection import reflection_node
from agents.apply import apply_node
from agents.project_qa import ProjectQA

def build_graph(llm, vector_store, retriever_agent):
    
    def retriever_node(state: State):
        return retriever_agent.run(state)
    
    def project_qa_node(state: State):
        project_qa = ProjectQA(llm, vector_store)
        return project_qa.run(state)
    
    # create graph
    graph = StateGraph(State)

    # add nodes
    graph.add_node("router", router_node)
    graph.add_node("planner", planner_node)
    graph.add_node("human", human_approval_node)
    graph.add_node("retriever", retriever_node)
    graph.add_node("coder", coder_node)
    graph.add_node("reflection", reflection_node)
    graph.add_node("apply", apply_node)
    graph.add_node("project_qa", project_qa_node)

    # add edges
    graph.add_edge(START, "router")
    graph.add_edge("planner", "human")
    graph.add_edge("retriever", "coder")
    graph.add_edge("coder", "reflection")
    graph.add_edge("apply", END)
    graph.add_edge("project_qa", END)

    # add conditional edges
    graph.add_conditional_edges(
        "router",
        lambda state: state["next_agent"],
        {
            "planner": "planner",
            "project_qa": "project_qa",
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

        print("\n===== Reflection Router =====")
        print("Approved:", state["reflection"].approved)
        print("Reflection Iteration:", state["reflection_iteration"])


        if state["reflection"].approved:
            print("Routing -> apply")
            return "approved"
        
        if state["reflection_iteration"] >= 3:
            print("Routing -> end")
            return "max_attempts"
        
        print("Routing -> retry")
        
        return "retry"

    graph.add_conditional_edges(
        "reflection",
        reflection_router,
        {
            "approved" : "apply",
            "retry": "coder",
            "max_attempts" : END
        }
    )

    return graph.compile()
