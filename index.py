from fastapi import FastAPI,Request
from fastapi.responses import StreamingResponse
import time
from fastapi.middleware.cors import CORSMiddleware
from backend_server import router
import uvicorn
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}

app.include_router(router.router)



