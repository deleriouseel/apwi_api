from typing import Optional, List, Union
from fastapi import HTTPException, FastAPI, Response, Depends, status, APIRouter, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from pydantic import Required
import datetime
from ..database import get_db
from .. import schemas, models

router = APIRouter(
	prefix="/v1/programs"
)

today = datetime.date.today().isoformat()


#get list of programs ordered by descending date
@router.get("/", status_code=status.HTTP_200_OK, summary="Get list of all programs")
def get_programs(db: Session= Depends(get_db)):
    """
    List all Apply Within programs. Returned in reverse chronological order from today's date.
    """
    
    programs = db.query(models.APWI).filter(models.APWI.airdate <= today).order_by(desc(models.APWI.airdate)).all()

    if not programs:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database did not return any programs")
    return programs


#get list of programs by title
@router.get("/{search}", summary="Get programs by book title")
def get_titles(search: str, response: Response, db: Session= Depends(get_db)):
    """
    List all Apply Within programs with search term in title.
    """

    programs = db.query(models.APWI).filter(models.APWI.title.ilike('%'+ search +'%')).order_by(desc(models.APWI.airdate)).all()
    print(programs)
    if not programs:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database did not return any programs")
    return programs  

