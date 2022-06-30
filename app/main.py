from fastapi import FastAPI, Response, status, HTTPException, Depends, Query
from pydantic import Required  
from typing import List, Union  
from dateutil import parser
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from . import models, schemas
from .database import engine, get_db
import datetime


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

today = datetime.date.today().isoformat()


def parsedate(dates):
    parsed_date = "words go here"
    return parsed_date


#root 
@app.get("/")
def read_root():
    return {"Hello": "World"}

#get list of programs ordered by descending date
@app.get("/v1/programs", status_code=status.HTTP_200_OK, summary="Get list of all programs")
def get_programs(response: Response, db: Session= Depends(get_db)):
    """
    List all Apply Within programs. Returned in reverse chronological order from today's date.
    """
    
    programs = db.query(models.APWI).filter(models.APWI.airdate <= today).order_by(desc(models.APWI.airdate)).all()

    if not programs:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database did not return any programs")
    return programs


#get list of programs by title
@app.get("/v1/books/{search}", summary="Get programs by book title")
def get_titles(search: str, response: Response, db: Session= Depends(get_db)):
    """
    List all Apply Within programs with search term in title.
    """

    programs = db.query(models.APWI).filter(models.APWI.title.ilike('%'+ search +'%')).order_by(desc(models.APWI.airdate)).all()
    print(programs)
    if not programs:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database did not return any programs")
    return programs  


#get list of radio stations in each network
@app.get("/v1/{network}", summary="List programs on one network: CALVARY or ACN")
def get_network(network, response: Response, db: Session= Depends(get_db)):
    """
    List programs by network (CALVARY or ACN). Returned in reverse chronological order from today's date.

    For future programs use /v1/{network}/{start_date}?end_date=
    """

    network = network.upper()

    programs = db.query(models.APWI).filter(models.APWI.network == network).filter(models.APWI.airdate <= today).order_by(desc(models.APWI.airdate)).all()

    if not programs:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database did not return any programs")
    return programs

#get list of programs on a network by date
@app.get("/v1/{network}/{start_date}", summary="Get programs by network and date")
def get_network_dates (network: str,  response: Response, db: Session= Depends(get_db), start_date: str = Query(default=Required, regex="^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"), end_date: Union[str, None] = Query(default=None, regex="^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$")):
    """
    Get programs on a specific network (CALVARY or ACN) by date (YYYY-MM-DD).  
    
    To return a range add ?end_date="YYYY-MM-DD" to query. Returned in reverse chronological order.
    """
    network = network.upper()
    #gotta have range
    if not end_date:
        end_date = start_date
      

    programs = db.query(models.APWI).filter(models.APWI.network == network).filter(models.APWI.airdate.between(start_date,end_date)).order_by(desc(models.APWI.airdate)).all()

    if not start_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Date not in correct format. Please use YYYY-MM-DD.")

    return programs