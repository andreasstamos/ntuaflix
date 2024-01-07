import aiofiles
import asyncio

from parser_tsv import parse_title_basics, parse_title_ratings, parse_title_principals,\
        parse_title_crew, parse_title_akas, parse_name_basics, parse_title_episode

async def main():
    async with aiofiles.open('truncated_data/truncated_title.basics.tsv', 'r') as afp:
        await parse_title_basics(afp)

    async with aiofiles.open('truncated_data/truncated_title.ratings.tsv', 'r') as afp:
        await parse_title_ratings(afp)

    async with aiofiles.open('truncated_data/truncated_title.principals.tsv', 'r') as afp:
        await parse_title_principals(afp)

    async with aiofiles.open('truncated_data/truncated_title.crew.tsv', 'r') as afp:
        await parse_title_crew(afp)

    async with aiofiles.open('truncated_data/truncated_title.akas.tsv', 'r') as afp:
        await parse_title_akas(afp)

    async with aiofiles.open('truncated_data/truncated_name.basics.tsv', 'r') as afp:
        await parse_name_basics(afp)

    async with aiofiles.open('truncated_data/truncated_title.episode.tsv', 'r') as afp:
        await parse_title_episode(afp)

asyncio.run(main())
print("Data import complete.")

