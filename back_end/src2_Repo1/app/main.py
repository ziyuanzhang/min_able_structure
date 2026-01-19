from fastapi import FastAPI
from app.router import router
from infra.models import init_db
init_db()

app = FastAPI()
app.include_router(router,prefix="/agent")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)