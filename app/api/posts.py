from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from ..models import Post, Comment, Like, User
from ..schemas import PostCreate, PostOut, CommentCreate, CommentOut
from ..repository.crud import (
    get_post,
    get_post_by_id,
    get_post_by_slug,
    create_post,
    create_comment,
    toggle_like,
    get_comments_for_post,
)
from ..db.session import get_db
from .deps import get_current_user
import shutil
import os
import uuid

router = APIRouter()


@router.get("/", response_model=list[PostOut])
def read_posts(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    posts = get_post(db, skip, limit)
    return posts


@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_new_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_post(db=db, post=post, user_id=current_user.id)  # type: ignore


@router.get("/{slug}", response_model=PostOut)
def read_post(slug: str, db: Session = Depends(get_db)):
    post = get_post_by_slug(db, slug)
    if not post:
        raise HTTPException(404, "Post not found")

    return post


@router.post("/{post_id}/image", response_model=PostOut)
def upload_post_image(
    post_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(404, "Post not found")

    if post.author_id != current_user.id:  # type: ignore
        raise HTTPException(403, "Not Authorized")

    # Sanitize the filename to prevent path traversal
    safe_filename = os.path.basename(file.filename)  # type: ignore
    file_location = f"app/static/{safe_filename}"

    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    post.cover_image = f"static/{safe_filename}"  # type: ignore

    db.commit()
    db.refresh(post)
    return post


@router.post(
    "/{post_id}/comments",
    response_model=CommentOut,
    status_code=status.HTTP_201_CREATED,
)
def add_comment(
    post_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(404, "Post not found")

    return create_comment(
        db=db, comment=comment, post_id=post_id, user_id=current_user.id  # type: ignore
    )


@router.get("/{post_id}/comments", response_model=list[CommentOut])
def read_comments(post_id: int, db: Session = Depends(get_db)):
    post = get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(404, "Post not found")

    return get_comments_for_post(db, post_id=post_id)


@router.post("/{post_id}/like")
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(404, "Post not found")

    result = toggle_like(db=db, post_id=post_id, user_id=current_user.id)  # type: ignore
    return result
