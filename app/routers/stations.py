from typing import Optional, List
from fastapi import HTTPException, Response, Depends, status, APIRouter, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
import datetime
from ..database import get_db
from .. import schemas, models, oauth2

router = APIRouter(prefix="/v1", tags=["Apply Within Radio Stations"])

today = datetime.date.today().isoformat()


def _get_station_or_404(idStation: int, db: Session) -> models.STATION:
    station = (
        db.query(models.STATION)
        .options(
            joinedload(models.STATION.locations),
            joinedload(models.STATION.airtimes),
        )
        .filter(models.STATION.idStation == idStation)
        .first()
    )

    if not station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Station with id: {idStation} does not exist",
        )

    return station


@router.get(
    "/stations",
    status_code=status.HTTP_200_OK,
    summary="Get list of all radio stations",
    response_model=List[schemas.StationBase],
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
            .options(
                joinedload(models.STATION.locations),
                joinedload(models.STATION.airtimes)
            )
            .limit(limit)
            .offset(skip)
            .all()
        )
    else:
        stations = (
            db.query(models.STATION)
            .filter(models.STATION.name.ilike(f"%{search}%"))
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


@router.get(
    "/stations/{idStation}",
    status_code=status.HTTP_200_OK,
    summary="Get a single radio station",
    response_model=schemas.StationBase,
)
def get_station(idStation: int, db: Session = Depends(get_db)):
    """
    Get one radio station by id.
    """
    station = _get_station_or_404(idStation, db)

    return station


@router.post(
    "/stations",
    status_code=status.HTTP_201_CREATED,
    summary="Add a radio station",
    response_model=schemas.StationBase,
)
def post_stations(
    station: schemas.StationCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Add a radio station to the database
    """
    # by_alias maps call_letters -> the "callletters" DB column.
    new_station = models.STATION(**station.model_dump(by_alias=True))
    db.add(new_station)
    db.commit()
    db.refresh(new_station)

    return new_station


@router.patch(
    "/stations/{idStation}",
    status_code=status.HTTP_200_OK,
    summary="Update a radio station",
    response_model=schemas.StationBase,
)
def patch_station(
    idStation: int,
    station: schemas.StationUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Partially update a radio station. Only the fields sent are changed.
    """
    existing = _get_station_or_404(idStation, db)

    # exclude_unset keeps an omitted field from being overwritten with None.
    updates = station.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided to update.",
        )

    for field, value in updates.items():
        # The model column is "callletters"; the API exposes "call_letters".
        setattr(existing, "callletters" if field == "call_letters" else field, value)

    db.commit()
    db.refresh(existing)

    return existing


@router.delete(
    "/stations/{idStation}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a radio station",
)
def delete_station(
    idStation: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Delete a radio station and its location/airtime links.
    """
    station = _get_station_or_404(idStation, db)

    # Clear the association rows first so the junction tables don't orphan.
    station.locations.clear()
    station.airtimes.clear()
    db.delete(station)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
