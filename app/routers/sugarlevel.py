from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2
from datetime import date
from typing import Annotated
router =APIRouter(
        tags=['Sugar Level'],
        prefix="/sugarlevel")


@router.get("/", response_model=list[schemas.SugarLevelOut])
async def get_all_sugar_levels(current_user:Annotated[int, Depends(oauth2.get_current_user)], db:Session=Depends(get_db)):
    levels = db.query(models.SugarLevel).filter(models.SugarLevel.owner_id == current_user.id).all()
    return levels

@router.post("/")
async def add_sugar_level(current_user: Annotated[int, Depends(oauth2.get_current_user)],sugar_level:schemas.SugarLevelIn, db:Session=Depends(get_db)):
    input_slevel = models.SugarLevel(owner_id=current_user.id, **sugar_level.dict())
    db.add(input_slevel)
    db.commit()
    db.refresh(input_slevel)
    return input_slevel

@router.put("/{id}", response_model=schemas.SugarLevelOut)
async def update(id:int, current_user:Annotated[int, Depends(oauth2.get_current_user)],updated_level:schemas.SugarLevelIn, db:Session=Depends(get_db)):
    level_to_update_query = db.query(models.SugarLevel).filter(models.SugarLevel.id == id, models.SugarLevel.owner_id == current_user.id)
    
    level_to_update=level_to_update_query.first()
    if not level_to_update:
        raise HTTPException(status_code=404, detail="Unavailable")
    level_to_update_query.update(updated_level.dict())
    db.commit()
    return level_to_update

@router.delete("/{id}")
async def delete_level(id:int, current_user:Annotated[str, Depends(oauth2.get_current_user)],db:Session=Depends(get_db)):
    deletable_level_query=db.query(models.SugarLevel).filter(models.SugarLevel.id == id, models.SugarLevel.owner_id == current_user.id)
    deletable_level = deletable_level_query.first()
    if not deletable_level:
        raise HTTPException(status_code=404, detail="Couldn't find the sugar level")
    deletable_level_query.delete()
    db.commit()
    return {"message":"success"}
