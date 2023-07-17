import pytest

from config import settings


@pytest.fixture(scope="package")
def scrape_idealista_endpoint():
    return f"{settings.host}"


@pytest.fixture(scope="package")
def event_fixture():
    return {
        "scrape_locations": ["/barcelona/sant-marti/el-poblenou/"],
        "idealista_url_root": "https://www.idealista.com/venta-viviendas",
    }


@pytest.fixture(scope="package")
def local_url_fixture():
    return (
        "http://localhost:3001/2015-03-31/functions/YourLambdaFunctionName/invocations"
    )
