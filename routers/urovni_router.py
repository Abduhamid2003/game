from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Uroven, Igra
from schemas import UrovenOut
from typing import List

router = APIRouter(prefix="/urovni", tags=["urovni"])

@router.post("/", response_model=UrovenOut)
def sozdat_uroven(uroven_data: dict, db: Session = Depends(get_db)):
    # Пример: {"nomer": 1, "nazvanie": "Tutorial", "nagrada_opyt": 50, "igra_id": 1}
    new_uroven = Uroven(**uroven_data)
    db.add(new_uroven)
    db.commit()
    db.refresh(new_uroven)
    return new_uroven

@router.get("/igra/{igra_id}", response_model=List[UrovenOut])
def poluchit_urovni_igry(igra_id: int, db: Session = Depends(get_db)):
    return db.query(Uroven).filter(Uroven.igra_id == igra_id).all()