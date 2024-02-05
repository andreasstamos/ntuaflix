# SoftEng-template

Template repository, used for NTUA/ECE Software Engineering, 2023-2024

Το αρχείο αυτό περιέχει οδηγίες για το στήσιμο του git repository που θα
χρησιμοποιήσετε.  Στο τέλος, θα το αντικαταστήσετε με το `README.md` που
θα περιγράφει το δικό σας project.

# NTUAFLIX

### Introduction
Access NTUAFLIX [here](http://ntuaflix.cloudns.be/ "here").
<img src="/front-end/public/meta-image.png" style="border-radius:8px;"/>

### Tech Stack
<div style="display:flex; justify-content: space-between;">
<img src="https://cdn.worldvectorlogo.com/logos/fastapi.svg" width="17%"/><img src="https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg" width="17%"/><img src="https://cdn.worldvectorlogo.com/logos/material-ui-1.svg" width="17%"/><img src="https://www.svgrepo.com/show/354115/nginx.svg" width="17%"/>
</div>

## Prerequisites

1. [Python](https://www.python.org/downloads/) , [pip](https://pip.pypa.io/en/stable/installation/)
2. [Node.js and npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
3. DBMS: [PostgreSQL](https://www.postgresql.org/download/)

## Quick Setup for Virtual Environment

### Make .venv
```bash
python3.10 -m venv .venv
```
### Activate .venv
For Windows
```bash
.venv\Scripts\activate
```
For Unix/MacOS
```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r back-end/requirements.txt
```

### Additional if you use MySQL
```bash
pip install pymysql
```

## Quick setup for frontend

```bash
npm install
```

## Local App Test

1. Create `back-end/.env` file to configure your database credentials, check the `.env` template in `back-end/README.md`. 
2. Create a database in your DBMS, for example `ntuaflix` and save the name in the `back-end/.env`. For the next steps your DBMS should be running (on localhost).
3. Run `back-end/models.py` to create tables of the schema.
4. Place `tsv` files for data import into a folder `back-end/truncated_data`
5. Run `back-end/input_tsv.py` to import data into the database from the tsv files.
6. Run `back-end/main.py` to run the back-end code
7. While `back-end/main.py` is running, run `npm start` in `front-end/` folder to start the front-end