from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas,models, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
router = APIRouter(
        tags=['Users'],
        prefix='/user'
        )

@router.post('/', response_model=schemas.UserOut)
async def create_user(user_data:schemas.UserIn, db:Session=Depends(get_db)):
    hashed_password = utils.hash_password(user_data.password)
    user_data.password = hashed_password
    user=models.User(**user_data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int,current_user:Annotated[dict, Depends(oauth2.get_current_user)], db: Session = Depends(get_db), ):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user
