from models.llm import get_llm
from models.planner_output import PlanOutput
from prompts.planner import planner_prompt
from langchain_core.messages import AIMessage

llm = get_llm()

planner = llm.with_structured_output(PlanOutput)

def planner_node(state):

    understanding = state["project_understanding"]

    result = planner.invoke(
        planner_prompt.format_messages(
            project_summary = understanding.summary,
            project_structure = understanding.architecture,
            technologies = understanding.technologies,
            user_request = state["user_input"]
        )
    )

    state["plan"] = result

    state["chat_history"].append(
        AIMessage(content=f"Implementation plan created:\n{result.goal}")
    )

    return state