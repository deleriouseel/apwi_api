from datetime import date
from pydantic import BaseModel


class ProgramBase(BaseModel):
    airdate: date
    title: str
    network: str

    class Config:
        orm_mode = True
