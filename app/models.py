from sqlalchemy import Column, Integer, String
from .database import Base


class APWI(Base):
    __tablename__ = "apwi"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    airdate = Column(String, nullable=False)
    title = Column(String, nullable=False)
    network = Column(String, nullable=False)
    filename = Column(String, nullable=True)
