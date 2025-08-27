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
    network = Column(String, nullable=True)
    url = Column(String, nullable=True)
    image = Column(String, nullable=True)
    name = Column(String, nullable=True)
    frequency = Column(String, nullable=True, default=None)
    # location = Column(Integer, ForeignKey("location.idLocation", ondelete="CASCADE"), nullable=True)
    # airtime = Column(Integer, ForeignKey("airtime.idAirtime", ondelete="CASCADE"), nullable=True)
    live = Column(Boolean, nullable=True, default=False)
    callletters = Column(String, nullable=True)
    locations = relationship("LOCATION", secondary="station_location", back_populates="stations")
    airtimes = relationship("AIRTIME", secondary="station_airtime", back_populates="stations")


class AIRTIME(Base):
    __tablename__ = "airtime"

    idAirtime = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    time = Column(Time, nullable=False)
    airdays = Column(String, nullable=False)  # weekdays, saturday, sunday
    stations = relationship("STATION", secondary="station_airtime", back_populates="airtimes")

class StationAirtime(Base):
    __tablename__ = "station_airtime"
    station_id = Column(Integer, ForeignKey("station.idStation"), primary_key=True)
    airtime_id = Column(Integer, ForeignKey("airtime.idAirtime"), primary_key=True)


class LOCATION(Base):
    __tablename__ = "location"

    idLocation: Optional[int] = Column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
    stations = relationship("STATION", secondary="station_location", back_populates="locations")

class StationLocation(Base):
    __tablename__ = "station_location"
    station_id = Column(Integer, ForeignKey("station.idStation"), primary_key=True)
    location_id = Column(Integer, ForeignKey("location.idLocation"), primary_key=True)


class User(Base):
    __tablename__ = "users"
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
