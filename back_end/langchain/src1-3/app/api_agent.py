from fastapi import APIRouter
from pydantic import BaseModel
from agents.graph import agent_graph
from storage.audit_writer import new_run,persist


router = APIRouter()
class AskReq(BaseModel):
    query:str
    role:str

@router.post("/ask")
async def ask(req:AskReq):
    run = new_run(req.query,req.role)
    state={
        "query":req.query,
        "role":req.role,
        "rag_calls":0,
        "_run":run
    }
    result = await agent_graph.ainvoke(state)
    persist(run)
    return {
        "run_id":run["run_id"],
        "answer":result["answer"]
    }

