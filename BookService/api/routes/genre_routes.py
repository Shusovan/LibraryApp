from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from database.db_connection import get_db
from model.genre import Genre
from schema.genre_schema import BulkGenreCreate, GenreCreate

router = APIRouter()


@router.post("/add-genres/")
async def create_genre(genre: GenreCreate, db: Session = Depends(get_db)):

    genres = Genre(name=genre.name)

    db.add(genres)
    db.commit()
    db.refresh(genres)

    return genres


@router.post("/add-genres/bulk")
async def create_genres_bulk(bulk_genres: BulkGenreCreate, db: Session = Depends(get_db)):

    # Get existing genre names to avoid duplicates
    existing_genres = db.query(Genre.name).all()
    existing_names = {genre[0].lower() for genre in existing_genres}
    
    created_genres = []
    skipped_genres = []
    
    for genre_data in bulk_genres.genres:
        # Check if genre already exists (case-insensitive)
        if genre_data.name.lower() in existing_names:
            skipped_genres.append({"name": genre_data.name, "reason": "already_exists"})
            continue
            
        # Create new genre
        db_genre = Genre(name=genre_data.name)
        db.add(db_genre)
        existing_names.add(genre_data.name.lower())  # Update our tracking set
        created_genres.append(genre_data.name)
    
    # Commit all new genres at once
    db.commit()
    
    # Return results
    return {
        "created": created_genres,
        "skipped": skipped_genres,
        "total_created": len(created_genres),
        "total_skipped": len(skipped_genres)
    }


@router.get("/genres/")
async def get_all_genres(db: Session = Depends(get_db)):

    return db.query(Genre).all()


@router.get("/genres/by-name/{name}")
async def get_genre_by_name(name: str, db: Session = Depends(get_db)):

    genre = db.query(Genre).filter(Genre.name == name).first()
    
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    
    return genre