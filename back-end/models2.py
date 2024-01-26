from sqlalchemy import create_engine, Sequence,Column, Integer, String, Date, Boolean, ForeignKey, Float, CHAR, REAL, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker,relationship
import os
from dotenv import load_dotenv
from datetime import date
from db_type import *

env_path = '.env'
load_dotenv(dotenv_path=env_path)

DB_USERSNAME = str(os.getenv('DB_USERNAME'))
DB_PASSWORD = str(os.getenv('DB_PASSWORD'))
DB_HOST = str(os.getenv('DB_HOST'))
DB_DATABASE = str(os.getenv('DB_DATABASE'))

DB_TYPE, DATABASE_URL = db_type_url(DB_USERSNAME, DB_PASSWORD, DB_HOST, DB_DATABASE)

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a declarative base class
Base = declarative_base()

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
    personal_collections = relationship("PersonalCollection", back_populates="user")



class Title(Base):
    __tablename__ = 'title'
    tconst = Column(CHAR(9), primary_key=True)
    end_year = Column(Integer)
    primary_title = Column(String(100), nullable=False)
    original_title = Column(String(100), nullable=False)
    title_type = Column(String(10), nullable=False)
    runtime_minutes = Column(Integer, nullable=False)
    genre_id = Column(String(100), nullable=False)
    known_for_by = Column(Integer)
    start_year = Column(Integer, nullable=False)
    is_adult = Column(Boolean, nullable=False)
    image_url = Column(String(100))
    principals = Column(Integer, nullable=False)
    average_rating = Column(Float)
    num_votes = Column(Integer)
    directors = Column(Integer)
    writers = Column(Integer)
    title_episodes = relationship("TitleEpisode", back_populates="title")
    personal_collections = relationship("PersonalCollection", back_populates="title")
    title_aliases = relationship("TitleAlias", back_populates="title")
    title_genres = relationship("TitleGenre", back_populates="title")
    principals = relationship("Principals", back_populates="title")
    titles_directed = relationship("TitleDirector", back_populates="title")
    titles_written = relationship("TitleWriter", back_populates="title")

# Add the index
Index('idx_title_type', Title.title_type)


class TitleEpisode(Base):
    __tablename__ = 'title_episode' 
    episode_tconst = Column(CHAR(9), primary_key=True)
    parent_tconst = Column(CHAR(9), ForeignKey('title.tconst'), nullable=False)
    season_number = Column(Integer)
    episode_number = Column(Integer)
    title = relationship("Title", back_populates="title_episodes")

# Add the title_episode index
Index('idx_parent_tconst',TitleEpisode.parent_tconst) 


class PersonalCollection(Base):
    __tablename__ = 'personal_collection'
    # ... other columns ...
    user = relationship("User", back_populates="personal_collections")
    title = relationship("Title", back_populates="personal_collections")

class TitleAlias(Base):
    __tablename__ = 'title_alias'
    # ... other columns ...
    title = relationship("Title", back_populates="title_aliases")

class Genre(Base):
    __tablename__ = 'genre'
    # ... other columns ...
    title_genres = relationship("TitleGenre", back_populates="genre")

class TitleGenre(Base):
    __tablename__ = 'title_genre'
    # ... other columns ...
    title = relationship("Title", back_populates="title_genres")
    genre = relationship("Genre", back_populates="title_genres")

class Person(Base):
    __tablename__ = 'person'
    # ... other columns ...
    principals = relationship("Principals", back_populates="person")
    titles_directed = relationship("TitleDirector", back_populates="person")
    titles_written = relationship("TitleWriter", back_populates="person")

class Profession(Base):
    __tablename__ = 'profession'
    # ... other columns ...
    principals_jobs = relationship("Principals", back_populates="profession_job")
    principals_categories = relationship("Principals", back_populates="profession_category")

class Principals(Base):
    __tablename__ = 'principals'
    # ... other columns ...
    title = relationship("Title", back_populates="principals")
    person = relationship("Person", back_populates="principals")
    profession_category = relationship("Profession", foreign_keys=[category_id], back_populates="principals_categories")
    profession_job = relationship("Profession", foreign_keys=[job_id], back_populates="principals_jobs")

class TitleDirector(Base):
    __tablename__ = 'title_director'
    # ... other columns ...
    title = relationship("Title", back_populates="titles_directed")
    person = relationship("Person", back_populates="titles_directed")

class TitleWriter(Base):
    __tablename__ = 'title_writer'
    # ... other columns ...
    title = relationship("Title", back_populates="titles_written")
    person = relationship("Person", back_populates="titles_written")

# Remember to update Base.metadata.create_all(engine) after modifying the schema

# You can now use these relationships to query related records more intuitively.
# For example, to get all titles in a user's personal collection:
# user_with_collection = session.query(User).filter_by(username='user').first()
# for title in user_with_collection.personal_collections:
#     print(title.title.primary_title)
