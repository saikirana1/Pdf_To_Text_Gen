from fastapi import FastAPI, Request, Query, Depends
from fastapi.responses import StreamingResponse
import time
from fastapi.middleware.cors import CORSMiddleware
from backend_server import router

from backend_server import auth

from fastapi.responses import JSONResponse
from backend_server.auth import verify_token

from pydantic import BaseModel

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


@app.middleware("http")
async def check_user_token(request: Request, call_next):
    # print(request.headers)
    public_paths = [
        "/token",
        "/register",
        "/get_response",
        "/docs",
        "/openapi.json",
        "/get_file_data",
    ]

    if request.method == "OPTIONS":
        return await call_next(request)

    if any(request.url.path.startswith(p) for p in public_paths):
        return await call_next(request)

    print("headers data", request.headers)
    auth_header = request.headers.get("Authorization")
    # print(auth_header, "auth_header")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=401, content={"detail": "Unauthorized: Missing token"}
        )

    token = auth_header.split(" ")[1]
    print("i ma from backed token", token)

    try:
        verify_token(token)
    except Exception:
        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized: Invalid or expired token"},
        )

    return await call_next(request)


app.include_router(auth.router)
app.include_router(router.router)
