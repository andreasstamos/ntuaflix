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
3. Run `models.py`
4. ...
5. ...

Note: To see the changes between mysql and postgres in `models.py`, you can Ctrl + F : `DIFFERENT` 

### .env template 
```bash
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_DATABASE=ntuaflix  # or the name you want for the Database
DEBUG=1
HOST=localhost
PORT=3307 # example port maybe 3306
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

