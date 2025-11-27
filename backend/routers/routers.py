from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import schemas
from .. import models
from ..database import get_db

router = APIRouter()

@router.get("/artists", response_model=List[schemas.ArtistOut])
def list_artists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    artists = db.query(models.Artist).offset(skip).limit(limit).all()
    return artists

@router.get("/tracks", response_model=List[schemas.TrackOut])
def list_tracks(
    q: Optional[str] = Query(None, description="Buscar por nombre de track"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    query = db.query(models.Track)
    if q:
        query = query.filter(models.Track.Name.ilike(f"%{q}%"))
    tracks = query.offset(skip).limit(limit).all()
    return tracks

@router.get("/tracks/{track_id}", response_model=schemas.TrackOut)
def get_track(track_id: int, db: Session = Depends(get_db)):
    track = db.query(models.Track).filter(models.Track.TrackId == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track no encontrado")
    return track
