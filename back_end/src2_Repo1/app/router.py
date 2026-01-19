from fastapi import APIRouter
from agent.runner import run_agent

router = APIRouter()

@router.post("/run")
async def run (bode:dict):
    return {"output": await run_agent(bode["input"])}