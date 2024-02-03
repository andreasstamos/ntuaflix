# Back-end

Ενδεικτικά περιεχόμενα:

- Πηγαίος κώδικας εφαρμογής για εισαγωγή, διαχείριση και
  πρόσβαση σε δεδομένα (backend).
- Database dump (sql ή json)
- Back-end functional tests.
- Back-end unit tests.
- RESTful API.

## Database Configuration & Connection

1. Use the `.env` file to configure your database credentials. 
2. Create a database in your DBMS, for example `ntuaflix` and save the name in the `.env`
3. Run `models.py` to create tables of the schema.
4. Run `input_tsv.py` to import data into the database from the tsv files.
5. Run `main.py` to run the back-end code
6. While `main.py` is running, run `npm start` in `front-end/` folder to start the front-end

Note: To see the changes between mysql and postgres in `models.py`, you can Ctrl + F : `DIFFERENT` 

### .env template 
```bash
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_DATABASE=ntuaflix  # or the name you want for the Database
DEBUG=1
HOST=localhost
PORT=8000 # should be the same as the port defined in front-end/src/api/api.js
DB_TYPE=postgres  # optional if postgres, for MySQL, DB_TYPE=mysql
```

### MySQL helping scripts 

- Quick script for dropping and creating a new database `ntuaflix` in MySQL CLI.
```bash
drop schema ntuaflix;
create schema ntuaflix;
use ntuaflix;
show tables;
```

- MySQL check after `models.py`
```bash
show tables;
show triggers;
```

## Quick Setup for Virtual Environment

```bash
python3.10 -m venv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install sqlalchemy python-dotenv pymysql aiofiles fastapi flatten_dict aiocsv jose python-jose passlib python-multipart pydantic[email] uvicorn frozendict
```

## Quick setup for frontend

```bash
npm install
```