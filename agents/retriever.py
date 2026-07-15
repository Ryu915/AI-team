

class RetrieverAgent:

    def __init__(self, vector_store):
        self.vector_store = vector_store # to retrieve from chromaDb

    def run(self, state):
        
        targets = state["plan"].retrieval_targets
        retrieved_docs = []

        for target in targets:
            docs = self.vector_store.search(target)
            retrieved_docs.append(docs)

        state["retrieved_context"] = retrieved_docs
        
        return state