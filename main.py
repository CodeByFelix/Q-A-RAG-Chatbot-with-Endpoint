from fastapi import FastAPI
from src.router import chat_router
from src.RAG import init_graph

app = FastAPI ()

app.include_router (router=chat_router)


@app.on_event ("startup")
async def startup_event ():
    nn = await init_graph ()