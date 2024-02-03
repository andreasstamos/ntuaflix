from pydantic import BaseModel

class GenreStatistics(BaseModel):
    genre_name: str
    title_count: int

class WatchlistStatistics(BaseModel):
    library_name: str
    item_count: int
    items_per_genre: list[GenreStatistics]

class OverallStatistics(BaseModel):
    total_number: int
    items_per_genre: list[GenreStatistics]