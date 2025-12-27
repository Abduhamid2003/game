from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Igra
from schemas import IgraBase, IgraOut
from typing import List

router = APIRouter(prefix="/igry", tags=["igry"])

@router.post("/", response_model=IgraOut)
def sozdat_igru(igra: IgraBase, db: Session = Depends(get_db)):
    new_igra = Igra(**igra.model_dump())
    db.add(new_igra)
    db.commit()
    db.refresh(new_igra)
    return new_igra

@router.get("/", response_model=List[IgraOut])
def poluchit_igry(db: Session = Depends(get_db)):
    return db.query(Igra).all()