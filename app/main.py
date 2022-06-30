from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from dateutil import parser
import psycopg2
from sqlalchemy.orm import Session
from sqlalchemy import desc
from . import models
from .config import settings
from .database import engine, get_db
import datetime


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

today = datetime.date.today().isoformat()

class Program(BaseModel):
    id: int
    title: str  
    link: str
    network: str
    date: str


def parsedate(dates):
    parsed_date = "words go here"
    return parsed_date


#root 
@app.get("/")
def read_root():
    return {"Hello": "World"}

#get list of radio stations in each network
@app.get("/v1/networks")
def get_network():
    return {"network": "Calvary or ACN"}

#get list of programs on a network by date
@app.get("/v1/networks/{dates}")
def get_network_dates (dates: int, response: Response):

    if not dates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Date not in correct format. Please use YYYY-MM-DD.")
    return{"network": f"the titles for {dates} are"}

#get list of programs ordered by descending  date
@app.get("/v1/programs", status_code=status.HTTP_200_OK)
def get_programs(response: Response, db: Session= Depends(get_db)):

    programs = db.query(models.APWI).order_by(desc(models.APWI.airdate)).filter(models.APWI.airdate <= today).all()

    if not programs:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database did not return any programs")
    return {"programs" : programs}

#get list of programs by title
@app.get("/v1/titles")
def get_titles (response: Response, db: Session= Depends(get_db)):

    titles = db.query(models.APWI).filter(models.APWI.title).all()
    return {"titles": "dates and network"}