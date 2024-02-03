from fastapi import APIRouter
from schemas import WatchlistStatistics, OverallStatistics
from sqlalchemy import text
from database import engine
from utils import FormatType, token_dependency
import pandas as pd
from fastapi.responses import StreamingResponse
import io
from starlette import status

router = APIRouter()

# Τα endpoints /user_stats_watchlists και /top_genres_overall είναι για τη
# λειτουργική απαίτηση του requirements workshop 2023:
# "Υπολογισμός προφιλ χρηστη με βαση τις ταινιες που αυτος εχει ηδη δει.
# Πχ στο προφιλ αρεσουν 20% ταινιες δρασης, 15% θριλερ, 40% κωμωδίες κτλ."

@router.get("/user_stats_watchlists", response_model=list[WatchlistStatistics], status_code=status.HTTP_200_OK)
async def genres_per_watchlist(user_id: token_dependency,
                               format: FormatType = FormatType.json):
    
    query = f"""select watchlists.library_name, watchlists.item_count, genre_name, title_count
            from (
                select watchlists.id as w_id, genre.name as genre_name, count(genre.id) as title_count
                from genre
                inner join title_genre on title_genre.genre = genre.id
                inner join watchlist_content on watchlist_content.title_id = title_genre.tconst
                inner join watchlists on watchlists.id = watchlist_content.watchlist_id
                where watchlists.user_id = {user_id}
                group by genre.id, watchlists.id
                )
            inner join watchlists on watchlists.id = w_id
            order by watchlists.library_name asc, title_count desc, genre_name asc;
        """
        
    with engine.connect() as connection:
        result = connection.execute(text(query))
        connection.close()
    
    if format == FormatType.csv:

        df = pd.DataFrame(result, columns=["Your Library Name",
                                           "Number of Titles in the Library",
                                           "Genre",
                                           "Number of Titles Belonging to Genre"])
        stream = io.StringIO()
        df.to_csv(stream, index=False, encoding='utf-8')
        response = StreamingResponse(iter([stream.getvalue()]),
                                     media_type="text/csv"
                                     )
        response.headers["Content-Disposition"] = "attachment; filename=statistics_per_watchlist.csv"

        return response

    WatchlistsStatistics_json = []
    GenreStatistics_json = []
    prev_row = None

    for row in result:

        if prev_row is None or prev_row.library_name == row.library_name:
            GenreStatistics_json.append(
                {
                    "genre_name": row.genre_name,
                    "title_count": row.title_count
                })
            prev_row = row
        else:
            WatchlistsStatistics_json.append(
                {
                    "library_name": prev_row.library_name,
                    "item_count": prev_row.item_count,
                    "items_per_genre": GenreStatistics_json
                })
            GenreStatistics_json = [
                {
                    "genre_name": row.genre_name,
                    "title_count": row.title_count
                }
            ]
            prev_row = None

    # Append the last WatchlistsStatistics Object after the loop
    if prev_row is not None:
        WatchlistsStatistics_json.append(
            {
                "library_name": prev_row.library_name,
                "item_count": prev_row.item_count,
                "items_per_genre": GenreStatistics_json
            })

    return WatchlistsStatistics_json


@router.get('/top_genres_overall', response_model=OverallStatistics, status_code=status.HTTP_200_OK)
async def genres_overall(user_id: token_dependency,
                               format: FormatType = FormatType.json):
    
    query_top_genres = f"""select genre.name as genre_name, count(genre.id) as title_count
                    from genre
                    inner join title_genre on title_genre.genre = genre.id
                    inner join watchlist_content on watchlist_content.title_id = title_genre.tconst
                    inner join watchlists on watchlists.id = watchlist_content.watchlist_id
                    where watchlists.user_id = {user_id}
                    group by genre.id
                    order by title_count desc, genre_name asc
                """
    
    query_total_number = f"""select sum(item_count) as total_number
                        from watchlists
                        where user_id = {user_id}
                        group by user_id;
                    """

    with engine.connect() as connection:
        result_top_genres = connection.execute(text(query_top_genres))
        result_total_number = connection.execute(text(query_total_number))
        connection.close()
    
    row_total_number = result_total_number.fetchone()
    if row_total_number is None:
        total_number = 0
    else:
        total_number = row_total_number.total_number

    if format == FormatType.csv:
        # Dataframe containing only the top genres
        df = pd.DataFrame(result_top_genres, columns=["Genre",
                                                      "Total Number of Titles Belonging to Genre"])

        # Create a column containing the result_total_number to insert into the dataframe
        df.insert(0, "Total Number of Titles in All Libraries", total_number, True)

        stream = io.StringIO()
        df.to_csv(stream, index=False, encoding='utf-8')
        response = StreamingResponse(iter([stream.getvalue()]),
                                     media_type="text/csv"
                                     )
        response.headers["Content-Disposition"] = "attachment; filename=top_genres_overall.csv"

        return response
    
    GenreStatistics_json = []

    for row in result_top_genres:
        GenreStatistics_json.append({
            "genre_name": row.genre_name,
            "title_count": row.title_count
        })

    OverallStatistics_json = {
        "total_number": total_number,
        "items_per_genre": GenreStatistics_json
    }

    return OverallStatistics_json