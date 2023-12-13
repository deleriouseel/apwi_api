from typing import Optional, List
from fastapi import HTTPException, Response, Depends, status, APIRouter, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
import datetime
from ..database import get_db
from .. import schemas, models

router = APIRouter(prefix="/v1", tags=["Apply Within Radio Stations"])

today = datetime.date.today().isoformat()


@router.get(
    "/stations",
    status_code=status.HTTP_200_OK,
    summary="Get list of all radio stations",
    response_model=List[schemas.ProgramBase],
)
async def get_stations(
    response: Response,
    db: Session = Depends(get_db),
    search: Optional[str] = Query(default=None),
    skip: int = 0,
    limit: int = 50,
):
    """
    List all radio stations Apply Within airs on.


    """
    # Sqlalchemy doesn't like ilike with None types so don't make it.
    if search is None:
        stations = (
            db.query(models.STATION)
            .join(
                models.LOCATION,
                models.Location.idLocation == models.STATION.location,
                isouter=True,
            )
            .all()
        )
    else:
        stations = (
            db.query(models.STATION)
            .filter(models.STATION.airdate <= datetime.date.today().isoformat())
            .filter(models.STATION.title.ilike(f"%{search}%"))
            .limit(limit)
            .offset(skip)
            .all()
        )

    if not stations:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database did not return any radio stations.",
        )

    return stations


@router.post(
    "/stations",
    status_code=status.HTTP_200_OK,
    summary="Add a radio station",
    response_model=List[schemas.ProgramBase],
    include_in_schema=False,
)
def post_stations(response: Response, db: Session = Depends(get_db)):
    """
    Add a radio station to the database
    """

    return response
