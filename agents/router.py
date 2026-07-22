from prompts.router import router_prompt
from models.router_output import RouterOutput
from models.llm import get_llm
from langchain_core.messages import HumanMessage, AIMessage

llm = get_llm()

router = llm.with_structured_output(RouterOutput)

def router_node(state):

    project_summary = (
        state["project_understanding"].summary
        if state["project_understanding"] is not None
        else "No project loaded."
    )

    state["project_qa_response"] = ""
    
    result = router.invoke(
        router_prompt.format_messages(
            project_summary = project_summary,
            chat_history = state["chat_history"],
            user_input = state["user_input"]
        )
    )

    state["next_agent"] = result.next_agent
    state["router_response"] = result.message

    # Save conversation
    state["chat_history"].append(
        HumanMessage(content=state["user_input"])
    )


    if result.next_agent == "none" or result.next_agent == "END":
        state["chat_history"].append(
            AIMessage(content=result.message)
        )

    print(f"\nNext agent: {result.next_agent}")
    
    return state