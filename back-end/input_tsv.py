import pandas as pd
from sqlalchemy.orm import Session
from models import *

# Function to read a TSV file
def read_tsv(file_path):
    return pd.read_csv(file_path, delimiter='\t', na_values=['\\N'], dtype=str)

# Read the files
titles_basics_df = read_tsv('truncated_data/truncated_title.basics.tsv')
titles_ratings_df = read_tsv('truncated_data/truncated_title.ratings.tsv')
titles_principals_df = read_tsv('truncated_data/truncated_title.principals.tsv')
titles_crew_df = read_tsv('truncated_data/truncated_title.crew.tsv')
titles_akas_df = read_tsv('truncated_data/truncated_title.akas.tsv')
names_basics_df = read_tsv('truncated_data/truncated_name.basics.tsv')
titles_episodes_df = read_tsv('truncated_data/truncated_title.episode.tsv')

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        session.add(instance)
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        return instance


# Insert data into the database
with Session(engine) as session:
    # Inserting data into the Title table
    for _, row in titles_basics_df.iterrows():
        title = Title(
            tconst=row['tconst'],
            title_type=row['titleType'],
            primary_title=row['primaryTitle'],
            original_title=row['originalTitle'],
            is_adult=row['isAdult'] == '1',
            start_year=int(row['startYear']) if not pd.isna(row['startYear']) else None,
            end_year=int(row['endYear']) if not pd.isna(row['endYear']) else None,
            runtime_minutes=int(row['runtimeMinutes']) if not pd.isna(row['runtimeMinutes']) else None,
            image_url=row['img_url_asset']
        )
        # Ratings data
        ratings_row = titles_ratings_df[titles_ratings_df['tconst'] == row['tconst']]
        if not ratings_row.empty:
            title.average_rating = float(ratings_row.iloc[0]['averageRating'])
            title.num_votes = int(ratings_row.iloc[0]['numVotes'])

        # Genres data
        if not pd.isna(row['genres']):
            genres = row['genres'].split(',')
            for genre_name in genres:
                title.genres.append(get_or_create(session, Genre, name=genre_name))

        session.add(title)

    # Inserting data into the Person table
    for _, row in names_basics_df.iterrows():
        person = Person(
            nconst=row['nconst'],
            primary_name=row['primaryName'],
            birth_year=int(row['birthYear']) if not pd.isna(row['birthYear']) else None,
            death_year=int(row['deathYear']) if not pd.isna(row['deathYear']) else None,
            image_url=row['img_url_asset']
        )

        professions = row['primaryProfession'].split(',') if not pd.isna(row['primaryProfession']) else []
        for profession_name in professions:
            person.primary_professions.append(get_or_create(session, Profession, name=profession_name))

        known_for_titles = row['knownForTitles'].split(',') if not pd.isna(row['knownForTitles']) else []
        for title_id in known_for_titles:
            known_title = session.query(Title).filter_by(tconst=title_id).first()
            if known_title:
                person.known_for_titles.append(known_title)

        session.add(person)

    # Inserting data into Title_Principals
    for _, row in titles_principals_df.iterrows():
        principal = Principals(
            tconst=row['tconst'],
            ordering=int(row['ordering']),
            nconst=row['nconst'],
            category=get_or_create(session, Profession, name=row['category']),
            job=get_or_create(session, Profession, name=row['job']) if not pd.isna(row['job']) else None,
            characters=row['characters'],
            image_url=row['img_url_asset']
        )
        session.add(principal)
    
    # Inserting data into TitleAlias
    for _, row in titles_akas_df.iterrows():
        title_alias = TitleAlias(
            tconst=row['titleId'],
            title_name=row['title'],
            ordering=int(row['ordering']),
            region=row['region'] if not pd.isna(row['region']) else None,
            language=row['language'] if not pd.isna(row['language']) else None,
            types=row['types'],
            attributes=row['attributes'],
            is_original_title=row['isOriginalTitle'] == '1'
        )
        session.add(title_alias)

    # Handle Title_Crew (Directors and Writers)
    for _, row in titles_crew_df.iterrows():
        tconst = row['tconst']
        title = session.query(Title).filter_by(tconst=tconst).first()
        if not title:
            continue

        # Directors
        directors = row['directors'].split(',') if not pd.isna(row['directors']) else []
        for director_id in directors:
            director = session.query(Person).filter_by(nconst=director_id).first()
            if director:
                title.directors.append(director)

        # Writers
        writers = row['writers'].split(',') if not pd.isna(row['writers']) else []
        for writer_id in writers:
            writer = session.query(Person).filter_by(nconst=writer_id).first()
            if writer:
                title.writers.append(writer)

    for _, row in titles_episodes_df.iterrows():
        title = session.query(Title).filter_by(tconst=row['tconst']).first()
        if not title:
            continue
        parent = session.query(Title).filter_by(tconst=row['parentTconst']).first()
        if not parent:
            continue
        
        episode = TitleEpisode(
                episode=title,
                parent=parent,
                season_number=row['season_number'] if not pd.isna(row['season_number']) else None,
                episode_number=row['episode_number'] if not pd.isna(row['episode_number']) else None,
                )
        session.add(episode)


    session.commit()

print("Data import complete.")

