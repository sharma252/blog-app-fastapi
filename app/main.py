import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .api import auth, posts, users
from .core.config import settings
from .db.session import Base, engine
from .utils.logging_config import setup_logging

# Configure logging before the app object is created.
setup_logging()


STATIC_DIR = Path(__file__).parent / "static"
STATIC_DIR.mkdir(exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup operations
    # Dev-only: create tables if missing. In prod, use Alembic migrations instead.
    Base.metadata.create_all(bind=engine)

    yield

    engine.dispose()  # Shutdown operation


app = FastAPI(
    title="Blog API",
    version="0.1.0",
    description="Dev environment",
    lifespan=lifespan,
)

# If later need cookies/auth cross-origin, list explicit origins and set -> allow_credentials=True.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])


@app.get("/")
def root():
    return {"message": "Welcome to the Blog API"}
