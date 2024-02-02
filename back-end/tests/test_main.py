import pytest
import os

def test_admin_register(admin_register):
    pass

def test_admin_token(admin_token):
    pass

def test_health_check(admin_client):
    response = admin_client.get("healthcheck/")
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload.keys() == {"status", "dataconnection"}, payload
    assert payload["status"] == "OK", payload
    assert payload["dataconnection"], payload
    
@pytest.fixture(scope="function")
def resetall(admin_client, test_db):
    response = admin_client.post("resetall/")
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload.keys() == {"status"}, payload
    assert payload["status"] == "OK", payload

def test_resetall(resetall, test_db):
    pass

def _upload_data_generic(admin_client, endpoint, fn):
    with open(fn, "rb") as f:
        files = {'file': (os.path.basename(f.name), f, 'text/tab-separated-values')}
        response = admin_client.post(f"upload/{endpoint}", files=files)
        assert response.status_code == 200, response.text
        payload = response.json()
        assert payload["status"] == "OK", payload


@pytest.fixture(scope="function")
def upload_data(admin_client):
    _upload_data_generic(admin_client, "titlebasics", "truncated_data/truncated_title.basics.tsv")
    _upload_data_generic(admin_client, "titleakas", "truncated_data/truncated_title.akas.tsv")
    _upload_data_generic(admin_client, "namebasics", "truncated_data/truncated_name.basics.tsv")
    _upload_data_generic(admin_client, "titlecrew", "truncated_data/truncated_title.crew.tsv")
    _upload_data_generic(admin_client, "titleepisode", "truncated_data/truncated_title.episode.tsv")
    _upload_data_generic(admin_client, "titleprincipals", "truncated_data/truncated_title.principals.tsv")
    _upload_data_generic(admin_client, "titleratings", "truncated_data/truncated_title.ratings.tsv")

def test_upload_data(upload_data):
    pass

