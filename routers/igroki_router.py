from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Polzovatel, Uroven, ProidennyjUroven, Dostizhenie, PolzovatelDostizhenie
from schemas import PolzovatelOut, ProitiUroven, DostizhenieOut
from auth import get_current_polzovatel
from typing import List

router = APIRouter(prefix="/igrok", tags=["igrok"])

@router.get("/profil", response_model=PolzovatelOut)
def poluchit_profil(curr: Polzovatel = Depends(get_current_polzovatel)):
    return curr

@router.get("/dostizheniya", response_model=List[DostizhenieOut])
def poluchit_moi_dostizheniya(curr: Polzovatel = Depends(get_current_polzovatel), db: Session = Depends(get_db)):
    dost = db.query(Dostizhenie).join(PolzovatelDostizhenie).filter(PolzovatelDostizhenie.polzovatel_id == curr.id).all()
    return dost

@router.post("/proiti-uroven")
def proiti_uroven(data: ProitiUroven, db: Session = Depends(get_db), curr: Polzovatel = Depends(get_current_polzovatel)):
    uroven = db.query(Uroven).filter(Uroven.id == data.uroven_id).first()
    if not uroven:
        raise HTTPException(404, "Uroven ne najden")

    # Проверяем, не пройден ли уже
    proiden = db.query(ProidennyjUroven).filter(
        ProidennyjUroven.polzovatel_id == curr.id,
        ProidennyjUroven.uroven_id == data.uroven_id
    ).first()
    if proiden:
        raise HTTPException(400, "Uroven uzhe proiden")

    # Добавляем опыт
    curr.opyt += uroven.nagrada_opyt

    # Повышаем уровень (пример: 100 * uroven опыта нужно на следующий уровень)
    while curr.opyt >= curr.uroven * 100:
        curr.opyt -= curr.uroven * 100
        curr.uroven += 1

    # Записываем прохождение
    new_proiden = ProidennyjUroven(polzovatel_id=curr.id, uroven_id=data.uroven_id)
    db.add(new_proiden)

    # Проверяем новые достижения
    dostizheniya = db.query(Dostizhenie).all()
    for d in dostizheniya:
        if d.uslovie_uroven and curr.uroven >= d.uslovie_uroven:
            if not db.query(PolzovatelDostizhenie).filter_by(polzovatel_id=curr.id, dostizhenie_id=d.id).first():
                db.add(PolzovatelDostizhenie(polzovatel_id=curr.id, dostizhenie_id=d.id))
        if d.uslovie_opyt and curr.opyt >= d.uslovie_opyt:
            if not db.query(PolzovatelDostizhenie).filter_by(polzovatel_id=curr.id, dostizhenie_id=d.id).first():
                db.add(PolzovatelDostizhenie(polzovatel_id=curr.id, dostizhenie_id=d.id))

    db.commit()
    return {"status": "Uroven proiden!", "novyj_uroven": curr.uroven, "opyt": curr.opyt}