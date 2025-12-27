from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import Polzovatel
from schemas import PolzovatelCreate, Token
from auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(polzovatel: PolzovatelCreate, db: Session = Depends(get_db)):
    """Регистрация нового пользователя"""
    # Проверяем, существует ли уже пользователь с таким username
    db_polzovatel = db.query(Polzovatel).filter(Polzovatel.username == polzovatel.username).first()
    if db_polzovatel:
        raise HTTPException(
            status_code=400,
            detail="Polzovatel s takim username uzhe sushchestvuet"
        )

    # Создаём нового пользователя с хэшированным паролем
    hashed = hash_password(polzovatel.password)
    new_polzovatel = Polzovatel(username=polzovatel.username, hashed_password=hashed)
    db.add(new_polzovatel)
    db.commit()
    db.refresh(new_polzovatel)

    # Сразу выдаём токен
    access_token = create_access_token(data={"sub": polzovatel.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Логин: получение JWT-токена"""
    polzovatel = db.query(Polzovatel).filter(Polzovatel.username == form_data.username).first()
    if not polzovatel or not verify_password(form_data.password, polzovatel.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nepravil'nyj username ili parol'"
        )

    access_token = create_access_token(data={"sub": polzovatel.username})
    return {"access_token": access_token, "token_type": "bearer"}