class RAGFlowClient:
    def retrieve(self,query:str,top_k:int=5):
        return [f"doc for {query}"]