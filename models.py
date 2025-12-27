from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base

class Polzovatel(Base):
    __tablename__ = "polzovateli"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    uroven = Column(Integer, default=1)           # Общий уровень игрока
    opyt = Column(Integer, default=0)              # Текущий опыт
    data_registracii = Column(DateTime, default=datetime.utcnow)

    dostizheniya = relationship("PolzovatelDostizhenie", back_populates="polzovatel")
    proidennye_urovni = relationship("ProidennyjUroven", back_populates="polzovatel")

class Igra(Base):
    __tablename__ = "igry"

    id = Column(Integer, primary_key=True, index=True)
    nazvanie = Column(String, unique=True, index=True)
    opisanie = Column(String)

    urovni = relationship("Uroven", back_populates="igra")
    dostizheniya = relationship("Dostizhenie", back_populates="igra")

class Uroven(Base):
    __tablename__ = "urovni"

    id = Column(Integer, primary_key=True, index=True)
    nomer = Column(Integer)                       # Номер уровня в игре
    nazvanie = Column(String)
    nagrada_opyt = Column(Integer, default=100)   # Сколько опыта даёт прохождение
    igra_id = Column(Integer, ForeignKey("igry.id"))

    igra = relationship("Igra", back_populates="urovni")
    proidennye = relationship("ProidennyjUroven", back_populates="uroven")

class Dostizhenie(Base):
    __tablename__ = "dostizheniya"

    id = Column(Integer, primary_key=True, index=True)
    nazvanie = Column(String)
    opisanie = Column(String)
    uslovie_uroven = Column(Integer, nullable=True)  # Нужно достичь уровня
    uslovie_opyt = Column(Integer, nullable=True)     # Нужно набрать опыта
    igra_id = Column(Integer, ForeignKey("igry.id"), nullable=True)  # Если привязанно к игре

    igra = relationship("Igra", back_populates="dostizheniya")
    polzovateli = relationship("PolzovatelDostizhenie", back_populates="dostizhenie")

class ProidennyjUroven(Base):
    __tablename__ = "proidennye_urovni"

    polzovatel_id = Column(Integer, ForeignKey("polzovateli.id"), primary_key=True)
    uroven_id = Column(Integer, ForeignKey("urovni.id"), primary_key=True)
    data_prohozhdeniya = Column(DateTime, default=datetime.utcnow)

    polzovatel = relationship("Polzovatel", back_populates="proidennye_urovni")
    uroven = relationship("Uroven", back_populates="proidennye")

class PolzovatelDostizhenie(Base):
    __tablename__ = "polzovatel_dostizheniya"

    polzovatel_id = Column(Integer, ForeignKey("polzovateli.id"), primary_key=True)
    dostizhenie_id = Column(Integer, ForeignKey("dostizheniya.id"), primary_key=True)
    data_polucheniya = Column(DateTime, default=datetime.utcnow)

    polzovatel = relationship("Polzovatel", back_populates="dostizheniya")
    dostizhenie = relationship("Dostizhenie", back_populates="polzovateli")