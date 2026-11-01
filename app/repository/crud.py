from sqlalchemy.orm import Session
from ..models import User, Post, Comment, Like
from ..schemas import UserCreate, PostCreate, CommentCreate
from ..core.security import hash_password
from ..utils.slug_generate import generate_slug
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
    return db.query(Post).offset(skip).limit(limit).all()


def create_post(db: Session, post: PostCreate, user_id: int):
    slug = generate_slug(post.title)

    existing_slug = db.query(Post).filter(Post.slug == slug).first()
    if existing_slug:
        slug = f"{slug}-{uuid.uuid4().hex[:6]}"

    db_post = Post(
        title=post.title,
        slug=slug,
        summary=post.summary,
        body=post.body,
        published=post.published,
        author_id=user_id,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


def get_post_by_slug(db: Session, slug: str):
    return db.query(Post).filter(Post.slug == slug).first()


def get_post_by_id(db: Session, id: int):
    return db.query(Post).filter(Post.id == id).first()


def create_comment(db: Session, comment: CommentCreate, post_id: int, user_id: int):
    db_comment = Comment(content=comment.content, post_id=post_id, user_id=user_id)
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
