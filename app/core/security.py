from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_DELTA

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + TOKEN_EXPIRE_DELTA
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
