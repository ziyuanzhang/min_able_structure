from fastapi import FastAPI
from app.router import router
from infra.models import init_db
from app.router_replay import router as router_replay
from app.router_human import router as router_human
from infra.middleware.auth import auth_middleware
init_db()

app = FastAPI()
app.middleware("http")(auth_middleware)
app.include_router(router,prefix="/agent")
app.include_router(router_replay,prefix="/agent")
app.include_router(router_human,prefix="/agent")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)