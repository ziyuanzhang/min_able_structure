from fastapi import APIRouter
from agent.runner import run_agent
from agent.runtime.supervisor_runner import run_supervisor

router = APIRouter()

@router.post("/run")
async def run (bode:dict):
    return {"output": await run_supervisor(bode["input"])}