from sqlalchemy.orm import Session
from fastapi import UploadFile
import aiocsv

from models import *

NULL_TOKEN = r'\N'

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance is not None:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        return instance

async def parse_title_basics(afp, session):
    async for row in aiocsv.AsyncDictReader(afp, delimiter='\t'):
        title = Title(
            tconst=row['tconst'],
            title_type=row['titleType'],
            primary_title=row['primaryTitle'],
            original_title=row['originalTitle'],
            is_adult=row['isAdult'] == '1',
            start_year=int(row['startYear']) if row['startYear'] != NULL_TOKEN else None,
            end_year=int(row['endYear']) if row['endYear'] != NULL_TOKEN else None,
            runtime_minutes=int(row['runtimeMinutes']) if row['runtimeMinutes'] != NULL_TOKEN else None,
            image_url=row['img_url_asset'].replace('{width_variable}', 'original') if row['img_url_asset'] != NULL_TOKEN else None,
        )
        session.add(title)
        if row['genres'] != NULL_TOKEN:
            genres = row['genres'].split(',')
            for genre_name in genres:
                title.genres.append(get_or_create(session, Genre, name=genre_name))
    session.commit()

async def parse_title_ratings(afp, session):
    async for row in aiocsv.AsyncDictReader(afp, delimiter='\t'):
        title = session.query(Title).filter_by(tconst = row['tconst']).first()
        if title is None: continue
        title.average_rating = float(row['averageRating']) if row['averageRating'] != NULL_TOKEN else None
        title.num_votes = int(row['numVotes']) if row['numVotes'] != NULL_TOKEN else None
    session.commit()

async def parse_name_basics(afp, session):
    async for row in aiocsv.AsyncDictReader(afp, delimiter='\t'):
        person = Person(
            nconst=row['nconst'],
            primary_name=row['primaryName'],
            birth_year=int(row['birthYear']) if row['birthYear'] != NULL_TOKEN else None,
            death_year=int(row['deathYear']) if row['deathYear'] != NULL_TOKEN else None,
            image_url=row['img_url_asset'] if row['img_url_asset'] != NULL_TOKEN else None
        )
        session.add(person)

        if row['primaryProfession'] != NULL_TOKEN:
            for profession_name in row['primaryProfession'].split(','):
                person.primary_professions.append(get_or_create(session, Profession, name=profession_name))

        if row['knownForTitles'] != NULL_TOKEN:
            for title_id in row['knownForTitles'].split(','):
                known_title = session.query(Title).filter_by(tconst=title_id).first()
                if known_title != None:
                    person.known_for_titles.append(known_title)
    session.commit()

async def parse_title_principals(afp, session):
    async for row in aiocsv.AsyncDictReader(afp, delimiter='\t'):
        principal = Principals(
            tconst=row['tconst'],
            ordering=int(row['ordering']),
            nconst=row['nconst'],
            category=get_or_create(session, Profession, name=row['category']),
            job=get_or_create(session, Profession, name=row['job']) if row['job'] != NULL_TOKEN else None,
            characters=row['characters'],
            image_url=row['img_url_asset']
        )
        session.add(principal)
    session.commit()

async def parse_title_akas(afp, session):
    async for row in aiocsv.AsyncDictReader(afp, delimiter='\t'):
        title_alias = TitleAlias(
            tconst=row['titleId'],
            title_name=row['title'],
            ordering=int(row['ordering']),
            region=row['region'] if row['region'] != NULL_TOKEN else None,
            language=row['language'] if row['language'] != NULL_TOKEN else None,
            types=row['types'] if row['types'] != NULL_TOKEN else None,
            attributes=row['attributes'] if row['attributes'] != NULL_TOKEN else None,
            is_original_title=row['isOriginalTitle'] == '1'
        )
        session.add(title_alias)
    session.commit()

async def parse_title_crew(afp, session):
    async for row in aiocsv.AsyncDictReader(afp, delimiter='\t'):
        title = session.query(Title).filter_by(tconst=row['tconst']).first()
        if title is None: continue

        if row['directors'] != NULL_TOKEN:
            for nconst in row['directors'].split(','):
                person = session.query(Person).filter_by(nconst=nconst).first()
                if person is not None:
                    title.directors.append(person)

        if row['writers'] != NULL_TOKEN:
            for nconst in row['writers'].split(','):
                person = session.query(Person).filter_by(nconst=nconst).first()
                if person is not None:
                    title.writers.append(person)
    session.commit()

async def parse_title_episode(afp, session):
    async for row in aiocsv.AsyncDictReader(afp, delimiter='\t'):
        title = session.query(Title).filter_by(tconst=row['tconst']).first()
        if title is None: continue

        parent = session.query(Title).filter_by(tconst=row['parentTconst']).first()
        if parent is None: continue
    
        episode = TitleEpisode(
                episode=title,
                parent=parent,
                season_number=row['season_number'] if row['season_number'] != NULL_TOKEN else None,
                episode_number=row['episode_number'] if row['episode_number'] != NULL_TOKEN else None,
                )
        session.add(episode)
    session.commit()

