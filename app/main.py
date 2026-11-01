from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, posts
from .db.session import engine, Base
from .api import users
from .core.config import settings
from fastapi.staticfiles import StaticFiles
import os

# Create tables for quick dev (use Alembic for prod)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)


if not os.path.exists("app/static"):
    os.makedirs("app/static")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])


@app.get("/")
def root():
    return {"message": "Welcome to the Blog API"}
