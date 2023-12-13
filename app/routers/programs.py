from typing import Optional, List
from fastapi import HTTPException, Response, Depends, status, APIRouter, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
import datetime
from ..database import get_db
from .. import schemas, models, oauth2

router = APIRouter(prefix="/v1", tags=["Apply Within Programs"])

today = datetime.date.today().isoformat()


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
    include_in_schema=False,
)
def create_program(
    program: schemas.ProgramCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_program = models.APWI(owner_id=current_user.id, **program.dict())
    db.add(new_program)
    db.commit()
    db.refresh(new_program)

    return new_program
