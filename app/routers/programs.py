from typing import Optional, List
from fastapi import HTTPException, Response, Depends, status, APIRouter, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
import datetime
from ..database import get_db
from .. import schemas, models, oauth2

router = APIRouter(prefix="/v1", tags=["Apply Within Programs"])

today = datetime.date.today().isoformat()


def _get_program_or_404(id: int, db: Session) -> models.APWI:
    program = db.query(models.APWI).filter(models.APWI.id == id).first()

    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Program with id: {id} does not exist",
        )

    return program


# Get list of programs ordered by descending date
@router.get(
    "/programs",
    status_code=status.HTTP_200_OK,
    summary="Get list of all programs",
    response_model=List[schemas.ProgramBase],
)
def get_programs(
    response: Response,
    db: Session = Depends(get_db),
    search: Optional[str] = Query(default=None),
    skip: int = 0,
    limit: int = 40,
):
    """
    List all Apply Within programs. Returned in reverse chronological order from today's date.

    Returns 40 programs (one month) by default. Use: ?limit= to get more results. ?skip= to get earlier results.

    Search all programs by title using: /?search=
    """
    # Sqlalchemy doesn't like ilike with None types so don't make it.
    if search is None:
        programs = (
            db.query(models.APWI)
            .filter(models.APWI.airdate <= datetime.date.today().isoformat())
            .order_by(desc(models.APWI.airdate), (models.APWI.network))
            .limit(limit)
            .offset(skip)
            .all()
        )
    else:
        programs = (
            db.query(models.APWI)
            .filter(models.APWI.airdate <= datetime.date.today().isoformat())
            .filter(models.APWI.title.ilike(f"%{search}%"))
            .limit(limit)
            .offset(skip)
            .all()
        )

    if not programs:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database did not return any programs",
        )

    return programs


@router.post(
    "/programs",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ProgramBase,
)
def create_program(
    program: schemas.ProgramCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Add a radio program to the database.

    """
    new_program = models.APWI(owner_id=current_user.id, **program.dict())
    db.add(new_program)
    db.commit()
    db.refresh(new_program)

    return new_program


@router.patch(
    "/programs/{id}",
    status_code=status.HTTP_200_OK,
    summary="Update a program",
    response_model=schemas.ProgramBase,
)
def patch_program(
    id: int,
    program: schemas.ProgramUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Partially update a program. Only the fields sent are changed.
    """
    existing = _get_program_or_404(id, db)

    updates = program.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided to update.",
        )

    for field, value in updates.items():
        # airdate is stored as a string column, so normalise the parsed date.
        setattr(existing, field, value.isoformat() if field == "airdate" else value)

    db.commit()
    db.refresh(existing)

    return existing


@router.delete(
    "/programs/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a program",
)
def delete_program(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Delete a program.
    """
    program = _get_program_or_404(id, db)

    db.delete(program)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
