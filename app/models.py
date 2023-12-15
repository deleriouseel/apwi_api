"""
 Controls how data is sent to the DB

"""
from sqlalchemy import Column, Integer, String, Boolean, Time, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from typing import Optional


class APWI(Base):
    __tablename__ = "apwi"

    id: Optional[int] = Column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    airdate = Column(String, nullable=False)
    title = Column(String, nullable=False)
    network = Column(String, nullable=False)
    filename = Column(String, nullable=True)
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )


class STATION(Base):
    __tablename__ = "station"

    idStation = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    frequency = Column(String, nullable=False)
    location = Column(
        Integer, ForeignKey("location.idLocation", ondelete="CASCADE"), nullable=False
    )
    airtime = Column(
        Integer, ForeignKey("airtime.idAirtime", ondelete="CASCADE"), nullable=False
    )
    live = Column(Boolean, nullable=False, server_default="0")
    network = Column(String, nullable=True)
    url = Column(String, nullable=True)
    image = Column(String, nullable=True)
    name = Column(String, nullable=True)
    callLetters = Column(String, nullable=True)


class AIRTIME(Base):
    __tablename__ = "airtime"

    idAirtime = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    time = Column(Time, nullable=False)
    airdays = Column(String, nullable=False)  # weekdays, saturday, sunday


class LOCATION(Base):
    __tablename__ = "location"

    idLocation: Optional[int] = Column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)


class User(Base):
    __tablename__ = "users"
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
