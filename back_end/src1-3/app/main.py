from fastapi import FastAPI
from app.api_agent import router



app = FastAPI(title="Agent Gateway (MVP)")
app.include_router(router,prefix="/agent")

if __name__ == "__main__":

    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)
