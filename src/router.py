from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from src.RAG import getResponse, streamResponse

chat_router = APIRouter (prefix="/chat", tags=['Chats'])

class InputRequest (BaseModel):
    message: str
    thread_id: str

class OutputRequest (BaseModel):
    message: str

@chat_router.post ("/chat_response", status_code=200, response_model=OutputRequest)
async def chatResponse (message:InputRequest):
    response = await getResponse (query=message.message, thread_id=message.thread_id)
    return {'message': response}

@chat_router.post ("/stream_response")
async def streamResponseMessage (message:InputRequest):
    return StreamingResponse (streamResponse (query=message.message, thread_id=message.thread_id), media_type="text/plain")