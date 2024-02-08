from pydantic import BaseModel
from datetime import date

class GenreStatistics(BaseModel):
    genre_name: str
    title_count: int

class TitleStattistics(BaseModel):
    date_posted: date
    tconst: str
    original_title: str

class ReactionStatistics(BaseModel):
    date_posted: date
    stars: int
    tconst: str
    original_title: str

class WatchlistStatistics(BaseModel):
    library_name: str
    item_count: int
    items_per_genre: list[GenreStatistics]

class OverallStatistics(BaseModel):
    total_number: int
    items_per_genre: list[GenreStatistics]

class ReviewStatistics(BaseModel):
    num_total_reviews: int
    num_total_users: int
    average_stars: float
    user_num_reviews: int
    user_avg_stars: float
    highest_ranking: int
    lowest_ranking: int
    count_most_likes: int
    count_most_dislikes: int
    highest_ranked_titles: list[TitleStattistics]
    lowest_ranked_titles: list[TitleStattistics]
    most_liked: list[ReactionStatistics]
    most_disliked: list[ReactionStatistics]