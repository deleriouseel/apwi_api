""" 
Controls how a response from the DB is returned

"""

from pydantic import BaseModel, EmailStr
from datetime import date, time, datetime
from typing import Optional, List


class ProgramBase(BaseModel):
    airdate: date
    title: str
    network: str
    filename: str
    id: int

    class Config:
        from_attributes = True


class ProgramCreate(BaseModel):
    airdate: date
    title: str
    network: str
    filename: str


class LocationBase(BaseModel):
    city: str
    state: str
    country: str
    idLocation: int

    class Config:
        from_attributes = True


class LocationCreate(LocationBase):
    city: str
    state: str
    country: str


class AirtimeBase(BaseModel):
    time: time
    airdays: Optional[str]
    idAirtime: int


class AirtimeCreate(AirtimeBase):
    pass


class StationBase(BaseModel):
    idStation: int
    network: Optional[str] = None
    url: Optional[str] = None
    image: Optional[str] = None
    name: Optional[str] = None
    frequency: Optional[str] = None
    live: Optional[bool] = None
    call_letters: Optional[str] = None
    locations: List[LocationBase] = []
    airtimes: List[AirtimeBase] = []

    class Config:
        from_attributes = True


class StationCreate(BaseModel):
    network: str
    url: Optional[str]
    image: Optional[str]
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
        from_attributes = True
