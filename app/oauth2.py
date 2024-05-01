from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from .database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException,status
from . import schemas, models
from .config import settings

SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=settings.access_token_expire_minutes


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_token(data:dict):
    to_encode=data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    if not expire:
        raise HTTPException(status_code=500, detail="Problem occurred when creating the token")
    to_encode.update({"exp":expire})
    encoded_data = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_data

def verify_token(token:str, credential_error):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id:str = payload.get("user_id")
        if id is None:
            raise credential_error
        print("ID: ", id)
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credential_error
    return token_data

def get_current_user(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token = verify_token(token, credential_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
