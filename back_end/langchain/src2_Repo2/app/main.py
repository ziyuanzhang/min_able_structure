from fastapi import FastAPI
from app.router import router
from infra.models import init_db
from app.router_replay import router as router_replay
init_db()

app = FastAPI()
app.include_router(router,prefix="/agent")
app.include_router(router_replay,prefix="/agent")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)