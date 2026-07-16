from models.reflection_output import ReflectionOutput
from models.llm import get_llm
from prompts.reflection import reflection_prompt


llm = get_llm()

reflection = llm.with_structured_output(ReflectionOutput)

def reflection_node(state):

    understanding = state["project_understanding"]
    plan = state["plan"]
    code_output = state["code_output"]
    retrieved_context = state["retrieved_context"]

    result = reflection.invoke(
        reflection_prompt.format_messages(
            project_summary = understanding.summary,
            plan = plan,
            retrieved_context = retrieved_context,
            code_changes = code_output
        )
    )

    state["reflection"] = result

    return state
