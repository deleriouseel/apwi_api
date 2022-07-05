from typing import Optional, List
from fastapi import HTTPException, Response, Depends, status, APIRouter, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
import datetime
from ..database import get_db
from .. import schemas, models

router = APIRouter(
    prefix="/v1",
    tags=['Apply Within Programs by Network']
)

today = datetime.date.today().isoformat()


# Get list of programs on one network
@router.get("/{network}", summary="List programs on one network: CALVARY or ACN", response_model=List[schemas.ProgramBase])
def get_network(network, response: Response, db: Session = Depends(get_db), search: Optional[str] = None, skip: int = 0, limit: int = 20):
    """
    List programs by network (CALVARY or ACN). Returned in reverse chronological order from today's date.

    Returns 20 programs (one month) by default. Use: ?limit= to get more results. ?skip= to get earlier results.

    Search within network for titles with network?search=

    For future programs use "Get programs by network and date" endpoint: /v1/{network}/{start_date}?end_date=
    """
    network = network.upper()

    # Sqlalchemy doesn't like ilike with  None types so don't make it.
    if search is None:
        programs = db.query(models.APWI).filter(models.APWI.network == network).filter(models.APWI.airdate <= datetime.date.today().isoformat()).order_by(desc(models.APWI.airdate)).limit(limit).offset(skip).all()
    else:
        programs = db.query(models.APWI).filter(models.APWI.network == network).filter(models.APWI.airdate <= datetime.date.today().isoformat()).filter(models.APWI.title.ilike(f'%{search}%')).order_by(desc(models.APWI.airdate)).limit(limit).offset(skip).all()

    if not programs:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database did not return any programs")
    return programs


# Get list of programs on a network by date
@router.get("/{network}/{start_date}", summary="Get programs by network and date", response_model=List[schemas.ProgramBase])
def get_network_dates(network: str,  response: Response, db: Session = Depends(get_db), start_date: str = Query(regex="^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"), end_date: Optional[str] = Query(default=None, regex="^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$")):
    """
    Get programs on a specific network (CALVARY or ACN) by date (YYYY-MM-DD).
  
    To return a range add ?end_date="YYYY-MM-DD" to query. Returned in reverse chronological order.
    """
    network = network.upper()
    # Gotta have range
    if not end_date:
        end_date = start_date
     
    programs = db.query(models.APWI).filter(models.APWI.network == network).filter(models.APWI.airdate.between(start_date, end_date)).order_by(desc(models.APWI.airdate)).all()

    # if not start_date:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database did not return any programs")
    if not programs:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database did not return any programs.")    

    return programs
