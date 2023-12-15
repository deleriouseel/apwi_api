from typing import Optional, List
from fastapi import HTTPException, Response, Depends, status, APIRouter, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
import datetime
from ..database import get_db
from .. import schemas, models

router = APIRouter(prefix="/v1/locations", tags=["Radio Station Locations"])

today = datetime.date.today().isoformat()


# Get list of locations
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Locations",
    response_model=List[schemas.LocationBase],
)
def get_location(
    response: Response,
    db: Session = Depends(get_db),
    search: Optional[str] = None,
):
    """
    List locations

    Search all locations by title using: /?search=

    """

    # Sqlalchemy doesn't like ilike with None types so don't make it.
    if search is None:
        locations = (
            db.query(models.LOCATION)
            .order_by(desc(models.LOCATION.country))
            .order_by(models.LOCATION.state)
            .order_by(models.LOCATION.city)
            .all()
        )
    else:
        locations = (
            db.query(models.LOCATION)
            .filter(
                or_(
                    models.LOCATION.city.ilike(f"%{search}%"),
                    models.LOCATION.state.ilike(f"%{search}%"),
                    models.LOCATION.country.ilike(f"%{search}%"),
                )
            )
            .order_by(desc(models.LOCATION.city))
            .all()
        )

    if not locations:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database did not return any locations",
        )
    return locations
