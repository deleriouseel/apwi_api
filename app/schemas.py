""" 
Controls how a response from the DB is returned

"""

from pydantic import BaseModel, EmailStr
from datetime import date, time, datetime
from typing import Optional


class ProgramBase(BaseModel):
    airdate: date
    title: str
    network: str
    filename: str
    id: int

    class Config:
        orm_mode = True


class ProgramCreate(BaseModel):
    airdate: date
    title: str
    network: str
    filename: str


class LocationBase(BaseModel):
    city: str
    state: str
    country: str
    id: int


class LocationCreate(LocationBase):
    city: str
    state: str
    country: str


class AirtimeBase(BaseModel):
    time: time
    live: bool
    airdays: Optional[int]
    id: int


class AirtimeCreate(AirtimeBase):
    pass


class StationBase(BaseModel):
    network: str
    url: str
    image: str
    name: str
    id: int


class StationCreate(StationBase):
    network: str
    url: str
    image: str
    name: str


class CallLettersBase(BaseModel):
    callletters: str
    airtime: time
    location: str
    station: str
    id: int


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
