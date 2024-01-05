# Import necessary libraries
from typing import List
from sqlalchemy import create_engine, Sequence,Column, Integer, String, Date, Boolean, ForeignKey, Float, CHAR, REAL, Index, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Mapped
import os
from dotenv import load_dotenv
from datetime import date

env_path = '.env'
load_dotenv(dotenv_path=env_path)

DB_USERSNAME = str(os.getenv('DB_USERNAME'))
DB_PASSWORD = str(os.getenv('DB_PASSWORD'))
DB_HOST = str(os.getenv('DB_HOST'))
DB_DATABASE = str(os.getenv('DB_DATABASE'))

# Replace 'your_username', 'your_password', 'your_database', and 'your_host' with your PostgreSQL credentials
DATABASE_URL = f"postgresql://{DB_USERSNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"
#DATABASE_URL = "sqlite+pysqlite:///ntuaflix.sqlite3" #### TODO: ONLY FOR DEV

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a declarative base class
Base = declarative_base()


# Define the User class
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(500), nullable=False)
    dob = Column(Date, nullable=False)
    is_admin = Column(Boolean, default=False)


class PersonalCollection(Base):
    __tablename__ = 'personal_collection'
    
    users_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    tconst = Column(CHAR(9), ForeignKey('title.tconst'), primary_key=True)

# Indexes for personal_collection
Index('idx_users_id', PersonalCollection.users_id)
Index('idx_tconst', PersonalCollection.tconst)

table_person_known_for_titles = Table(
        "person_known_for_titles",
        Base.metadata,
        Column("tconst", ForeignKey("title.tconst"), primary_key=True),
        Column("nconst", ForeignKey("person.nconst"), primary_key=True),
        )

table_title_director = Table(
        "title_director",
        Base.metadata,
        Column("tconst", ForeignKey("title.tconst"), primary_key=True),
        Column("nconst", ForeignKey("person.nconst"), primary_key=True),
        )

table_title_writer = Table(
        "title_writer",
        Base.metadata,
        Column("tconst", ForeignKey("title.tconst"), primary_key=True),
        Column("nconst", ForeignKey("person.nconst"), primary_key=True),
        )

table_title_genre = Table(
        "title_genre",
        Base.metadata,
        Column("genre", ForeignKey("genre.id"), primary_key=True),
        Column("tconst", ForeignKey("title.tconst"), primary_key=True),
        )



# Creating the tables and the indexes ...
class Title(Base):
    __tablename__ = 'title'
    
    tconst = Column(CHAR(9), primary_key=True)
    end_year = Column(Integer)
    primary_title = Column(String(100), nullable=False)
    original_title = Column(String(100), nullable=False)
    title_type = Column(String(10), nullable=False)
    runtime_minutes = Column(Integer, nullable=True)
    start_year = Column(Integer, nullable=False)
    is_adult = Column(Boolean, nullable=False)
    image_url = Column(String(100))
    principals = Column(Integer, nullable=False)
    average_rating = Column(Float)
    num_votes = Column(Integer)

    known_for_by: Mapped[List['Person']] = relationship(secondary=table_person_known_for_titles, back_populates="known_for_titles")
    principals: Mapped[List['Principals']] = relationship(back_populates="title")
    directors: Mapped[List['Person']] = relationship(secondary=table_title_director, back_populates="titles_as_director")
    writers: Mapped[List['Person']] = relationship(secondary=table_title_writer, back_populates="titles_as_writer")
    aliases: Mapped[List['TitleAlias']] = relationship(back_populates="title")
    genres: Mapped[List['Genre']] = relationship(secondary=table_title_genre, back_populates="titles")

    episodes: Mapped[List['TitleEpisode']] = relationship(back_populates="parent", foreign_keys="TitleEpisode.parent_tconst")

# Add the index
Index('idx_title_type', Title.title_type)

class TitleEpisode(Base):
    __tablename__ = 'title_episode'
    
    episode_tconst = Column(CHAR(9), ForeignKey('title.tconst'), primary_key=True)
    episode: Mapped['Title'] = relationship(foreign_keys=[episode_tconst])

    parent_tconst = Column(CHAR(9), ForeignKey('title.tconst'), nullable=False)
    parent: Mapped['Title'] = relationship(foreign_keys=[parent_tconst], back_populates="episodes")
    
    season_number = Column(Integer)
    episode_number = Column(Integer)

