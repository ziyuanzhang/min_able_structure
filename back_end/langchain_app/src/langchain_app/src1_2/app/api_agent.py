from fastapi import APIRouter
from pydantic import BaseModel
from agents.graph import agent_graph


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

    result = await agent_graph.ainvoke(state)
    return {"answer":result["answer"]}

