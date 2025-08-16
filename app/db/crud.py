from sqlalchemy.orm import Session
from app.db import models
from app.core.utils import hash_password, verify_password
import random

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, username: str, password: str):
    hashed = hash_password(password)
    user = models.User(username=username, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_quote(db: Session, text: str, author: str, owner_id: int | None = None):
    quote = models.Quote(text=text, author=author, owner_id=owner_id)
    db.add(quote)
    db.commit()
    db.refresh(quote)
    return quote

def get_all_quotes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Quote).offset(skip).limit(limit).all()

def search_quotes_by_author(db: Session, author_query: str):
    return db.query(models.Quote).filter(models.Quote.author.ilike(f"%{author_query}%")).all()

def get_random_quote(db: Session):
    all_ids = [q.id for q in db.query(models.Quote.id).all()]
    if not all_ids:
        return None
    chosen = random.choice(all_ids)
    return db.query(models.Quote).filter(models.Quote.id == chosen).first()
