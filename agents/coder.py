from models.llm import get_llm
from models.coder import CoderOutput
from prompts.coder import coder_prompt

llm = get_llm()

coder = llm.with_structured_output(CoderOutput)

def coder_node(state):

    plan = state["plan"]

    understanding = state["project_understanding"]

    retrieved_context = state["retrieved_context"]

    reflection = state["reflection"]

    feedback = ""
    if reflection is not None:
        feedback = reflection.feedback

    result = coder.invoke(
        coder_prompt.format_messages(
            project_summary = understanding.summary,
            plan = plan,
            retrieved_context = retrieved_context,
            feedback = feedback
        )
    )

    state["code_output"] = result
    state["reflection_iteration"] += 1

    print("\n===========Coder=============" )
    print(f"\n{state["code_output"].explanation}")

    return state