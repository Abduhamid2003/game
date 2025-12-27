from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class PolzovatelCreate(BaseModel):
    username: str
    password: str

class PolzovatelOut(BaseModel):
    id: int
    username: str
    uroven: int
    opyt: int
    data_registracii: datetime

    class Config:
        from_attributes = True

class IgraBase(BaseModel):
    nazvanie: str
    opisanie: Optional[str] = None

class IgraOut(IgraBase):
    id: int

    class Config:
        from_attributes = True

class UrovenOut(BaseModel):
    id: int
    nomer: int
    nazvanie: str
    nagrada_opyt: int
    igra_id: int

    class Config:
        from_attributes = True

class DostizhenieOut(BaseModel):
    id: int
    nazvanie: str
    opisanie: str
    igra_id: Optional[int]

    class Config:
        from_attributes = True

class ProitiUroven(BaseModel):
    uroven_id: int