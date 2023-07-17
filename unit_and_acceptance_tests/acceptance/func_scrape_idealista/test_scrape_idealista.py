from config import settings
import requests

import pytest


def test_happy_scrape_idealista_endpoint(event_fixture, local_url_fixture):
    response = requests.post(local_url_fixture, json=event_fixture)
    print(f"URL: {local_url_fixture}")
    print(f"Code: {response.status_code}")
    print(f"Resp body: {response.text}")
    assert response.status_code == 200
