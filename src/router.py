from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from src.RAG import getResponse, streamResponse
from src.embedding import embedPDF
import os

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

@chat_router.post ("/upload", status_code=200)
async def upload_file (file:UploadFile = File (...)):
    fileName = file.filename
    if not fileName.endswith (".pdf"):
        raise HTTPException (status_code=400, detail=f"File type not supported {fileName}")
    
    uploadPath = "PDF/Upload"
    os.makedirs (uploadPath, exist_ok=True)

    filePath = os.path.join (uploadPath, fileName)

    if os.path.exists(filePath):
        raise HTTPException(status_code=400, detail=f"File '{fileName}' already uploaded")
    
    with open(filePath, "wb") as f:
        content = await file.read()
        f.write(content)

    if await embedPDF (filePath):
        return {'status': "Successful", "detail": f"File {fileName} Uploaded successfully"}
    else:
        raise HTTPException (status_code=400, detail="File not embedded into vector store.")