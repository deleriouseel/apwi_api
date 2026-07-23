from typing import Optional, List
from fastapi import HTTPException, Response, Depends, status, APIRouter, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
import datetime
from ..database import get_db
from .. import schemas, models, oauth2

router = APIRouter(prefix="/v1/locations", tags=["Radio Station Locations"])

today = datetime.date.today().isoformat()


def _get_location_or_404(idLocation: int, db: Session) -> models.LOCATION:
    location = (
        db.query(models.LOCATION)
        .filter(models.LOCATION.idLocation == idLocation)
        .first()
    )

    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with id: {idLocation} does not exist",
        )

    return location


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


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Add a location",
    response_model=schemas.LocationBase,
)
def create_location(
    location: schemas.LocationCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Add a location to the database.
    """
    new_location = models.LOCATION(**location.model_dump())
    db.add(new_location)
    db.commit()
    db.refresh(new_location)

    return new_location


@router.patch(
    "/{idLocation}",
    status_code=status.HTTP_200_OK,
    summary="Update a location",
    response_model=schemas.LocationBase,
)
def patch_location(
    idLocation: int,
    location: schemas.LocationUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Partially update a location. Only the fields sent are changed.
    """
    existing = _get_location_or_404(idLocation, db)

    updates = location.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided to update.",
        )

    for field, value in updates.items():
        setattr(existing, field, value)

    db.commit()
    db.refresh(existing)

    return existing


@router.delete(
    "/{idLocation}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a location",
)
def delete_location(
    idLocation: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Delete a location and unlink it from any stations.
    """
    location = _get_location_or_404(idLocation, db)

    location.stations.clear()
    db.delete(location)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
