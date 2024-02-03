import pytest
from .endpoints_testdata import *

@pytest.mark.parametrize("titleID, title", TEST_TITLES)
def test_title(client, upload_data, titleID, title):
    response = client().get(f"title/{titleID}")
    assert response.status_code == 200
    assert response.json() == title

