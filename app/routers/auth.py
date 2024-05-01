from fastapi import APIRouter, Depends, HTTPException
from ..utils import verify_password
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, oauth2
router=APIRouter(
        tags=['Authentication'],
        prefix='/login'
        )

@router.post('/')
async def login(user_data:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="No user with that credential")
    if not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=405, detail="Unauthorized")
    access_token = oauth2.create_token(data={"user_id":user.id})
    return {"access_token" : access_token, "token_type":"Bearer"}
