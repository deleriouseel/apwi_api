from typing import Optional, List
from fastapi import HTTPException, Response, Depends, status, APIRouter, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
import datetime
from ..database import get_db
from .. import schemas, models

router = APIRouter(
    prefix="/v1",
    tags=['Apply Within Programs']
)

today = datetime.date.today().isoformat()


# Get list of programs ordered by descending date
@router.get("/programs", status_code=status.HTTP_200_OK, summary="Get list of all programs",
            response_model=List[schemas.ProgramBase])
def get_programs(response: Response, db: Session = Depends(get_db), search: Optional[str] = Query(default=None),
                 skip: int = 0, limit: int = 40):
    """
    List all Apply Within programs. Returned in reverse chronological order from today's date.

    Returns 40 programs (one month) by default. Use: ?limit= to get more results. ?skip= to get earlier results.
    
    Search all programs by title using: /?search=
    """
    # Sqlalchemy doesn't like ilike with None types so don't make it.
    if search is None:
        programs = db.query(models.APWI).filter(models.APWI.airdate <= datetime.date.today().isoformat()).order_by(desc(models.APWI.airdate)).limit(limit).offset(skip).all()
    else:   
        programs = db.query(models.APWI).filter(models.APWI.airdate <= datetime.date.today().isoformat()).filter(models.APWI.title.ilike(f'%{search}%')).limit(limit).offset(skip).all()

    if not programs:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database did not return any programs")

    return programs

