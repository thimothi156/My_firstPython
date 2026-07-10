import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import User


security = HTTPBearer()

def encode_token(payload):
    secret_key = "your_secret_key"
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token

def decode_token(token):
    return jwt.decode(token, "your_secret_key", algorithms=["HS256"])


def get_current_user(token: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = token.credentials
    if token:
        try:
            payload = decode_token(token)
            user_id = payload.get("id")
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token"
                )
            return user
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
    else:
        raise HTTPException(
            status_code=401,
            detail="Authorization token is missing"
        )


