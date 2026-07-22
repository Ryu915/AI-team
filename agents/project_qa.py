from langchain_core.messages import SystemMessage
from prompts.project_qa import PROJECT_QA_PROMPT

class ProjectQA:

    def __init__(self, llm, vector_store):
        self.llm = llm
        self.vector_store = vector_store

    def run(self, state):
        print("\nProject QA...")
        question = state["user_input"]
        context = self._retrieve_context(question)

        messages = PROJECT_QA_PROMPT.format_messages(
            project_summary=state["project_understanding"].summary,
            retrieved_context=context,
            chat_history=state["chat_history"],
            question=question,
        )

        answer = self.llm.invoke(messages)

        state["chat_history"].append(answer)


        print(f"\nAssistant: {answer.content}")

        return state

    def _retrieve_context(self, question):
        return self.vector_store.search(question)