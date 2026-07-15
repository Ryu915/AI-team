from models.llm import get_llm
from models.coder import CoderOutput
from prompts.coder import coder_prompt

llm = get_llm()

coder = llm.with_structured_output(CoderOutput)

def coder_node(state):

    plan = state["plan"]

    understanding = state["project_understanding"]

    retrieved_context = state["retrieved_context"]

    result = coder.invoke(
        coder_prompt.format_messages(
            project_summary = understanding.summary,
            plan = plan,
            retrieved_context = retrieved_context
        )
    )

    state["code_output"] = result

    print("\n===========Coder=============" )
    print(f"\n{state["code_output"]}")

    return state