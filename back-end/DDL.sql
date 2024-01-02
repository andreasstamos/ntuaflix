CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(500) NOT NULL,
    dob DATE NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE title (
    tconst CHAR(9) PRIMARY KEY,
    end_year INT,
    primary_title VARCHAR(100) NOT NULL,
    original_title VARCHAR(100) NOT NULL,
    title_type VARCHAR(10) NOT NULL,
    runtime_minutes INT NOT NULL,
    genre_id VARCHAR(100) NOT NULL,
    known_for_by INT,
    start_year INT NOT NULL,
    is_adult BOOLEAN NOT NULL,
    image_url VARCHAR(100),
    principals INT NOT NULL,
    average_rating REAL,
    num_votes INT,
    directors INT,
    writers INT
);

CREATE INDEX idx_title_type ON title (title_type);

CREATE TABLE title_episode (
    episode_tconst CHAR(9) PRIMARY KEY,
    parent_tconst CHAR(9) NOT NULL REFERENCES title(tconst),
    season_number INT,
    episode_number INT
);

CREATE TABLE personal_collection (
    users_id INT REFERENCES users(id),
    tconst CHAR(9) REFERENCES title(tconst),
    PRIMARY KEY (users_id, tconst)
);

CREATE INDEX idx_users_id ON personal_collection (users_id);
CREATE INDEX idx_tconst ON personal_collection (tconst);

CREATE TABLE title_alias (
    id SERIAL PRIMARY KEY,
    tconst CHAR(9) NOT NULL REFERENCES title(tconst),
    title VARCHAR(255) NOT NULL,
    ordering INT NOT NULL,
    region VARCHAR(2) NOT NULL,
    language VARCHAR(2),
    types VARCHAR(10),
    attributes VARCHAR(255),
    is_original_title BOOLEAN NOT NULL
);

CREATE INDEX idx_tconst_alias ON title_alias (tconst);

CREATE TABLE genre (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE title_genre (
    title_tconst CHAR(9) REFERENCES title(tconst),
    genre_id INT REFERENCES genre(id),
    PRIMARY KEY (title_tconst, genre_id)
);

CREATE INDEX idx_title_tconst_genre ON title_genre (title_tconst);
CREATE INDEX idx_genre_id ON title_genre (genre_id);

CREATE TABLE person (
    nconst CHAR(9) PRIMARY KEY,
    image_url VARCHAR(255),
    primary_name VARCHAR(100) NOT NULL,
    birth_year INT,
    death_year INT
);

CREATE TABLE profession (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE person_primary_profession (
    person_nconst CHAR(9) REFERENCES person(nconst),
    profession_id INT REFERENCES profession(id),
    PRIMARY KEY (person_nconst, profession_id)
);

CREATE INDEX idx_person_nconst_profession ON person_primary_profession (person_nconst);
CREATE INDEX idx_profession_id ON person_primary_profession (profession_id);

CREATE TABLE principals (
    id SERIAL PRIMARY KEY,
    tconst CHAR(9) NOT NULL REFERENCES title(tconst),
    nconst CHAR(9) NOT NULL REFERENCES person(nconst),
    category_id INT NOT NULL REFERENCES profession(id),
    job_id INT REFERENCES profession(id),
    ordering INT,
    characters TEXT, -- Changed to TEXT to accommodate potential length
    image_url VARCHAR(255)
);

CREATE INDEX idx_tconst_principals ON principals (tconst);
CREATE INDEX idx_nconst_principals ON principals (nconst);
CREATE INDEX idx_category_id_principals ON principals (category_id);
CREATE INDEX idx_job_id_principals ON principals (job_id);

CREATE TABLE person_titles_known_for (
    person_nconst CHAR(9) REFERENCES person(nconst),
    title_tconst CHAR(9) REFERENCES title(tconst),
    PRIMARY KEY (person_nconst, title_tconst)
);

CREATE INDEX idx_title_tconst_known_for ON person_titles_known_for (title_tconst);
CREATE INDEX idx_person_nconst_known_for ON person_titles_known_for (person_nconst);

CREATE TABLE title_director (
    title_tconst CHAR(9) REFERENCES title(tconst),
    person_nconst CHAR(9) REFERENCES person(nconst),
    PRIMARY KEY (title_tconst, person_nconst)
);

CREATE INDEX idx_title_tconst_director ON title_director (title_tconst);
CREATE INDEX idx_person_nconst_director ON title_director (person_nconst);

CREATE TABLE title_writer (
    title_tconst CHAR(9) REFERENCES title(tconst),
    person_nconst CHAR(9) REFERENCES person(nconst),
    PRIMARY KEY (title_tconst, person_nconst)
);

CREATE INDEX idx_title_tconst_writer ON title_writer (title_tconst);
CREATE INDEX idx_person_nconst_writer ON title_writer (person_nconst);
