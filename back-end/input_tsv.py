from sqlalchemy.orm import Session
import aiofiles
import asyncio
from database import get_db

from utils import parse_title_basics, parse_title_ratings, parse_title_principals,\
        parse_title_crew, parse_title_akas, parse_name_basics, parse_title_episode

async def main():
    db = next(get_db())

    async with aiofiles.open('truncated_data/truncated_title.basics.tsv', 'r') as afp:
        await parse_title_basics(afp, db)

    async with aiofiles.open('truncated_data/truncated_title.ratings.tsv', 'r') as afp:
        await parse_title_ratings(afp, db)

    async with aiofiles.open('truncated_data/truncated_title.principals.tsv', 'r') as afp:
        await parse_title_principals(afp, db)

    async with aiofiles.open('truncated_data/truncated_title.crew.tsv', 'r') as afp:
        await parse_title_crew(afp, db)

    async with aiofiles.open('truncated_data/truncated_title.akas.tsv', 'r') as afp:
        await parse_title_akas(afp, db)

    async with aiofiles.open('truncated_data/truncated_name.basics.tsv', 'r') as afp:
        await parse_name_basics(afp, db)

    async with aiofiles.open('truncated_data/truncated_title.episode.tsv', 'r') as afp:
        await parse_title_episode(afp, db)

asyncio.run(main())
print("Data import complete.")