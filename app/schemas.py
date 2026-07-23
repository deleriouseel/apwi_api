""" 
Controls how a response from the DB is returned

"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field
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


class LocationCreate(BaseModel):
    city: str
    state: str
    country: str


class AirtimeBase(BaseModel):
    time: time
    airdays: Optional[str]
    idAirtime: int

    model_config = ConfigDict(from_attributes=True)


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
    local: Optional[bool] = None
    # DB column is "callletters"; expose it as "call_letters" in the API.
    call_letters: Optional[str] = Field(default=None, validation_alias="callletters")
    locations: List[LocationBase] = []
    airtimes: List[AirtimeBase] = []

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class StationCreate(BaseModel):
    network: str
    url: Optional[str] = None
    image: Optional[str] = None
    name: str
    frequency: Optional[str] = None
    live: Optional[bool] = False
    local: Optional[bool] = False
    call_letters: Optional[str] = Field(default=None, serialization_alias="callletters")

    model_config = ConfigDict(populate_by_name=True)


class StationUpdate(BaseModel):
    """PATCH body -- every field optional; only what is sent gets changed."""

    network: Optional[str] = None
    url: Optional[str] = None
    image: Optional[str] = None
    name: Optional[str] = None
    frequency: Optional[str] = None
    live: Optional[bool] = None
    local: Optional[bool] = None
    call_letters: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class ProgramUpdate(BaseModel):
    airdate: Optional[date] = None
    title: Optional[str] = None
    network: Optional[str] = None
    filename: Optional[str] = None


class LocationUpdate(BaseModel):
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None


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
