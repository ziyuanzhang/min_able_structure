
# prompt_tokens = llm_response.usage.prompt_tokens
# completion_tokens = llm_response.usage.completion_tokens

class RAGFlowClient:
    def retrieve(self,query:str,top_k:int=5):
        return [f"doc for {query}"]