from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Genre
from sqlalchemy.orm import joinedload
import json
from schemas import TitleObject
router = APIRouter()

# Index Route File


# INEFFICIENT MUST CHANGE LATER
@router.get('/index-movies')
async def index(db: Session = Depends(get_db)):
    # Assuming Genre and Title are your SQLAlchemy models
    genres = db.query(Genre).limit(5).all()
    movies = []

    for genre in genres:
        # Use joinedload to eager load the Genre relationship
        genre_with_movies = db.query(Genre).filter_by(id=genre.id).options(joinedload(Genre.titles)).first()
        
        if genre_with_movies:
            # Assuming Genre.titles is the relationship between Genre and Title
            genre_movies = genre_with_movies.titles
            non_adult_movies = [movie for movie in genre_movies if not movie.is_adult][:20]
            movies.append({
                'genre': genre.name,
                'movies': non_adult_movies,
            })

    return movies