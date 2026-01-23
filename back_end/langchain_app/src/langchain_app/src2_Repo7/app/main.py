from fastapi import FastAPI
from app.router import router
from infra.models import init_db
from infra.calculate_cost import sync_usage_data
from app.router_replay import router as router_replay
from app.router_human import router as router_human
from app.router_billing import router as router_billing
from infra.middleware.auth import auth_middleware
init_db()
sync_usage_data()

app = FastAPI()
app.middleware("http")(auth_middleware)
app.include_router(router,prefix="/agent")
app.include_router(router_replay,prefix="/agent")
app.include_router(router_human,prefix="/agent")
app.include_router(router_billing,prefix="/billing")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)