from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.db import crud
from app.db.database import get_db
from app.schemas.quote import QuoteCreate, QuoteOut
from app.core.security import decode_access_token

router = APIRouter(prefix="/quotes", tags=["quotes"])
bearer = HTTPBearer()

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
    return payload.get("user_id")

@router.post("/", response_model=QuoteOut)
def create_quote(payload: QuoteCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    quote = crud.create_quote(db, payload.text, payload.author, owner_id=user_id)
    return quote

@router.get("/random", response_model=QuoteOut)
def random_quote(db: Session = Depends(get_db)):
    q = crud.get_random_quote(db)
    if not q:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no quotes found")
    return q

@router.get("/search", response_model=List[QuoteOut])
def search_quotes(author: str = Query(...), db: Session = Depends(get_db)):
    return crud.search_quotes_by_author(db, author)

@router.get("/", response_model=List[QuoteOut])
def list_quotes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_quotes(db, skip=skip, limit=limit)
