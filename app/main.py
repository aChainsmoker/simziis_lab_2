from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.auth import router as auth_router
from app.api.data import confidential_router, public_router
from app.infrastructure.database import Base, engine
from app.infrastructure import models  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lab 2 Secure Data API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(confidential_router)
app.include_router(public_router)

frontend = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", StaticFiles(directory=frontend, html=True), name="frontend")

