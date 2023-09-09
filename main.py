from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain import title_router

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://223.130.138.51:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(title_router.router)