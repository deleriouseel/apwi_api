from datetime import date
from pydantic import BaseModel


class ProgramBase(BaseModel):
    airdate: date
    title: str
    network: str
    filename: str
    id: int

    class Config:
        orm_mode = True
