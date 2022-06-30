from pydantic import BaseModel


class ProgramBase(BaseModel):
    airdate: str
    title: str
    network: str

    class Config:
        orm_mode = True


class Program(ProgramBase):
    title: str