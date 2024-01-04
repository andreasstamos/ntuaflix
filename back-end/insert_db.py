from sqlalchemy import create_engine, Sequence, Column, Integer, String, Date, Boolean, ForeignKey, Float, CHAR, REAL, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from datetime import date
from models import *
import csv

# Load environment variables
env_path = '.env'
load_dotenv(dotenv_path=env_path)

DB_USERSNAME = str(os.getenv('DB_USERNAME'))
DB_PASSWORD = str(os.getenv('DB_PASSWORD'))
DB_HOST = str(os.getenv('DB_HOST'))
DB_DATABASE = str(os.getenv('DB_DATABASE'))

DATABASE_URL = f"postgresql://{DB_USERSNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"

engine = create_engine(DATABASE_URL)
Base = declarative_base()



Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


def load_tsv_data(file_path, model, mappings):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  
        for row in reader:
            data = {db_field: row[file_index] for db_field, file_index in mappings.items()}
            record = model(**data)
            session.add(record)
        session.commit()

# Define mappings for each file
person_mappings = {
    'nconst': 0,
    # Add the rest of the mappings here
}

title_alias_mappings = {
    'tconst': 0,
    # Add the rest of the mappings here
}

title_mappings = {
    'tconst': 0,
    # Add the rest of the mappings here
}

# ... Define mappings for the rest of your tables ...

# Load data from each TSV file into the respective table
load_tsv_data('/mnt/data/truncated_name.basics.tsv', Person, person_mappings)
load_tsv_data('/mnt/data/truncated_title.akas.tsv', TitleAlias, title_alias_mappings)
load_tsv_data('/mnt/data/truncated_title.basics.tsv', Title, title_mappings)
# ... 



session.close()

