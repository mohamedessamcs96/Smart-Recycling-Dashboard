# app/routes/stats.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db        # same place you import it in items routes
from .. import crud            # uses your updated crud.get_stats

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/")
def read_stats(db: Session = Depends(get_db)):
    return crud.get_stats(db)