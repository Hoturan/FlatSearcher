import pytest

from lambda_layers.python.config import settings

@pytest.fixture(scope='package')
def scrape_idealista_endpoint():
    return f"{settings.host}"