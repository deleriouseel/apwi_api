from typing import Optional, List, Union
from fastapi import HTTPException, FastAPI, Response, Depends, status, APIRouter, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from pydantic import Required
import datetime
from ..database import get_db
from .. import schemas, models

router = APIRouter(
	prefix="/v1"
)

today = datetime.date.today().isoformat()


#get list of programs on one network
@router.get("/{network}", summary="List programs on one network: CALVARY or ACN")
def get_network(network, response: Response, db: Session= Depends(get_db), search: Optional[str]=None):
    """
    List programs by network (CALVARY or ACN). Returned in reverse chronological order from today's date.
    
    Search within network with network?search=

    For future programs use "Get programs by network and date" endpoint: /v1/{network}/{start_date}?end_date=
    """
    network = network.upper()
    if search is None:
        programs = db.query(models.APWI).filter(models.APWI.network == network).filter(models.APWI.airdate <= today).order_by(desc(models.APWI.airdate)).all()
    else:
        programs = db.query(models.APWI).filter(models.APWI.network == network).filter(models.APWI.airdate <= today).filter(models.APWI.title.ilike(f'%{search}%')).order_by(desc(models.APWI.airdate)).all() 

    if not programs:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database did not return any programs")
    return programs

#get list of programs on a network by date
@router.get("/{network}/{start_date}", summary="Get programs by network and date")
def get_network_dates (network: str,  response: Response, db: Session= Depends(get_db), start_date: str = Query(regex="^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"), end_date: Optional[str] = Query(default=None, regex="^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$")):
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



