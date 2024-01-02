# Import necessary libraries
from sqlalchemy import create_engine, Sequence,Column, Integer, String, Date, Boolean, ForeignKey, Float, CHAR, REAL, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker
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

# Creating the tables and the indexes ...
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
    
# Add the index
Index('idx_title_type', Title.title_type)

class TitleEpisode(Base):
    __tablename__ = 'title_episode'
    
    episode_tconst = Column(CHAR(9), primary_key=True)
    parent_tconst = Column(CHAR(9), ForeignKey('title.tconst'), nullable=False)
    season_number = Column(Integer)
    episode_number = Column(Integer)

# Add the title_episode index
Index('idx_parent_tconst',TitleEpisode.parent_tconst) 


class PersonalCollection(Base):
    __tablename__ = 'personal_collection'
    
    users_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    tconst = Column(CHAR(9), ForeignKey('title.tconst'), primary_key=True)

# Indexes for personal_collection
Index('idx_users_id', PersonalCollection.users_id)
Index('idx_tconst', PersonalCollection.tconst)

class TitleAlias(Base):
    __tablename__ = 'title_alias'
    
    id = Column(Integer, primary_key=True)
    tconst = Column(CHAR(9), ForeignKey('title.tconst'), nullable=False)
    title = Column(String(255), nullable=False)
    ordering = Column(Integer, nullable=False)
    region = Column(String(2), nullable=False)
    language = Column(String(2))
    types = Column(String(10))
    attributes = Column(String(255))
    is_original_title = Column(Boolean, nullable=False)

# Index for tilte_alias
Index('idx_tconst_alias', TitleAlias.tconst)

class Genre(Base):
    __tablename__ = 'genre'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

class TitleGenre(Base):
    __tablename__ = 'title_genre'
    
    title_tconst = Column(CHAR(9), ForeignKey('title.tconst'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('genre.id'), primary_key=True)

# Indexes for title_genre
Index('idx_title_tconst_genre', TitleGenre.title_tconst)
Index('idx_genre_id', TitleGenre.genre_id)

class Person(Base):
    __tablename__ = 'person'
    
    nconst = Column(CHAR(9), primary_key=True)
    image_url = Column(String(255))
    primary_name = Column(String(100), nullable=False)
    birth_year = Column(Integer)
    death_year = Column(Integer)

class Profession(Base):
    __tablename__ = 'profession'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class PersonPrimaryProfession(Base):
    __tablename__ = 'person_primary_profession'
    
    person_nconst = Column(CHAR(9), ForeignKey('person.nconst'), primary_key=True)
    profession_id = Column(Integer, ForeignKey('profession.id'), primary_key=True)

# Indexes for person_primary_profession
Index('idx_person_nconst_profession', PersonPrimaryProfession.person_nconst)
Index('idx_profession_id', PersonPrimaryProfession.profession_id)

class Principals(Base):
    __tablename__ = 'principals'
    
    id = Column(Integer, primary_key=True)
    tconst = Column(CHAR(9), ForeignKey('title.tconst'), nullable=False)
    nconst = Column(CHAR(9), ForeignKey('person.nconst'), nullable=False)
    category_id = Column(Integer, ForeignKey('profession.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('profession.id'))
    ordering = Column(Integer)
    characters = Column(String(255))
    image_url = Column(String(255))

# Indexes for principals
Index('idx_tconst_principals', Principals.tconst)
Index('idx_nconst_principals', Principals.nconst)
Index('idx_category_id_principals', Principals.category_id)
Index('idx_job_id_principals', Principals.job_id)

class PersonTitlesKnownFor(Base):
    __tablename__ = 'person_titles_known_for'
    
    person_nconst = Column(CHAR(9), ForeignKey('person.nconst'), primary_key=True)
    title_tconst = Column(CHAR(9), ForeignKey('title.tconst'), primary_key=True)

# Indexes for person_titles_known_for
Index('idx_title_tconst_known_for', PersonTitlesKnownFor.title_tconst)
Index('idx_person_nconst_known_for', PersonTitlesKnownFor.person_nconst)

class TitleDirector(Base):
    __tablename__ = 'title_director'
    
    title_tconst = Column(CHAR(9), ForeignKey('title.tconst'), primary_key=True)
    person_nconst = Column(CHAR(9), ForeignKey('person.nconst'), primary_key=True)

# Indexes for title_director
Index('idx_title_tconst_director', TitleDirector.title_tconst)
Index('idx_person_nconst_director', TitleDirector.person_nconst)

class TitleWriter(Base):
    __tablename__ = 'title_writer'
    
    title_tconst = Column(CHAR(9), ForeignKey('title.tconst'), primary_key=True)
    person_nconst = Column(CHAR(9), ForeignKey('person.nconst'), primary_key=True)
    
# Indexes for title_writer
Index('idx_title_tconst_writer', TitleWriter.title_tconst)
Index('idx_person_nconst_writer', TitleWriter.person_nconst)



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