# Add the title_episode index
Index('idx_parent_tconst',TitleEpisode.parent_tconst) 

class TitleAlias(Base):
    __tablename__ = 'title_alias'
    
    id = Column(Integer, primary_key=True)
    tconst = Column(CHAR(9), ForeignKey('title.tconst'), nullable=False)
    title: Mapped['Title'] = relationship(back_populates="aliases")
    
    title_name = Column(String(255), nullable=False)
    ordering = Column(Integer, nullable=False)
    region = Column(String(2), nullable=True)
    language = Column(String(2), nullable=True)
    types = Column(String(10))
    attributes = Column(String(255))
    is_original_title = Column(Boolean, nullable=False)

# Index for tilte_alias
Index('idx_tconst_alias', TitleAlias.tconst)


class Genre(Base):
    __tablename__ = 'genre'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    titles: Mapped[List['Title']] = relationship(secondary=table_title_genre, back_populates="genres")



table_person_profession = Table(
        "person_profession",
        Base.metadata,
        Column("profession", ForeignKey("profession.id"), primary_key=True),
        Column("nconst", ForeignKey("person.nconst"), primary_key=True),
        )


class Person(Base):
    __tablename__ = 'person'
    
    nconst = Column(CHAR(9), primary_key=True)
    image_url = Column(String(255))
    primary_name = Column(String(100), nullable=False)
    birth_year = Column(Integer)
    death_year = Column(Integer)

    primary_professions: Mapped[List['Profession']] = relationship(secondary=table_person_profession, back_populates="people")
    known_for_titles: Mapped[List['Title']] = relationship(secondary=table_person_known_for_titles, back_populates="known_for_by")

    image_url = Column(String(100))

    titles_as_principal: Mapped[List['Principals']] = relationship(back_populates="person")

    titles_as_director: Mapped[List['Title']] = relationship(secondary=table_title_director, back_populates="directors")
    titles_as_writer: Mapped[List['Title']] = relationship(secondary=table_title_writer, back_populates="writers")



class Profession(Base):
    __tablename__ = 'profession'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    people: Mapped[List['Person']] = relationship(secondary=table_person_profession, back_populates="primary_professions")


class Principals(Base):
    __tablename__ = 'principals'
    
    id = Column(Integer, primary_key=True)
    tconst = Column(CHAR(9), ForeignKey('title.tconst'), nullable=False)
    title: Mapped['Title'] = relationship(back_populates="principals")
    nconst = Column(CHAR(9), ForeignKey('person.nconst'), nullable=False)
    person: Mapped['Person'] = relationship(back_populates="titles_as_principal")
    
    category_id = Column(Integer, ForeignKey('profession.id'), nullable=False)
    category: Mapped['Profession'] = relationship(foreign_keys=[category_id])

    job_id = Column(Integer, ForeignKey('profession.id'))
    job: Mapped['Profession'] = relationship(foreign_keys=[job_id])

    ordering = Column(Integer)
    characters = Column(String(255))
    image_url = Column(String(255))

# Indexes for principals
Index('idx_tconst_principals', Principals.tconst)
Index('idx_nconst_principals', Principals.nconst)
Index('idx_category_id_principals', Principals.category_id)
Index('idx_job_id_principals', Principals.job_id)


# # Create the table in the database
Base.metadata.create_all(engine)

# # Create a session to interact with the database
# Session = sessionmaker(bind=engine)
# session = Session()

# # Example: Adding a user to the database with date of birth and password
# new_user = User (
    # username='user',
    # first_name='user_firstname',
    # last_name='user_lastname',
    # email='user@example.com',
    # dob=date(2002, 2, 2),  # Replace with the actual date of birth
    # password='secure_password'  # Replace with the actual password
# )

# session.add(new_user)
# session.commit()

# # Querying the database
# user_query = session.query(User).filter_by(username='user').first()
# print(user_query.username, user_query.email, user_query.dob, user_query.password)

# # Remember to close the session when done
# session.close()
