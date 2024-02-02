import pytest

from fastapi.testclient import TestClient
from app_factory import create_app
import httpx

from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

import models
import database

test_dbms = factories.postgresql_proc(port=None, dbname="test_db")

@pytest.fixture(scope="session")
def db_sessionmaker(test_dbms):
    pg_host = test_dbms.host
    pg_port = test_dbms.port
    pg_user = test_dbms.user
    pg_password = test_dbms.password
    pg_db = test_dbms.dbname

    with DatabaseJanitor(
        pg_user, pg_host, pg_port, pg_db, test_dbms.version, pg_password
    ):
        connection_str = f"postgresql+psycopg2://{pg_user}:@{pg_host}:{pg_port}/{pg_db}"
        engine = create_engine(connection_str)
        models.Base.metadata.create_all(engine)
        yield sessionmaker(bind=engine, expire_on_commit=False)

@pytest.fixture(scope="function")
def test_db(db_sessionmaker):
    try:
        db = db_sessionmaker()
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session")
def client(db_sessionmaker):
    def override_get_db():
        try:
            db = db_sessionmaker()
            yield db
        finally:
            db.close()

    app = create_app()
    app.dependency_overrides[database.get_db] = override_get_db
    res = TestClient(app)
    res.base_url = res.base_url.join(httpx.URL('/ntuaflix_api'))
    return res

