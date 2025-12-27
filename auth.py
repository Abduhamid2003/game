from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import Polzovatel
from database import get_db

# Настройки JWT
SECRET_KEY = "super-secret-key-izmeni-v-productions-na-silnyj"  # ОБЯЗАТЕЛЬНО ИЗМЕНИ В РЕАЛЬНОМ ПРОЕКТЕ!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 час

# Контекст для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 схема для получения токена из заголовка Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password: str) -> str:
    """Хэширует пароль"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль на соответствие хэшу"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    """Создаёт JWT-токен"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_polzovatel(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Зависимость: получает текущего авторизованного пользователя по токену"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Ne udalos' proverit' uchetnye dannye",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    polzovatel = db.query(Polzovatel).filter(Polzovatel.username == username).first()
    if polzovatel is None:
        raise credentials_exception
    return polzovatel