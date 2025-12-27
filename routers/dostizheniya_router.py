from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Dostizhenie, Igra
from schemas import DostizhenieOut
from typing import List, Optional

router = APIRouter(prefix="/dostizheniya", tags=["dostizheniya"])

@router.post("/", response_model=DostizhenieOut)
def sozdat_dostizhenie(
    nazvanie: str,
    opisanie: str,
    uslovie_uroven: Optional[int] = None,
    uslovie_opyt: Optional[int] = None,
    igra_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Создать новое достижение (для админа в будущем можно защитить)"""
    new_dost = Dostizhenie(
        nazvanie=nazvanie,
        opisanie=opisanie,
        uslovie_uroven=uslovie_uroven,
        uslovie_opyt=uslovie_opyt,
        igra_id=igra_id
    )
    db.add(new_dost)
    db.commit()
    db.refresh(new_dost)
    return new_dost

@router.get("/", response_model=List[DostizhenieOut])
def poluchit_vse_dostizheniya(db: Session = Depends(get_db)):
    return db.query(Dostizhenie).all()

@router.get("/igra/{igra_id}", response_model=List[DostizhenieOut])
def poluchit_dostizheniya_igry(igra_id: int, db: Session = Depends(get_db)):
    return db.query(Dostizhenie).filter(Dostizhenie.igra_id == igra_id).all()

@router.get("/globalnye", response_model=List[DostizhenieOut])
def poluchit_globalnye_dostizheniya(db: Session = Depends(get_db)):
    return db.query(Dostizhenie).filter(Dostizhenie.igra_id.is_(None)).all()