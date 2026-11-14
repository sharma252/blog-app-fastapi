from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # this allow to return orm models directly rather then first converting it python dict
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class PostCreate(BaseModel):
    title: str
    body: str
    summary: str | None = None
    published: bool | None = None


class PostOut(BaseModel):
    id: int
    title: str
    summary: str | None = None
    body: str
    published: bool
    likes_count: int | None = 0
    author: UserOut | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CommentCreate(BaseModel):
    content: str


class CommentOut(BaseModel):
    id: int
    content: str
    post_id: int
    author_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LikeOut(BaseModel):
    id: int
    user_id: int
    post_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
