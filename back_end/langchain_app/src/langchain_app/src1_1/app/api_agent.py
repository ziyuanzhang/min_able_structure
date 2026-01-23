from fastapi import APIRouter
from pydantic import BaseModel
from langchain_app.src1_1.agents.graph import agent_graph


router = APIRouter()
class AskReq(BaseModel):
    query:str
    role:str

@router.post("/ask")
async def ask(req:AskReq):
    state={
        "query":req.query,
        "role":req.role,
        "rag_calls":0
    }

    result = agent_graph.invoke(state)
    return {"answer":result["answer"]}

