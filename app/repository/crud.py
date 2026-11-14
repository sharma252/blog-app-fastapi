from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from ..models import User, Post, Comment, Like
from ..schemas import UserCreate, PostCreate, CommentCreate, PostOut
from ..core.security import hash_password
import uuid


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    hashed_password_val = hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password_val)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_post(db: Session, skip: int = 0, limit: int = 20):
    return (
        db.query(Post).order_by(Post.updated_at.desc()).offset(skip).limit(limit).all()
    )


def get_posts_with_likes(db: Session, skip: int = 0, limit: int = 20) -> list[PostOut]:
    results = (
        db.query(Post, func.count(Like.id).label("likes_count"))
        .outerjoin(Like, Like.post_id == Post.id)
        .group_by(Post.id)
        .order_by(Post.updated_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [
        PostOut(
            id=post.id,
            title=post.title,
            body=post.body,
            published=post.published,
            created_at=post.created_at,
            updated_at=post.updated_at,
            likes_count=likes_count,
        )
        for post, likes_count in results
    ]


def create_post(db: Session, post: PostCreate, user_id: int):

    db_post = Post(
        title=post.title,
        summary=post.summary,
        body=post.body,
        published=post.published,
        author_id=user_id,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


def get_post_by_id(db: Session, id: int):
    return db.query(Post).filter(Post.id == id).first()


def create_comment(db: Session, comment: CommentCreate, post_id: int, user_id: int):
    db_comment = Comment(
        content=comment.content, post_id=post_id, author_name="unanonymous"
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments_for_post(db: Session, post_id: int):
    return db.query(Comment).filter(Comment.post_id == post_id).all()


def toggle_like(db: Session, post_id: int, user_id: int):
    # Check if the user already liked the post
    existing_like = (
        db.query(Like).filter(Like.post_id == post_id, Like.user_id == user_id).first()
    )

    if existing_like:
        # Unlike (delete the record)
        db.delete(existing_like)
        db.commit()
        return {"status": "unliked"}
    else:
        # Like (create the record)
        new_like = Like(post_id=post_id, user_id=user_id)
        db.add(new_like)
        db.commit()
        return {"status": "liked"}


def likes_count_for_post(db: Session, post_id: int):
    return db.query(Like).filter(Like.post_id == post_id).count()
