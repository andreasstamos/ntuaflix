# Import necessary libraries
from sqlalchemy import create_engine, Column, Date, Boolean, Integer, String, Sequence
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